import os
import pytest
import logging
import asyncio
import pytest_asyncio
from jira import JIRA
from requests import Session
from WeTest.util import encry
from WeTest.util.api import API
from aiohttp import ClientSession
from WeTest.util import notification
from WeTest.util.config import read_yaml
from WeTest.util.client import DataBase, RabbitMQ, SSH, SFTP, Hive, Nacos, S3


def pytest_terminal_summary(terminalreporter, exitstatus, config):

    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    error = len(terminalreporter.stats.get("error", []))
    skipped = len(terminalreporter.stats.get("skipped", []))

    # reused pytest-html fixture
    htmlpath = config.getoption("htmlpath")

    if htmlpath and (failed or error):
        key = os.getenv("ROBOT_KEY")
        notification.send_report(key, htmlpath)


def pytest_html_report_title(report):

    report.title = "TEST REPORT"


def pytest_html_results_table_row(report, cells):

    if report.passed:
        del cells[:]


@pytest_asyncio.fixture(scope="session")
async def session():

    session = ClientSession()

    yield session

    await session.close()


@pytest.fixture(scope="session")
def event_loop():

    loop = asyncio.get_event_loop()

    yield loop

    loop.close()


# @pytest.fixture(scope="session")
# def nacos():

#     nacos_host = os.getenv("NACOS_HOST")
#     nacos_username = os.getenv("NACOS_USERNAME")
#     nacos_password = os.getenv("NACOS_PASSWORD")

#     nacos = Nacos()
#     nacos.connect(nacos_host, nacos_username, nacos_password)

#     return nacos


# @pytest.fixture(scope="session", params=[os.getenv("TEST_ENV", "dev")], ids=lambda data: f"[{data.upper()}]")
# def config(request, nacos: Nacos):

#     env = request.param

#     logging.info("*" * 50)
#     logging.info(f"     >>>>> CURRENT ENVIRONMENT: {env.upper()} <<<<<")
#     logging.info("*" * 50)

#     nacos_group = os.getenv("NACOS_GROUP", "HCS")
#     nacos_tenant = os.getenv("NACOS_TENANT")

#     return nacos.get_config(nacos_tenant, data_id=env, group=nacos_group)


@pytest.fixture(scope="session", params=[os.getenv("TEST_ENV", "dev")], ids=lambda data: f"[{data.upper()}]")
def config(request):

    env = request.param
    path = "env/dev.yaml"

    logging.info("*" * 50)
    logging.info(f"     >>>>> CURRENT ENVIRONMENT: {env.upper()} <<<<<")
    logging.info("*" * 50)

    return read_yaml(path)


@pytest.fixture(
    scope="session",
    params=os.getenv("TEST_ROLE", "root").lower().split(","),
    ids=lambda data: f"[{data}]",
)
def user_info(config, request):

    role = request.param
    return config["portal"]["user"][role]


@pytest.fixture(scope="session")
def api(config, user_info):

    proxies = config["portal"]["proxy"]
    domain = config["portal"]["sku"]["api"]

    auth_url = config["portal"]["auth"]["auth_url"]
    client_id = config["portal"]["auth"]["client_id"]
    client_secret = config["portal"]["auth"]["client_secret"]
    grant_type = config["portal"]["auth"]["grant_type"]

    auth_type = config["portal"]["auth_type"]

    email = user_info["email"]
    password = user_info["password"]
    cookie = user_info["cookie"]
    identify = user_info["identify"]

    api = API()

    if auth_type.lower() == "auth":
        token = api.get_token(auth_url, email, password, client_id, client_secret, grant_type, proxies)
        api.set_headers(token)

    elif auth_type.lower() == "cookie":
        headers = {"cookie": cookie}
        api.set_headers(headers)

    elif auth_type.lower() == "identify":
        headers = {"identify": identify}
        api.set_headers(headers)

    elif auth_type.lower() == "x-auth-user":
        headers = {"x-auth-user": email}
        api.set_headers(headers)

    api.set_domain(domain)

    return api


