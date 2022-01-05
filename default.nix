{ lib, buildPythonPackage }:

buildPythonPackage rec {
  pname = "lowbattery";
  version = "1.0.0";

  src = ./.;

  doCheck = false;

  meta = with lib; {
    homepage = "https://github.com/smatting/low-battery";
    description = "A tool that notifies when the laptop battery runs low.";
    license = licenses.mit;
  };
}
