from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from .models import Player
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
import json
from django.forms.models import model_to_dict
from teams.models import Team
from matches.models import IPLSeason, AppUser

def index(request):
    return HttpResponse("Hello, world. You're at the players page.")


class players_list(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token)
            print(request.user)
            data = serializers.serialize(
                "json", Player.objects.filter(user=us))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=404)



class players_list_by_team(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk):
        try:
            tm = Team.objects.get(team_name=pk, year=IPLSeason.objects.get(pk=2020))
            data = serializers.serialize(
                "json", Player.objects.filter(team=tm))
            json_data = {"status": "success", "data": json.loads(data)}
            return Response(json_data)
        except:
            return Response({"status": "failed"}, status=404)


class player_details(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, pk):
        try:
            print(pk)
            player_detail = Player.objects.get(pk=pk)
            player_detail_dict = model_to_dict(player_detail)
            json_data = {"status": "success", "data": player_detail_dict}
            return Response(json_data, status=200)
        except:
            err_data = {
                "status": "failed",
                "err_message": "Player Doesn't exist with the given player id"}
            return Response(err_data, status=404)




class add_player(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        try:
            token = request.headers["Authorization"][7:]
            print(token)
            us = AppUser.objects.get(key=token)
            print(request.data)
            data = request.data["body"]
            if data["team"] != "Not Known":
                tm = Team.objects.filter(team_name=data["team"], year=IPLSeason.objects.filter(season=data["season"], user=us)[0])[0]
                print(tm)
                player = Player(first_name=data["first_name"], last_name=data["last_name"], date_of_birth=data["date_of_birth"], nationality = data["nationality"], team=tm, user=us, team_name=data["team"])
                player.save()
            else:
                player = Player(first_name=data["first_name"], last_name=data["last_name"], date_of_birth=data["date_of_birth"], nationality = data["nationality"], team=None)
                player.save()

            return Response({"status": "success"}, status=201)
        except AttributeError:
            return Response({"status": "failed", "err_message": "Please enter the valid attribute credential"}, status=403)
        except ValueError:
            return Response({"status": "failed", "err_message": "Please enter the valid credential"}, status=403)



class delete_player(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, pk):
        if Player.objects.filter(pk=pk).exists():
            Player.objects.filter(pk=pk).delete()
            return Response({"status": "success"}, status=203)
        else:
            return Response({"status": "success"}, status=403)



class update_player(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, pk):
        data = request.data["body"]
        # try:
        token = request.headers["Authorization"][7:]
        print(token)
        us = AppUser.objects.get(key=token)
        if Player.objects.filter(pk=pk).exists():
            qs = Player.objects.get(pk=pk)
            dictionary_model = model_to_dict(qs)

            if data["team"] != 'Not Known':
                # print(Team.objects.filter(team_name=data["team"], year=IPLSeason.objects.filter(season=data["season"], user = us)[0]))
                print(us)
                print(Team.objects.filter(team_name=data["team"]))
                print(Team.objects.filter(user=us))
                tm = Team.objects.filter(team_name=data["team"], user=us)[0]

                Player.objects.filter(pk=pk).update(first_name=data["first_name"], last_name=data["last_name"],
                                                                        date_of_birth=data["date_of_birth"], nationality = data["nationality"], team=tm, team_name=data["team"])
                return Response({"status": "success", "data": dictionary_model}, status=201)
            else:
                Player.objects.filter(pk=pk).update(first_name=data["first_name"], last_name=data["last_name"],
                                                                        date_of_birth=data["date_of_birth"], nationality = data["nationality"], team=None)
                return Response({"status": "success", "data": dictionary_model}, status=201)

        else: 
            return Response({"status": "failed", "err_message": "Player with the given Id doesn't exist"}, status=403)
        # except:
            # return Response({"status": "failed", "err_message": "Server error"}, status=503)