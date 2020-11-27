from django.db import models
from teams.models import Team
from matches.models import AppUser

# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=10, null=False)
    last_name = models.CharField(max_length=10, null=False)
    date_of_birth = models.DateField(null=False)
    nationality = models.CharField(max_length=10, default="India")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, default="")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, default="", blank=False)
    team_name = models.CharField(max_length=30, default="")
    year = models.IntegerField(default=2020)

    def __str__(self):
        return self.first_name + ' ' + self.last_name