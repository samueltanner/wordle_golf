from django.core.management.base import BaseCommand
import myapi.cron as cron


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        cron.remind_users_to_submit_scores()
