from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

import cStringIO
from PIL import Image
from PIL import ImageFilter

import re
import os, base64

def index(request):
	return render(request, 'main/index.html', {})

def calibrate(request):
	return render(request, 'main/calibrate.html', {})

# Create your views here.
def main(request):
	file_name = request.GET.get('file_name')

	if not file_name:
		file_name = "foo.png"

	image = Image.open(settings.STATIC_ROOT + "/images/" + file_name)

	resized_image = image.resize((1200, 800), Image.ANTIALIAS)

	test_image_name = "test_resized.png"
	resized_image.save(settings.STATIC_ROOT + "/images/" + test_image_name)

	return render(request, 'main/main.html', {'test_image_name': test_image_name})

def save_image(request):
	imageURI = request.POST.get('image')
	file_name = request.POST.get('file_name')

	tempimg = cStringIO.StringIO(imageURI.decode('base64'))

	image = Image.open(tempimg)

	loc = settings.STATIC_ROOT + "/images/" + file_name

	image.save(loc)

	return HttpResponse('Image saved to: ' + loc)

def combine_images(request):
	image_file = request.POST.get('image_file')
	mask_file = request.POST.get('mask_file')
	
	image = Image.open(settings.STATIC_ROOT + "/images/" + image_file)
	mask = Image.open(settings.STATIC_ROOT + "/images/" + mask_file)
	
	blurred = image.filter(ImageFilter.GaussianBlur(70))
	sharpened = image.filter(ImageFilter.DETAIL)

	mask.save(settings.STATIC_ROOT + "/images/mask_resize.png")
	# BLUR - use GaussianBlur(50) instead
	# CONTOUR - Looks like a sketch
	# EMBOSS - Like plastic wrap or something
	# FIND_EDGES - Highlights edges only
	# SHARPEN
	
	mask = mask.filter(ImageFilter.GaussianBlur(50))
	
	final_image = Image.composite(blurred, sharpened, mask)

	final_loc = settings.STATIC_ROOT + "/images/" + "iterable3.png"

	final_image.save(final_loc)
	
	return HttpResponse(final_loc)
	
	
def blur(request):
	im_file = request.POST.get('im_file')
	
	image = Image.open(settings.STATIC_ROOT + "/images/" + im_file)
	
	image = image.filter(ImageFilter.GaussianBlur(50))
	
	image.save(settings.STATIC_ROOT + "/images/" + "blurred.png")
	
	return HttpResponse('Image blurred')
	
	
	