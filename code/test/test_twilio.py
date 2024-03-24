""" from twilio.rest import Client

account_sid = 'AC44993aed976dd5210997b2519df5a254'
auth_token = '2f03469ee4713d8785f90eadd5100fac'
client = Client(account_sid, auth_token)

phone_number = input("Enter your phone number: ")

message = client.messages.create(
  from_='+19163024424',
  body='Testing Hurriscan',
  to=phone_number
)

print(message.sid) """