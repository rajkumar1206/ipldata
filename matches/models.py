from django.db import models

from teams.models import Team
from django.contrib.auth.models import User

# Create your models here
class AppUser(models.Model):
    key = models.CharField(max_length=50, primary_key=True, blank=False)
    username = models.CharField(max_length=20, default="")

    def __str__(self):
        return str(self.key)



class IPLSeason(models.Model):
    id = models.AutoField(primary_key=True)
    season = models.IntegerField(default=2020)
    user = models.ForeignKey(AppUser, blank=False, on_delete=models.CASCADE, default="")

    def __str__(self):
        return str(self.season) + ' season'+' ' + str(self.user.username)

    class Meta:
        ordering = ['season']
        unique_together = (('season', 'user'), )


class Matches(models.Model):

    options = (
        ('B', 'BAT'),
        ('F', 'FIELD'),
    )

    year = models.ForeignKey(IPLSeason, on_delete=models.CASCADE, default=2020)
    match_no = models.AutoField(primary_key=True)
    team_one = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, related_name="team_one", default="")
    team_two = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, related_name="team_two", default="")
    team_one_txt = models.CharField(max_length=10, default="")
    team_two_txt = models.CharField(max_length=10, default="")
    toss_txt = models.CharField(max_length=10, default="")
    match_won_txt = models.CharField(max_length=10, default="")
    toss = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, related_name="toss", default="")
    elected = models.CharField(max_length=1, choices=options)
    first_inning_score = models.IntegerField(blank=False)
    first_inning_over = models.FloatField(blank=False)
    second_inning_score = models.IntegerField(blank=False)
    second_inning_over = models.FloatField(blank=False)
    match_won = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="match_won", default="")

    def __str__(self):
        return str(self.match_no) + ' ' + str(self.team_one) + ' vs ' + str(self.team_two)