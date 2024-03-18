from twilio.rest import Client

account_sid = 'AC44993aed976dd5210997b2519df5a254'
auth_token = '834adc531af2f6b71e3d8d94c884b2fb'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+19163024424',
  body='Testing Hurriscan',
  to='+13065702634'
)

print(message.sid)