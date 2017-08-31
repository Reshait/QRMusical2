# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, CreateView

# Login
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Settings
from django.contrib.auth.mixins import LoginRequiredMixin

# Play + Multimedia
from .models import Player
import global_vars

# Multimedia
from .models import Multimedia
import os
from PIL import Image
from django.conf import settings
from django.views.generic.edit import FormView
from .forms import UploadMultimediaForm

# Player
from .models import Player
from .forms import UploadPlayerForm
from django.core.urlresolvers import reverse_lazy

#Player Game
import threading
import subprocess


from django.core.urlresolvers import reverse




# Create your views here.
class Home(TemplateView):
	template_name="home.html"
	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_blue"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "welcome to QRMusical project, made by Teo."
		context['title'] = "Welcome!"
		context['subtitle'] = "Willkommen, Bienvenue, Benvenuti, Bienvenido, Namaste, karibu. Let's go to play!!"		
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


def message(request):
#	global_vars.message
	context = {'glob_message' : global_vars.message,}
#	return render(request, 'glob_message.html', context)


def read_code():
		data = global_vars.zbar_status.readline()
		qrcode = str(data)[8:]
		if qrcode:
			print(qrcode)
			global_vars.message = qrcode


def start_cam():
	if global_vars.cam == 0:
		global_vars.message = 'Get close QR code to cam'
		global_vars.cam = 1

	elif global_vars.cam == 1:
		global_vars.zbar_status = os.popen('/usr/bin/zbarcam --prescale=%sx%s' % (global_vars.cam_width, global_vars.cam_height),'r')
		global_vars.cam = 2
		
	elif global_vars.cam == 2:
		if global_vars.zbar_status != None:
			t = threading.Thread(target=read_code)
			t.start()	

def game(id_player):
	if global_vars.game_initialized == False: # First start of game
		mults = Multimedia.objects.filter(players__in=Player.objects.filter(id = id_player))
		global_vars.game_number_objects = mults.count()
		mults = list(mults)
		global_vars.game_objects = mults
		global_vars.game_initialized = True

	url=""
	qrcode = global_vars.message[:-1] # del "\n" in end

	matching = False

	context = {}

	if global_vars.game_success == global_vars.game_number_objects:
		global_vars.game_display = "inline"

	else:
		for obj in global_vars.game_objects:
			if "images" == qrcode.split('/')[0]:
				url = obj.image.url
				
			elif "songs" == qrcode.split('/')[0] or "video" == qrcode.split('/')[0]:
				if obj.file:
					url = obj.file.url
					
			url = url[6:]  # del "files/" of url
			
			if url == qrcode: # Match OK
				global_vars.game_success +=1
				global_vars.game_objects.remove(obj)
				print("ACIERTO!!!!===================================\n%s__\n%s" % (url, global_vars.message))
				global_vars.last_message = global_vars.message
				matching = True
				global_vars.message_alert = "alert-success"
				global_vars.game_image = ('/%s%s') % (settings.MEDIA_URL,obj.image.url[6:])
#				if obj.file and global_vars.game_last_image != global_vars.game_image:
#					command = 'mplayer %s%s' % (settings.MEDIA_ROOT,obj.file.url[6:])
#					print('==========================================\n%s' % command)
#					t = threading.Thread(os.system(command))
#					t.start()
#					global_vars.game_last_image = global_vars.game_image
		
		if global_vars.last_message != global_vars.message and matching == False: # Doesnt match
			global_vars.game_fail += 1
			global_vars.last_message = global_vars.message
			global_vars.message_alert = "alert-danger"
	
	return context
					
		
def player_game(request, id_player):	
	player = Player.objects.get(id=id_player)

	start_cam()

	print(global_vars.message)

	game(id_player)

	context = {'message_alert' : global_vars.message_alert}	
	context['image'] = global_vars.game_image
	context['file'] = global_vars.game_file
	context['message_text'] = global_vars.message
	context['title'] = "%s Player Game" % player.name
	context['subtitle'] = "Select a list of songs"
	context['id_player'] = id_player 
	context['name_player'] = player.name 
	context['game_fail'] = global_vars.game_fail
	context['game_success'] = global_vars.game_success
	context['game_points'] = global_vars.game_points
	context['game_number_objects'] = global_vars.game_number_objects
	context['game_display'] = global_vars.game_display
	
	return render(request, 'player_game.html', context)


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
		if self.object.file:
			url = str(self.object.file.url)
		else:  # If there are not file and only exists image:
			url = str(self.object.image.url)

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
	canvas.save(settings.MEDIA_ROOT+"/temp/img_QR.jpg")


@login_required(login_url='login')
def upload_multimedia(request):

	context = {
		'message_alert' : 	'alert-info',
		'message_head'	:	'Info, ',
		'message_text'	:	'Select a File, and press Upload.',
	}

	if request.method == 'POST':
		context['form'] = UploadMultimediaForm(request.POST, request.FILES)
		if context['form'].is_valid():
			file_up = Multimedia()
			files = request.FILES
			data = request.POST
			file_up.image = files['image']

			if 'file' in files:
				file_up.file = files['file']
				file_up.name = file_up.file.name
			else:
				file_up.file = None
				file_up.name = file_up.image.name

			name, ext = file_up.name.rsplit('.', 1)
			file_up.name = name
			file_up.filetype = ext
			file_up.save()
			file_up.players = dict(request.POST.iterlists())['players']

			context['message_alert'] = "alert-success"
			context['message_head'] = "Success! "
			context['message_text'] = "File \"%s\" upload success" % (file_up.name)

	else:
		context['form'] = UploadMultimediaForm()

	return render(request, 'upload.html', context)	


