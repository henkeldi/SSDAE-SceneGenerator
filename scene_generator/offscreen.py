# -*- coding: utf-8 -*-

from OpenGL.EGL import *
from OpenGL.GL.NV.bindless_texture import *

class Offscreen(object):

    def __init__(self):
        major, minor = ctypes.c_long(), ctypes.c_long()
        self._display = eglGetDisplay(EGL_DEFAULT_DISPLAY)
        if not eglInitialize(self._display, major, minor):
            raise RuntimeError('Unable to initialize')

        num_configs = ctypes.c_long()
        configs = (EGLConfig*2)()

        eglChooseConfig(self._display, None, configs, 2, num_configs)

        eglBindAPI(EGL_OPENGL_API)

        ctx = eglCreateContext(self._display, configs[0], EGL_NO_CONTEXT, None)
        if ctx == EGL_NO_CONTEXT:
            raise RuntimeError( 'Unable to create context' )

        eglMakeCurrent(self._display, EGL_NO_SURFACE, EGL_NO_SURFACE, ctx)

        if not glInitBindlessTextureNV():
            raise RuntimeError('Bindless Textures not supported')

    def close(self):
        eglTerminate(self._display)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()