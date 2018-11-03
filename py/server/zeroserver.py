import zmq
import time
import sys
import math
import json
import openvr
import math
import numpy
def main():
    openvr.init(openvr.VRApplication_Scene)

    poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
    poses = poses_t()
    port = "5556"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
   
    while True:
        openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
        hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
        #print(str(hmd_pose.mDeviceToAbsoluteTracking))
        rotation = getQuaternion(hmd_pose.mDeviceToAbsoluteTracking)
        location = getLocation(hmd_pose.mDeviceToAbsoluteTracking)
        #print(rotation.x, rotation.y, rotation.z, rotation.w)
        #print("one"+hmd_pose.mDeviceToAbsoluteTracking[1])
        #print("two"+hmd_pose.mDeviceToAbsoluteTracking[2])
        #sys.stdout.flush()
        #  Wait for next request from client
        #i = time.time()
        message = socket.recv()
        print("Received a request: ", message)
        socket.send_string(send_json(rotation=rotation,location=location))
        time.sleep(.00166) 


def send_json(rotation=None, location=None,keys=None):
        i = time.time()
        #"rotation_euler" : "(" + str(0) + "," + str(math.sin(i*.005)*180) + "," + str(0)+")"
        #data["location"]= "("+str(math.sin(i)) +"," + str(0) +"," + str(0) +")" #debug
        data = { "name" : str("bpy.data.objects['Camera']")}
        if location != None:
            data["location"]= "("+str(location.x) +"," + str(location.y) +"," + str(location.z) +")"
            pass 
        
        if rotation != None:    
            data["rotation_quaternion"] = "(" + str(rotation.w) +","+str(rotation.x) +"," + str(rotation.z) +"," + str(rotation.y*-1)+")" 
        
        stringer = json.dumps(data)
        return stringer

def getQuaternion(matrix):
    q = openvr.HmdQuaternion_t()
    q.w = math.sqrt(numpy.fmax(0, 1 + matrix.m[0][0] + matrix.m[1][1]+ matrix.m[2][2])) / 2
    q.x = math.sqrt(numpy.fmax(0, 1 + matrix.m[0][0] - matrix.m[1][1] - matrix.m[2][2])) / 2
    q.y = math.sqrt(numpy.fmax(0, 1 - matrix.m[0][0] + matrix.m[1][1] - matrix.m[2][2])) / 2
    q.z = math.sqrt(numpy.fmax(0, 1 - matrix.m[0][0] - matrix.m[1][1] + matrix.m[2][2])) / 2
    q.x = math.copysign(q.x, matrix.m[2][1] - matrix.m[1][2])
    q.y = math.copysign(q.y, matrix.m[0][2] - matrix.m[2][0])
    q.z = math.copysign(q.z, matrix.m[1][0] - matrix.m[0][1])
    return q

def getLocation(matrix):
    vector = openvr.HmdVector3_t()
    vector.v[0] = matrix.m[0][3]
    vector.v[1] = matrix.m[1][3]
    vector.v[2] = matrix.m[2][3]

main()
