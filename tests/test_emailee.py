import os
from pathlib import Path

import pytest

import emailee
import tests.mail_examples as mail_examples

# --- Emailee class initiation --- #


def test_blank_class():
    email = emailee.Emailee()
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


# --- sender method tests --- #


def test_sender_valid():
    email = emailee.Emailee()
    email.sender("correct.sender@fakeemail.com")
    assert (
        email.__repr__()
        == "{'sender': 'correct.sender@fakeemail.com', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


@pytest.mark.parametrize("bad_data", ["", "a", "127.0.0.1", "bad+email@something"])
def test_sender_invalid_value(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sender(bad_data)


@pytest.mark.parametrize("bad_data", [None, True, False, 0, 2, 1.5, [], {}])
def test_sender_invalid_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sender(bad_data)


def test_replyto_valid():
    email = emailee.Emailee()
    email.sender("correct.sender@fakeemail.com", "correct.replyto@fakeemail.com")
    assert (
        email.__repr__()
        == "{'sender': 'correct.sender@fakeemail.com', 'replyTo': 'correct.replyto@fakeemail.com', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


@pytest.mark.parametrize("bad_data", ["a", "127.0.0.1", "bad+email@something"])
def test_replyto_invalid_value(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sender("correct.sender@fakeemail.com", replyTo=bad_data)


@pytest.mark.parametrize(
    "bad_data",
    [
        True,
        3,
        1.5,
    ],
)
def test_replyto_invalid_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sender("correct.sender@fakeemail.com", replyTo=bad_data)


def test_full_sender_no_params():
    email = emailee.Emailee()
    email.sender("sender@fakeemail.com", "replyto@fakeemail.com")


def test_full_sender_with_params():
    email = emailee.Emailee()
    email.sender(sender="sender@fakeemail.com", replyTo="replyto@fakeemail.com")


# --- subject method tests --- #


@pytest.mark.parametrize("bad_data", [None, True, False, 0, 2, 1.5, [], {}])
def test_subject_invalid_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.subject(bad_data)


def test_subject_invalid_value():
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.subject(
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
        )


def test_subject_max_value():
    email = emailee.Emailee()
    email.subject(
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    )


def test_subject_empty_value():
    email = emailee.Emailee()
    email.subject("")


def test_subject_with_params():
    email = emailee.Emailee()
    email.subject(subject="Test subject")


def test_subject_valid():
    email = emailee.Emailee()
    email.subject(subject="Test subject")
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': 'Test subject', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


# --- msgContent method tests --- #


@pytest.mark.parametrize("bad_data", [None, True, False, 0, 2, 1.5, [], {}])
def test_msgtext_invalid_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.msgContent(msgText=bad_data)


@pytest.mark.parametrize("bad_data", [None, True, False, 0, 2, 1.5, [], {}])
def test_msghtml_invalid_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.msgContent(msgHTML=bad_data)


def test_msgtext_empty_value():
    email = emailee.Emailee()
    email.msgContent(msgText="")


def test_msghtml_empty_value():
    email = emailee.Emailee()
    email.msgContent(msgHTML="")


def test_msgcontent_empty_value():
    email = emailee.Emailee()
    email.msgContent(msgText="", msgHTML="")


def test_msgcontent_no_params():
    email = emailee.Emailee()
    email.msgContent("text field", "HTML field")
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': 'text field', 'msgHTML': 'HTML field', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_msgtext_valid():
    email = emailee.Emailee()
    email.msgContent(msgText="text field")
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': 'text field', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_msghtml_valid():
    email = emailee.Emailee()
    email.msgContent(msgHTML="HTML field")
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': 'HTML field', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_msgcontent_valid():
    email = emailee.Emailee()
    email.msgContent(msgText="text field", msgHTML="HTML field")
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': 'text field', 'msgHTML': 'HTML field', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


# --- sendTo method tests --- #


def test_sendto_empty():
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sendTo()


@pytest.mark.parametrize(
    "bad_data", ["valid.email@fakeemail.com", "", "a", None, True, False, 0, 2, 1.5, {}]
)
def test_sendto_to_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(
            to=bad_data,
            cc=["valid.data@fakeemail.com"],
            bcc=["valid.data@fakeemail.com"],
        )


@pytest.mark.parametrize(
    "bad_data", ["valid.email@fakeemail.com", "", "a", None, True, False, 0, 2, 1.5, {}]
)
def test_sendto_cc_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(
            to=["valid.data@fakeemail.com"],
            cc=bad_data,
            bcc=["valid.data@fakeemail.com"],
        )


@pytest.mark.parametrize(
    "bad_data", ["valid.email@fakeemail.com", "", "a", None, True, False, 0, 2, 1.5, {}]
)
def test_sendto_bcc_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(
            to=["valid.data@fakeemail.com"],
            cc=["valid.data@fakeemail.com"],
            bcc=bad_data,
        )


@pytest.mark.parametrize(
    "bad_data", ["valid.email@fakeemail.com", "", "a", None, 0, 2, 1.5, {}]
)
def test_sendto_ignoreerror_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(
            to=["valid.data@fakeemail.com"],
            cc=["valid.data@fakeemail.com"],
            bcc=["valid.data@fakeemail.com"],
            ignoreErrors=bad_data,
        )


def test_sendto_with_params():
    email = emailee.Emailee()
    email.sendTo(
        to=["valid.to@fakeemail.com"],
        cc=["valid.cc@fakeemail.com"],
        bcc=["valid.bcc@fakeemail.com"],
        ignoreErrors=False,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.to@fakeemail.com'], 'cc': ['valid.cc@fakeemail.com'], 'bcc': ['valid.bcc@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_no_params():
    email = emailee.Emailee()
    email.sendTo(
        ["valid.to@fakeemail.com"],
        ["valid.cc@fakeemail.com"],
        ["valid.bcc@fakeemail.com"],
        False,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.to@fakeemail.com'], 'cc': ['valid.cc@fakeemail.com'], 'bcc': ['valid.bcc@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_to_only():
    email = emailee.Emailee()
    email.sendTo(to=["valid.to@fakeemail.com"])
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.to@fakeemail.com'], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_to_only_multi():
    email = emailee.Emailee()
    email.sendTo(to=["valid.to@fakeemail.com", "another.valid.to@fakeemail.com"])
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.to@fakeemail.com', 'another.valid.to@fakeemail.com'], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_cc_only():
    email = emailee.Emailee()
    email.sendTo(cc=["valid.cc@fakeemail.com"])
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': ['valid.cc@fakeemail.com'], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_cc_only_multi():
    email = emailee.Emailee()
    email.sendTo(cc=["valid.cc@fakeemail.com", "another.valid.cc@fakeemail.com"])
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': ['valid.cc@fakeemail.com', 'another.valid.cc@fakeemail.com'], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_bcc_only():
    email = emailee.Emailee()
    email.sendTo(bcc=["valid.bcc@fakeemail.com"])
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': ['valid.bcc@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_bcc_only_multi():
    email = emailee.Emailee()
    email.sendTo(bcc=["valid.bcc@fakeemail.com", "another.valid.bcc@fakeemail.com"])
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': ['valid.bcc@fakeemail.com', 'another.valid.bcc@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


@pytest.mark.parametrize("bad_data", [[None], [True], [False], [0], [2], [1.5], [{}]])
def test_sendto_to_items_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(to=bad_data)


@pytest.mark.parametrize("bad_data", [[None], [True], [False], [0], [2], [1.5], [{}]])
def test_sendto_cc_items_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(cc=bad_data)


@pytest.mark.parametrize("bad_data", [[None], [True], [False], [0], [2], [1.5], [{}]])
def test_sendto_bcc_items_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.sendTo(bcc=bad_data)


@pytest.mark.parametrize(
    "bad_data",
    [
        [""],
        ["a"],
        ["asdasd@bademail"],
        ["valid.email@fakeemail.com", "invalid.email@fakeemail"],
        [
            "valid.email@fakeemail.com",
            "invalid.email@fakeemail",
            "another.valid.email@fakeemail.com",
        ],
        ["invalid.email@fakeemail", "valid.email@fakeemail.com"],
    ],
)
def test_sendto_to_items_value(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sendTo(to=bad_data)


@pytest.mark.parametrize(
    "bad_data",
    [
        [""],
        ["a"],
        ["asdasd@bademail"],
        ["valid.email@fakeemail.com", "invalid.email@fakeemail"],
        [
            "valid.email@fakeemail.com",
            "invalid.email@fakeemail",
            "another.valid.email@fakeemail.com",
        ],
        ["invalid.email@fakeemail", "valid.email@fakeemail.com"],
    ],
)
def test_sendto_cc_items_value(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sendTo(cc=bad_data)


@pytest.mark.parametrize(
    "bad_data",
    [
        [""],
        ["a"],
        ["asdasd@bademail"],
        ["valid.email@fakeemail.com", "invalid.email@fakeemail"],
        [
            "valid.email@fakeemail.com",
            "invalid.email@fakeemail",
            "another.valid.email@fakeemail.com",
        ],
        ["invalid.email@fakeemail", "valid.email@fakeemail.com"],
    ],
)
def test_sendto_bcc_items_value(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sendTo(bcc=bad_data)


@pytest.mark.parametrize(
    "bad_data",
    [
        [""],
        ["a"],
        ["asdasd@bademail"],
        ["valid.email@fakeemail.com", "invalid.email@fakeemail"],
        [
            "valid.email@fakeemail.com",
            "invalid.email@fakeemail",
            "another.valid.email@fakeemail.com",
        ],
        ["invalid.email@fakeemail", "valid.email@fakeemail.com"],
    ],
)
def test_sendto_all_items_value(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.sendTo(to=bad_data, cc=bad_data, bcc=bad_data)


def test_sendto_ignoreerror_to_all_valid():
    email = emailee.Emailee()
    email.sendTo(
        to=["valid.email@fakeemail.com", "another.valid.email@fakeemail.com"],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.email@fakeemail.com', 'another.valid.email@fakeemail.com'], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_cc_all_valid():
    email = emailee.Emailee()
    email.sendTo(
        cc=["valid.email@fakeemail.com", "another.valid.email@fakeemail.com"],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': ['valid.email@fakeemail.com', 'another.valid.email@fakeemail.com'], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_bcc_all_valid():
    email = emailee.Emailee()
    email.sendTo(
        bcc=["valid.email@fakeemail.com", "another.valid.email@fakeemail.com"],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': ['valid.email@fakeemail.com', 'another.valid.email@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_to_one_invalid():
    email = emailee.Emailee()
    email.sendTo(
        to=["valid.email@fakeemail.com", "invalid.emailfakeemail.com"],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.email@fakeemail.com'], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_to_two_invalid():
    email = emailee.Emailee()
    email.sendTo(
        to=[
            "invalid.email@fakeemail",
            "valid.email@fakeemail.com",
            "invalid.emailfakeemail.com",
        ],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.email@fakeemail.com'], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_to_two_both():
    email = emailee.Emailee()
    email.sendTo(
        to=[
            "invalid.email@fakeemail",
            "valid.email@fakeemail.com",
            "invalid.emailfakeemail.com",
            "another.valid.email@fakeemail.com",
        ],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': ['valid.email@fakeemail.com', 'another.valid.email@fakeemail.com'], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_cc_one_invalid():
    email = emailee.Emailee()
    email.sendTo(
        cc=["valid.email@fakeemail.com", "invalid.emailfakeemail.com"],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': ['valid.email@fakeemail.com'], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_cc_two_invalid():
    email = emailee.Emailee()
    email.sendTo(
        cc=[
            "invalid.email@fakeemail",
            "valid.email@fakeemail.com",
            "invalid.emailfakeemail.com",
        ],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': ['valid.email@fakeemail.com'], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_cc_two_both():
    email = emailee.Emailee()
    email.sendTo(
        cc=[
            "invalid.email@fakeemail",
            "valid.email@fakeemail.com",
            "invalid.emailfakeemail.com",
            "another.valid.email@fakeemail.com",
        ],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': ['valid.email@fakeemail.com', 'another.valid.email@fakeemail.com'], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_bcc_one_invalid():
    email = emailee.Emailee()
    email.sendTo(
        bcc=["valid.email@fakeemail.com", "invalid.emailfakeemail.com"],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': ['valid.email@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_bcc_two_invalid():
    email = emailee.Emailee()
    email.sendTo(
        bcc=[
            "invalid.email@fakeemail",
            "valid.email@fakeemail.com",
            "invalid.emailfakeemail.com",
        ],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': ['valid.email@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerror_bcc_two_both():
    email = emailee.Emailee()
    email.sendTo(
        bcc=[
            "invalid.email@fakeemail",
            "valid.email@fakeemail.com",
            "invalid.emailfakeemail.com",
            "another.valid.email@fakeemail.com",
        ],
        ignoreErrors=True,
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': ['valid.email@fakeemail.com', 'another.valid.email@fakeemail.com'], 'attachmentFiles': [], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_sendto_ignoreerrors_no_valid_emails():
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        bad_data = ["not.valid@fakeemail", "another.not.validfakeemail.com"]
        email.sendTo(to=bad_data, cc=bad_data, bcc=bad_data, ignoreErrors=True)


# --- attachmentFiles method tests --- #


@pytest.mark.parametrize("bad_data", [None, True, False, 0, 2, 1.5, {}])
def test_attachments_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.attachmentFiles(bad_data)


@pytest.mark.parametrize("bad_data", [[[]], [True], [False], [0], [2], [1.5], [{}]])
def test_attachments_individual_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.attachmentFiles(bad_data)


@pytest.mark.parametrize(
    "bad_data", [["notafile.pdf"], ["./notafile2.xlsx", "doesnotexist.pdf"]]
)
def test_attachments_bad_file_path(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.attachmentFiles(bad_data)


def test_attachments_relative_path():
    email = emailee.Emailee()
    email.attachmentFiles(
        [
            "./tests/test_attachments/test.pdf",
            "./tests/test_attachments/kitten_pic.jpg",
            "./tests/test_attachments/sine_wave.wav",
            "./tests/test_attachments/test_spreadsheet.xlsx",
            "./tests/test_attachments/test_archive.zip",
        ]
    )
    assert (
        email.__repr__()
        == "{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': ['./tests/test_attachments/test.pdf', './tests/test_attachments/kitten_pic.jpg', './tests/test_attachments/sine_wave.wav', './tests/test_attachments/test_spreadsheet.xlsx', './tests/test_attachments/test_archive.zip'], 'smtpServer': '', 'port': 0, 'SSLTLS': None}"
    )


def test_attachments_full_path():
    email = emailee.Emailee()
    email.attachmentFiles(
        [
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test.pdf",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/kitten_pic.jpg",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/sine_wave.wav",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_spreadsheet.xlsx",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_archive.zip",
        ]
    )
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': ['{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test.pdf', '{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/kitten_pic.jpg', '{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/sine_wave.wav', '{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_spreadsheet.xlsx', '{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_archive.zip'], 'smtpServer': '', 'port': 0, 'SSLTLS': None}}"
    )


# --- server method tests --- #


@pytest.mark.parametrize("bad_data", [[], None, True, False, 0, 2, 1.5, {}])
def test_server_smtpserver_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.server(smtpServer=bad_data)


@pytest.mark.parametrize("bad_data", ["", "a", [], None, 1.5, {}])
def test_server_port_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            port=bad_data,
        )


@pytest.mark.parametrize("bad_data", [[], None, True, False, 0, 2, 1.5, {}])
def test_server_ssltls_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            SSLTLS=bad_data,
        )


@pytest.mark.parametrize("bad_data", [[], None, True, False, 0, 2, 1.5, {}])
def test_server_authusername_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            authUsername=bad_data,
        )


@pytest.mark.parametrize("bad_data", [[], None, True, False, 0, 2, 1.5, {}])
def test_server_authpassword_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            authPassword=bad_data,
        )


@pytest.mark.parametrize("bad_data", [-1, -20, 65536, -65535, -65536, 1000000])
def test_server_port_invalid_values(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            port=bad_data,
        )


@pytest.mark.parametrize("good_data", [0, 5, 65535])
def test_server_port_valid_values(good_data):
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        port=good_data,
    )


@pytest.mark.parametrize("bad_data", ["SSLS", "TLSS", "a"])
def test_server_SSLTLS_invalid_values(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            SSLTLS=bad_data,
        )


@pytest.mark.parametrize("good_data", ["", "TLS", "SSL"])
def test_server_SSLTLS_valid_values(good_data):
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS=good_data,
    )


@pytest.mark.parametrize("bad_data", ["", "a", [], None, 1.5, {}])
def test_server_timeout_type(bad_data):
    email = emailee.Emailee()
    with pytest.raises(TypeError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            timeout=bad_data,
        )


@pytest.mark.parametrize("bad_data", [-1, -20, 0, -10000])
def test_server_timeout_invalid_values(bad_data):
    email = emailee.Emailee()
    with pytest.raises(ValueError):
        email.server(
            smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
            timeout=bad_data,
        )


@pytest.mark.parametrize("good_data", [5, 60, 120])
def test_server_timeout_valid_values(good_data):
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        timeout=good_data,
    )


def test_server_scenario_1():
    email = emailee.Emailee()
    email.server(smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"])
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 25, 'SSLTLS': None}}"
    )


def test_server_scenario_2():
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="SSL",
    )
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 465, 'SSLTLS': <_EncType.SSL: 1>}}"
    )


def test_server_scenario_3():
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
    )
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 587, 'SSLTLS': <_EncType.TLS: 2>}}"
    )


def test_server_scenario_4():
    email = emailee.Emailee()
    email.server(smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"], port=465)
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 465, 'SSLTLS': <_EncType.SSL: 1>}}"
    )


def test_server_scenario_5():
    email = emailee.Emailee()
    email.server(smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"], port=587)
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 587, 'SSLTLS': <_EncType.TLS: 2>}}"
    )


def test_server_scenario_6():
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        authUsername="fake.name",
    )
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 25, 'SSLTLS': None}}"
    )


def test_server_scenario_7():
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        authUsername="fake.name",
        authPassword="fake.password",
    )
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 25, 'SSLTLS': None}}"
    )


