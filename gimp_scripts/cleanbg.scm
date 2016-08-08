; this is a test to see if i can remove everything

(define (script-fu-clean-bg img inLayer)

  ; clean up transparency
  ( let * (
          ( mask ( car( gimp-layer-copy inLayer TRUE)))
          ( origSel ( car(gimp-selection-save img)))
          )
    (gimp-selection-none img)

    (gimp-image-add-layer img mask -1)

    ;turn into a mask (fully black)
    (gimp-brightness-contrast mask 0 -127)
    (gimp-threshold mask 0 0)

    ;remove alpha channel
    (gimp-layer-flatten mask)

    ;select only ROI
    (gimp-by-color-select mask '(0 0 0) 0 CHANNEL-OP-REPLACE TRUE FALSE 0 FALSE)

    ;invert selection
    (gimp-selection-invert img)

    ;delete
    (gimp-edit-clear inLayer)
    (gimp-layer-add-alpha mask)
    (gimp-edit-clear mask)
    (gimp-image-lower-layer img mask)

    ; Done
    (gimp-selection-load origSel)

    (gimp-displays-flush)

  )
)


(script-fu-register "script-fu-clean-bg"
					_"_Clean Background..."
					_"Clean up background after editing colortoalpha"
					"Genevieve Serafin"
					"Genevieve Serafin"
					"Aug 2016"
          "RGB* GRAY*"
          SF-IMAGE       "Image"      0
          SF-DRAWABLE    "Drawable"   0
					)

(script-fu-menu-register "script-fu-clean-bg"
                    "<Image>/Layer/Transparency/")
