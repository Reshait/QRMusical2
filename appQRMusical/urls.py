from django.conf.urls import include, url
from appQRMusical.views import Home, Settings, Play, Songs, Gallery, Multimedia_detail, Multimedia_delete, Players_list, Update_player, Create_player, Multimedia_update, Player_delete, User
from . import views

# For load images in dev mode
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	# Home
	url(r'^$', Home.as_view(), name='home'),	

	# Play
	url(r'^play/$', Play.as_view(), name='play'),	
	url(r'^play/songs_list/$', Songs.as_view(), name='songs_list'),	
	url(r'^play/songs_list/(?P<id_player>\d+)/player_game/$', views.player_game, name='player_game'),	

    # Login
	url(r'^login/$', views.Login, name='login'),
	url(r'^logout/$', views.Logout, name='logout'), 	

	# Settings
	url(r'^settings/$', Settings.as_view(), name='settings'), 
	# Settings - Gallery
	url(r'^settings/gallery/$', Gallery.as_view(), name='gallery'), 
	url(r'^settings/gallery/multimedia_detail/(?P<pk>\d+)/$', Multimedia_detail.as_view(), name='multimedia_detail'), 
	url(r'^settings/gallery/multimedia_update/(?P<pk>\d+)/$', Multimedia_update.as_view(), name='multimedia_update'), 	
	url(r'^settings/gallery/(?P<pk>\d+)/delete/$', Multimedia_delete.as_view(), name='multimedia_delete'), 	
	url(r'^settings/gallery/upload/$', views.upload_multimedia, name='upload_multimedia'), 
	# Settings - Play
	url(r'^settings/players_list/$', Players_list.as_view(), name='players_list'), 
	url(r'^settings/players_list/(?P<pk>\d+)/update/$', Update_player.as_view(), name='update_player'), 
	url(r'^settings/players_list/(?P<pk>\d+)/delete/$', Player_delete.as_view(), name='player_delete'), 
	url(r'^settings/players_list/create/$', Create_player.as_view(), name='create_player'), 
	url(r'^settings/players_list/(?P<id>\d+)/add_multimedia_to_player/$', views.add_multimedia_to_player, name='add_multimedia_to_player'), 
	url(r'^settings/players_list/(?P<id_player>\d+)/add_multimedia_to_player/(?P<id_multimedia>\d+)/$', views.add_multimedia_to_player_function, name='add_multimedia_to_player_function'), 
	url(r'^settings/players_list/(?P<id_player>\d+)/update/(?P<id_multimedia>\d+)/$', views.del_multimedia_of_player_function, name='del_multimedia_of_player_function'), 
	# Settigns - Camera
	url(r'^settings/camera/$', views.camera, name='camera'), 
	# Settigns - User	
	url(r'^settings/user/$', User.as_view(), name='user'), 
	url(r'^settings/user/edit_email/$', views.edit_email, name='edit_email'), 
	url(r'^settings/user/edit_password/$', views.edit_password, name='edit_password'), 


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