def test_server_scenario_8():
    email = emailee.Emailee()
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        authPassword="fake.password",
    )
    assert (
        email.__repr__()
        == f"{{'sender': '', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 25, 'SSLTLS': None}}"
    )


def test_server_scenario_9():
    email = emailee.Emailee()
    email.sender("fake.sender@fakeemail.com")
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        authPassword="fake.password",
    )
    assert (
        email.__repr__()
        == f"{{'sender': 'fake.sender@fakeemail.com', 'replyTo': '', 'subject': '', 'msgText': '', 'msgHTML': '', 'to': [], 'cc': [], 'bcc': [], 'attachmentFiles': [], 'smtpServer': '{os.environ['EMAILEE_TEST_SMTP_SERVER']}', 'port': 25, 'SSLTLS': None}}"
    )


# --- ready method tests --- #


def test_new_email_not_ready():
    email = emailee.Emailee()
    assert not email.ready()


def test_new_email_is_ready_fake_data():
    email = emailee.Emailee()
    email.sender("fake.sender@fakeemail.com")
    email.sendTo(["fake.receiver@fakemail.com"])
    email.server("smtp.fakeemail.com")
    assert email.ready()


def test_new_email_not_ready_authentication():
    email = emailee.Emailee()
    email.server("smtp.fakeemail.com", authPassword="fake.password")
    email.sendTo(["fake.receiver@fakemail.com"])
    assert not email.ready()


