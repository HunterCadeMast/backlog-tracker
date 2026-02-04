import requests
from django.core.mail.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        sent_count = 0
        for message in email_messages:
            data = {'from': message.from_email, 'to': message.to, 'subject': message.subject, 'text': message.body,}
            response = requests.post(f'https://api.mailgun.net/v3/{message.extra_headers.get('MAILGUN_DOMAIN') or 'mg.gaminglogjam.com'}/messages', auth = ('api', message.extra_headers.get('MAILGUN_API_KEY') or ''), data = data, timeout = 10,)
            if response.status_code == 200:
                sent_count += 1
            else:
                if not self.fail_silently:
                    raise Exception(f'Mailgun send failed! {response.text}!')
        return sent_count