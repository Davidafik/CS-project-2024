# DJI-MSDK-to-PC / OpenDJI
This project seek to give convenient way to control DJI's drones with MSDK enabled, without the
need to make android app each time!

Supported drones:

* `Matrice 350 RTK`
* `Matrice 300 RTK`
* `DJI Mini 4 Pro`
* `DJI Mini 3`
* `DJI Mini 3 Pro`
* `DJI Mavic 3 Enterprise Series`
* `DJI Mavic 3M`
* `DJI Mavic 3TA`
* `Matrice 30 Series`
* `Matrice 4E/4T`
* `Matrice 4D/4TD`
* `Matrice 400`

The project consists of android app that you run on a phone connected to the remote controller,
from your PC you connect to your phone, and you have control over the drone using:
*python*, *c++* or any language you would like with ease over sockets. A complete python library
included with examples for integrating the project easily with any python code.


## How to use
Everything you need is set up and working in main branch.

This project provide, but not limited to:
* ***live video stream*** - from the drone up to your PC monitor, so you can see,
  or even better, process by code, the frames and control your drone by image navigation.
* ***live control*** - you can send movements to the drone from your PC in real time,
  move it however you like in all 8 directions. Imagine you have the joystick functionality,
  but from your python code!
* ***live queries data*** - get access to all the drone features that it can provide,
  get sensor data, including GPS and altitude, control different characteristics of the drone,
  in example distance limit or camera zoom, move the gimbal (camera holder) around to see from different angles,
  and much much more, all in real time.
* ***python library*** - all of this is also maintained from a python library, that provide clear and easy
  usage of the features that the application provides, with plenty of examples, to help you start
  programming and implementing your project in no time.


## How to compile - drone side (server side)
### Android studio
To complie / build the project you will need to install android studio:
https://developer.android.com/studio/install </br>
Follow the the installation guide, and try to compile a blank app.
If that doesn't work, google is your best friend.


### Registering as DJI Developer
To use the MSDK with the drone, one need to obtain a developer key. <br>
For that register to DJI Developer : https://account.dji.com/register <br>
We suggest using the school / university email address for that.

Once registered, go to the developer center : https://developer.dji.com/user/apps <br>
And register an app with the following parameters:
* App Type : `Mobile SDK`
* App Name : `MSDKRemote`
* Software Platform : `Android`
* Package Name : `com.msdkremote`
* Category : *as you want*
* Description : *as you want*

> **Make sure to enter all the names correctly! </br> Failing to do so will result in difficult to identify errors.**

Where ever confirmation is needed just follow the sites quests, usually email confirmation. <br>
Now if you go again to developer center, you should see the app listed, and by clicking in the app-key should appear,
a 24 long hexdecimal string. It will be used in the next step.


### Setting the Project 
Open Android Studio, when promoted to create or open a project, click on open and open the `/MSDKRemote` folder as the root of the project.
> **Do not open the whole git repository!**

