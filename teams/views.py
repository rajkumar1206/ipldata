from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from .models import Team
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
import json
from django.forms.models import model_to_dict
from matches.models import IPLSeason, AppUser


def index(request):
    return HttpResponse("Hello, world. You're at the teams page.")


class team_list_season(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(us)
            print(pk)
            data = serializers.serialize(
                "json", Team.objects.filter(year=IPLSeason.objects.filter(season=pk, user=us)[0], user=us))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=404)



class team_list(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(us)
            data = serializers.serialize(
                "json", Team.objects.filter(year=IPLSeason.objects.filter(season=2020, user=us)[0], user=us))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=400)



class add_team(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token) 
            print(us)
            print(request.data)
            data = request.data
            team = Team(team_name=data["team_name"], year=IPLSeason.objects.filter(season=data["season"], user=us)[0], user=us, team_color=data["team_color"])
            team.save()

            return Response({"status": "success"}, status=201)
        except AttributeError:
            return Response({"status": "failed", "err_message": "Please enter the valid attribute credential"}, status=403)
        except ValueError:
            return Response({"status": "failed", "err_message": "Please enter the valid credential"}, status=403)
