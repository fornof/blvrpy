import sys
import time
import openvr
import math
import numpy
openvr.init(openvr.VRApplication_Scene)

poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
poses = poses_t()
def main():
    for i in range(10000):
        openvr.VRCompositor().waitGetPoses(poses, len(poses), None, 0)
        hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
        #print(str(hmd_pose.mDeviceToAbsoluteTracking))
        rotation = getQuaternion(hmd_pose.mDeviceToAbsoluteTracking)
        print(rotation.x, rotation.y, rotation.z, rotation.w)
        #print("one"+hmd_pose.mDeviceToAbsoluteTracking[1])
        #print("two"+hmd_pose.mDeviceToAbsoluteTracking[2])
        sys.stdout.flush()
        time.sleep(0.01)

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


main()
openvr.shutdown()