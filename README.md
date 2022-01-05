# low-battery

A tool that notifies when the laptop battery runs low.

```
usage: lowbattery [-h] [--warn PERCENTAGE]
                  [--critical PERCENTAGE]

A tool that notifies when the laptop battery runs low.

optional arguments:
  -h, --help            show this help message and exit
  --warn PERCENTAGE     notify with critical warning below this
                        battery level. (default: 15)
  --critical PERCENTAGE
                        notify with warning below this battery
                        level. (default: 5)
```

`lowbattery` is written in python. It depends on `upower` and `notify-send` being on the `PATH`.
