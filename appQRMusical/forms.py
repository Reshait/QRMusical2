# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Multimedia, Player

# Create your tests here.

class UploadMultimediaForm(forms.ModelForm):	
	class Meta:
		model = Multimedia
		fields = ['file', 'image', 'players']

	def __init__(self, *args, **kwargs):
		super(UploadMultimediaForm, self).__init__(*args, **kwargs)
		self.fields['file'].widget.attrs.update({'class' : 'form-control'})
		self.fields['image'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})
		self.fields['players'].widget.attrs.update({'class' : 'selectpicker', 'multiple' : 'multiple'})

class UploadPlayerForm(forms.ModelForm):	
	class Meta:
		model = Player
		fields = ['name', 'description', 'image', 'enabled']

	def __init__(self, *args, **kwargs):
		super(UploadPlayerForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class' : 'form-control'})
		self.fields['description'].widget.attrs.update({'class' : 'form-control'})
		self.fields['image'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})		
		self.fields['enabled'].widget.attrs.update({'class' : 'custom-control-input'})
