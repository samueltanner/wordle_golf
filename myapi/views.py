from distutils.dir_util import create_tree
from http.client import responses
from django_twilio.decorators import twilio_view
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GolfGroupSerializer, UserAPISerializer, UserSerializer, ScoreSerializer
from .models import User, Score, GolfGroup
from twilio.twiml.messaging_response import MessagingResponse
from datetime import date, timedelta


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserAPISerializer


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
                r.message(
                    'Alright you trigger happy little shit! You already submitted your score today. No take backsies!')
                return r

            score = Score.objects.create(
                game_number=game_number, score=game_score, user=user)
            score.save()

            r.message('Thank you for submitting your score')
            return r
        elif message_array[0].lower() == 'score':
            score = self.get_own_score(user)
            message = "Hey %s, how's it going you fucking dunce? You are %s for the week" % (
                user.username, score)
            r.message(message)
            return r
        elif message_array[0].lower() == 'scoreboard':
            message = "Here comes the shortbus, it's a wonder any of you can even read: "
            group_score_dict = self.get_group_score(1)
            print(group_score_dict)
            for key, value in group_score_dict.items():
                message += "%s: %s, " % (key, value)
            r.message(message)
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

    def roast(score):
        hello


class GolfGroupViewSet(viewsets.ModelViewSet):
    queryset = GolfGroup.objects.all()
    serializer_class = GolfGroupSerializer
