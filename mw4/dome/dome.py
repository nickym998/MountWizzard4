############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.7.5
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
import logging
# external packages
import PyQt5
# local imports
from mw4.dome.domeIndi import DomeIndi
from mw4.dome.domeAlpaca import DomeAlpaca


class DomeSignals(PyQt5.QtCore.QObject):
    """
    The DomeSignals class offers a list of signals to be used and instantiated by
    the Mount class to get signals for triggers for finished tasks to
    enable a gui to update their values transferred to the caller back.

    This has to be done in a separate class as the signals have to be subclassed from
    QObject and the Mount class itself is subclassed from object
    """

    __all__ = ['DomeSignals']

    azimuth = PyQt5.QtCore.pyqtSignal(object)
    slewFinished = PyQt5.QtCore.pyqtSignal()
    message = PyQt5.QtCore.pyqtSignal(object)

    serverConnected = PyQt5.QtCore.pyqtSignal()
    serverDisconnected = PyQt5.QtCore.pyqtSignal(object)
    deviceConnected = PyQt5.QtCore.pyqtSignal(object)
    deviceDisconnected = PyQt5.QtCore.pyqtSignal(object)


class Dome:

    __all__ = ['Dome',
               ]

    logger = logging.getLogger(__name__)

    def __init__(self, app):

        self.app = app
        self.threadPool = app.threadPool
        self.signals = DomeSignals()

        self.data = {}
        self.framework = None
        self.run = {
            'indi': DomeIndi(self.app, self.signals, self.data),
            'alpaca': DomeAlpaca(self.app, self.signals, self.data),
        }
        self.name = ''

        self.host = ('localhost', 7624)
        self.isGeometry = False

        # signalling from subclasses to main
        self.run['alpaca'].clientSignals.serverConnected.connect(self.serverConnected)
        self.run['alpaca'].clientSignals.serverDisconnected.connect(self.serverDisconnected)
        self.run['alpaca'].clientSignals.deviceConnected.connect(self.deviceConnected)
        self.run['alpaca'].clientSignals.deviceDisconnected.connect(self.deviceDisconnected)
        self.run['indi'].client.signals.serverConnected.connect(self.serverConnected)
        self.run['indi'].client.signals.serverDisconnected.connect(self.serverDisconnected)
        self.run['indi'].client.signals.deviceConnected.connect(self.deviceConnected)
        self.run['indi'].client.signals.deviceDisconnected.connect(self.deviceDisconnected)

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value
        if self.framework in self.run.keys():
            self.run[self.framework].host = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self.framework in self.run.keys():
            self.run[self.framework].name = value

    # wee need to collect dispatch all signals from the different frameworks
    def deviceConnected(self, deviceName):
        self.signals.deviceConnected.emit(deviceName)

    def deviceDisconnected(self, deviceName):
        self.signals.deviceDisconnected.emit(deviceName)

    def serverConnected(self):
        self.signals.serverConnected.emit()

    def serverDisconnected(self, deviceList):
        self.signals.serverDisconnected.emit(deviceList)

    def slewDome(self, altitude=0, azimuth=0):
        """

        :param altitude:
        :param azimuth:
        :return: success
        """

        if not self.data:
            return False

        if self.isGeometry:
            ha = self.app.mount.obsSite.haJNowTarget.radians
            dec = self.app.mount.obsSite.decJNowTarget.radians
            lat = self.app.mount.obsSite.location.latitude.radians
            pierside = self.app.mount.obsSite.piersideTarget
            alt, az = self.app.mount.geometry.calcTransformationMatrices(ha=ha,
                                                                         dec=dec,
                                                                         lat=lat,
                                                                         pierside=pierside)
            alt = alt.degrees
            az = az.degrees
        else:
            alt = altitude
            az = azimuth
        geoStat = 'On' if self.isGeometry else 'Off'
        text = f'Slewing  dome:      az correction: {geoStat}, delta: {azimuth-az:3.1f}°'
        self.app.message.emit(text, 0)

        suc = self.run[self.framework].slewToAltAz(azimuth=az)

        return suc

    def startCommunication(self):
        """

        """

        if self.framework in self.run.keys():
            suc = self.run[self.framework].startCommunication()
            return suc
        else:
            return False

    def stopCommunication(self):
        """

        """

        if self.framework in self.run.keys():
            suc = self.run[self.framework].stopCommunication()
            return suc
        else:
            return False
