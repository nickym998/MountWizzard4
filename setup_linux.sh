#!/bin/bash
rm -rf mountwizzard4
rm -rf mw4
mkdir mountwizzard4
virtualenv mw4 -p python3.7
source mw4/bin/activate
pip install PyQt5==5.12.2
pip install astropy==3.1.2
pip install matplotlib==3.1.1
pip install wakeonlan==1.1.6
pip install requests==2.22.0
pip install requests-toolbelt==0.9.1
pip install skyfield==1.10