### User

# from locust import User, task, constant


# class LocustTest_01(User):
#     weight = 2
#     wait_time = constant(1)

#     @task
#     def launch_01(self):
#         print("Launching the URL launch_01")

#     @task
#     def search_01(self):
#         print("Searching search_01")


# class LocustTest_02(User):
#     weight = 2
#     wait_time = constant(1)

#     @task
#     def launch_02(self):
#         print("Launching the URL launch_02")

#     @task
#     def search_02(self):
#         print("Searching search_02")


# RUN: locust -f test/stress/locustfile.py
# URL: http://0.0.0.0:8089
# ORDER: Random


### HttpUser

# from locust import HttpUser, task, constant


# class LocustTest(HttpUser):

#     host = "https://reqres.in"
#     wait_time = constant(1)

#     @task
#     def get_users(self):
#         response = self.client.get("/api/users?page=2")
#         # assert response.status_code == 200
#         print(response.text)
#         print(response.status_code)
#         print(response.headers)

#     @task
#     def create_user(self):
#         data = '{name: "morpheus", job: "leader"}'
#         response = self.client.post("/api/users", data=data)
#         print(response.text)
#         print(response.status_code)
#         print(response.headers)


### TaskSet
# import random
# from locust import HttpUser, TaskSet, constant, task


# class MyTaskSet(TaskSet):
#     @task
#     def get_status(self):
#         self.client.get("/200")
#         print("Get status of 200")

#     @task
#     def get_random_status(self):
#         status_code = random.choice([100, 200, 302, 401, 502])
#         self.client.get(f"/{status_code}")
#         print(f"Get status of {status_code}")

#     class MyNestTaskSet(TaskSet):
#         @task
#         def get_500_status(self):
#             self.client.get("/500")
#             print("Get status of 500")
#             self.interrupt(reschedule=False)


# class LocustTest(HttpUser):
#     host = "https://http.cat"
#     wait_time = constant(1)
#     tasks = [MyTaskSet]


### SequentialTaskSet

# from locust import SequentialTaskSet, HttpUser, constant, task


# class MySequentialTaskSet(SequentialTaskSet):
#     @task
#     def get_200_status(self):
#         self.client.get("/200")
#         print("Status of 200")

#     @task
#     def get_500_status(self):
#         self.client.get("/500")
#         print("Status of 500")


# class LocustTest(HttpUser):
#     host = "https://http.cat"
#     wait_time = constant(1)
#     tasks = [MySequentialTaskSet]


### wait_time
# from locust import User, task, constant, between, constant_pacing


# class LocustTest(User):

#     # wait_time = constant(1)
#     # wait_time = between(2, 5)
#     wait_time = constant_pacing(3)

#     @task
#     def launch(self):
#         print(f"This will inject delay")


### on_start & on_stop

# from locust import User, task, constant


# class LocustTest(User):

#     wait_time = constant(1)

#     def on_start(self):
#         print("starting")

#     @task
#     def task_01(self):
#         print("My task01")

#     def on_stop(self):
#         print("stopping")


# from locust import SequentialTaskSet, HttpUser, constant, task


# class MySequentialTaskSet(SequentialTaskSet):
#     def on_start(self):
#         print("start")

#     @task
#     def get_200_status(self):
#         self.client.get("/200")
#         print("Status of 200")

#     @task
#     def get_500_status(self):
#         self.client.get("/500")
#         print("Status of 500")

#     def on_stop(self):
#         print("stop")


# class LocustTest(HttpUser):
#     host = "https://http.cat"
#     wait_time = constant(1)
#     tasks = [MySequentialTaskSet]


### Validation

# from locust import HttpUser, task, constant, SequentialTaskSet


# class MyTask(SequentialTaskSet):
#     @task
#     def get_xml(self):
#         result = self.client.get("/xml", name="XML")
#         print(result)

#     @task
#     def get_json(self):
#         expect = "Wake up to WonderWidgets!"

#         with self.client.get("/json", catch_response=True, name="JSON") as response:
#             result = True if expect in response.text else False
#             print(self.get_json.__name__, result)
#             response.success()

#     @task
#     def get_robots(self):
#         expect = "*"
#         result = "Fail"

#         with self.client.get("/robots.txt", catch_response=True, name="Robots") as response:
#             if expect in response.text:
#                 result = "Success"
#                 response.failure("Not a failure")

#         print(self.get_robots.__name__, result)

#     @task
#     def get_failure(self):
#         expect = 404