def test_new_email_not_ready_authentication_sendTo():
    email = emailee.Emailee()
    email.server("smtp.fakeemail.com", authPassword="fake.password")
    email.sendTo(["fake.receiver@fakemail.com"])
    email.sender("fake.sender@fakeemail.com")
    assert email.ready()


# --- send method tests --- #


@pytest.mark.parametrize("bad_data", [0, [], None, True, False, 1.5, {}])
def test_send_email_outputfile_invalid_type(bad_data):
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=3,
    )
    with pytest.raises(TypeError):
        email.send(bad_data)


def test_send_email_success_missing_username(file_setup):
    email = emailee.Emailee()
    email.subject(
        f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | Test email"
    )
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=60,
    )
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    pytest.SENT_EMAIL_NUM += 1
    email.send(os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt")


def test_send_email_outputfile_doesnt_exist(file_setup):
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject(
        f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | Test email"
    )
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=60,
    )
    pytest.SENT_EMAIL_NUM += 1
    email.send(os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt")


def test_send_email_outputfile_does_exist_empty(file_setup):
    Path(os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt").touch()
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject(
        f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | Test email"
    )
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=60,
    )
    pytest.SENT_EMAIL_NUM += 1
    email.send(os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt")


def test_send_email_outputfile_does_exist_not_empty(file_setup):
    Path(os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt").touch()
    with open(
        os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt", "w"
    ) as output_file:
        output_file.write("some text")
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=3,
    )
    with pytest.raises(OSError):
        email.send(os.environ["EMAILEE_TEST_EMAILEE_PATH"] + "/tests/test_output.txt")


def test_send_email_outputfile_no_access():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=3,
    )
    with pytest.raises(PermissionError):
        email.send("/root/no_file_access.txt")


def test_send_email_invalid_server_1():
    email = emailee.Emailee()
    email.sender("fake.sender@fakeemail.com")
    email.subject("Test email")
    email.sendTo(["fake.receiver@fakeemail.com"])
    email.server(smtpServer="asdadas.fakeemail.com", timeout=3)
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_server_2():
    email = emailee.Emailee()
    email.sender("fake.sender@fakeemail.com")
    email.subject("Test email")
    email.sendTo(["fake.receiver@fakeemail.com", "another.fake.receiver@fakeemail.com"])
    email.server(smtpServer="asdadas.fakeemail.com", SSLTLS="SSL", timeout=3)
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_server_3():
    email = emailee.Emailee()
    email.sender("fake.sender@fakeemail.com")
    email.subject("Test email")
    email.sendTo(
        ["fake.receiver@fakeemail.com"], cc=["another.fake.receiver@fakeemail.com"]
    )
    email.server(smtpServer="asdadas.fakeemail.com", SSLTLS="TLS", timeout=3)
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_server_4():
    email = emailee.Emailee()
    email.sender("fake.sender@fakeemail.com")
    email.subject("Test email")
    email.sendTo(
        ["fake.receiver@fakeemail.com"],
        cc=["fake.receiver@fakeemail.com", "another.fake.receiver@fakeemail.com"],
    )
    email.server(smtpServer="asdadas.fakeemail.com", port=65, timeout=3)
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_auth_1():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo(
        cc=["fake.receiver@fakeemail.com", "another.fake.receiver@fakeemail.com"]
    )
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        timeout=3,
    )
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_auth_2():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo(cc=["fake.receiver@fakeemail.com"])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="SSL",
        timeout=3,
    )
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_auth_3():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo(bcc=["fake.receiver@fakeemail.com"])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername="fake.name",
        authPassword="fake.password",
        timeout=3,
    )
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_auth_4():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo(to=["fake.receiver@fakeemail.com"])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="SSL",
        authUsername="fake.name",
        authPassword="fake.password",
        timeout=3,
    )
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_auth_5():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject("Test email")
    email.sendTo(["fake.receiver@fakeemail.com"])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="SSL",
        authPassword="fake.password",
        timeout=3,
    )
    with pytest.raises(ValueError):
        email.send()


