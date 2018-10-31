import bpy
import os.path
import time
import math
import zmq
import sys
import json
""" Author : Robert Fornof
    License : MIT License
    Notes: This script is meant to be run in Blender.
    pip must be installed on Blender.

"""
class ModalTimerOperator(bpy.types.Operator):
    use_read_zeromq = True
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "verypy"
    previous_frame =0
    _timer = None
    # parse json into settings
    def parse_json(self):
         pass
    def get_openvr(self):
        pass

    # this is laggy
    # is there something with smoother
    def read_zeromq(self):
        context = zmq.Context()
        port = 5556
        socket = context.socket(zmq.REQ)
        socket.connect ("tcp://localhost:%s" % port)
        socket.send_string("gimme a json ")
        result = socket.recv()
        #print("from server:" + str(result))
        return result


    def modal(self, context, event):

        frame_current =bpy.data.scenes['Scene'].frame_current
        if frame_current != self.previous_frame:


            x= time.time()
            self.previous_frame = frame_current
            stuff = math.sin(x)
            if self.use_read_zeromq:
                zeromq_result = float(self.read_zeromq())
            if event.type == 'TIMER':
                camera = bpy.data.objects['Camera']

                camera.location =(zeromq_result,camera.location[1], camera.location[2])

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        # timer at .01 for updating works fine
        # 0.001 for heavy machinery
        self._timer = wm.event_timer_add(.0166, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print('timer removed')

def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.ops.screen.animation_play()


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
