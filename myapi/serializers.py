from rest_framework import serializers
from .models import User, Score, GolfGroup


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'id', 'phone_number')


# class ScoreApiSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Score
#         fields = ('game_number', 'score', 'user', 'created_at')


class ScoreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Score
        fields = ('id', 'game_number', 'score', 'user', 'created_at')


class GolfGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GolfGroup
        fields = ('id', 'group_name', 'members')
