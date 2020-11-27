from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Matches, IPLSeason, AppUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
import json
from django.forms.models import model_to_dict
from teams.models import Team
import django
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import string 
import random 
from rest_framework.authtoken.models import Token


@api_view(['GET', 'POST'])
def index(request):
    return Response({"data": "This is the body field..."}, status=200)



class create_user(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            data = request.data
            print(data)
            # usr = AppUser(key=data["username"])
            # usr.save()
            random_pass = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k = 7))

            print("Random password : "+str(random_pass))

            user =  User.objects.create_user(data["username"], None, random_pass )
            user.save()

            send_mail(
                'Your user ID and password',
                'Your username is : '+ data["username"] + " \npassword : " + random_pass+"\nemail: "+data["email"],
                settings.EMAIL_HOST_USER,
                ['rajkumar.r.mys@gmail.com'],
                fail_silently=False,
            )

            token = Token.objects.create(user=user)
            print(token.key)

            u = AppUser(key=token.key, username=data["username"])
            u.save()

            print("After Adding user")
            return Response({"status": "success"}, status=201)
        except django.db.utils.IntegrityError:
            return Response({"status": "failed", "err": "already exist with the given username"}, status=302)




class add_season(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            data = request.data
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(data)
            print(request.headers)
            obj = IPLSeason(season=data["year"], user=us)
            obj.save()
            return Response({"status": "success"}, status=201)
        except django.db.utils.IntegrityError:
            return Response({"status": "err", "message": "The entered season already exists"}, status=403)


class season_list(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(token)

            data = serializers.serialize(
                "json", IPLSeason.objects.filter(user=us))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=400)



class matches_list(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(token)
            data = serializers.serialize(
                "json", Matches.objects.filter(year=IPLSeason.objects.filter(season=2020, user=us)[0]))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=404)



class matches_list_season(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(token)
            data = serializers.serialize(
                "json", Matches.objects.filter(year=IPLSeason.objects.filter(season=pk, user=us)[0]))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=400)



class add_match(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            # print(request.data)
            data = request.data
            # print(data["year"])
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(token)

            ipl = IPLSeason.objects.filter(season=data["year"], user=us)[0]
            team1 = Team.objects.filter(team_name=data["team_one"], year=IPLSeason.objects.filter(season=data["year"], user=us)[0])[0]
            team2 = Team.objects.filter(team_name=data["team_two"], year=IPLSeason.objects.filter(season=data["year"], user=us)[0])[0]
            toss = Team.objects.filter(team_name=data["toss"], year=IPLSeason.objects.filter(season=data["year"], user=us)[0])[0]
            match_won = Team.objects.filter(team_name=data["match_won"], year=IPLSeason.objects.filter(season=data["year"], user=us)[0])[0]

            print(data["elected"].upper()[0])
            match = Matches(year=ipl, team_one=team1, team_two=team2, team_one_txt=data["team_one"], team_two_txt=data["team_two"], toss_txt=data["toss"], match_won_txt=data["match_won"], toss=toss, elected=data["elected"].upper()[0], first_inning_score=data["first_inning_score"], second_inning_score=data["second_inning_score"], first_inning_over=data["first_inning_over"], second_inning_over=data["second_inning_over"], match_won=match_won )
            match.save()

            Team.objects.filter(team_name=data["team_one"], year=IPLSeason.objects.filter(season=data["year"], user=us)[0]).update(total_matches=data["new_total_matches_1"], wins=data["new_wins_1"], losses=data["new_losses_1"], points=data["new_points_1"], nrr=data["new_nrr_1"])
            Team.objects.filter(team_name=data["team_two"], year=IPLSeason.objects.filter(season=data["year"], user=us)[0]).update(total_matches=data["new_total_matches_2"], wins=data["new_wins_2"], losses=data["new_losses_2"], points=data["new_points_2"], nrr=data["new_nrr_2"])

            return Response({"status": "success"}, status=201)
        except AttributeError:
            return Response({"status": "failed", "err_message": "Please enter the valid attribute credential"}, status=403)
        except ValueError:
            return Response({"status": "failed", "err_message": "Please enter the valid credential"}, status=403)
        except:
            return Response({"status": "failed", "err_message": "Please enter the valid credential"}, status=500)

