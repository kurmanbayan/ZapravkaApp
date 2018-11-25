from django.http import Http404

from ..models import Station
from ..serializers import StationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# class based view (CBV)
class StationList(APIView):
    def get(self, city_id, fuel_id):
        stations= Station.objects.filter(city_id=city_id, fuel_id=fuel_id)
        ser = StationSerializer(stations, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

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

    def get(self, station_id):
        station = self.get_object(station_id)
        serializer = StationSerializer(station)
        return Response(serializer.data)

    def put(self, request, station_id):
        station = self.get_object(station_id)
        serializer = StationSerializer(instance=station, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, station_id):
        station = self.get_object(station_id)
        station.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
