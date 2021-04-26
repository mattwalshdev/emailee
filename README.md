# emailee

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Code Quality][quality-image]][quality-url]
[![Code Factor][codefactor-image]][codefactor-url]
[![versions][versions-image]][versions-url]
[![license][license-image]][license-url]

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/emailee
[pypi-url]: https://pypi.org/project/emailee/

[build-image]: https://github.com/mattwalshdev/emailee/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/mattwalshdev/emailee/actions/workflows/build.yml

[coverage-image]: https://codecov.io/gh/mattwalshdev/emailee/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/mattwalshdev/emailee

[quality-image]: https://api.codeclimate.com/v1/badges/0360d77f65da3d985d03/maintainability
[quality-url]: https://codeclimate.com/github/mattwalshdev/emailee

[codefactor-image]: https://www.codefactor.io/repository/github/mattwalshdev/emailee/badge
[codefactor-url]: https://www.codefactor.io/repository/github/mattwalshdev/emailee

[versions-image]: https://img.shields.io/pypi/pyversions/emailee.svg
[versions-url]: https://github.com/mattwalshdev/emailee

[license-image]: https://img.shields.io/github/license/mattwalshdev/emailee.svg
[license-url]: https://github.com/mattwalshdev/emailee/blob/main/LICENSE

A robust SMTP mailer library, with async mail send features built-in using Threads and Multiprocessing. Zero PyPI (production) dependencies.

## Installation

Install with `pip install emailee`.

## Some quick examples

Send a simple text email

```Python
import emailee

my_email = emailee.Emailee()
my_email.sender("john.smith@fakeemail.com")
my_email.subject("Test email")
my_email.msgContent("some poorly formatted raw text")
my_email.sendTo(["jill.smith@fakeemail.com"])
my_email.server("smtp.fakeemail.com")

if my_email.ready():
    my_email.send()
```

Send multiple asyncronous emails

```Python
import emailee

emails_list = [{...}]
server_dict = {...}

emails = emailee.AsyncThreads(emails_list, server_dict, outputFile='output.txt')
```

## Documentation

There are only three classes exposed to the user of this library, `Emailee`, `AsyncThreads` and `AsyncMP`. The latter two utilise the Emailee class to send emails via the Threading or Multiprocessing async APIs respectively.

### Emailee class

If you have used the `smtplib` and `email` libraries in the past, you may of found how difficult it is getting the email logic set up properly to handle attachments and different sending scenarios. All customisations are built into Emailee, which takes the guess work out of how to configure.

The following methods are exposed to the user:

#### Emailee.sender(sender: str, replyTo: str = "") -> None

* **sender** - email address of who is sending the email
* **replyTo** (optional) - alternative email address the receiver can reply to

#### Emailee.subject(subject: str = "") -> None

* **subject** (optional) - email subject line, maximum of 255 characters

#### Emailee.msgContent(msgText: str = "", msgHTML: str = "") -> None

* **msgText** (optional) - email message in raw text format
* **msgHTML** (optional) - email message in email HTML format

It's a good idea to use both of these to replicate your email, so users who can't read HTML emails can read your fallback raw text email. Look online for HTML email generators

#### Emailee.sendTo(to: List[str] = [], cc: List[str] = [], bcc: List[str] = [], ignoreErrors: bool = False) -> None

* **to** (optional) - list of to addresses to send emails to
* **cc** (optional) - list of cc addresses to send emails to
* **bcc** (optional) - list of bcc addresses to send emails to
* **ignoreErrors** (optional) - all addresses are validated by regex to be in a valid email format. By default, if an email address is found to be invalid the program will raise an exception. If changed to True, the program will ignore and remove invalid emails and continue with sending the email.

#### Emailee.attachmentFiles(attachmentFiles: List[str] = []) -> None

* **attachmentFiles** (optional) - list of attachments for email, can be listed by relative or full path

#### Emailee.server(smtpServer: str, port: int = 0, SSLTLS: str = "", authUsername: str = "", authPassword: str = "", timeout: int = 30) -> None

* **smtpServer** - server name or IP address of SMTP server
* **port** (optional) - port number for SMTP server, if connection not authenticated and port left blank, port will default to 25. If connection set to SSL or TLS and port left blank, port will default to 465 or 587 respectively.
* **SSLTLS** (optional) - encrypted connection setting, value either "SSL" or "TLS"
* **authUsername** (optional) - username for logging into the SMTP server, if authentication required. If left blank, but authPassword filled in, this will default to the sender email.
* **authPassword** (optional) - password for logging into the SMTP server
* **timeout** (optional) - server connection and email send timeout limit. Extend this value if on a slow network, or sending emails with large attachments

#### Emailee.ready() -> bool

Returns True if the minimal fields to send an email have been set.

#### Email.send(outputFile: str) -> bool