When the project is all loaded (give it some time for the gardle to sync) in the right side in the project tree, go to `app/res/values`,
right click on it and create `value resource file`. Name him `secrets`, and leave the other options alone. Now, inside `app/res/values`
should be file named `secrets.xml`. Open him and set him as following:
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="API_KEY">xxxxxxxxxxxxxxxxxxxxxxxx</string>
</resources>
```
Replace the `x`'s with your app key you obtained the previous step. 

### Running the Project
That's it! you now can build the app (the hummer icon upper right side) or even run it on your device! (green arrow icon at the top). <br>
First build may take time as the Android Studio download dependencies that needed to build the app. The next builds are instant.


### Conclusion - android app
That's all! Whenever you like to use the project, you need to launch the app.
> We suggest to try and first fly the drone with the DJI's native app, as it is more user friendly,
> and may help you make sure you know how to connect the drone and get familier with it.

Some features of the app:
* At the top you will see icons of joystick and drone, grey when not connected and green when connected,
  for easy and instant debugging. Near them you will also see the battery percentage left.
* With the three slots in the middle, you can turn off/on each aspect of the project.
  Usually, you will leave them on. They also provide (except the video server) small debugging about the connection,
  so when connected, the text under the title should show that a connection is established.
* Network type and IP address are below the emergency button, show you the IP address of the phone,
  you should connect from the script to (the phone act as the server and you connnect to it from the PC).
* In the bottom of the screen there should be live video stream from the drone. If that doesn't show the video,
  then you whould not get it from your PC either.
  
> Note: some networks, (usually public WIFIs, e.g. univesities and schools) does not permit connection over the local network.
> That mean, even though the IP is correct and the network is the same, no connection will be established.
> We suggest to open local network (hot-point) or use your home WIFI. The text under "Control Server" and "Query Server"
> should help you debugging that.

> Note: `EMERGENCY STOP` button, as the name suggest, is used to stop the drone in emergency.
> If your application loses control of the drone, for example it the application crushed mid flight,
> tap the button to stop all of it movements, return the control to the remote controller (joystick),
> and start automatic landing. </br>
> Don't forget it! it may save your drone's life.

And that all about the application! you should not mind the code of the application.
The intention is that you use it as black box. However, feel free to look inside,
and if you wish to extend and add your own features, just *fork* this repo.
I tried to comment the code and and write it as logical as I could, all for you.


## How to compile - user side (from the PC)
Most of the scripts provided in are in pure python, so it souldn't be a problem to just run them,
once all the relevant packages are installed. But that should not overwhelm you! </br>

You want to use the project from your C++/Java or any other client side language?
Just do it. The communication are all TCP based, and simple string parsing is needed.
And for the video, most video decoder will handle without problem (although we suggets FFMPEG).
If that looks too complex, make wrapper using the python implementation
and send or convert to whatever you can use and familiar with.

NOTE : some scripts uses both *OpenCV* and [*AV*](https://pypi.org/project/av/) (ffmpeg python wrap),
and becouse both use ffmpeg library underhood, that may create [unexpected behavior](https://stackoverflow.com/a/78482628). <br>
To address this issue, install *av* with as following:
```bash
sudo apt-get install libavformat-dev libavdevice-dev
pip install av --no-binary av
```


### Python class - OpenDJI.py
The single python file `OpenDJI.py` contain a class that can manage all that this project can offer.
The methods are commented so you should be able to understand them. The classes that you should
work with are the first two, `OpenDJI` and `EventListener`. The `OpenDJI` class is what holds all
the commands, and `EventListener` is an 'abstruct' class that you should implement (extend),
and provide to asynchronous methods.
The other three classes are used internally, so you should not touch them.
They are mainly to control the network communication in separate threads.

All the modules, (video, control and query) have examples in python to help you understand and use them.


### Python examples
Actually, what you want to do is jump to the python examples, rether then dig in the OpenDJI class.
The examples cover all the functionality you may wish from the project.
The examples are also self explained and heavily commented.

For start, go and run the `FPVDemo` - in this example you can control the drone (if everything is setup correctly),
and fly it like a FPV game from your PC! use the keyboard to control the drone, and see its live image!
Read the file description in the start for more details.


#### Control
This give you control about over the drone, like the controller / joystick. </br>
It can be said that it wrappes the [VirtualStickManager](https://developer.dji.com/api-reference-v5/android-api/Components/IVirtualStickManager/IVirtualStickManager.html).

* `ExampleControl` - In this example you will see how to use the OpenDJI library to control the drone,
  in all of the eight directions, takeoff and land, and to gain control, and set them back, to the controller.
* `ExampleControlRaw` - Just like the previous example, but this one use 'raw' socket and not the ready library.
  If you wish to implement the client side yourself, this example will show you the technicalities of the communication.


#### Video
This give you live imagery from the drone main camera. </br>
Basically, send raw H264 data over the net, uses [CameraStreamManager](https://developer.dji.com/api-reference-v5/android-api/Components/IMediaDataCenter/ICameraStreamManager.html).

* `ExampleVideoSync` - Simple example how to connect to the drone, and get the most recent available frame.
  Actually most of the code is boilerplate to visualize the image with OpenCV, but you don't have to see it to have it (and process it).
* `ExampleVideoAsync` - Example to get the frames asynchronously, and all of them. This is good when you need all the frames,
  a frame flaw, (the sync version may skip frames to get you the most recent), to process it. Just remember, the EventListener
  is called within the thread that handle the socket, so don't block it too much and let the thread continue and parse the next frame.
* `ExampleVideoRaw` - Example on how to handle the video with sockets. This example use PyAV, a wrapper for FFMPEG, so for example,
  if you want to use C++, just download FFMPEG and call it with similar implementation. If you wish to use different video decoder,
  the implementation should be strait forward, the raw packages are H264 stream, and you can actualy save some stream to a file,
  end it with `.avi` or similar, and run it with a video player. For the advanced users, in a new connection, the first frame
  is always a 'P' frame, so you should not worry about connecting after the drone is on.


#### Query
This one gives you control over parameters and different hardware and software characteristics. </br>
I strongly suggest to go and read about the released and available keys [DJIKey](https://developer.dji.com/api-reference-v5/android-api/Components/IKeyManager/DJIKey.html).
You don't have to implement from them notting, but it will show you what keys are available, and can be used.
They also organize the keys by subjects, so it easier to work with thier documentation.

As the number of keys are by the hundreds, it is not the right way to implement them one by one,
and even DJI doesn't do so. The implementation are text based,
somewhat like SQL is, and each command have it own behavior, that you need to know before using. 
That way new released keys are available without any further implementation.
For that the commands are divided in the use itself (get / set / listen / action),
and 'help' function to help you get information about the different keys.

* `ExampleQueryHelp` - In this example you will see how to call helper function about the query commands.
  The queries work with modules divided by hardware component (drone / conroller / camera etc.),
  and by key (battery status / gps location / storage info etc.). The methods inside this module are not for production,
  they are there for the first time you want to use a new key, to understand how to use it.
  This example will show how to get all the available modules, all the available keys inside a specific module,
  (note, some keys are not officialy documented keys), and information about specific key.
* `ExampleQueryGet` - This example show how to get information from a specific key, and parse it.
  This implementation show a bit the difficalt characteristics of the query process,
  as each key needed to be studied individually by the user before use.
* `ExampleQueryListen` - This method show how to listen on a 'key'. Listening on a 'key' will call your implementation
  of 'EventListener' on each new value from this key. Bold example will be GPS, that will update you each new
  coordinate available. This is like calling 'get', but only when the 'get' return a new value.
* `ExampleQuerySet` - The example will teach you how to set a value to a specific key (that can be set).
* `ExampleQueryAction` - The 'action' command is quite similar to the 'set' command, but usually associated
  with more physical actions. For example, turning the motors on is an action, and setting height limit
  is a 'set' command. Moreover, the action command can return special information. 'Set' will return only
  'success' on success, but some action may return different results, conditioned on the environment.
* `ExampleQueryRaw` - As the name suggest, it will show you how to communicate with the drone (or phone)
  directly, with sockets over TCP, rether then the implemented library. Moreover, the script give you everything,
  you can 'get'/'set'/'action'/'listen' and 'help' on any key, in real time. This script, although does not use
  the implemented library is excelent to learn about new keys, and test them. When open, just type '?' and get
  all the information about this script.

The keys are different, and you should get used to use the `ExampleQueryRaw` to understand them.
Play with it as you want, you don't even have to connect the drone, only open the application on
your phone and you are ready and set to test things out.

The keys arguments are divided to three types, native objects, enums, and DJI classes.
They can be identified by the `parameter` in the information of a key.
* The native are the easiest ones, no fency string parsing, just type the value.
  For example, for double value, just type float point number, e.g. 142.63445,
  and for boolean just type it `true` of `false`. They can be identified by parameters
  starting with 'java.lang.' suffix, for example 'java.lang.Integer' for integers.
  For example, type in `ExampleQueryRaw` the command `help Battery Voltage`.
* The enums are values, that cannot be expressed by number or text, but by a name.
  For example, the drone type that is connected, although can be expressed by string,
  have only handful of legitimate values. They can be identified by square brackets '[]'
  in the `values` section, and contain all the available values,
  Type `help Product ProductType` for example.
* The last type are the DJI classes. Each one is of different arguments and and types.
  They are usually to manage multiple values at once. They are mostly in 'Json' like
  format, and can be identified by curvy brackets '{}' in the example.
  A example to use it is in the `ExampleQuerySet` example.
  Type with `help FlightController LEDsSettings` in the `ExampleQueryRaw` to understand it better.

> You don't need a drone to play with the keys. Run the application,
> and connect to it with `ExampleQueryRaw`, to play with it. </br>
> You can also test your 'set' and 'action' arguments, as the the application will return
> a specific error if the argument is invalid, before the error that the
> drone is not connected.

> As written before, the [original DJI documentation](https://developer.dji.com/api-reference-v5/android-api/Components/IKeyManager/DJIKey.html)
> is a friend. All the official keys from there should work flawlessly.
> They are stable and can be explained in greater detail.
> After finding what you want, most of the time the corresponding key
> name is the same but without the 'Key' prefix. (Capitals matter!)

> Be careful when using undocumented keys! some are not working at all
> (not imlemented yet and some just not supported on the device),
> and with no information about them, thier behavior is truly undefined.
