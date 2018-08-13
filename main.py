import uuid
import os
import time

import NetworkManager

ssid = os.getenv('WIFI_SSID')
password = os.getenv('WIFI_PASSWORD')
interface = os.getenv('WIFI_INTERFACE')

if not ssid:
    print('WIFI_SSID not exported')
    exit()

if not password:
    print('WIFI_PASSWORD not exported')
    exit()

if not interface:
    print('WIFI_INTERFACE not exported')
    exit()

device = NetworkManager.NetworkManager.GetDeviceByIpIface(interface)
print('Device:', device.object_path)

start_sleep = 15
print('Sleeping for', start_sleep, 'seconds')
time.sleep(start_sleep)

settings = {
    '802-11-wireless': {
        'mode': 'infrastructure',
        'security': '802-11-wireless-security',
        'ssid': ssid,
    },
    '802-11-wireless-security': {
        'auth-alg': 'open',
        'key-mgmt': 'wpa-psk',
        'psk': password,
    },
    'connection': {
        'id': ssid,
        'type': '802-11-wireless',
        'uuid': str(uuid.uuid4())
    },
    'ipv4': {
        'method': 'auto'
    },
    'ipv6': {
        'method': 'auto'
    }
}

connection = NetworkManager.Settings.AddConnection(settings)

print('Connection added:', connection.object_path)

add_sleep = 5
print('Sleeping for', add_sleep, 'seconds')
time.sleep(add_sleep)

active_connection = NetworkManager.NetworkManager.ActivateConnection(connection, device, '/')

print('Active connection:', active_connection.object_path)

activate_sleep = 20
print('Sleeping for', activate_sleep, 'seconds')
time.sleep(activate_sleep)

print('State:', active_connection.State)
