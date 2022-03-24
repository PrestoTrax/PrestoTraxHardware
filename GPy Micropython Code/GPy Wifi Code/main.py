import socket
import time
import pycom
from machine import RTC
from network import LTE
from network import WLAN
import ssl

HOST = "prestoapi.azurewebsites.net"
PORT = 443

lte = LTE()


def APIPost(path, data):
    """This is the function to post data to the PrestoTrax API (After authentication).

    Args:
        path (string): API path
        data (string): JSON data string to send

    Returns:
        array: [http status (int), api response short (string)]
    """
    port = 443
    host = 'prestoapi.azurewebsites.net'
    req = 'POST /' + path + ' HTTP/1.1\r\nHost: ' + str(host) + '\r\n'
    req += 'Content-Type: application/json\r\nContent-Length: ' + str(len(data)) + '\r\nConnection: keep-alive\r\n\r\n'
    req += data
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s = ssl.wrap_socket(s)
    s.connect(addr)
    print("\n\n" + req + "\n")
    s.send(req)
    time.sleep(3)
    res = s.recv(500)
    s.close()
    return res


def APIGet(path):
    """This is the function to get data from the PrestoTrax API (After authentication).

    Args:
        path (string): API path

    Returns:
        array: [http status (int), data (string)]
    """
    port = 443
    host = 'prestoapi.azurewebsites.net'
    req = 'GET /' + path + ' HTTP/1.1\r\nHost: ' + str(host) + '\r\n\r\n'
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s = ssl.wrap_socket(s)
    s.connect(addr)
    print("\n\n" + req + "\n")
    s.send(req)
    time.sleep(3)
    res = s.recv(500)
    s.close()
    return res


    
# Program starts here.
print('Begin.')
pycom.heartbeat(False)
pycom.rgbled(0x330000)

import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='LOPES')
while not wlan.isconnected():
    pycom.rgbled(0x000000)
    time.sleep_ms(300)
    pycom.rgbled(0x0080FF)
    time.sleep_ms(300)
print("WiFi connected succesfully")
print(wlan.ifconfig())

print(APIPost('records/new', '{"owner_id": 8,"parent_device": 1,"reported_lost": 0,"location": { "latitude": "33.512766 / N 33 30\' 45.956", "longitude": "-112.126330 / W 112 7\' 34.786"} }'))
pycom.rgbled(0x00FF60)