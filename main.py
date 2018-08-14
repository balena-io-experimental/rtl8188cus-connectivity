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


for connection in NetworkManager.Settings.ListConnections():
    if connection.GetSettings()['connection']['id'] == ssid:
        print('Connection profile already defined. Exiting...')
        exit()

device = NetworkManager.NetworkManager.GetDeviceByIpIface(interface)
print('Device: {}'.format(device.object_path))

start_sleep = 15
print('Sleeping for {} seconds'.format(start_sleep))
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
        'uuid': str(uuid.uuid4()),
        'interface-name': interface,
    },
    'ipv4': {
        'method': 'auto'
    },
    'ipv6': {
        'method': 'auto'
    }
}

connection = NetworkManager.Settings.AddConnection(settings)

print('Connection added: {}'.format(connection.object_path))

try:
    device.RequestScan({})
    print('Scanning for networks...')
except:
    pass

add_sleep = 5
print('Sleeping for {} seconds'.format(add_sleep))
time.sleep(add_sleep)

active_connection = NetworkManager.NetworkManager.ActivateConnection(connection, device, '/')

print('Active connection: {}'.format(active_connection.object_path))

activate_sleep = 20
print('Sleeping for {} seconds'.format(activate_sleep))
time.sleep(activate_sleep)

print('State: {}'.format(active_connection.State))
