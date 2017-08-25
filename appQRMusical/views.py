# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Play + Multimedia
from .models import Player

# Multimedia
from .models import Multimedia
import os
from PIL import Image

# Create your views here.
class Home(TemplateView):
	template_name="home.html"
	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_gray"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "welcome to QRMusical project, made by Teo."
		return context

# ======== PLAY zone ========
class Play(TemplateView):
	template_name="play.html"
	def get_context_data(self, **kwargs):
		context = super(Play, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_pink"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a game."
		context['title'] = "Play"
		context['subtitle'] = "Select a list"
		return context


class Songs(ListView):
	model = Player
	template_name="songs_list.html"
	def get_context_data(self, **kwargs):
		context = super(Songs, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_pink"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select a songs list."
		context['title'] = "Songs list"
		context['subtitle'] = "Select a list of songs"
		return context


# ======== Login zone ========
def Login(request):    
	context = {
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info!',
		'message_text'	:	'Sign in form access to settings.',
	}

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				context['message_alert'] = "alert-success"
				context['message_head'] = "Success! "
				context['message_text'] = "The user <%s> is active." % username

			else:
				context['message_alert'] = "alert-danger"
				context['message_head'] = "Error, "
				context['message_text'] = "The account-user %s is disable." % username		
		else:
			context['message_alert'] = "alert-danger"
			context['message_head'] = "Error, "
			context['message_text'] = "Username or pass incorrects: {0}, {1}".format(username, password)			

	return render(request, 'login.html', context)  


@login_required
def Logout(request):
    logout(request)
    context = {
    	'message_alert' : 	'alert-success',
    	'message_head'	:	'Success!',
    	'message_text'	:	'User logout correctly.',
    }
    return render(request, 'home.html', context)


# ======== Settings zone ========
class Settings(LoginRequiredMixin, TemplateView):
	template_name="settings.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Settings, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Select one to configure."
		context['title'] = "Settings"
		context['subtitle'] = "Configure your app"
		return context


class Gallery(LoginRequiredMixin, ListView):
	model = Multimedia
	template_name="gallery.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	def get_context_data(self, **kwargs):
		context = super(Gallery, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting of the gallery."
		context['title'] = "Gallery"
		context['subtitle'] = "Configure your app"
		return context


class Multimedia_detail(LoginRequiredMixin, DetailView):
	model = Multimedia
	template_name = "multimedia_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Multimedia_detail, self).get_context_data(**kwargs)
		url = str(self.object.file.url)
		url = url[6:] # Deleting 'files/'
		
		if not os.path.exists('appQRMusical/files/temp/'):
			os.mkdir('appQRMusical/files/temp/')
		
		qrencode_command = "qrencode %s -o appQRMusical/files/temp/temp.png -s 6" % (url)
		context['qr'] = os.popen(qrencode_command)

		if context['qr']:
			print("QR code of %s make it!" % self.object.name)

		context['QRM_color'] = "QRM_orange"
		context['title'] = "QR code"
		context['subtitle'] = "QR of multimedia %s" % self.object.name

		img_thumb = square_thumbnail(self.object.image.path)
		imgQR = img_QR("appQRMusical/files/temp/temp.png")
		join_thumbnails(img_thumb, imgQR)

		return context


def square_thumbnail(url):
	thumb_size =300, 300

	img = Image.open(url)
	width, height = img.size

	if width > height:
		delta = width - height
		left = int(delta/2)
		upper = 0
		right = height + left
		lower = height
	else:
		delta = height - width
		left = 0
		upper = int(delta/2)
		right = width
		lower = width + upper

	img = img.crop((left, upper, right, lower))
	img.thumbnail(thumb_size)
	img = img.resize((300,300))
	return img

def img_QR(url):
	imgQR = Image.open(url)
	imgQR = imgQR.resize((300,300))
	imgQR = imgQR.convert('RGB')
	return imgQR


def join_thumbnails(img, imgQR):
	canvas = Image.new('RGB',(600,300))
	canvas.paste(img,(0,0))
	canvas.paste(imgQR,(300,0))
	canvas.show()
	return canvas

