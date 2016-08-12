 #!/usr/bin/env python

import math
import os
import random
from gimpfu import *

def remove_specs(img, layer, x,y):

	pdb.gimp_fuzzy_select(layer, x, y, 255, 2, 1, 0, 0, 0)
	pdb.gimp_selection_invert(img)
	pdb.gimp_edit_clear(layer)
	#gimp.Display()

register(
        "python_fu_remove_specs",
        "Remove additional specs",
    	"",
    	"Genevieve Serafin",
    	"ABR",
    	"Aug 2016",
    	"<Image>/Filters/Test/remove_specs",
        "",
        [
			(PF_INT, 	"x", 	"x coordinate of initial seed fill point", 	864),
			(PF_INT, 	"y", 	"y coordinate of initial seed fill point", 	864),
        ],
        [],
        remove_specs
        )

main()