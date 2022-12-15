**Welcome to the Flinders University OpenCat Project repository!**


Simplfied step by step assembly guide for Nybble:
1. Upload firmwire to the Nyboard using the Petoi Desktop app. Be sure to zero the IMU (gyro sensor) on a flat benchtop or Nybble will not balance well.
https://docs.petoi.com/desktop-app/firmware-uploader

2. To control Nybble with a Rasberry Pi, a pre 4 model must be used due to compatability issues. Follow the Petoi guide to set up the serial port of the Rasberry Pi to interface with the Nybble.
https://docs.petoi.com/api/raspberry-pi-serial-port-as-an-interface

3. Download the OpenCat repository to the Rasberry Pi. With a Github account, the repository can be set up on your Pi using the Pi terminal:
$ sudo apt-get update
$ sudo apt-get install git
$ git config --global user.email "Your@email.com"
$ git config -- global user.name "Your GITHUB username"

To clone the repository to your device, then use:
$ git clone https://github.com/PetoiCamp/OpenCat.git

ALternatively, using the same link, download and install manually.

4. ArdSerial is used to issue serial commands from the Rasberry Pi to the Nyboard. 






https://www.putty.org/
disable ghetty

ardSerial
calibrate
Open cat web interface
ifconfig : find IP address for SSH and VNC to remote control via Wifi

