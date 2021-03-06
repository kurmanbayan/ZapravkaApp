import math
from django.http import Http404
from .models import City, Station, Comment, Fuel, Feature, StationFuel
from .serializers import CitySerializer, StationSerializer, CommentSerializer, FeatureSerializer, StationFuelSerializer
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

# function based view (FBV)
@api_view(['GET', 'POST'])
def city_list(request, format=None):
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        ser = CitySerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def city_detail(request, city_id):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = CitySerializer(city)
        return Response(ser.data)
    elif request.method == 'PUT':
        ser = CitySerializer(instance=city, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class based view (CBV)
class StationList(APIView):
    def get_city_id(self, city):
        try:
            return City.objects.get(name=city.lower()).id
        except City.DoesNotExist:
            raise Http404
    
    def get(self, request, city, fuel_id):
        city_id = City.objects.get(name=city.lower())
        stations= StationFuel.objects.filter(fuel=fuel_id)
        station_list = []
        for sta in stations:
            if sta.station.city_id == city_id:
                station_ser = StationSerializer(sta.station)
                data = station_ser.data
                data["price"] = sta.price
                station_list.append(
                    data
                )
        return Response(station_list)

    def post(self, request):
        ser = StationSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

# class based view (CBV)
class StationDetail(APIView):
    def get_object(self, station_id):
        try:
            return Station.objects.get(id=station_id)
        except Station.DoesNotExist:
            raise Http404

    def get(self, request, station_id):
        stations = StationFuel.objects.all()

        fuels = []
        for station in stations:
            if station.station.id == station_id:
                fuels.append(
                    {
                        "price": station.price,
                        "fuel": Fuel.objects.get(id = station.fuel.id).name
                    }
                )

        station = Station.objects.get(id = stations[0].station.id)
        serializer = StationSerializer(station)
        data = serializer.data
        data["fuels"] = fuels
        return Response(data)

    def put(self, request, station_id):
        station = self.get_object(station_id)
        serializer = StationSerializer(instance=station, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, station_id):
        station = self.get_object(station_id)
        station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        comments = Comment.objects.filter(station = self.get_station(station_id))
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
                    user = self.get_user_info(user_id),
                    station = self.get_station(station_id),
                    status = status,
                    body = body
                )
                return Response({"message": "created"})
        except Token.DoesNotExist:
            raise Http404

        return Response({"asd": "asd"})

@api_view(['POST'])
def get_nearby_stations(request):
    longitude = float(request.POST["longitude"])
    latitude = float(request.POST["latitude"])

    stations = Station.objects.all()
    station_list = []
    for station in stations:
        dst = math.sqrt(pow(longitude - float(station.longitude), 2) + pow(latitude - float(station.latitude), 2))
        station_list.append((dst, station))
    station_list.sort()
    
    qlist = []
    for (dst, station) in station_list[0:5]:
        qlist.append(station)

    ser = StationSerializer(qlist, many=True)

    return Response(ser.data)

@api_view(['GET'])
def features(request):
    features = Feature.objects.all()
    ser = FeatureSerializer(features, many=True)
    return Response(ser.data, status=status.HTTP_200_OK)
    


# function based view (FBV)




# def station(request):
#    if request.method == "GET":
#       station = Station.objects.all()
#       ser = StationSerializer(station, many=True)
#       return JsonResponse(ser.data, safe=False)
#
# @csrf_exempt
# def station_detail(request, station_id):
#   try:
#     stationDetails = Station.objects.get(pk=station_id)
#   except Exception as e:
#     return JsonResponse({"error": str(e)}, status=404)
#
#   if request.method == "GET":
#     ser = StationSerializer(stationDetails)
#     return JsonResponse(ser.data)
#
# @csrf_exempt
# def user_register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         print (form.errors);
#         if form.is_valid():
#           new_user = form.save()
#           login(request, new_user)
#           return HttpResponse('success')
#         else:
#           return JsonResponse(form.errors)
#     else:
#         return JsonResponse({'output' : "404.html"})

# @csrf_exempt
# def user_login(request):
#     if request.POST:
#         username = password = ''
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         print (user)
#         if user is not None and user.is_active:
#             print("User Login:  Username:" + username + '    Password:' + password)
#             login(request, user)
#             return JsonResponse({'output' : request.user.username})
#         else:
#             return JsonResponse({'output' : "Username or Password wrong!"})
#     else:
#         return JsonResponse({'output' : "404.html"})