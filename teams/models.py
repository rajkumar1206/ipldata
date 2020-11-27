from django.db import models

# Create your models here.
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=30)
    year = models.ForeignKey('matches.IPLSeason', on_delete=models.CASCADE)
    user = models.ForeignKey('matches.AppUser', on_delete=models.CASCADE, default="")
    team_color = models.CharField(max_length=30, default="white")
    total_matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    nrr = models.FloatField(default=0.0)

    def __str__(self):
        return self.team_name

    class Meta:
        ordering = ['-points', '-nrr']
        unique_together = (("team_name", "year"),)