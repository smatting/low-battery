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


## How to build (nix)

Just build by calling `python3Packages.callPackage` on the repo dir.
For example, run

```
nix-shell -p 'pkgs.python3Packages.callPackage (builtins.fetchTarball {url = https://github.com/smatting/low-battery/archive/c59a29ea3b4c8588dca5331cc84199ddf92bf7b5.tar.gz; sha256 = "09k2zj66c3snz6z9zg6z090v8fkfpyma8addk9ns5g9ra4m4jcbq";}) {}'
```

to create an adhoc shell with `lowbattery` command available.
