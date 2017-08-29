from django import template
import subprocess
import os

from appQRMusical import global_vars

register = template.Library()


@register.simple_tag
def stop_cam():
	print("Stop Cam")

	if global_vars.zbar_status != None:
		os.system("ps -A | grep zbar| awk '{print $1}' | xargs kill -9 $1")
		global_vars.zbar_status = None
		global_vars.message = 'Get close QR code to cam'
		global_vars.cam = 1

	
