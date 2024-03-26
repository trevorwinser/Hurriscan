""" import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

email = input("Enter your email address: ")

message = Mail(
    from_email="noah.stasuik@gmail.com",
    to_emails=email,
    subject='Hurriscan Alert!',
    html_content='<strong>Warning!</strong> Hurricane Activity in your area!!')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))  """