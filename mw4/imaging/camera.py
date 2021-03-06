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
from mw4.base.loggerMW import CustomLogger
from mw4.imaging.cameraIndi import CameraIndi
from mw4.imaging.cameraAlpaca import CameraAlpaca


class CameraSignals(PyQt5.QtCore.QObject):
    """
    The DomeSignals class offers a list of signals to be used and instantiated by
    the Mount class to get signals for triggers for finished tasks to
    enable a gui to update their values transferred to the caller back.

    This has to be done in a separate class as the signals have to be subclassed from
    QObject and the Mount class itself is subclassed from object
    """

    __all__ = ['CameraSignals']

    integrated = PyQt5.QtCore.pyqtSignal()
    saved = PyQt5.QtCore.pyqtSignal(object)
    message = PyQt5.QtCore.pyqtSignal(object)

    serverConnected = PyQt5.QtCore.pyqtSignal()
    serverDisconnected = PyQt5.QtCore.pyqtSignal(object)
    deviceConnected = PyQt5.QtCore.pyqtSignal(str)
    deviceDisconnected = PyQt5.QtCore.pyqtSignal(str)


class Camera:

    __all__ = ['Camera',
               ]

    logger = logging.getLogger(__name__)
    log = CustomLogger(logger, {})

    def __init__(self, app):

        self.app = app
        self.threadPool = app.threadPool
        self.signals = CameraSignals()

        self.data = {}
        self.framework = None
        self.run = {
            'indi': CameraIndi(self.app, self.signals, self.data),
            'alpaca': CameraAlpaca(self.app, self.signals, self.data),
        }
        self.name = ''
        self.host = ('localhost', 7624)
        self.isGeometry = False

        # signalling from subclasses to main
        alpacaSignals = self.run['alpaca'].client.signals
        alpacaSignals.serverConnected.connect(self.signals.serverConnected)
        alpacaSignals.serverDisconnected.connect(self.signals.serverDisconnected)
        alpacaSignals.deviceConnected.connect(self.signals.deviceConnected)
        alpacaSignals.deviceDisconnected.connect(self.signals.deviceDisconnected)

        indiSignals = self.run['indi'].client.signals
        indiSignals.serverConnected.connect(self.signals.serverConnected)
        indiSignals.serverDisconnected.connect(self.signals.serverDisconnected)
        indiSignals.deviceConnected.connect(self.signals.deviceConnected)
        indiSignals.deviceDisconnected.connect(self.signals.deviceDisconnected)

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

    def startCommunication(self):
        """
        startCommunication enables the cyclic polling in framework driver

        :return: success
        """

        if self.framework in self.run.keys():
            suc = self.run[self.framework].startCommunication()
            return suc
        else:
            return False

    def stopCommunication(self):
        """
        stopCommunication disables the cyclic polling in framework driver

        :return: success

        """

        if self.framework in self.run.keys():
            suc = self.run[self.framework].stopCommunication()
            return suc
        else:
            return False

    def canSubFrame(self, subFrame=100):
        """
        canSubFrame checks if a camera supports sub framing and reports back

        :param subFrame:
        :return: success
        """
        if subFrame > 100:
            return False
        if subFrame < 10:
            return False
        if 'CCD_FRAME.X' not in self.data or 'CCD_FRAME.Y' not in self.data:
            return False

        # todo: what is the right setting for alpaca as we can ask explicit for subframe

        return True

    def canBinning(self, binning=1):
        """
        canBinning checks if the camera supports that type of binning

        :param binning:
        :return: success
        """
        if binning < 1:
            return False
        if binning > 4:
            return False
        if 'CCD_BINNING.HOR_BIN' not in self.data:
            return False

        return True

    def calcSubFrame(self, subFrame=100):
        """
        calcSubFrame calculates the subFrame parameters depending on the percentage of
        the reduction. the subFrame will be centered on the image area.

        :param subFrame: percentage 0-100 of
        :return: success
        """

        if 'CCD_INFO.CCD_MAX_X' not in self.data:
            return False
        if 'CCD_INFO.CCD_MAX_Y' not in self.data:
            return False

        if subFrame < 10 or subFrame > 100:
            width = self.data['CCD_INFO.CCD_MAX_X']
            height = self.data['CCD_INFO.CCD_MAX_Y']
            posX = 0
            posY = 0
        else:
            width = int(self.data['CCD_INFO.CCD_MAX_X'] * subFrame / 100)
            height = int(self.data['CCD_INFO.CCD_MAX_Y'] * subFrame / 100)
            posX = int((self.data['CCD_INFO.CCD_MAX_X'] - width) / 2)
            posY = int((self.data['CCD_INFO.CCD_MAX_Y'] - height) / 2)

        return posX, posY, width, height

    def sendDownloadMode(self, fastReadout=False):
        """
        setDownloadMode sets the readout speed of the camera

        :return: success
        """

        if self.framework in self.run.keys():
            suc = self.run[self.framework].sendDownloadMode(fastReadout=fastReadout)
            return suc
        else:
            return False

    def expose(self,
               imagePath='',
               expTime=3,
               binning=1,
               subFrame=100,
               fastReadout=True):
        """

        :param imagePath:
        :param expTime:
        :param binning:
        :param subFrame:
        :param fastReadout:
        :return: success
        """

        if self.framework not in self.run.keys():
            return False
        if not imagePath:
            return False
        if not self.canSubFrame(subFrame=subFrame):
            return False
        if not self.canBinning(binning=binning):
            return False

        subFrame = self.calcSubFrame(subFrame)

        if not subFrame:
            return False

        posX, posY, width, height = subFrame

        suc = self.run[self.framework].expose(imagePath=imagePath,
                                              expTime=expTime,
                                              binning=binning,
                                              fastReadout=fastReadout,
                                              posX=posX,
                                              posY=posY,
                                              width=width,
                                              height=height)
        return suc

    def abort(self):
        """
        abort cancels the exposing

        :return: success
        """

        if self.framework not in self.run.keys():
            return False

        suc = self.run[self.framework].abort()
        return suc

    def sendCoolerSwitch(self, coolerOn=False):
        """
        sendCoolerTemp send the desired cooler temp, but does not switch on / off the cooler

        :param coolerOn:
        :return: success
        """

        if self.framework not in self.run.keys():
            return False
        suc = self.run[self.framework].sendCoolerSwitch(coolerOn=coolerOn)
        return suc

    def sendCoolerTemp(self, temperature=0):
        """
        sendCoolerTemp send the desired cooler temp, indi does automatically start cooler

        :param temperature:
        :return: success
        """

        if self.framework not in self.run.keys():
            return False

        suc = self.run[self.framework].sendCoolerTemp(temperature=temperature)
        return suc
