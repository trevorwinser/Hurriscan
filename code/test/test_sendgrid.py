# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='noah.stasuik@gmail.com',
    to_emails='noah.stasuik@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>andd easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('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'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)