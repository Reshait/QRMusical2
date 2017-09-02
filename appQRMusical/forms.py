# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from .models import Multimedia, Player
from django.contrib.auth.models import User

# Create your tests here.

class UploadMultimediaForm(forms.ModelForm):	
	class Meta:
		model = Multimedia
		fields = ['file', 'image', 'players']

	def __init__(self, *args, **kwargs):
		super(UploadMultimediaForm, self).__init__(*args, **kwargs)
		self.fields['file'].widget.attrs.update({'class' : 'form-control'})
		self.fields['image'].widget.attrs.update({'class' : 'form-control btn btn-default btn-file'})
		self.fields['players'].widget.attrs.update({'class' : 'selectpicker', 'multiple' : 'multiple', 'id' : 'select'})


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


class EditEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Get request"""
        self.request = kwargs.pop('request')
        return super(EditEmailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Change email?
        last_email = self.request.user.email
        username = self.request.user.username
        if email != last_email:
            # If doesnt exists in BD
            exists = User.objects.filter(email=email).exclude(username=username)
            if exists:
                raise forms.ValidationError('This emails is already registed.')
        return email


class EditPassForm(forms.Form):
    last_password = forms.CharField(
        label='Last password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='New password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repeat new password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Match pass1 & pass2."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('The passwords doesn\'t be equal.')
        return password2