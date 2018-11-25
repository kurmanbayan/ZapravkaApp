from django.db import models

# Create your models here.
class City(models.Model):
	name = models.CharField(max_length=100)
	region_id = models.IntegerField(default=0)
	latitude = models.CharField(max_length=200)
	longitude = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Fuel(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Station(models.Model):
	city_id = models.ForeignKey(City, blank=True, default=None, on_delete=models.CASCADE)
	fuel_id = models.ForeignKey(Fuel, blank=True, default=None, on_delete=models.CASCADE)
	station_name = models.CharField(max_length=100)
	rating = models.FloatField(default=0)
	rating_counter = models.IntegerField(default=0)
	longitude = models.CharField(max_length=100)
	latitude = models.CharField(max_length=100)
	address = models.CharField(max_length=200)
	# city_id = models.IntegerField(default=0)
	price = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
	tel = models.CharField(max_length=100)
	image_path = models.CharField(max_length=200)
	brand_id = models.IntegerField(default=0)

	def __str__(self):
		return self.station_name

class Feature(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

# TODO: relate auth.User with this model
# class Reviews