import zmq
import time
import sys
import math
import json
def main():
    port = "5556"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
   
    while True:
        #  Wait for next request from client
        i = time.time()
        message = socket.recv()
        print("Received a request: ", message)
        socket.send_string(send_json())
        time.sleep(.0083) 


def send_json(object=None,keys=None):
        i = time.time()
        #"rotation_euler" : "(" + str(0) + "," + str(math.sin(i*.005)*180) + "," + str(0)+")"
        data = { "name" : str("bpy.data.objects['Camera']"), "location": "("+str(math.sin(i)) +"," + str(0) +"," + str(0) +")" 
        }
        stringer = json.dumps(data)
        return stringer

main()
