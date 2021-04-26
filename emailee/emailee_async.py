import multiprocessing
import threading
import time
from typing import Any, Dict, List, Union

from .emailee import Emailee, _helperOutputFileCheck


class _SendAsync:
    """
    No point having a great SMTP library without the ability to send asynchronous mail!
    You can roll your own using the Emailee class but all the hard work is already done here.
    Uses either Threaded or Multiprocessing libraries:
        Threaded - Create x amount of threads on same CPU core
        Multiprocessing - Create processes utilising all CPU cores
    See docstrings for AsyncThreads and AsyncMP on how to implement.

    Parameters
    -------
        mailList -
            [
                {
                    'sender': sender email,
                    'replyTo': reply to email, optional
                    'subject': email subject, optional
                    'msgText': raw text message, optional
                    'msgHTML': HTML formatted message, optional
                    'to': list of to emails, optional
                    'cc': list of cc emails, optional
                    'bcc': list of bcc emails, optional
                    'ignoreErrors': will continue to send the email, skipping invalid to/cc/bcc mail items, optional
                    'attachmentFiles': list of attachment file paths, optional
                },
                {...},
            ]
        serverDict -
            {
                'smtpServer': SMTP server,
                'port': port number, optional
                'SSLTLS': SSL or TLS encryption, optional
                'authUsername': authenticated username, optional
                'authPassword': authenticated password, optional
            }
        outputFile: str - empty or non-existant text file to write successful sent email metadata to.
            Similar to AsyncThreads/AsyncMP.emailReport(), but the outputFile is written to during the email
            processing, so if there is an exception which crashes the mail run you will have a list of what successfully
            sent. Helpful to check against mail send throttling issues, which you may not notice otherwise.
        waitTime: int or float - time in seconds between each mail item sent, useful if your sending too
             many emails, too quickly utilising services like gmail, who will stop sending emails if it looks like spam
    """

    def __init__(
        self,
        mailList: List[Dict[str, Any]],
        serverDict: Dict[str, Any],
        outputFile: str,
        waitTime: Union[int, float] = 0,
    ) -> None:
        if not isinstance(mailList, list):
            raise TypeError("Email items not valid type")

        if not isinstance(serverDict, dict):
            raise TypeError("Server items not valid type")

        if not isinstance(waitTime, int) and not isinstance(waitTime, float):
            raise TypeError("Email wait time not valid number")

        if waitTime < 0:
            raise ValueError("waitTime cannot be a negative number")

        self._mailList: List[Dict[str, str]] = mailList
        self._serverDict: Dict[str, str] = serverDict
        self._waitTime: Union[int, float] = waitTime
        self._outputFileReady: bool = False

        self.emailReport: List[Dict[str, Any]] = []

        self._processQueue: multiprocessing.Queue = multiprocessing.Queue()

        self._outputFileReady = _helperOutputFileCheck(outputFile)
        self._outputFile: str = outputFile

        self._outputFileReady

    def _runTest(self):
        # run initial mail item procedurally to check server works
        try:
            _sendMailFunc(
                self._mailList[0],
                self._serverDict,
                self._processQueue,
                self._outputFile,
                self._outputFileReady,
            )
            self.emailReport.append(self._processQueue.get())
        except Exception as error:
            raise ValueError(error)


def _sendMailFunc(
    mailItem: Dict,
    mailServer: Dict,
    processQueue: multiprocessing.Queue,
    outputFile: str,
    outputFileReady: bool,
) -> None:
    """
    Helper function that sends each asynchronous mail item
    when using AsyncThreads or AsyncMP

    Parameters
    -------
        mailItem - Individual mail dict from _SendAsync.self._mailList
        mailServer - Server settings in dict from _SendAsync.self._serverDict
        processQueue - Queue object that sending results are added to
        outputFile - Text file append successful sends metadata to
    """

    mailItem.setdefault("sender", "")
    mailItem.setdefault("replyTo", "")
    mailItem.setdefault("subject", "")
    mailItem.setdefault("msgText", "")
    mailItem.setdefault("msgHTML", "")
    mailItem.setdefault("to", [])
    mailItem.setdefault("cc", [])
    mailItem.setdefault("bcc", [])
    mailItem.setdefault("ignoreErrors", False)
    mailItem.setdefault("attachmentFiles", [])

    mailServer.setdefault("smtpServer", [])
    mailServer.setdefault("port", 0)
    mailServer.setdefault("SSLTLS", None)
    mailServer.setdefault("authUsername", "")
    mailServer.setdefault("authPassword", "")
    mailServer.setdefault("timeout", 30)

    mail = Emailee()
    # override the class attribute as we've already checked the output
    #  file is valid for all async email sends
    mail._outputFileReady = outputFileReady
    mail.sender(sender=mailItem["sender"], replyTo=mailItem["replyTo"])
    mail.subject(mailItem["subject"])
    mail.msgContent(msgText=mailItem["msgText"], msgHTML=mailItem["msgHTML"])
    mail.sendTo(
        to=mailItem["to"],
        cc=mailItem["cc"],
        bcc=mailItem["bcc"],
        ignoreErrors=mailItem["ignoreErrors"],
    )
    mail.attachmentFiles(mailItem["attachmentFiles"])

    mail.server(
        smtpServer=mailServer["smtpServer"],
        port=mailServer["port"],
        SSLTLS=mailServer["SSLTLS"],
        authUsername=mailServer["authUsername"],
        authPassword=mailServer["authPassword"],
        timeout=mailServer["timeout"],
    )
    try:
        if mail.ready():
            mail.send(outputFile)
            processQueue.put(
                {
                    "sender": mailItem["sender"],
                    "replyTo": mailItem["replyTo"],
                    "subject": mailItem["subject"],
                    "to": mailItem["to"],
                    "cc": mailItem["cc"],
                    "bcc": mailItem["bcc"],
                }
            )
    except Exception as error:
        raise ValueError(error)


