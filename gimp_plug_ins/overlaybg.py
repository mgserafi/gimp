#!/usr/bin/env python

import math
import os
import random
from gimpfu import *

DATA_DIR = "D:/data"
DATA_PROC = "C:/Users/Genevieve/Documents/DataSets/Gimp/Processed"

def overlay_bg(obj,fname,n_obj,n,img_w,img_h):

	if (n_obj > 1):
		obj_list = list()
		obj_names = str.split(obj)
		for i in range(n_obj):
		    # store image names
			temp = list()
			for img in os.listdir("%s/%s" % (DATA_PROC, obj_names[i])):
				temp.append("%s/%s/%s" % (DATA_PROC, obj_names[i], img))
			obj_list.append(temp)

	else:
		objs = list()
		for img in os.listdir("%s/%s" % (DATA_PROC, obj)):
			objs.append("%s/%s/%s" % (DATA_PROC, obj, img))

	for i in range(n):

		#create image	
		img = gimp.Image(4000, 3000, RGB)

		# Upload background images
		bgs = list()
		for fold in os.listdir("%s/bg_images" % (DATA_DIR)):
			for im in os.listdir("%s/bg_images/%s" % (DATA_DIR, fold)):
				bgs.append("%s/bg_images/%s/%s" % (DATA_DIR, fold, im))
		
		bg_filename = bgs[int(random.uniform(0,len(bgs)-1))]
		bg_layer = pdb.gimp_file_load_layer(img, bg_filename)
		img.add_layer(bg_layer)
		pdb.gimp_image_lower_item_to_bottom(img, bg_layer)

		# loop through objects
		for j in range(n_obj):

			if (n_obj > 1):
				obj = obj_names[j]
				objs = obj_list[j]

			#upload image as individual layer
			obj_image = None
			obj_filename = objs[int(random.uniform(0,len(objs)-1))]
			obj_layer = pdb.gimp_file_load_layer(img, obj_filename)
			img.add_layer(obj_layer)
		
			#rescale image
			bg_layer.scale(img_w, img_h,False)
			img.resize(bg_layer.width, bg_layer.height, 0,0)

			#rescale, translate and rotate object
			scale = int(random.uniform(5,15))
			obj_layer.scale(obj_layer.width/scale, obj_layer.height/scale, False)

			x = int(random.uniform(0, img_w-obj_layer.width))
			y = int(random.uniform(0, img_h-obj_layer.height))
			obj_layer.translate(x,y)

			angle = random.uniform(0, math.pi*2)
			pdb.gimp_item_transform_rotate(obj_layer, angle, True, obj_layer.width/2, obj_layer.height/2)

			#save mask
			pdb.gimp_layer_resize_to_image_size(obj_layer)
			mask = obj_layer.create_mask(2)
			pdb.file_png_save(img, mask, 
								("%s/gimp_renders/%s/%s_%d_mask_%d.png" % (DATA_DIR, fname, fname, i, j)),
								 "raw_filename", 0, 9, 1, 0, 0, 1, 1)

		#save current image to file
		layer = pdb.gimp_image_merge_visible_layers(img, 1)
		pdb.file_png_save(img, layer, ("%s/gimp_renders/%s/%s_%d.png" % (DATA_DIR, fname, fname, i)),
											 "raw_filename", 0, 9, 1, 0, 0, 1, 1)
		#display image
		# gimp.Display(img)      

register(
        "python_fu_overlay_bg",
        "Save overlaying images to files. Separate object names with space",
    	"Separate object names with space",
    	"Genevieve Serafin",
    	"ABR",
    	"2013",
        "<Toolbox>/Xtns/Languages/Python-Fu/Test/_Overlay",
        "",
        [
        	(PF_STRING, "obj", 	"Object(s) to Overlay", 	"munchkin_white_hot_duck_bath_toy"),
        	(PF_STRING, "fname", 	"Filename to save to", 	"munchkin_white_hot_duck_bath_toy"),
        	(PF_INT, 	"n_obj", 	"Number of objects", 	1),
        	(PF_INT, 	"n", 	"Number of images", 	1),
        	(PF_INT, 	"img_w", 	"Output width", 	640), 
        	(PF_INT, 	"img_h", 	"Output height", 	640),  
        ],
        [],
        overlay_bg
        )

main()