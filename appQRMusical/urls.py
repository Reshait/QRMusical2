from django.conf.urls import include, url
from appQRMusical.views import Home, Settings, Play, Songs, Gallery, Multimedia_detail, Multimedia_delete
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

    # Login
	url(r'^login/$', views.Login, name='login'),
	url(r'^logout/$', views.Logout, name='logout'), 

	# Settings
	url(r'^settings/$', Settings.as_view(), name='settings'), 
	url(r'^settings/gallery/$', Gallery.as_view(), name='gallery'), 
	url(r'^settings/gallery/multimedia_detail/(?P<pk>\d+)/$', Multimedia_detail.as_view(), name='multimedia_detail'), 
	url(r'^settings/gallery/(?P<pk>\d+)/delete/$', Multimedia_delete.as_view(), name='multimedia_delete'), 	
	url(r'^settings/gallery/upload/$', views.upload_multimedia, name='upload_multimedia'), 

	  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)