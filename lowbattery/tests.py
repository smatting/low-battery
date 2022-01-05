#!/usr/bin/env python3

import unittest
import lowbattery.cli

default_config = {'warn_battery_level': 15,
                  'critical_battery_level': 5}

class Tests(unittest.TestCase):
    def test_regular(self):
        state = {'warning_state': None}

        state, notification = lowbattery.cli.update(default_config, state, {'tto': None, 'battery_level': 99, 'charging': 'discharging'})
        assert notification == None
        assert state['warning_state'] == None

        # drops to configred level
        state, notification = lowbattery.cli.update(default_config, state, {'tto': None, 'battery_level': 15, 'charging': 'discharging'})
        assert state['warning_state'] == 'warn'
        assert notification is not None
        assert notification['urgency'] == 'normal'
        assert 'is low' in notification['summary']

        # dont warn on next poll
        state, notification = lowbattery.cli.update(default_config, state, {'tto': None, 'battery_level': 15, 'charging': 'discharging'})
        assert notification is None
        assert state['warning_state'] == 'warn'

        # warn again when critical level is hit
        state, notification = lowbattery.cli.update(default_config, state, {'tto': None, 'battery_level': 5, 'charging': 'discharging'})
        assert notification is not None
        assert notification['urgency'] == 'critical'
        assert 'is critically low' in notification['summary']

        # charger plugged in -> everything resets
        state, notification = lowbattery.cli.update(default_config, state, {'tto': None, 'battery_level': 5, 'charging': 'charging'})
        assert notification is None
        assert state['warning_state'] is None

        # charger unplugged at critical level -> warn again
        state, notification = lowbattery.cli.update(default_config, state, {'tto': None, 'battery_level': 5, 'charging': 'discharging'})
        assert notification is not None
        assert notification['urgency'] == 'critical'
        assert 'is critically low' in notification['summary']

if __name__ == '__main__':
    unittest.main()
