#!/usr/bin/env python3

import re
import subprocess
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
        summary = f'Battery is critically low. Battery is at {battery_level}%.'
    else:
        summary = f'Battery is low. Battery is at {battery_level}%.'
    if tto is not None:
        summary += f' You have approximately {tto}, before the battery runs out of power.'

    notification = {'urgency': urgency, 'summary': summary}
    return notification

def notify(notification):
    subprocess.run(f'notify-send --urgency={notification["urgency"]} "{notification["summary"]}"', shell=True)

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

# TODO: argparse
def main():
    # return poll_upower_info()
    config = {'warn_battery_level': 98,
              'critical_battery_level': 96}
    main_loop(config)

    # with open('./data/discharging.txt', 'r') as f:
    #     print(parse_upower(f.read()))

if __name__ == '__main__':
    main()
