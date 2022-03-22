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
    req = 'POST /' + path + ' HTTP/1.1\r\n\r\nHost:' + str(host) + str(port) + '\r\n\r\n'
    req += 'Content-Type: application/json\r\nContent-Length: ' + str(len(data)) + '\r\nConnection: keep-alive\r\n\r\n'
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes(req, 'utf8'))
    res = ''
    while True:
        incoming = s.recv(500)
        if incoming:
            res = incoming
        else:
            break
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
    req = 'GET /' + path + ' HTTP/1.1\r\n\r\nHost:' + str(host) + str(port) + '\r\n\r\n'
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s = ssl.wrap_socket(s)
    s.connect(addr)
    s.send(req)
    time.sleep(3)
    res = s.recv(5000)
    print(res)
    s.close()
    return res


    
# Program starts here.
print('Begin.')
pycom.heartbeat(False)
pycom.rgbled(0x330000)

import machine
wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='AWI-110361', auth=(WLAN.WPA2, '3el3pAPP'))
while not wlan.isconnected():
    pycom.rgbled(0x000000)
    time.sleep_ms(300)
    pycom.rgbled(0x0080FF)
    time.sleep_ms(300)
print("WiFi connected succesfully")
print(wlan.ifconfig())

print(APIGet('/records/new'))
pycom.rgbled(0x00FF60)