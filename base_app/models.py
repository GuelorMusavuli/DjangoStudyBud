from django.db import models
from django.contrib.auth.models import User # built-user model

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    # The actual user that is gonna be connected to host a room
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    # A topic can have multiple rooms, whereas a room can only have one topic
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null= True)
    name = models.CharField(max_length=200)
    # null means this field can be blank in the DB, blank means we can insert empty form on submission
    description = models.TextField(null=True, blank=True)
    # participants =
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_date', '-created_date']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # oneTomany
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # When room get deleted, also the msgs
    body = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] # displays only 5o chars and not the full msg
