# AutomationWinTest
Develop automation tool in Windows

问题：
什么是PWM？

日志：
20200619:
今天得到一个重要的结论，远程SSH进去的，不管怎么下命令，叫出来的程式只能在后台执行
必须要改成用远程执行当地脚本的方式才可以

20200610:
需要解决的问题：
1. 开机后，登入到Windows桌面，怎么远程操作Windows系统？
   1. 利用PowerShell的远程处理原理(WinRM)
   2. 
2. 
3. \r'是回车，前者bai使光标到行首，（ducarriage return）

'\n'是换行，zhi后者使光标下移一格，（line feed）

Python中远程控制Windows的方式
1. WMI
2. pywinrm
3. ssh
4. paramiko

## Pywinrm远程管理windows
什么是winRM?

pywinrm github库：https://github.com/diyan/pywinrm

假设现在有A，B两台机器， A作为主控机，B为被控机；

A主控机上面的设置：
1. pip3 install pywinrm
2. done!

B被控机上面的设置：
配置winrm服务：
1. 进入设置/网路：将网路配置文件设置成专用
2. 管理员身份执行Powershell
3. 在PS下执行 "Enable-PSRemoting" 启用winrm
4. 输入以下命令：
   ```Bash
   winrm e winrm/config/listener  #查看winrm service listener
   winrm set winrm/config/service/auth '@{Basic="true"}' #为winrm service配置auth
   winrm set winrm/config/service '@{AllowUnencrypted = "true"}' #为winrm service配置加密方式为允许非加密

   #查看winrm服务的配置
   winrm get winrm/config
   ```
5. 测试
   ```python
   import winrm
   wintest = winrm.Session('http://192.168.0.104:5985/wsman',auth=('Luntest', 'qtc12345'))
   ret = wintest.run_ps('calc')  #用ps执行一个计算机程式，如果要用cmd，就变成run_cmd('calc')
   print(ret)

   '''
   <Response code 0, out "b''", err "b''">
   这段返回值代表什么意思？
   ''' 
   ```
6. 如何查询winrm.Session中有什么函数可以用？
   ```Bash
   $python3
   >>>import winrm
   >>>help(winrm.Session)
   ```
7. pywinrm的用法：
   1. 

## Raspberry GPIO basic operation
### 1. Mainstream GPIO lib intro.
[Python GPIO]  for python use
[wiringPi]  for C use

### 2. Python GPIO config.
1. input above command to install python-dev
   1. `sudo apt-get install python3-dev`
   2. `wget https://sourceforge.net/projects/raspberry-gpio-python/files/latest/download` 下载RPiGPIO库
   3. `tar -zxvf RPi.GPIO-0.7.0.tar.gz` 解压
   4. `cd RPi.GPIO-0.7.0` 进入解压后的资料夹
   5. `sudo python3 setup.py install` 安装RPi.GPIO
   6. 
2. 



```Bash
raspistill -k   # 说这个可以操作Raspberry的cam module
```
Raspberry下可以操作的GPIO库 
1. GPIO Zero
2. WiringPI
3. 

Reference:  
https://pinout.xyz/pinout/pcm
https://gpiozero.readthedocs.io/en/stable/installing.html

Raspberry PI有一个OTP的应用  
https://www.raspberrypi.org/documentation/hardware/industrial/README.md

1、Python GPIO实现
【安装配置】
【1】输入以下指令，安装python-dev
```Bash
sudo apt-get install python-dev
```
【2】依次输入以下指令，安装RPi.GPIO。特别说明，由于RPi.GPIO仍处于不断完善的过程中，请参考<这里>下载最新的安装代码。（或者到本文开头的网盘链接~）
```Bash
cd Downloads
wget https://sourceforge.net/projects/raspberry-gpio-python/files/latest/download
```

输入以下指令进行解压
```Bash
tar -zxvf RPi.GPIO-0.7.0.tar.gz
```
【4】进入解压后的目录

cd RPi.GPIO-0.7.0/
sudo python setup.py install
————————————————
版权声明：本文为CSDN博主「ReCclay」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/ReCclay/article/details/103676649




```python
# Use python to capture a pic.
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(3)
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()
```
If the picture is upside-down you can either reposition your camera using a mount, or leave it as it is and tell Python to flip the image. To do this, add the following lines:

```python
camera.rotation = 180
```

```python
# Use python to capture a pic.
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation = 180
camera.start_preview()
sleep(3)
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()
```

![hardware button](pic/picamera-gpio-setup.png)

Import Button from the gpiozero module at the top of the code, create up a Button connected to pin 17, and change the sleep line to use button.wait_for_press like so:

```python
from picamera import PiCamera
from time import sleep
from gpiozero import Button

button = Button(17)
camera = PiCamera()

camera.start_preview()
button.wait_for_press()
camera.capture('/home/pi/image.jpg')
camera.stop_preview()
```

Take a selfie
If you want to take a photograph of yourself with the camera board, you are going to have to add in a delay to enable you to get into position. You can do this by modifying your program.
>Add a line to your code to tell the program to sleep briefly before capturing an image, as below:

```python
camera.start_preview()
button.wait_for_press()
sleep(3)
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()
```

Stop motion animation
Now that you have successfully taken individual photographs with your camera, it’s time to try combining a series of still images to make a stop motion animation.

>IMPORTANT You must create a new folder to store your stills. In the terminal window, enter mkdir animation.

Modify your code to add a loop to keep taking pictures every time the button is pressed:
```python
camera.start_preview()
frame = 1
while True:
    try:
        button.wait_for_press()
        camera.capture('/home/pi/animation/frame%03d.jpg' % frame)
        frame += 1
    except KeyboardInterrupt:
        camera.stop_preview()
        break
```

Because while True goes on forever, you have to be able to make it exit gracefully. Using try and except means it can deal with an exceptional circumstance - if you force it to stop with Ctrl + C it will close the camera preview and exit the loop

frame%03d means the file will be saved as the name “frame” followed by a 3-digit number with leading zeroes - 001, 002, 003, etc. This allows them to be easily sorted into the correct order for the video.

To generate the video, begin by returning to the terminal window.

Run the video rendering command:

```python
avconv -r 10 -i animation/frame%03d.jpg -qscale 2 animation.h264
```

>Note you’re using %03d again - this is a common format which both Python and avconv understand, and means the photos will be passed in to the video in order.

avconv: command not found ?
If you receive the error avconv: command not found you will need to to install libav-tools.

Enter the following commands in to the terminal to update and upgrade your system:
```Bash
sudo apt-get update
sudo apt-get upgrade
# Now install the libav-tools package:
sudo apt-get install libav-tools
```

Play your video using omxplayer.
```Bash
omxplayer animation.h264
```
You can adjust the frame rate by editing the rendering command. Try changing -r 10 (10 frames per second) to another number.

You can also change the filename of the rendered video to stop it from overwriting your first attempt. To do this, change animation.h264 to something else.