@pytest.fixture(scope="session", autouse=True)
def sqlite():

    path = "server/data/db/test.db"

    database = DataBase(database=path, type="sqlite")

    sql_query_root = "select * from user where email='root@test.com'"
    sql_insert_root = "insert into user (name, email, role, status, creator, password, created, updated) values ('root', 'root@test.com', 0, 1, 1, '$2b$12$Mky27TOoMnYkO4Gb7G4uR.O/viTeY/oIs928xtuAQ/uN8W5UIqwAO', '2022-09-10 12:43:06.189924', '2022-09-10 12:43:06.189926')"

    root = database.query_to_dict(sql_query_root)
    if not root:
        database.exec_sql(sql_insert_root)

    yield database

    # Note: sqlite_schema is not support for default python3 default sqlite version(3.22.0)
    # tables = database.query_to_dict("select name from sqlite_schema where type='table' and name not like 'sqlite_%'")
    tables = ["user", "file"]
    for table in tables:
        database.exec_sql(f"delete from {table}")

    database.close()


@pytest.fixture(scope="session")
def mysql(config):

    db_host = config["database"]["management"]["host"]
    db_port = config["database"]["management"]["port"]
    db_username = config["database"]["management"]["username"]
    db_password = config["database"]["management"]["password"]
    db_dbname = config["database"]["management"]["dbname"]

    database = DataBase(db_username, db_password, db_host, db_port, db_dbname)

    yield database

    database.close()


@pytest.fixture(scope="session")
def sftp(config):

    host = config["sftp"]["host"]
    port = config["sftp"]["port"]
    username = config["sftp"]["username"]
    password = config["sftp"]["password"]

    sftp = SFTP()
    sftp.connect(host, port, username, password)

    yield sftp

    sftp.close()


@pytest.fixture(scope="session")
def ssh(config):

    host = config["ssh"]["host"]
    port = config["ssh"]["port"]
    username = config["ssh"]["username"]
    password = config["ssh"]["password"]

    ssh = SSH()
    ssh.connect(host, port, username, password)

    yield ssh

    ssh.close()


@pytest.fixture(scope="session")
def s3(config):

    endpoint = config["s3"]["endpoint"]
    access_key = config["s3"]["access_key"]
    secret_key = config["s3"]["secret_key"]

    s3 = S3()
    s3.connect(access_key, secret_key, endpoint)

    return s3


@pytest.fixture(scope="session")
def rabbitmq(config):

    host = config["rabbitmq"]["host"]
    port = config["rabbitmq"]["port"]
    username = config["rabbitmq"]["username"]
    password = config["rabbitmq"]["password"]
    vhost = config["rabbitmq"]["vhost"]

    rabbitmq = RabbitMQ()
    rabbitmq.connect(host, port, vhost, username, password)

    return rabbitmq


@pytest.fixture(scope="session")
def hive(config):

    host = config["hive"]["host"]
    port = config["hive"]["port"]
    username = config["hive"]["username"]
    password = config["hive"]["password"]
    database = config["hive"]["database"]
    auth_mechanism = config["hive"]["auth_mechanism"]

    hive = Hive()
    hive.connect(host=host, port=port, user=username, password=password, auth_mechanism=auth_mechanism, database=database)

    return hive


@pytest.fixture(scope="session")
def jira(config):

    host = config["jira"]["host"]
    username = encry.aes_decrypt(*config["jira"]["username"].split(","))
    password = encry.aes_decrypt(*config["jira"]["password"].split(","))

    return JIRA(basic_auth=(username, password), server=host)


@pytest.fixture(scope="session")
def confluence(config):

    host = config["confluence"]["host"]
    username = encry.aes_decrypt(*config["confluence"]["username"].split(","))
    password = encry.aes_decrypt(*config["confluence"]["password"].split(","))

    data = {"os_username": username, "os_password": password}

    session = Session()
    session.post(host, data=data)

    yield host, session

    session.close()
