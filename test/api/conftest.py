import os
import sys

sys.path.append(os.getcwd())

import json
import pytest
import logging
from pathlib import Path
from WeTest.util import date


@pytest.fixture(scope="session")
def resource():

    env = os.getenv("TEST_ENV", "dev")
    path = f"config/{env}__resource.json"

    resource = {"now": date.get_time(), "user_id": 0, "user_email": ""}

    if Path(path).exists():
        with open(path, "r") as f:
            resource = json.load(f)

    yield resource

    logging.info(f"Gloable Resource: {path}")
    logging.info(json.dumps(resource, indent=4, ensure_ascii=False))

    with open(path, "w") as f:
        json.dump(resource, f, indent=4, ensure_ascii=False)
