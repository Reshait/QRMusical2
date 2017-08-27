# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os

# Create your models here.
class Player(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200, blank=True)
	enabled = models.BooleanField(default=False)

	def __str__(self):
		return self.name

def directory_to_upload(self, file):
    name, extension = os.path.splitext(file)
    extension.lower()
    directory = ''

    if extension == '.jpg' or extension == '.jpeg':
        directory = 'images/'

    elif extension == '.mp3' or extension == '.mp4':
        directory = 'songs/'

    elif extension == '.mov':
        directory = 'movies/'

    return os.path.join(directory, file)

class Multimedia(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	file = models.FileField(upload_to=directory_to_upload, null=True, blank=True)
	image = models.ImageField(upload_to='images/')
	filetype = models.CharField(max_length=3)
	datetime = models.DateTimeField(auto_now_add=True)
	players = models.ManyToManyField(Player)

	class Meta:
		ordering = ('datetime',)

	def __str__(self):
		return self.name