def test_send_email_invalid_auth_6():
    email = emailee.Emailee()
    email.sender(
        os.environ["EMAILEE_TEST_SENDER"], replyTo="fake.replyto@fakeemail.com"
    )
    email.subject("Test email")
    email.sendTo(["fake.receiver@fakeemail.com"])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authPassword="fake.password",
        timeout=3,
    )
    with pytest.raises(ValueError):
        email.send()


def test_send_email_valid_auth_1():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject(
        f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | Test email"
    )
    email.sendTo([os.environ["EMAILEE_TEST_RECEIVER1"]])
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=60,
    )
    pytest.SENT_EMAIL_NUM += 1
    email.send()


def test_send_email_valid_auth_2():
    email = emailee.Emailee()
    email.sender(os.environ["EMAILEE_TEST_SENDER"])
    email.subject(
        f"Successful test email {pytest.SENT_EMAIL_NUM} of {pytest.SENT_EMAIL_MAX} | Test email"
    )
    email.msgContent(
        msgText=mail_examples.textExample, msgHTML=mail_examples.htmlExample
    )
    email.attachmentFiles(
        [
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test.pdf",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/kitten_pic.jpg",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/sine_wave.wav",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_spreadsheet.xlsx",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_archive.zip",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test.txt",
            f"{os.environ['EMAILEE_TEST_EMAILEE_PATH']}/tests/test_attachments/test_octet-stream",
        ]
    )
    email.sendTo(
        [os.environ["EMAILEE_TEST_RECEIVER1"], os.environ["EMAILEE_TEST_RECEIVER2"]],
        cc=[os.environ["EMAILEE_TEST_SENDER"]],
        bcc=[os.environ["EMAILEE_TEST_RECEIVER3"]],
    )
    email.server(
        smtpServer=os.environ["EMAILEE_TEST_SMTP_SERVER"],
        SSLTLS="TLS",
        authUsername=os.environ["EMAILEE_TEST_AUTH_USERNAME"],
        authPassword=os.environ["EMAILEE_TEST_AUTH_PASSWORD"],
        timeout=60,
    )
    pytest.SENT_EMAIL_NUM += 1
    email.send()
