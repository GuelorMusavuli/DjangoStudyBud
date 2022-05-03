# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base_app.models import Room
from .serializers import RoomSerializer


@api_view(['GET']) #http method to access this view
def getRoutes(request):
    """ shows off all the routes(urls) in the api """
    routes =[
        'GET/api',# route to the home page
        'GET/api/rooms', # route to all the rooms
        'GET/api/rooms/:id' # route to a single object room
    ]
    # safe means that we can use more than just python dictionnary inside of this response. It'll turn the routes list into a Json data or list
    # return JsonResponse(routes, safe=False) #simple jsonresponse from a very minimal rest api

    # Using DRF
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # many means we're serializig a queryset of many of room's objects
    return Response(serializer.data) # we want to get back the data attribute rather than the object

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False) 
    return Response(serializer.data)
