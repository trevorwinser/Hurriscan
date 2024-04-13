import pytest
from unittest.mock import MagicMock, patch
from routing import predictions

@pytest.mark.parametrize("kind", ['email', 'phone'])
def test_send_alert(kind):
    user = {'email': 'test@example.com', 'phone': '1234567890'}
    month = 6
    risk = 'High'
    data = {'user': user, 'month': month, 'risk': risk, 'kind': kind}

    with patch('flask.request.get_json', MagicMock(return_value=data)), \
         patch('routing.predictions.Client') as MockClient:
        predictions.send_alert()

        if kind == 'email':
            MockClient().messages.create.assert_called_once_with(
                from_='+19163024424',
                body='Alert Hurricane Risk: High\nMonth: 6',
                to='test@example.com'
            )
        elif kind == 'phone':
            MockClient().messages.create.assert_called_once_with(
                from_='+19163024424',
                body='Alert Hurricane Risk: High\nMonth: 6',
                to='1234567890'
            )