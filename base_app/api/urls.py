from django.urls import path
from . import views

# url to visit the endpoints
urlpatterns =[
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),
]
