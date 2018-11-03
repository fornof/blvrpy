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
    def send_json(self,object=bpy.data.objects['Camera'],keys=None):
        data = { "name" : str(object.name), "location": "("+str(object.location.x) +"," + str(object.location.y) +"," + str(object.location.z) +")" ,
        "rotation_euler" : "(" + str(object.rotation_euler.x) + "," + str(object.rotation_euler.y) + "," + str(object.rotation_euler.z)+")"}
        stringer = json.dumps(data)
        return stringer
    
    def insert_keyframe(self ,object=bpy.data.objects['Camera']):
            object.keyframe_insert(data_path='location',
                    )
            object.keyframe_insert(data_path='rotation_quaternion',
                    )
    # parse json into settings 
    def parse_json(self,json_string):
        my_json= json.loads(str(json_string))
        return my_json
    
    def get_openvr(self):
        pass
  
    def read_zeromq(self,host = "localhost", port=5556):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect ("tcp://%s:%s" % (host ,port))
        #socket.send_string("gimme a json ")
        #blah = self.Container()
        #socket.send_json(self.send_json())
        socket.send_string(self.send_json())
        result = socket.recv()
        print("from server:" + str(result.decode("utf-8")))
        return result.decode("utf-8")
  
    def sculptit(self, context, location):
        tuple_location = tuple(location.strip("()").split(","))
        stroke = [{ "name": "defaultStroke",
                            "mouse" : (0.0, 0.0),
                            "pen_flip" : False,
                            "is_start": True,
                            "location": tuple_location,
                            "pressure": 1.0,
                            "time": 1.0}]
        #bpy.ops.sculpt.brush_stroke(stroke=stroke) 
        
    def modal(self, context, event):
        
        frame_current =bpy.data.scenes['Scene'].frame_current
        if frame_current != self.previous_frame: 
            x= time.time()
            self.previous_frame = frame_current
            zeromq_result = math.sin(x)
            zeromq_result = self.read_zeromq() 
            json = self.parse_json(zeromq_result)
            if event.type == 'TIMER':
                object = json['name']
                ignore_these = ["name", "_id"]
                for key, value in json.items():
                    if key not in ignore_these:
                        print(key, value)
                        exec(object +"." + key +"=" +value)
                        if key == "location":
                            self.sculptit(context, value)
                            
                #exec("camera.location =" + json["location"])
                #print("json rotation is :" + json["rotation_euler"])
                #exec("camera.rotation_euler =" +json["rotation_euler"])
                #self.insert_keyframe(camera)

        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        # timer at .01 for updating works fine
        # 0.001 for heavy machinery 
        self._timer = wm.event_timer_add(.0083, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        print('timer removed')

def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.data.objects['Camera'].rotation_mode = 'QUATERNION'
    bpy.ops.screen.animation_play()


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()