# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Multimedia

# Create your tests here.

class UploadMultimediaForm(forms.ModelForm):	
	class Meta:
		model = Multimedia
		fields = ['file', 'image', 'players']
