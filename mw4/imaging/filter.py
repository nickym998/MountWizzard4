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
from mw4.imaging.filterIndi import FilterIndi


class FilterSignals(PyQt5.QtCore.QObject):
    """
    The FilterSignals class offers a list of signals to be used and instantiated by
    the Mount class to get signals for triggers for finished tasks to
    enable a gui to update their values transferred to the caller back.

    This has to be done in a separate class as the signals have to be subclassed from
    QObject and the Mount class itself is subclassed from object
    """

    __all__ = ['FilterSignals']

    azimuth = PyQt5.QtCore.pyqtSignal(object)
    slewFinished = PyQt5.QtCore.pyqtSignal()
    message = PyQt5.QtCore.pyqtSignal(object)

    serverConnected = PyQt5.QtCore.pyqtSignal()
    serverDisconnected = PyQt5.QtCore.pyqtSignal(object)
    deviceConnected = PyQt5.QtCore.pyqtSignal(str)
    deviceDisconnected = PyQt5.QtCore.pyqtSignal(str)


class Filter:

    __all__ = ['Filter',
               ]

    logger = logging.getLogger(__name__)
    log = CustomLogger(logger, {})

    def __init__(self, app):

        self.app = app
        self.threadPool = app.threadPool
        self.signals = FilterSignals()

        self.data = {}
        self.framework = None
        self.run = {
            'indi': FilterIndi(self.app, self.signals, self.data),
        }
        self.name = ''

        self.host = ('localhost', 7624)

        # signalling from subclasses to main
        self.run['indi'].client.signals.serverConnected.connect(self.signals.serverConnected)
        self.run['indi'].client.signals.serverDisconnected.connect(self.signals.serverDisconnected)
        self.run['indi'].client.signals.deviceConnected.connect(self.signals.deviceConnected)
        self.run['indi'].client.signals.deviceDisconnected.connect(self.signals.deviceDisconnected)

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

        """

        if self.framework not in self.run.keys():
            return False

        suc = self.run[self.framework].startCommunication()
        return suc

    def stopCommunication(self):
        """

        """

        if self.framework not in self.run.keys():
            return False

        suc = self.run[self.framework].stopCommunication()
        return suc

    def sendFilterNumber(self, filterNumber=1):
        """

        """

        if self.framework not in self.run.keys():
            return False

        suc = self.run[self.framework].sendFilterNumber(filterNumber=filterNumber)
        return suc
