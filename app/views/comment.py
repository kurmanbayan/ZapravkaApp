from django.http import Http404

from ..models import Station, Comment
from ..serializers import CommentSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

# class based view (CBV)

class StationComment(APIView):
    def get_user_info(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get_station(self, station_id):
        try:
            return Station.objects.get(id=station_id)
        except Station.DoesNotExist:
            raise Http404

    def get(self, request, station_id):
        comments = Comment.objects.filter(station=self.get_station(station_id))
        ser_com = CommentSerializer(comments, many=True)
        return Response(ser_com.data, status=status.HTTP_200_OK)

    def post(self, request, station_id):
        user_id = request.POST["user_id"]
        status = request.POST["status"]
        body = request.POST["body"]
        token = request.META['HTTP_TOKEN']
        try:
            if Token.objects.get(key=token).user.id == int(user_id):
                Comment.objects.create(
                    user=self.get_user_info(user_id),
                    station=self.get_station(station_id),
                    status=status,
                    body=body
                )
                return Response({"message": "created"})
        except Token.DoesNotExist:
            raise Http404

        return Response({"asd": "asd"})
