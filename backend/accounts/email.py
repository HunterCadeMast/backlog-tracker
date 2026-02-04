import requests
from django.core.mail.backends.base import BaseEmailBackend
import os

class EmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        sent_count = 0
        api_key = os.getenv('MAILGUN_API_KEY')
        domain = os.getenv('MAILGUN_DOMAIN', 'mg.gaminglogjam.com')
        for message in email_messages:
            data = {'from': message.from_email, 'to': message.to, 'subject': message.subject, 'text': message.body,}
            response = requests.post(f'https://api.mailgun.net/v3/{domain}/messages', auth = ('api', api_key), data = data, timeout = 10,)
            if response.status_code == 200:
                sent_count += 1
            else:
                if not self.fail_silently:
                    raise Exception(f'Mailgun send failed! {response.text}!')
        return sent_count