class _myThread(threading.Thread):
    """
    Class called by AsyncThreads to generate a new thread

    Parameters
    -------
        mailItem - Individual mail dict from _SendAsync.self._mailList
        serverDict - Server settings in dict from _SendAsync.self._serverDict
        poolSema - Pool BoundedSemaphore for threading
        processQueue - Queue object that sending results are added to
    """

    def __init__(
        self,
        mailItem: Dict,
        serverDict: Dict,
        poolSema: threading.BoundedSemaphore,
        processQueue: multiprocessing.Queue,
        outputFile: str,
        outputFileReady: bool,
    ) -> None:
        threading.Thread.__init__(self)

        self._mailItem: Dict = mailItem
        self._serverDict: Dict = serverDict
        self._poolSema = poolSema
        self._processQueue = processQueue
        self._outputFile: str = outputFile
        self._outputFileReady: bool = outputFileReady

    def run(self):
        self._poolSema.acquire()
        try:
            _sendMailFunc(
                self._mailItem,
                self._serverDict,
                self._processQueue,
                self._outputFile,
                self._outputFileReady,
            )
        except Exception as error:
            raise error
        finally:
            self._poolSema.release()


class AsyncThreads(_SendAsync):
    """
    Class to call to send emails asyncronously using threads.
    Threads are bound to the CPU that the core program sits on
    but can be rate limited if you don't want to max out your hardware.
    AsyncThreads.emailReport will return a list of all sent emails, useful for logging

    See https://github.com/mattwalshdev/emailee for additional documentation

    Parameters
    -------
        mailList - List of all mail items, sent to _SendAsync
        serverDict - Server settings in dict, sent to _SendAsync
        maxThreads - Maximum number of concurrent threads allowed, optional, default 10
        outputFile - Empty text file to store successfuly sends, sent to _SendAsync
        waitTime - Time in seconds before each email item, sent to _SendAsync

    Example
    -------
    import emailee

    emails = [{...}]
    server = {...}

    emails = emailee.AsyncThreads(emails, server, outputFile='output.txt', waitTime=0.250)
    print(emails.emailReport)
    """

    def __init__(
        self,
        mailList: List[Dict[str, Any]],
        serverDict: Dict[str, Any],
        outputFile: str,
        maxThreads: int = 10,
        waitTime: Union[int, float] = 0,
    ) -> None:
        _SendAsync.__init__(self, mailList, serverDict, outputFile, waitTime)

        if not isinstance(maxThreads, int):
            raise TypeError("maxThread is not valid int")

        if maxThreads <= 0:
            raise ValueError("maxThreads must be a number greater than 0")
        self._maxThreads = maxThreads

        self._active: List = []

        self.run()

    def run(self) -> List:
        self._runTest()
        if len(self._mailList) == 1:
            return self.emailReport

        self._poolSema = threading.BoundedSemaphore(value=self._maxThreads)

        for mailItem in self._mailList[1:]:
            newThread = _myThread(
                mailItem,
                self._serverDict,
                self._poolSema,
                self._processQueue,
                self._outputFile,
                self._outputFileReady,
            )
            newThread.start()
            self._active.append(newThread)
            time.sleep(self._waitTime)

        # wait for all items to complete before exiting
        for jobs in self._active:
            jobs.join()

        while self._processQueue.qsize():
            self.emailReport.append(self._processQueue.get())

        return self.emailReport


class AsyncMP(_SendAsync):
    """
    Class to call to send emails asyncronously using multiprocessing.
    Processes are able to utilise all CPU cores, but take up more memory
    due to isolated binaries copied for each process. Depending on work load
    you may utilise 100% of your CPU cycles running this.
    AsyncMP.emailReport will return a list of all sent emails, useful for logging

    See https://github.com/mattwalshdev/emailee for additional documentation

    Parameters
    -------
        mailList - List of all mail items, sent to _SendAsync
        serverDict - Server settings in dict, sent to _SendAsync
        outputFile - Empty text file to store successfuly sends, sent to _SendAsync
        waitTime - Time in seconds before each email item, sent to _SendAsync

    Example
    -------
    import emailee

    emails = [{...}]
    server = {...}

    emails = emailee.AsyncMP(emails, server, outputFile='output.txt', waitTime=0.250)
    print(emails.emailReport)
    """

    def __init__(
        self,
        mailList: List[Dict[str, Any]],
        serverDict: Dict[str, Any],
        outputFile: str,
        waitTime: Union[int, float] = 0,
    ) -> None:
        _SendAsync.__init__(self, mailList, serverDict, outputFile, waitTime)

        self._active: List = []

        self.run()

    def run(self) -> List:
        self._runTest()
        if len(self._mailList) == 1:
            return self.emailReport

        for mailItem in self._mailList[1:]:
            newProcess = multiprocessing.Process(
                target=_sendMailFunc,
                args=(
                    mailItem,
                    self._serverDict,
                    self._processQueue,
                    self._outputFile,
                    self._outputFileReady,
                ),
            )
            newProcess.start()
            self._active.append(newProcess)
            time.sleep(self._waitTime)

        # wait for all items to complete before exiting
        for jobs in self._active:
            jobs.join()

        while not self._processQueue.empty():
            self.emailReport.append(self._processQueue.get())

        return self.emailReport
