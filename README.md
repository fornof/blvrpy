Hello there, 
to run this , you will need to install pip for blender
https://blender.stackexchange.com/questions/56011/how-to-use-pip-with-blenders-bundled-python

Next you wil need to install the requirements 
```
pip install -R requirements.txt
```

or  ```pip install pyzmq  ``` 

# Start the server
to start the server using blender python (or python with pyzmq installed):

``` python zeroserver.py 5556 ```

This listens for incoming connections on port 5556 and sends them on that socket. 

# Load the blender file 

``` blender blend/blvrpy.blend ```

# Open the blvr.py:
Blender Text Editor 

File

Open 

open py/blender/blvr.py

click Run Script (or alt+ p)

# Results
if all goes well you should see a camera with location being modified across a socket.
This means that technically anything could be used as input for blender now, 
I have the server sending JSON and it is currently setup to read /set  any property of the object. 
the format is this : 
```<object.name>"."<object.key> = <value>```
```
{
   "name":"bpy.data.objects['Camera']",
   "location":"(0,1,2)" 

}
```
would execute as:

```
bpy.data.object["Camera"].location = (0,1,2)
```


# Troubleshooting 
If your blender freezes, go to the console and hit ctrl+c to stop the script. 
It will freeze if the server is not running. 
