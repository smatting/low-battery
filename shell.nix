let
  pkgs = import <nixpkgs> {};
  lowbattery = pkgs.python3Packages.callPackage ./. {};
in
  (pkgs.python39.withPackages (ps: [ps.setuptools lowbattery])).env
