import smtplib

from email.message import EmailMessage

from app.configure import EMAIL, EMAIL_PASSWORD


def send_welcome_email(receiver_email: str):

    message = EmailMessage()

    message["Subject"] = "Welcome"

    message["From"] = EMAIL

    message["To"] = receiver_email

    message.set_content(
        f"""
Hello,

Your account has been created successfully.

Welcome to Student Management System.

Thank you.
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

        smtp.starttls()

        smtp.login(
            EMAIL,
            EMAIL_PASSWORD
        )

        smtp.send_message(message)

    print("Welcome email sent successfully.")