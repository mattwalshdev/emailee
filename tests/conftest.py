import os
from pathlib import Path

import pytest
import toml

# generate test environment settings from file if testing locally,
#  otherwise they will be generated from secrets in a github action
if Path("tests/.test.env.toml").is_file():
    try:
        test_config = toml.load("tests/.test.env.toml")
        os.environ["EMAILEE_TEST_SMTP_SERVER"] = test_config["smtp"]["smtp_server"]
        os.environ["EMAILEE_TEST_AUTH_USERNAME"] = test_config["smtp"]["auth_username"]
        os.environ["EMAILEE_TEST_AUTH_PASSWORD"] = test_config["smtp"]["auth_password"]

        os.environ["EMAILEE_TEST_EMAILEE_PATH"] = test_config["variables"][
            "emailee_path"
        ]
        os.environ["EMAILEE_TEST_SENDER"] = test_config["variables"]["sender"]
        os.environ["EMAILEE_TEST_RECEIVER1"] = test_config["variables"]["receiver1"]
        os.environ["EMAILEE_TEST_RECEIVER2"] = test_config["variables"]["receiver2"]
        os.environ["EMAILEE_TEST_RECEIVER3"] = test_config["variables"]["receiver3"]
    except Exception as error:
        raise (error)


# used for numbering the emails in the subject line
def pytest_configure():
    pytest.SENT_EMAIL_NUM = 1
    pytest.SENT_EMAIL_MAX = 36


# delete each async test email output before the next one runs
@pytest.fixture()
def file_setup():
    # Path(os.environ['EMAILEE_TEST_EMAILEE_PATH'] + "/tests/test_output.txt").touch()
    yield
    if Path(
        os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt"
    ).is_file():
        Path(
            os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt"
        ).unlink()


# delete all environment variables at end of testing
@pytest.fixture(scope="session", autouse=True)
def teardown():
    yield
    del os.environ["EMAILEE_TEST_SMTP_SERVER"]
    del os.environ["EMAILEE_TEST_AUTH_USERNAME"]
    del os.environ["EMAILEE_TEST_AUTH_PASSWORD"]

    del os.environ["EMAILEE_TEST_EMAILEE_PATH"]
    del os.environ["EMAILEE_TEST_SENDER"]
    del os.environ["EMAILEE_TEST_RECEIVER1"]
    del os.environ["EMAILEE_TEST_RECEIVER2"]
    del os.environ["EMAILEE_TEST_RECEIVER3"]
