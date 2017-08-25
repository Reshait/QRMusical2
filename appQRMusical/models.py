# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Player(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200, blank=True)
	enabled = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Multimedia(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	file = models.FileField()
	image = models.ImageField(upload_to='images/')
	filetype = models.CharField(max_length=3)
	datetime = models.DateTimeField(auto_now_add=True)
	players = models.ManyToManyField(Player)

	class Meta:
		ordering = ('datetime',)

	def __str__(self):
		return self.name
