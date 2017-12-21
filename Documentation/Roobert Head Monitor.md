Roobert V2 - second version of home robot project

		________            ______             _____ 
		___  __ \______________  /_______________  /_
		__  /_/ /  __ \  __ \_  __ \  _ \_  ___/  __/
		_  _, _// /_/ / /_/ /  /_/ /  __/  /   / /_  
		/_/ |_| \____/\____//_.___/\___//_/    \__/

Project website: [http://roobert.springwald.de](http://roobert.springwald.de "http://roobert.springwald.de")

# Head monitor

## Monitor type:

- Geekcreit® 7 Inch 1024 x 600 HD Capacitive IPS LCD Display 5 Point Touch Screen Support Raspberry pi
- [Find it at Bangood](https://www.banggood.com/de/7-Inch-1024-x-600-HDMI-Capacitive-IPS-LCD-Display-For-Raspberry-Pi-Banana-Pi-p-1059318.html?rmmds=search&cur_warehouse=CN "Banggood")

## Usage:

Add to Raspberry Pi config.txt:

	hdmi_group=2
	hdmi_mode=1
	hdmi_mode=87
	hdmi_cvt 1024 600 60 6 0 0 0
	hdmi_drive=1