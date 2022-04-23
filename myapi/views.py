from distutils.dir_util import create_tree
from http.client import responses
from django_twilio.decorators import twilio_view
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GolfGroupSerializer, UserAPISerializer, UserSerializer, ScoreSerializer
from .models import User, Score, GolfGroup
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date, timedelta
import random
from .resources.words import adjectives, nouns, body_parts
from twilio.rest import Client
import os
from rest_framework import permissions


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    # serializer_class = UserAPISerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsSuperUser, ]
        return super(self.__class__, self).get_permissions()


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all().order_by('user')
    serializer_class = ScoreSerializer

    @twilio_view
    def create(self, request):
        message = request.POST.get('Body', '')
        r = MessagingResponse()

        if not message:
            return super().create(request)

        phone_number = request.POST.get('From', '')
        phone_number = phone_number[1:]
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            print("does not exist")
            r.message("You aren't a part of the cool kids club, asshole")
            return r

        message_array = message.split(" ")

        if message_array[0] == 'Wordle':
            game_number = message_array[1]
            game_score = message_array[2][0]

            if game_score.lower() == 'x':
                game_score = 7

            if self.check_game(user, game_number):
                message = 'Alright you trigger-happy, %s! You already submitted your score today. No take backsies!' % (
                    self.roast())
                r.message(message)
                return r

            score = Score.objects.create(
                game_number=game_number, score=game_score, user=user)
            score.save()

            r.message(self.roast(game_score))
            return r
        elif message_array[0].lower() == 'score':
            score = self.get_own_score(user)
            message = "Hey %s, how's it going you %s? You are %s for the week" % (
                user.username, self.roast(), score)
            r.message(message)
            return r
        elif message_array[0].lower() == 'scoreboard':
            message = "Here comes the shortbus, you all are a bunch of %ss: " % (
                self.roast())
            group_score_dict = self.get_group_score(1)
            print(group_score_dict)
            for key, value in group_score_dict.items():
                message += "%s: %s, " % (key, value)
            r.message(message)
            return r
        elif message_array[0].lower() == 'roast' and message_array[1].lower() == 'mitch':
            to = os.environ.get('MITCH_PHONE_NUMBER', None)
            message = "Hey Mitch, you %s! How are those %s? Sent with love from, %s" % (
                self.roast(), random.choice(body_parts), user.username)
            client = Client(os.environ.get('TWILIO_ACCOUNT_SID', None),
                            os.environ.get('TWILIO_AUTH_TOKEN', None))
            client.messages.create(
                body=message,
                to=to, from_=os.environ.get('TWILIO_PHONE_NUMBER', None))
            r.message("Congrats, you roasted Mitch.")
            return r
        else:
            r.message(
                'Please text the result of the "Share" button from Wordle.com')
            return r

    def check_game(self, user, game_number):
        score = Score.objects.filter(user=user, game_number=game_number)
        if score:
            return True
        False

    def get_own_score(self, user):
        r = MessagingResponse()
        score_sum = 0
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        scores = Score.objects.filter(
            user=user, created_at__range=(start, end)).values_list('score', flat=True)
        total_available_points = today.isoweekday() * 6
        days_behind = today.isoweekday() - len(scores)
        score_sum += days_behind * 6

        for n in scores:
            score_sum += n
            score_ratio = '%s/%s' % (score_sum, total_available_points)

        return score_ratio

    def get_group_score(self, group):
        group_score_dict = {}
        group = GolfGroup.objects.get(id=1)
        users = group.members.all()
        for user in users:
            group_score_dict[user.username] = (self.get_own_score(user))

        return group_score_dict

    def roast(self, score=False):
        adj = random.choice(adjectives)
        n = random.choice(nouns)
        if not score:
            return "%s %s" % (adj, n)
        if score:
            if score == "1":
                return "Wow, so you cheated, way to go you %s %s. Your score was recorded." % (adj, n)
            if score == "2":
                return "You must think you are one smart, %s %s. Your score was recorded." % (adj, n)
            if score == "3":
                return "Congrats you average %s %s. Your score was recorded." % (adj, n)
            if score == "4":
                return "I'm not surprised you couldn't do better. Your score was recorded."
            if score == "5":
                return "Was that really hard for you? Your score was recorded."
            if score == "6":
                return "Your performance is astoundingly lacking, you %s %s. Your score was recorded." % (adj, n)
            if score == "7":
                return "Hahahahahahaha! Your score was recorded."


class GolfGroupViewSet(viewsets.ModelViewSet):
    queryset = GolfGroup.objects.all()
    serializer_class = GolfGroupSerializer