#         with self.client.get("/status/404", catch_response=True, name="HTTP 404") as response:
#             if response.status_code == expect:
#                 response.failure("Got 404")
#             else:
#                 response.success()


# class LocustTest(HttpUser):
#     host = "https://httpbin.org"
#     wait_time = constant(1)
#     tasks = [MyTask]


### Data Parameterization

# import random
# from locust import HttpUser, task, constant, SequentialTaskSet


# class MyTask(SequentialTaskSet):
#     @task
#     def place_order(self):
#         test_data = [
#             {
#                 "custname": "test01",
#                 "custtel": "12388888888",
#                 "custemail": "test@test.com",
#                 "size": "Small",
#                 "topping": "bacon",
#                 "delivery": "20:15",
#                 "comments": "test",
#             },
#             {
#                 "custname": "test02",
#                 "custtel": "12388888888",
#                 "custemail": "test@test.com",
#                 "size": "Small",
#                 "topping": "bacon",
#                 "delivery": "20:15",
#                 "comments": "test",
#             },
#         ]

#         data = random.choice(test_data)

#         payload = """
#         {{
#             "custname": {custname},
#             "custtel": {custtel},
#             "custemail": {custemail},
#             "size": {size},
#             "topping": {topping},
#             "delivery": {delivery},
#             "comments": {comments}
#         }}
#         """.format(
#             **data
#         )

#         name = f"Order for {data['custname']}"

#         with self.client.post("/post", catch_response=True, name=name, data=payload) as response:
#             if response.status_code == 200 and data["custname"] in response.text:
#                 response.success()
#             else:
#                 response.failure("Failure in processing the order")


# class LocustTest(HttpUser):
#     host = "https://httpbin.org"
#     wait_time = constant(1)
#     tasks = [MyTask]


### Tags

# from locust import HttpUser, task, constant, SequentialTaskSet, tag


# class MyTask(SequentialTaskSet):
#     @task
#     @tag("get", "xml")
#     def get_xml(self):
#         result = self.client.get("/xml", name="XML")
#         print(result)

#     @task
#     @tag("get", "json")
#     def get_json(self):
#         expect = "Wake up to WonderWidgets!"

#         with self.client.get("/json", catch_response=True, name="JSON") as response:
#             result = True if expect in response.text else False
#             print(self.get_json.__name__, result)
#             response.success()


# class LocustTest(HttpUser):
#     host = "https://httpbin.org"
#     wait_time = constant(1)
#     tasks = [MyTask]


# locust -f test/stress/locustfile.py --tags get
# locust -f test/stress/locustfile.py --exclude-tags xml


### Correlation
# import re
# import random
# from locust import HttpUser, SequentialTaskSet, task, constant


# class MyTask(SequentialTaskSet):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.jsession = ""
#         self.random_product = ""

#     @task
#     def home_page(self):
#         with self.client.get("", catch_response=True, name="T00_HomePage") as response:
#             if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds() < 2.0:
#                 response.success()
#             else:
#                 response.failure("Home page took too long to load and/or text check has failed.")

#     @task
#     def enter_store(self):
#         products = ["Fish", "Dogs", "Cats", "Reptiles", "Birds"]

#         with self.client.get("/actions/Catalog.action", catch_response=True, name="T10_EnterStore") as response:
#             for product in products:
#                 if product in response.text:
#                     response.success()
#                 else:
#                     response.failure("Products check failed.")
#                     break
#             try:
#                 jsession = re.search(r"jsessionid=(.+?)\?", response.text)
#                 self.jsession = jsession.group(1)
#             except AttributeError:
#                 self.jsession = ""

#     @task
#     def signin_page(self):
#         self.client.cookies.clear()
#         url = "/actions/Account.action;jsessionid=" + self.jsession + "?signonForm="

#         with self.client.get(url, catch_response=True, name="T20_SignInPage") as response:
#             if "Please enter your username and password." in response.text:
#                 response.success()
#             else:
#                 response.failure("Sign in page check failed")

#     @task
#     def login(self):
#         self.client.cookies.clear()
#         url = "/actions/Account.action"
#         data = {"username": "j2ee", "password": "j2ee", "signon": "Login"}

#         with self.client.post(url, name="T30_SignIn", data=data, catch_response=True) as response:
#             if "Welcome ABC!" in response.text:
#                 response.success()
#                 try:
#                     random_product = re.findall(r"Catalog.action\?viewCategory=&categoryId=(.+?)\"", response.text)
#                     self.random_product = random.choice(random_product)
#                 except AttributeError:
#                     self.random_product = ""
#             else:
#                 response.failure("Sign in Failed")

