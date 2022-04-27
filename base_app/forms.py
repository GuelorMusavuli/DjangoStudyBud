# Class based representation of the form
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):

    class Meta():

        model = Room
        fields = '__all__'
        exclude = ['host', 'participants'] #these will be automatically added based on the authenticated user 
