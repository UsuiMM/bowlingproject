from django.contrib.auth import default_app_config
from django.db import models

class MemberModel(models.Model):
    membername = models.CharField(max_length=10)
    point_total = models.IntegerField(default=0)
    ave = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    user_set = models.CharField(max_length=20, default=0)
    def __str__(self):
        return self.membername

class GameModel(models.Model):
    membername = models.CharField(max_length=10)
    point_total = models.IntegerField(default=0)
    ave = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    user_set = models.CharField(max_length=20, default=0)
    def __str__(self):
        return self.membername

class TeamCalculusModel(models.Model):
    team = models.CharField(max_length=3, default=0)
    raund = models.IntegerField(default=0)
    sum_total = models.IntegerField(default=0)
    point_alloc = models.IntegerField(default=0)
    user_set = models.CharField(max_length=20, default=0)
    def __str__(self):
        return self.team + ', SUM ' + str(self.sum_total) + ', Point ' + str(self.point_alloc)

class CoreModel(models.Model):
    teams = (('A', 'A'),('B', 'B'),('C', 'C'),)
    member = models.CharField(max_length=10, default=0)
    raund = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    ave = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    min = models.IntegerField(default=0)
    team_choice = models.CharField(max_length=1, choices=teams)
    pin = models.IntegerField(default=0)
    handicap = models.CharField(default=0, max_length=5)
    score_h = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    user_set = models.CharField(max_length=20, default=0)
    def __str__(self):
        return self.member + ', R' + str(self.raund) + ', Score ' + str(self.score)

class EachGameDataModel(models.Model):
    datetime = models.CharField(max_length=20)
    members = models.TextField(max_length=100)
    points = models.TextField(max_length=100)
    aves = models.TextField(max_length=100)
    maxs = models.TextField(max_length=100)
    mins = models.TextField(max_length=100)
    user_set = models.CharField(max_length=20, default=0)
    def __str__(self):
        return self.datetime