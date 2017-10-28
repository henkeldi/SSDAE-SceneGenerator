# -*- coding: utf-8 -*-

import numpy as np

import gl_utils as gu

from OpenGL.GL import *
import pyassimp

class Renderer(object):


    def __init__(self, meshfile, width, height, samples):
        self._W = width
        self._H = height
        self._scene_fbo = gu.Framebuffer(
            {
                GL_COLOR_ATTACHMENT0: 
                    gu.TextureMultisample(samples, GL_RGB8, self._W, self._H, True)
            }
        )

        self._fbo = gu.Framebuffer(
            {
                GL_COLOR_ATTACHMENT0: 
                    gu.Renderbuffer(GL_RGB8, self._W, self._H)
            }
        )

        scene = pyassimp.load(meshfile)
        vertices =  scene.meshes[0].vertices
        faces =  scene.meshes[0].faces
        pyassimp.release(scene)

        self._vao = gu.VAO(
            {
                (gu.Buffer(vertices*10), 0, 3*4): [(0, 3, GL_FLOAT, GL_FALSE, 0)]
            }, gu.Buffer(faces))       

        ibo_data = np.array([6744, 1, 0, 0, 0], dtype=np.uint32)
        self._ibo = gu.Buffer(ibo_data)

        camera = gu.Camera()

        scene_buffer = gu.Buffer(
            camera.data,
            GL_DYNAMIC_STORAGE_BIT|GL_MAP_WRITE_BIT|GL_MAP_PERSISTENT_BIT
        )

        object_data = np.eye(4, dtype=np.float32)

        object_buffer = gu.Buffer(
            object_data,
            GL_DYNAMIC_STORAGE_BIT|GL_MAP_WRITE_BIT|GL_MAP_PERSISTENT_BIT
        )

        scene_buffer.bind_range(GL_SHADER_STORAGE_BUFFER, 0)
        object_buffer.bind_range(GL_SHADER_STORAGE_BUFFER, 1)

        gu.Program.shader_folder = 'shader'
        self._program = gu.Program('shader.vs', 'shader.frag')
        self._program.compile_and_use()


    def render(self):
        self._vao.bind()
        self._ibo.bind(GL_DRAW_INDIRECT_BUFFER)
        
        self._scene_fbo.bind()
        self._program.use()
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, self._W, self._H)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glUniform1ui(0, 0) # object_id
        glDrawElementsIndirect(GL_TRIANGLES, GL_UNSIGNED_INT, ctypes.c_void_p(0*20))

        glBlitNamedFramebuffer(
            self._scene_fbo.id,
            self._fbo.id,
            0,
            0,
            self._W,
            self._H,
            0,
            0,
            self._W,
            self._H,
            GL_COLOR_BUFFER_BIT,
            GL_NEAREST
        )

        self._fbo.bind()
        img = np.fromstring(glReadPixels(0, 0, self._W, self._H, GL_BGR, GL_UNSIGNED_BYTE), dtype=np.uint8)
        img = img.reshape(self._H, self._W, 3)
        img = np.flipud(img)
        return img