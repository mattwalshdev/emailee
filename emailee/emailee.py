import enum
import mimetypes
import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path
from typing import BinaryIO, List, TextIO, Union


def _helperOutputFileCheck(filename: str) -> bool:
    try:
        if Path(filename).is_file():
            try:
                fileSize: int = Path(filename).stat().st_size
            except Exception as error:
                raise error
            if fileSize != 0:
                raise OSError(
                    "outputFile is not empty, please empty or delete it and try again"
                )
        else:
            try:
                Path(filename).touch()
            except Exception as error:
                raise PermissionError(f"No access to create the new file - {error}")
    except Exception as error:
        raise PermissionError(
            f"No access to file location to check if file exists - {error}"
        )
    return True


class _EncType(enum.Enum):
    """
    Enumerations of TLS and SSL, for encryption logic in Emailee
    """

    SSL = 1
    TLS = 2


class Emailee:
    """
    A robust SMTP email solution for Python.
    Zero external dependencies (unless testing).
    Allows sending via SSL or TLS, attachments, reply-to and to/cc/bcc.
    Emails are built with the below structure -

    multipart/mixed
        ├─── multipart/related
        │    └── multipart/alternative
        │        ├─── text/plain
        │        └─── text/html
        ├─── application/text - embedded attachment
        ├─── application/image - embedded attachment
        ├─── application/audio - embedded attachment
        └─── application/pdf etc. - other application attachment

    See https://github.com/mattwalshdev/emailee for additional documentation

    Methods
    -------
        sender(sender: str, replyTo: str) - email (required), email
        subject(subject: str) - text
        msgContent(msgText: str, msgHTML: str) - raw text, html text
        sendTo(to: List[str], cc: List[str], bcc: List[str], ignoreErrors: bool) -
            List of emails in each, one required. Set ignoreErrors True if you
            want it to still send emails if there is 1+ invalid emails listed
        attachmentFiles(attachmentFiles: List[str]) - List of full and/or
            relative paths to files
        server(smtpServer: str, port: int, SSLTLS: str, authUsername: str,
            authPassword: str, timeout: int) - servername (required),
            port no, encryption type, credentials,
            timeout for server connection timeout in seconds, default 30 seconds,
            increase if on slow connection
        ready() - will return True if all required fields are entered and valid,
            does not guarantee emails actually exist
        send(outputFile: str) - attempt to send the email, optional addition of an
            outputFile to save metadata to. OutputFile is mandatory when sending emails in either async mode

    Example
    -------
    import emailee

    my_email = emailee.Emailee()
    my_email.sender("john.smith@fakeemail.com")
    my_email.subject("Test email")
    my_email.msgContent("raw text, poorly formatted")
    my_email.sendTo(["jill.smith@fakeemail.com"])
    my_email.server("smtp.fakeemail.com")

    if my_email.ready():
        my_email.send()
    """

    _EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def __init__(self) -> None:
        self._sender: str = ""
        self._replyTo: str = ""
        self._subject: str = ""
        self._msgText: str = ""
        self._msgHTML: str = ""
        self._to: List[str] = []
        self._cc: List[str] = []
        self._bcc: List[str] = []
        self._attachmentFiles: List[str] = []
        self._smtpServer: str = ""
        self._port: int = 0
        self._SSLTLS: Union[_EncType, None] = None
        self._authUsername: str = ""
        self._authPassword: str = ""
        self._timeout: int = 30
        self._outputFile: str = ""
        self._outputFileReady: bool = False

    def __repr__(self) -> str:
        outputDict = {
            "sender": self._sender,
            "replyTo": self._replyTo,
            "subject": self._subject,
            "msgText": self._msgText,
            "msgHTML": self._msgHTML,
            "to": self._to,
            "cc": self._cc,
            "bcc": self._bcc,
            "attachmentFiles": self._attachmentFiles,
            "smtpServer": self._smtpServer,
            "port": self._port,
            "SSLTLS": self._SSLTLS,
        }
        return str(outputDict)

    def __str__(self) -> str:
        outputDict = {
            "sender": self._sender,
            "replyTo": self._replyTo,
            "subject": self._subject,
            "to": self._to,
            "cc": self._cc,
            "bcc": self._bcc,
        }
        return str(outputDict)

    def _addressCheck(
        self, emailList: List[str], type: str, ignoreErrors: bool
    ) -> List[str]:
        self._tempEmailList = []
        for email in emailList:
            if not isinstance(email, str):
                raise TypeError(f"{type} email not a string - {email}")

            if not Emailee._EMAIL_REGEX.fullmatch(email):
                if not ignoreErrors:
                    raise ValueError(f"Invalid {type} email - {email}")
                else:
                    continue
            if ignoreErrors:
                self._tempEmailList.append(email)
        if ignoreErrors:
            return self._tempEmailList
        return emailList

    def sender(self, sender: str, replyTo: str = "") -> None:
        if not isinstance(sender, str):
            raise TypeError("sender not a string")

        self._sender = self._addressCheck([sender], "sender", ignoreErrors=False)[0]

        if replyTo:
            if not isinstance(replyTo, str):
                raise TypeError("replyTo not a string")

            self._replyTo = self._addressCheck(
                [replyTo], "replyTo", ignoreErrors=False
            )[0]

    def subject(self, subject: str) -> None:
        if not isinstance(subject, str):
            raise TypeError("subject not a string")

        if len(subject) > 255:
            raise ValueError("subject string too long")
        self._subject = subject

    def msgContent(self, msgText: str = "", msgHTML: str = "") -> None:
        if not isinstance(msgText, str):
            raise TypeError("msgText not a string")

        if not isinstance(msgHTML, str):
            raise TypeError("msgHTML not a string")

        self._msgText = msgText
        self._msgHTML = msgHTML

    def sendTo(
        self,
        to: List[str] = [],
        cc: List[str] = [],
        bcc: List[str] = [],
        ignoreErrors: bool = False,
    ) -> None:
        if not to and not cc and not bcc:
            raise ValueError("No email addresses to send to are defined")

        if (
            not isinstance(to, list)
            or not isinstance(cc, list)
            or not isinstance(bcc, list)
        ):
            raise TypeError("sendTo items are not in list format")

        if not isinstance(ignoreErrors, bool):
            raise TypeError("sendTo ignoreErrors is not a bool")

        self._to = self._addressCheck(to, "to", ignoreErrors)
        self._cc = self._addressCheck(cc, "cc", ignoreErrors)
        self._bcc = self._addressCheck(bcc, "bcc", ignoreErrors)

        if not self._to and not self._cc and not self._bcc:
            raise ValueError("No email addresses to send to are properly defined")

    def attachmentFiles(self, attachmentFiles: List[str] = []) -> None:
        if not isinstance(attachmentFiles, list):
            raise TypeError("attachmentFiles not in list format")

        for file in attachmentFiles:
            if not isinstance(file, str):
                raise TypeError(f"file name listed not in string format - {file}")

            if not Path(file).is_file():
                raise ValueError(
                    f"Attachment listed is not a file or not accessible - {file}"
                )

        self._attachmentFiles = attachmentFiles

    def server(
        self,
        smtpServer: str,
        *,
        port: int = 0,
        SSLTLS: str = "",
        authUsername: str = "",
        authPassword: str = "",
        timeout: int = 30,
    ) -> None:
        if not isinstance(smtpServer, str):
            raise TypeError("smtpServer name not in string format")

        if not isinstance(port, int):
            raise TypeError("smtpServer port not in integer format")

        if not isinstance(SSLTLS, str):
            raise TypeError("smtpServer SSLTLS option not in string format")

        if not isinstance(authUsername, str):
            raise TypeError("smtpServer auth username not in string format")

        if not isinstance(authPassword, str):
            raise TypeError("smtpServer auth password not in string format")

        if not isinstance(timeout, int):
            raise TypeError("timeout server option not in integer format")

        if port < 0 or port > 65535:
            raise ValueError("Port is an invalid number")

        if SSLTLS not in _EncType.__members__ and SSLTLS != "":
            raise ValueError("SSLTLS option is invalid")

        if timeout <= 0:
            raise ValueError("Server timeout period is an invalid number")

        self._smtpServer = smtpServer

        if port > 0:
            self._port = port
        elif SSLTLS == "TLS":
            self._port = 587
        elif SSLTLS == "SSL":
            self._port = 465
        else:
            self._port = 25

        if SSLTLS:
            self._SSLTLS = _EncType[f"{SSLTLS}"]
        elif port == 587:
            self._SSLTLS = _EncType.TLS
        elif port == 465:
            self._SSLTLS = _EncType.SSL

        if authUsername and authPassword:
            self._authUsername = authUsername
            self._authPassword = authPassword
        elif authPassword:
            self._authUsername = self._sender
            self._authPassword = authPassword

        self._timeout = timeout

    def ready(self) -> bool:
        if self._authPassword and not self._authUsername and self._sender:
            # this may happen if server methods are invoked before
            #  the sender method AND the person has not added an
            #  authUsername BUT has added an authPassword
            self._authUsername = self._sender

        if (
            self._sender
            and (self._to or self._cc or self._bcc)
            and self._smtpServer
            and self._port
        ):
            # minimum requirements in place to send an email
            return True
        else:
            return False

    def _generate(self) -> str:
        message = MIMEMultipart("mixed")

        message["to"] = ", ".join(self._to) if self._to else ""

        message["cc"] = ", ".join(self._cc) if self._cc else ""

        message["from"] = self._sender
        message["subject"] = self._subject
        message["date"] = formatdate(localtime=True)

        if self._replyTo:
            message.add_header("reply-to", self._replyTo)

        messageRelated = MIMEMultipart("related")
        messageAlternative = MIMEMultipart("alternative")

        if self._msgText:
            messageAlternative.attach(MIMEText(self._msgText, "plain"))
        if self._msgHTML:
            messageAlternative.attach(MIMEText(self._msgHTML, "html"))

        messageRelated.attach(messageAlternative)

        message.attach(messageRelated)

        for attFile in self._attachmentFiles or []:
            contentType, encoding = mimetypes.guess_type(attFile)

            if contentType is None or encoding is not None:
                contentType = "application/octet-stream"
            mainType, subType = contentType.split("/", 1)

            attachment: Union[MIMEText, MIMEImage, MIMEAudio, MIMEApplication]
            fp: Union[TextIO, BinaryIO]

            if mainType == "text":
                with open(attFile, "r") as fp:
                    attachment = MIMEText(fp.read(), _subtype=subType)
            else:
                with open(attFile, "rb") as fp:
                    if mainType == "image":
                        attachment = MIMEImage(fp.read(), _subtype=subType)
                    elif mainType == "audio":
                        attachment = MIMEAudio(fp.read(), _subtype=subType)
                    else:
                        attachment = MIMEApplication(fp.read(), _subtype=subType)

            filename = Path(attFile).stem
            attachment.add_header(
                "Content-Disposition", "attachment; filename=" + filename
            )
            message.attach(attachment)

        return message.as_string()

    def send(self, outputFile: str = "") -> bool:
        if self._authPassword and not self._authUsername and self._sender:
            # this may happen if server methods are invoked before
            #  the sender method AND the person has not added an
            #  authUsername BUT has added an authPassword
            self._authUsername = self._sender

        if not isinstance(outputFile, str):
            raise TypeError("outputFile path not in string format")

        # run checks against the output file, unless it's already been run
        #  during this run, this is for async batch jobs of emails
        #  where send is called repeatedly
        if outputFile:
            if not self._outputFileReady:
                self._outputFileReady = _helperOutputFileCheck(outputFile)
            self._outputFile = outputFile

        try:
            generatedEmail: str = self._generate()
        except Exception as error:
            raise (error)

        try:
            smtp: object

            if self._SSLTLS == _EncType.SSL:
                try:
                    smtp = smtplib.SMTP_SSL(
                        self._smtpServer, self._port, timeout=self._timeout
                    )
                except Exception as error:
                    raise ValueError(error)
            else:
                try:
                    smtp = smtplib.SMTP(
                        self._smtpServer, self._port, timeout=self._timeout
                    )
                except Exception as error:
                    raise ValueError(error)

            smtp.ehlo()

            if self._SSLTLS == _EncType.TLS:
                smtp.starttls()
                smtp.ehlo()
        except Exception as error:
            raise error
        if self._authUsername and self._authPassword:
            try:
                smtp.login(self._authUsername, self._authPassword)
            except Exception as error:
                raise ValueError(error)

        try:
            smtp.sendmail(self._sender, self._to + self._cc + self._bcc, generatedEmail)
        except Exception as error:
            raise ValueError(error)

        try:
            smtp.close()
            if self._outputFile:
                with open(self._outputFile, "a") as file:
                    file.write(self.__str__() + "\n")
            return True
        except Exception as error:
            raise (error)
