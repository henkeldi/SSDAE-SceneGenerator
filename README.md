# SSDAE Scene Generator

```python
# -*- coding: utf-8 -*-

import os
if not os.environ.get( 'PYOPENGL_PLATFORM' ):
    os.environ['PYOPENGL_PLATFORM'] = 'egl'

import cv2

import renderer
import offscreen

SAMPLES = 16
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MESHFILE = '../asset/Battery.stl'

context = offscreen.Offscreen()

renderer = renderer.Renderer(MESHFILE, WINDOW_WIDTH, WINDOW_HEIGHT, SAMPLES)
img = renderer.render()
cv2.imshow('', img)
cv2.waitKey(0)

context.close()
```