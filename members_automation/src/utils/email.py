import smtplib
from email.message import EmailMessage
import os


def send_email(
    message: str, credentials: dict, recipients: list, server: str, port: int
) -> None:
    """
    Wrapper function to send an email message using smtplib.
    Parameters
    ----------
    message: String, message to be sent
    credentials: Dict of the form {user: example@example.com, password: 3x4mpl3_P4ss}
    recipients: list of recipients to send the email to: [recipient@gmail.com, recipient2@hotmail.com]
    server: server to use for sending example smtp.gmail.com
    port: port to use for sending, example: 587

    Returns None
    -------

    """

    # If no message in the input, don't send anything
    if message is None:
        return None

    # Define message to send
    msg = EmailMessage()
    msg["Subject"] = message
    msg["From"] = credentials["user"]
    msg["To"] = recipients

    # Initialize server
    server = smtplib.SMTP(server, port)
    server.starttls()

    # Log in with credentials
    server.login(**credentials)

    # Send email
    server.sendmail(credentials["user"], recipients, msg.as_string())

    # Close connection
    server.quit()
    return None


def unzip_file(origin_path, destination_path):
    """
    Unzips a file
    Args:
        origin_path:
        destination_path:

    Returns:

    """
    os.system(f"unzip -oj {origin_path} -d {destination_path}")
    return None
