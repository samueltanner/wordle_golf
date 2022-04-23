from datetime import datetime, timedelta
from myapi.models import User, Score
from django.db.models import Q
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os


def remind_users_to_submit_scores():
    r = MessagingResponse()
    today = datetime.utcnow() - timedelta(hours=8)
    non_submitting_users = User.objects.filter(~Q(score__in=Score.objects.filter(
        created_at__gte=today)))

    for user in non_submitting_users:
        print(user.phone_number)
        message = "Hey asshat, don't forget to submit your score!"
        client = Client(os.environ.get('TWILIO_ACCOUNT_SID', None),
                        os.environ.get('TWILIO_AUTH_TOKEN', None))
        client.messages.create(
            body=message,
            to=user.phone_number, from_=os.environ.get('TWILIO_PHONE_NUMBER', None))
    return
