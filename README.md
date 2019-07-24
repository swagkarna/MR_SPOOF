![MR_LOGO](https://i.imgur.com/BqnGkVK.png)

# MR_SPOOF v1.2
![made with python](https://forthebadge.com/images/badges/made-with-python.svg) 
![no gluten](https://forthebadge.com/images/badges/gluten-free.svg) 
MR_SPOOF is a python 3 script that can send malicious arp packet in order to disable someone network connection.
please note that this script is in heavy development, if you have any issue, be sure to tell me and i'll do my best to fix it.

- compatible with Debian.
- *Not* compatible with Windows.
- may be compatible with MACos if the requirements are installed correctly.

## Next updates: (if i'm not too lazy)

* global arp spoofing
* intelligent spoofing
* better device scan (because big lol for netdiscover)

### what do you need to run this program ?

you will need:
```
Python 3
the uuid module
the netifaces module
the scapy module
```

### Installation

```
git clone https://github.com/b3rt1ng/MR_SPOOF
cd MR_SPOOF
python3 -m pip3 install -r requirements.txt
```
you may get some issues with the scapy module. to install it, use "pip3 install -r requirements.txt"

### Common issues

__I am running my machine on a VMware, and the script doesn't seems to send any packet proprely.__ 
> Running a pentest machine on a virtual machine can be very tricky when it comes to network attacks and check if your VM is connected hrough wifi and not emulated cable. You can also install scapy using another method than pip3 [here](https://scapy.net/download/). 

__Can i try to run the program on windows ?__
> Yeah, you can also make the program run on a spaceship and on a your grand mother pacemaker kido. 

## what more ?

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

Do not use this script for any illegal purposes.

If you have any kind of error, you can tell me your problems right here [Issues](https://github.com/b3rt1ng/MR_SPOOF/issues)

You can contact me on discord (Berting#4260)
