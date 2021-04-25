import os
from typing import Any, Dict, List

import pytest

import emailee


def helper_set_subject(workingEmails, expectedOutput=None):
    sent_email_num_copy = pytest.SENT_EMAIL_NUM
    for email in workingEmails:
        if "|" in email["subject"]:
            original_subject = email["subject"].split(" | ", 1)[1]
            email[
                "subject"
            ] = f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | {original_subject}"
        else:
            email[
                "subject"
            ] = f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | {email['subject']}"
        pytest.SENT_EMAIL_NUM += 1

    if expectedOutput:
        for output in expectedOutput:
            if "|" in output["subject"]:
                original_subject = output["subject"].split(" | ", 1)[1]
                output[
                    "subject"
                ] = f"Successful test email {sent_email_num_copy} of {pytest.SENT_EMAIL_MAX} | {original_subject}"
            else:
                output[
                    "subject"
                ] = f"Successful test email {sent_email_num_copy} of {pytest.SENT_EMAIL_MAX} | {output['subject']}"
            sent_email_num_copy += 1


# --- SendAsync class tests --- #

serverWorking: Dict[str, Any] = {
    "smtpServer": os.environ["EMAILEE_TEST_SMTP_SERVER"],
    "port": 587,
    "SSLTLS": "TLS",
    "authUsername": os.environ["EMAILEE_TEST_AUTH_USERNAME"],
    "authPassword": os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
    "pingServer": True,
}

serverWorkingBare: Dict[str, Any] = {
    "smtpServer": os.environ["EMAILEE_TEST_SMTP_SERVER"],
    "SSLTLS": "TLS",
    "authPassword": os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
}

serverBroken: Dict[str, Any] = {
    "smtpServer": "asdasd.fakeemail.com",
    "port": 587,
    "SSLTLS": "TLS",
    "authUsername": "fake.name",
    "authPassword": "fake.password",
    "pingServer": False,
    "timeout": 3,
}

emailsWorkingSingle: List[Dict[str, Any]] = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Single test email",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    }
]

emailsWorkingSingleExpectedOutput: List[Dict[str, Any]] = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Single test email",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    }
]

emailsWorkingSingleBare: List[Dict[str, Any]] = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "subject": "Another single test email",
        "msgText": "Raw text email for testing emailee",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
    }
]

emailsWorkingSingleBareExpectedOutput: List[Dict[str, Any]] = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Another single test email",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    }
]

emailsWorking: List[Dict[str, Any]] = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 1 of 5",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 2 of 5",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 3 of 5",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 4 of 5",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 5 of 5",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
]

emailsWorkingExpectedOutput = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 1 of 5",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 2 of 5",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 3 of 5",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 4 of 5",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 5 of 5",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
    },
]

emailsWorkingLong: List[Dict[str, Any]] = [
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 1 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 2 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 3 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 4 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 5 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 6 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 7 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 8 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 9 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
    {
        "sender": os.environ["EMAILEE_TEST_SENDER"],
        "replyTo": "",
        "subject": "Email test 10 of 10",
        "msgText": "Raw text email for testing emailee",
        "msgHTML": "",
        "to": [os.environ["EMAILEE_TEST_RECEIVER1"]],
        "cc": [],
        "bcc": [],
        "ignoreErrors": False,
        "attachmentFiles": [],
    },
]


@pytest.mark.parametrize(
    "bad_data",
    [
        "",
        "a",
        [],
        {},
        None,
    ],
)
def test_send_emails_threaded_invalid_wait_time_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncThreads(
            emailsWorking,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
            waitTime=bad_data,
        )


@pytest.mark.parametrize(
    "bad_data",
    [
        -1,
        -1.0,
        -1000,
        -1203.124,
    ],
)
def test_send_emails_threaded_invalid_wait_time_value(bad_data):
    with pytest.raises(ValueError):
        emailee.AsyncThreads(
            emailsWorking,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
            waitTime=bad_data,
        )


@pytest.mark.parametrize(
    "bad_data",
    [
        "",
        "a",
        [],
        {},
        None,
    ],
)
def test_send_emails_multiprocessing_invalid_wait_time_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncMP(
            emailsWorking,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
            waitTime=bad_data,
        )


@pytest.mark.parametrize(
    "bad_data",
    [
        -1,
        -1.0,
        -1000,
        -1203.124,
    ],
)
def test_send_emails_multiprocessing_invalid_wait_time_value(bad_data):
    with pytest.raises(ValueError):
        emailee.AsyncMP(
            emailsWorking,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
            waitTime=bad_data,
        )


@pytest.mark.parametrize("bad_data", ["", "a", {}, None, True, False, 0, 1.5])
def test_send_emails_threaded_invalid_emails_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncThreads(
            bad_data,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
        )


@pytest.mark.parametrize("bad_data", ["", "a", {}, None, True, False, 0, 1.5])
def test_send_emails_multiprocessing_invalid_emails_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncMP(
            bad_data,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
        )


@pytest.mark.parametrize("bad_data", ["", "a", [], None, True, False, 1.5, 0])
def test_send_emails_threaded_invalid_server_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncThreads(
            emailsWorking,
            bad_data,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
        )


