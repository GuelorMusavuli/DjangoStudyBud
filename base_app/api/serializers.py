# Classes that take a model and fields or object that we want to serialize or turn into a Json data or JavaScript object.

from rest_framework.serializers import ModelSerializer
from base_app.models import Room

class RoomSerializer(ModelSerializer):
    class Meta :
        model = Room
        fields = '__all__'
