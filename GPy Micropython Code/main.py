import socket
import time
import pycom
from machine import RTC
from network import LTE
from network import WLAN

# HOST = "cloudsocket.hologram.io"
# PORT = 9999
HOST = "prestoapi.azurewebsites.net"
PORT = 443
DEVICE_KEY = "ABCDEFG" #generated on hologram's portal for each SIM card.
TOPIC = "TOPIC1"

# # Need to use global variables.
# # If in each function you delare a new reference, functionality is broken
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
    host = 'route/test?hellodata=3&hi=true'
    headers = 'POST /api/data/adddata HTTP/1.1\r\n\r\nHost:' + str(host) + str(port) + '\r\n'
    headers += 'Content-Type: application/json\r\nContent-Length: ' + str(len(data)) + '\r\nConnection: keep-aliver\r\n\r\n'
    addr = socket.getaddrinfo(host, port)[0][-1]
    resp = ''
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        incoming = s.recv(500)
        if incoming:
            resp = incoming
        else:
            break
    s.close()
    return []

def APIGet(path, data):
    """This is the function to get data from the PrestoTrax API (After authentication).

    Args:
        path (string): API path

    Returns:
        array: [http status (int), data (string)]
    """
    port = 443
    host = 'route/test?hellodata=3&hi=true'
    headers = 'POST /api/data/adddata HTTP/1.1\r\n\r\nHost:' + str(host) + str(port) + '\r\n'
    headers += 'Content-Type: application/json\r\nContent-Length: ' + str(len(data)) + '\r\nConnection: keep-aliver\r\n\r\n'
    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

    return []


# Returns a network.LTE object with an active Internet connection.
def getLTE():
    # If already used, the lte device will have an active connection.
    # If not, need to set up a new connection.
    if lte.isconnected():
        return lte

    # Modem does not connect successfully without first being reset.
    print("Resetting LTE modem ... ", end="")
    lte.send_at_cmd('AT^RESET')
    print("OK")
    time.sleep(1)
    # While the configuration of the CGDCONT register survives resets,
    # the other configurations don't. So just set them all up every time.
    print("Configuring LTE ", end='')
    # lte.attach(band=2, apn="hologram")
    lte.send_at_cmd('AT+CGDCONT=1,"IP","hologram"')  # Changed this from origninal
    print(".", end='')
    lte.send_at_cmd('AT!="RRC::addscanfreq band=4 dl-earfcn=9410"') # changed band from 28 to 4. I dont know what earfcn=9410 is;
    print(".", end='')
    lte.send_at_cmd('AT+CFUN=1')
    print(" OK")

    # If correctly configured for carrier network, attach() should succeed.
    if not lte.isattached():
        print("Attaching to LTE network ", end='')
        lte.attach()
        while(True):
            if lte.isattached():
                print(" OK")
                pycom.rgbled(0x00FF00)
                time.sleep(.5)
                pycom.rgbled(0x000000)
                break
            #print('.', end='')
            print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
            time.sleep(1)

    # Once attached, connect() should succeed.
    if not lte.isconnected():
        print("Connecting on LTE network ", end='')
        lte.connect()
        while(True):
            if lte.isconnected():
                print(" OK")
                break
            print('.', end='')
            time.sleep(1)

    # Once connect() succeeds, any call requiring Internet access will
    # use the active LTE connection.
    return lte

# Clean disconnection of the LTE network is required for future
# successful connections without a complete power cycle between.
def endLTE():
    print("Disonnecting LTE ... ", end='')
    lte.disconnect()
    print("OK")
    time.sleep(1)
    print("Detaching LTE ... ", end='')
    lte.dettach()
    print("OK")
    
# Program starts here.
try:
    pycom.heartbeat(False)
    pycom.rgbled(0x330000)
    lte = getLTE()
    print(lte)
    s = socket.socket()
    print(s)
    dns_records = socket.getaddrinfo(HOST, PORT)
    print("got dns_records")
    print(dns_records)
    
    message = "Hello World!"
    
    for record in dns_records:
        try:
            # s.connect(record[-1])
            # print("connected")
            # data = '{"k": "%s", "d": "%s", "t": "%s"}' % (DEVICE_KEY, message, TOPIC)
            # s.send(bytes(data, 'ascii'))
            # print("sent")
            # result = s.recv(8).decode()
            # print(result)
            # s.close()
            # s.send()
            

            pycom.rgbled(0x00FF60)
            break
        except Exception as err1:
            try:
                s.close()
            except:
                pass
            print(err1)
            continue

except Exception as err:
    print(err)
    try:
        s.close()
    except:
        pass

finally:
   endLTE()

# from network import LTE
# import time
# import socket
# import pycom

# pycom.heartbeat(False)
# pycom.rgbled(0x330000)

# lte = LTE()
# #lte.init(carrier="tmo")

# #some carriers do not require an APN
# #also, check the band settings with your carrier
# lte.attach(band=2, apn="hologram")
# print("attaching..", end='')
# while not lte.isattached():
#     time.sleep(0.25)

#     print('.',end='')
#     print(lte.send_at_cmd('AT!="fsm"'))         # get the System FSM
# print("attached!")

# lte.connect()
# print("connecting [##",end='')
# while not lte.isconnected():
#     time.sleep(0.25)
#     print('#',end='')
#     print(lte.send_at_cmd('AT!="showphy"'))
#     print(lte.send_at_cmd('AT!="fsm"'))
# print("] connected!")

# pycom.rgbled(0xFF00FF)

# print(socket.getaddrinfo('pycom.io', 80))  
# lte.deinit()
# #now we can safely machine.deepsleep()