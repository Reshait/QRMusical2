# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Multimedia, Player

# Create your tests here.

class UploadMultimediaForm(forms.ModelForm):	
	class Meta:
		model = Multimedia
		fields = ['file', 'image', 'players']

class UploadPlayerForm(forms.ModelForm):	
	class Meta:
		model = Player
		fields = ['name', 'description', 'enabled']
