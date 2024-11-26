import traceback

from django.core.mail import send_mail
from utility.background_task import BackgroundTask


class EmailReport(BackgroundTask):

    def __init__(self):
        super().__init__()


    def process(self, **kwargs):
        try:
            send_mail(subject=kwargs.get('subject'), message=kwargs.get('message'), from_email=kwargs.get('from_email'),
                      recipient_list=kwargs.get('to_email'))
        except Exception:
            traceback.print_exc()