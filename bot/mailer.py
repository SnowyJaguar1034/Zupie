# Script to send email with optional attachments using gmail

import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from pathlib import Path
from smtplib import SMTP, SMTPAuthenticationError
from textwrap import dedent
from typing import List


def send_mail(
    send_from: str,
    send_to: str,
    username: str,
    password: str,
    subject: str,
    message: str,
    files: List[str],
    server: str = "smtp.gmail.com",
    port: int = 587,
    use_tls=True,
):
    "Compose and send email with provided info and attachments."
    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(message))
    for path in files:
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", "attachment; filename={}".format(Path(path).name)
        )
        msg.attach(part)
    try:
        smtp = SMTP("smtp.gmail.com", port)
        smtp.ehlo()
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
    except SMTPAuthenticationError as err:
        code = err.args[0]
        subcode = ""
        mesg = err.args[1].decode("utf-8")
        ERR_REGEX = re.compile(r"(^|\n)(?P<subcode>\d(?:\.\d+)*)\s+", re.DOTALL)
        m = ERR_REGEX.search(mesg)
        if m:
            subcode = m.group("subcode")
            mesg = ERR_REGEX.sub("\\1", mesg)
        print("\x1b[1;41;37m", end="")
        print(f"Error code {code} - server rejected authentication", end="")
        print("\x1b[0;1;31m")
        print(mesg, end="")
        print("\x1b[0m")
        if code == 534 and subcode == "5.7.9":
            print(
                dedent(
                    """
          NOTE: Steps to generate app-specific password
            • Log in to your Google account
            • Go to My Account > Sign-in & Security > App Passwords
            • Scroll down to Select App (in the Password & sign-in method box)
            • Choose 'Other (custom name)'
            • Give this app password a name, e.g. "mymailer"
            • Choose Generate
            • Copy the long generated password and paste it into your script."""
                )
            )
        return err
    result = smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    return result


if __name__ == "__main__":
    # See instructions above and/or
    # https://support.google.com/mail/?p=InvalidSecondFactor
    send_mail(
        "<YOUR USERNAME>@gmail.com",  # your gmail address : From address
        "<YOUR USERNAME>@gmail.com",  # your gmail address : To address
        username="<YOUR USERNAME>@gmail.com",
        password="<APP-SPECIFIC GMAIL PASSWORD>",
        subject="Test",
        message="Hello, this is a test",
        files=[],
    )
