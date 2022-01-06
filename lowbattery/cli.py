#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys
import time

def parse_upower(s):
    battery_level_m = re.search('percentage:\s*(.*)%', s)
    battery_level_str, = battery_level_m.groups()
    battery_level = int(battery_level_str)

    tto_m = re.search('time to empty:\s*(.*)', s)
    tto = None
    if tto_m is not None:
        tto, = tto_m.groups()

    charging_m = re.search('state:\s*(.*)', s)
    charging, = charging_m.groups()
    return {'battery_level': battery_level, 'tto': tto, 'charging': charging}

def poll_upower_info():
    rp = subprocess.run('upower -i /org/freedesktop/UPower/devices/battery_BAT0', shell=True, check=True, capture_output=True)
    return parse_upower(rp.stdout.decode('utf8'))

def compute_notify(warning_state, battery_level, tto):
    urgency = 'normal'
    if warning_state == 'critical':
        urgency = 'critical'
        body = f'Battery is critically low ({battery_level}%).'
    else:
        body = f'Battery is low ({battery_level}%).'
    if tto is not None:
        body += f' You have approximately {tto}, before the battery runs out of power.'

    notification = {'urgency': urgency, 'body': body}
    return notification

def notify(notification):
    subprocess.run(f'notify-send --urgency={notification["urgency"]} "Battery warning" "{notification["body"]}"', shell=True)

def update(config, last_state, upower_info):
    warning_state = None
    notification = None

    if upower_info['charging'] == 'discharging':
        if upower_info['battery_level'] <= config['critical_battery_level']:
            warning_state = 'critical'
        elif upower_info['battery_level'] <= config['warn_battery_level']:
            warning_state = 'warn'

        if warning_state is not None and warning_state != last_state['warning_state']:
            notification = compute_notify(warning_state, upower_info['battery_level'], upower_info['tto'])

    new_state = {'warning_state': warning_state}
    return new_state, notification

def main_loop(config):
    state = {'warning_state': None}
    while True:
        upower_info = poll_upower_info()
        state, notification = update(config, state, upower_info)
        if notification:
            notify(notification)
        time.sleep(10)

def command_exists(name):
    rp = subprocess.run(f'command -v {name} > /dev/null', shell=True)
    return rp.returncode == 0

def check_dependencies(cmds=['notify-send', 'upower']):
    d = {}
    all_exists = True
    for cmd in cmds:
        d[cmd] = command_exists(cmd)
        all_exists = all_exists and d[cmd]
    if not all_exists:
        print('The following commands are not available, but are required by lowbattery. Please install them.')
        for (command, exists) in d.items():
            if not exists:
                print(f'- "{command}"')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='A tool that notifies when the laptop battery runs low.')
    parser.add_argument('--warn', metavar='PERCENTAGE', type=int, help='notify with critical warning below this battery level. (default: 15)', default=15)
    parser.add_argument('--critical', metavar='PERCENTAGE', type=int, help='notify with warning below this battery level. (default: 5)', default=5)
    args = parser.parse_args(sys.argv[1:])
    config = {
      'warn_battery_level': args.warn,
      'critical_battery_level': args.critical
    }
    check_dependencies()
    main_loop(config)

if __name__ == '__main__':
    main()
