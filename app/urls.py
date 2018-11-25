from django.urls import path
from . import views

urlpatterns = [
    path('cities/', views.city_list, name='city_list'),
    path('cities/<int:city_id>/', views.city_detail),

    path('stations/', views.StationList.as_view(), name='station'),
    path('stations/<int:station_id>/', views.StationDetail.as_view()),
    # path('auth/join/', views.user_register)
]