@pytest.mark.parametrize("bad_data", ["", "a", [], None, True, False, 1.5, 0])
def test_send_emails_multiprocessing_invalid_server_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncMP(
            emailsWorking,
            bad_data,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
        )


@pytest.mark.parametrize("bad_data", ["", "a", [], {}, None, 1.5])
def test_send_emails_threaded_invalid_throttled_type(bad_data):
    with pytest.raises(TypeError):
        emailee.AsyncThreads(
            emailsWorking,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
            maxThreads=bad_data,
        )


@pytest.mark.parametrize("bad_data", [0, True, False, [], {}, None, 1.5])
def test_send_emails_threaded_invalid_outputfile_type(bad_data):
    with pytest.raises(PermissionError):
        emailee.AsyncThreads(emailsWorking, serverWorking, outputFile=bad_data)


@pytest.mark.parametrize("bad_data", [0, True, False, [], {}, None, 1.5])
def test_send_emails_multiprocessing_invalid_outputfile_type(bad_data):
    with pytest.raises(PermissionError):
        emailee.AsyncMP(emailsWorking, serverWorking, outputFile=bad_data)


def test_send_emails_threaded_invalid_outputfile_access():
    with pytest.raises(PermissionError):
        emailee.AsyncThreads(
            emailsWorking, serverWorking, outputFile="/root/noFileAccess.txt"
        )


def test_send_emails_multiprocessing_invalid_outputfile_access():
    with pytest.raises(PermissionError):
        emailee.AsyncMP(
            emailsWorking, serverWorking, outputFile="/root/noFileAccess.txt"
        )


@pytest.mark.parametrize(
    "bad_data",
    [
        0,
        -1,
        -100,
    ],
)
def test_send_emails_threaded_invalid_throttled_value(bad_data):
    with pytest.raises(ValueError):
        emailee.AsyncThreads(
            emailsWorking,
            serverWorking,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
            maxThreads=bad_data,
        )


def test_send_emails_threaded_broken_server():
    with pytest.raises(ValueError):
        emailee.AsyncThreads(
            emailsWorking,
            serverBroken,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
        )


def test_send_emails_multiprocessing_broken_server():
    with pytest.raises(ValueError):
        emailee.AsyncMP(
            emailsWorking,
            serverBroken,
            outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"]
            + "/tests/test_output.txt",
        )


def test_send_emails_threaded_working_one_email(file_setup):
    helper_set_subject(emailsWorkingSingle, emailsWorkingSingleExpectedOutput)
    email = emailee.AsyncThreads(
        emailsWorkingSingle,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingSingleExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_multiprocessing_working_one_email(file_setup):
    helper_set_subject(emailsWorkingSingle, emailsWorkingSingleExpectedOutput)
    email = emailee.AsyncMP(
        emailsWorkingSingle,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingSingleExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_threaded_working_one_min_params(file_setup):
    helper_set_subject(emailsWorkingSingleBare, emailsWorkingSingleBareExpectedOutput)
    email = emailee.AsyncThreads(
        emailsWorkingSingleBare,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingSingleBareExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_multiprocessing_working_one_min_params(file_setup):
    helper_set_subject(emailsWorkingSingleBare, emailsWorkingSingleBareExpectedOutput)
    email = emailee.AsyncMP(
        emailsWorkingSingleBare,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingSingleBareExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_threaded_working_one_min_params_server(file_setup):
    helper_set_subject(emailsWorkingSingleBare, emailsWorkingSingleBareExpectedOutput)
    email = emailee.AsyncThreads(
        emailsWorkingSingleBare,
        serverWorkingBare,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingSingleBareExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_multiprocessing_working_one_min_params_server(file_setup):
    helper_set_subject(emailsWorkingSingleBare, emailsWorkingSingleBareExpectedOutput)
    email = emailee.AsyncMP(
        emailsWorkingSingleBare,
        serverWorkingBare,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingSingleBareExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_threaded_working(file_setup):
    helper_set_subject(emailsWorking, emailsWorkingExpectedOutput)
    email = emailee.AsyncThreads(
        emailsWorking,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
        waitTime=0.250,
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_multiprocessing_working(file_setup):
    helper_set_subject(emailsWorking, emailsWorkingExpectedOutput)
    email = emailee.AsyncMP(
        emailsWorking,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
        waitTime=0.250,
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_threaded_working_throttled(file_setup):
    helper_set_subject(emailsWorking, emailsWorkingExpectedOutput)
    email = emailee.AsyncThreads(
        emailsWorking,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
        maxThreads=1,
    )
    emailReportSorted = sorted(email.emailReport, key=lambda i: i["subject"])
    emailExpectedSorted = sorted(
        emailsWorkingExpectedOutput, key=lambda i: i["subject"]
    )
    assert [
        i
        for i in emailReportSorted + emailExpectedSorted
        if i not in emailReportSorted or i not in emailExpectedSorted
    ] == []


def test_send_emails_multiprocessing_large(file_setup):
    helper_set_subject(emailsWorkingLong)
    emailee.AsyncMP(
        emailsWorkingLong,
        serverWorking,
        outputFile=os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt",
        waitTime=0.250,
    )