class Multimedia_update(LoginRequiredMixin, UpdateView):
	model = Multimedia
	fields = ['file', 'image', 'players']
	template_name = 'upload.html'
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_success_url(self):
		return reverse('multimedia_update', kwargs={'pk': self.object.id})


class Multimedia_delete(DeleteView):
	model = Multimedia
	success_url = '/settings/gallery'
	def get_object(self):
		obj = super(Multimedia_delete, self).get_object()

		if obj.file:
			path_file = join_url_with_media_root(obj.file.url)
			os.remove(path_file)

		path_image = join_url_with_media_root(obj.image.url)
		os.remove(path_image)
		return obj	


def join_url_with_media_root(url):
	url = url[6:] # del 'files/'....
	path = os.path.join(settings.MEDIA_ROOT+'%s' % url)
	return path


class Players_list(LoginRequiredMixin, ListView):
	model = Player
	template_name="players_list.html"
	login_url='/login/'
	redirect_field_name = "/login/"

	def get_context_data(self, **kwargs):
		context = super(Players_list, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Players"
		context['subtitle'] = "Configure your app"
		return context


class Update_player(LoginRequiredMixin, UpdateView):
	model = Player
	form_class = UploadPlayerForm
	template_name="player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Update_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Update Player"
		context['subtitle'] = "Update and Configure your player"
		context['songs'] = Multimedia.objects.filter(players__in=[self.object])
		context['btn_label'] = 'Update'
		context['player_id'] = self.object.id
		return context


class Create_player(LoginRequiredMixin, CreateView):
	model = Player
	form_class = UploadPlayerForm
	template_name="player_detail.html"
	login_url='/login/'
	redirect_field_name = "/login/"
	success_url = reverse_lazy('players_list')

	def get_context_data(self, **kwargs):
		context = super(Create_player, self).get_context_data(**kwargs)
		context['QRM_color'] = "QRM_orange"
		context['message_alert'] = "alert-info"
		context['message_head'] = "Info, "
		context['message_text'] = "Setting player's game."
		context['title'] = "Create Player"
		context['subtitle'] = "Create your player"
		context['songs'] = Multimedia.objects.filter(players__in=[self.object])
		context['btn_label'] = "Create"
		return context


@login_required(login_url='login')
def add_multimedia_to_player(request, id):
	objs = Player.objects.filter(id=id)

	context = { 
		'object_list' 	: Multimedia.objects.exclude(players__in=[id]),
		'title' 		: objs[0],
		'subtitle'		: "Add songs to Player %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id
		}

	return render(request, 'add_multimedia_to_player.html', context)	


@login_required(login_url='login')
def add_multimedia_to_player_function(request, id_player, id_multimedia):
	player_to_add = Player.objects.get(id=id_player)
	mults = Multimedia.objects.filter(id=id_multimedia)
	mults[0].players.add(player_to_add)

	objs = Player.objects.filter(id=id_player)

	context = { 
		'object_list' 	: Multimedia.objects.exclude(players__in=[id_player]),
		'title' 		: objs[0],
		'subtitle'		: "Add songs to Player %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		'player_id'		: id_player
		}
	return render(request, 'add_multimedia_to_player.html', context)	


@login_required(login_url='login')
def del_multimedia_of_player_function(request, id_player, id_multimedia):
	player_to_del = Player.objects.get(id=id_player)
	mults = Multimedia.objects.filter(id=id_multimedia)
	mults[0].players.remove(player_to_del)

	objs = Player.objects.filter(id=id_player)

	context = { 
		'object_list' 	: Multimedia.objects.exclude(players__in=[id_player]),
		'title' 		: objs[0],
		'subtitle'		: "Add songs to Player %s" % objs[0],
		'QRM_color'		: "QRM_orange",
		}

	return HttpResponseRedirect('/settings/players_list/%s/update/' % id_player)


@login_required(login_url='login')
def camera(request):    
	cam_width = global_vars.cam_width
	cam_height = global_vars.cam_height
	cam_refresh = global_vars.cam_refresh

	message_alert = 'alert-info'
	message_head = 'Info!'
	message_text = 'Configure the values of camera.' 

	if request.method == 'POST':

		cam_width = request.POST.get('Width')
		cam_height = request.POST.get('Height')
		cam_refresh = request.POST.get('Refresh')

		global_vars.cam_width = cam_width 
		global_vars.cam_height = cam_height
		global_vars.cam_refresh = cam_refresh
		
		message_alert = 'alert-success'
		message_head = 'Success!. '
		message_text = 'Changes saved successfully'

	context = {
		'message_alert' : 	message_alert,
		'message_head'	:	message_head,
		'message_text'	:	message_text,
		'cam_width'		:	cam_width,
		'cam_height'	: 	cam_height,
		'cam_refresh'	: 	cam_refresh,
	}

	return render(request, 'camera.html', context)  