#     @task
#     def random_product_page(self):
#         url = "/actions/Catalog.action?viewCategory=&categoryId=" + self.random_product
#         name = "T40_" + self.random_product + "_Page"

#         with self.client.get(url, name=name, catch_response=True) as response:
#             if self.random_product in response.text:
#                 response.success()
#             else:
#                 response.failure("Product page not loaded")

#     @task
#     def sign_out(self):
#         with self.client.get("/actions/Account.action?signoff=", name="T50_SignOff", catch_response=True) as response:
#             if response.status_code == 200:
#                 response.success()
#             else:
#                 response.failure("Log off failed")
#         self.client.cookies.clear()


# class LocustTest(HttpUser):
#     host = "https://petstore.octoperf.com"
#     wait_time = constant(1)
#     tasks = [MyTask]


### Logging
# import logging
# from locust import HttpUser, SequentialTaskSet, task, constant


# class MyTask(SequentialTaskSet):
#     @task
#     def home_page(self):
#         with self.client.get("", catch_response=True, name="T00_HomePage") as response:
#             if "Welcome to JPetStore 6" in response.text and response.elapsed.total_seconds() < 2.0:
#                 response.success()
#                 logging.info("Home page load success")
#             else:
#                 response.failure("Home page took too long to load and/or text check has failed.")
#                 logging.error("Home page didn't load success")


# class LocustTest(HttpUser):
#     host = "https://petstore.octoperf.com"
#     wait_time = constant(1)
#     tasks = [MyTask]


# locust -f test/stress/locustfile.py --skip-log-setup
# locust -f test/stress/locustfile.py --logfile locust.log
# locust -f test/stress/locustfile.py --logfile locust.log --loglevel INFO


### Events

# from locust import HttpUser, task, constant, SequentialTaskSet, events


# @events.spawning_complete.add_listener
# def spawn_users(user_count, **kwargs):
#     print(f"Spawned... {user_count} users.")


# @events.request_success.add_listener
# def send_notification(**kwargs):
#     print("Sending the success notification")


# @events.request_failure.add_listener
# def send_notification(**kwargs):
#     print("Sending the failed notification")


# @events.quitting.add_listener
# def sla(environment, **kwargs):
#     if environment.stats.total.fail_ratio > 0.01:
#         print("Test failed due to failure ratio > 0.01%")
#         environment.process_exit_code = 1
#         print(environment.process_exit_code)

#     else:
#         environment.process_exit_code = 0
#         print(environment.process_exit_code)


# class MyTask(SequentialTaskSet):
#     @task
#     def home_page(self):
#         self.client.get("/", name="T00_SuccessRequests")
#         self.client.get("/failed", name="T01_FailRequests")


# class LocustTest(HttpUser):
#     host = "https://onlineboutique.dev"
#     wait_time = constant(1)
#     tasks = [MyTask]


### EventHook

from locust.event import EventHook
from locust import HttpUser, task, constant

send_email_notifcation = EventHook()
send_text_notification = EventHook()


def send_email(i, j, req_id, message=None, **kwargs):
    print(f"Sending {message} in Email for the request {req_id}")


def send_sms(i, j, req_id, message=None, **kwargs):
    print(f"Sending {message} in SMS for the request {req_id}")


send_email_notifcation.add_listener(send_email)
send_text_notification.add_listener(send_sms)


class LocustTest(HttpUser):
    wait_time = constant(1)
    host = "https://onlineboutique.dev"

    @task
    def home_page(self):
        with self.client.get("/", catch_response=True, name="T00_HomePage") as response:
            if response.status_code == 200:
                send_email_notifcation.fire(i=1, j=2, req_id=1, message="success")
                send_text_notification.fire(i=1, j=2, req_id=2, message="success")
            else:
                send_email_notifcation.fire(i=1, j=2, req_id=1, message="failed")
                send_text_notification.fire(i=1, j=2, req_id=2, message="failed")

        with self.client.get("/test", catch_response=True, name="T01_FailHomePage") as response:
            if response.status_code == 200:
                send_email_notifcation.fire(i=1, j=2, req_id=3, message="success")
                send_text_notification.fire(i=1, j=2, req_id=4, message="success")
            else:
                send_email_notifcation.fire(i=1, j=2, req_id=3, message="failed")
                send_text_notification.fire(i=1, j=2, req_id=4, message="failed")