* **outputFile** (optional) - relative or full path location of a file to write report output metadata to, required for async classes when sending mail, file must be empty or not currently exist

Returns True if successful, does not guarantee email was delivered, just sent.

#### Email.__repr__() -> str

Print class function, will print a dictionary of email metadata, useful for testing and debugging.

---

### Data for async classes

Both async classes are very similar in their function and both require emails and server config in the exact same format:

```Python
mail_list = [
    {
        'sender': sender # see Emailee.sender()
        'replyTo': replyTo # see Emailee.sender()
        'subject': email_subject # see Emailee.subject()
        'msgText': raw_text_message # see Emailee.msgContent()
        'msgHTML': HTML_formatted_message # see Emailee.msgContent()
        'to': list_of_to_emails # see Emailee.sendTo()
        'cc': list_of_cc_emails # see Emailee.sendTo()
        'bcc': list_of_bcc_emails # see Emailee.sendTo()
        'ignoreErrors': True # see Emailee.sendTo()
        'attachmentFiles': list_of_attachment_file_paths # see Emailee.attachmentFiles()
    },
    {...},
]
```

```Python
server_dict = {
    'smtpServer': SMTP_server # see Emailee.server()
    'port': port_number # see Emailee.server()
    'SSLTLS': 'TLS' # see Emailee.server()
    'authUsername': authenticated_username # see Emailee.server()
    'authPassword': authenticated_password # see Emailee.server()
}
```

### AsyncThreads class

AsyncThreads uses the threading API to enable asyncronous sending of email. Threading only utilises the same CPU core that the Python program is currently running on, so it can only maximise a single core usage, but the benefits are you can throttle how many threads are allowed to run concurrently and it has a lower overhead compared to `AsyncMP`.

#### AsyncThreads(mailList: List[Dict], serverDict: Dict, outputFile: str, maxThreads: int = 10, waitTime: float = 0)

* **mailList** - see mail_list above for format
* **serverDict** - see server_dict above for format
* **outputFile** - relative or full path location of a file to write report output metadata to, file must be empty or not currently exist. Mandatory for async classes to handle errors.
* **maxThreads** - maximum number of concurrent threads to send emails on
* **waitTime** - wait time in seconds to pause between each thread being spawned, this helps if your SMTP server throttles your connection if you send too many emails in a short time span

### AsyncMP class

AsyncMP uses the multiprocessing API to enable asyncronous sending of email. Multiprocessing utilises all CPU cores of the system the Python program is running on, but does not allow throttling, so you run the risk of maxing out your CPU and RAM, slowing down your system.

#### AsyncMP(mailList: List[Dict], serverDict: Dict, outputFile: str, waitTime: float = 0)

* **mailList** - see mail_list above for format
* **serverDict** - see server_dict above for format
* **outputFile** - relative or full path location of a file to write report output metadata to, file must be empty or not currently exist. Mandatory for async classes to handle errors.
* **waitTime** - wait time in seconds to pause between each process being spawned, this helps if your SMTP server throttles your connection if you send too many emails in a short time span

### Reporting on async output

Upon completion of either async class, you can call the `emailReport()` method to return a metadata list of all emails sent.
This won't work if an exception is thrown during the sending process, hence the **outputFile** requirement.
The output file will be written to after each successful email send so you can analyse against `emailReport()` or see who received emails before a thrown exception or manual cancellation of the sending process.

## Development and Testing

Emailee is built with [**poetry**](https://python-poetry.org/), tested with [**pytest**](https://pytest.org), [**tox**](https://tox.readthedocs.io/en/latest/) and [**coverage**](https://coverage.readthedocs.io/en/coverage-5.5/), type checked with [**mypy**](http://mypy-lang.org/) and formatted with [**black**](https://github.com/psf/black).

### Dev Installation

#### Install with Poetry

Clone the repo, `cd` into it and run `poetry install`

#### Install with pip

Clone the repo, `cd` into it, build and run a new virtual environment, then open the `pyproject.toml` file and `pip install` all packages listed under **[tool.poetry.dev-dependencies]**

### Testing

To successfully run local tests you will need to rename `tests/example.test.env.toml` to `tests/test.env.toml` and modify the config inside the file to contain valid email and SMTP server connection data.

Testing and coverage can then be run with `pytest --cov-report term-missing --cov=emailee tests`

Tox can be used to run pytest against all support Python environments. Open `tox.ini` and check if you have all versions of Python installed listed under *envlist*.

### Pre-commit hooks

Run `pre-commit install` to install the pre-commit hooks in the `.pre-commit-config.yaml` file. Then run `pre-commit run --all-files` to auto-check every file for issues.

Feel free to send me any changes or feedback.

---

Thanks for reading :)

:envelope: :envelope: :envelope: :envelope: :envelope:
