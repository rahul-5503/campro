import os, json, time
import threading
#from test import find_camera_ip
import scapy.all as scapy

def find_camera_ip(mac_address):
    # Scan local network for all devices                                                                          have to set static jio
    devices = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst="192.168.29.1/24"), timeout=2, verbose=0)[0]
    for _, device in devices:
        if device.haslayer(scapy.ARP):
            if device[scapy.ARP].hwsrc == mac_address:
                #print(device[scapy.ARP].psrc)
                return device[scapy.ARP].psrc  # Return the corresponding IP address

    return None  # Return None if the camera with the given MAC address is not found

def conn_check():
    file_path = 'user_data.json'
    with open(file_path ,'r') as json_file:
        data =json.load(json_file)
        while True:
            time.sleep(20)
            for obj in data:
                mac_address=obj.get('macaddress')
                t1=threading.Thread(target=find_status,args=(mac_address, ),daemon=True)
                t1.start()
                t1.join()
                #print("for")
    
def find_status(mac_address):
    ip_check=find_camera_ip(mac_address)
    if ip_check :#it check the ip address of the is like or not
        print('present',ip_check)
    else:
        print('not')

#conn_check()

