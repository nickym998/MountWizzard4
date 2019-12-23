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
from mw4.base.indiClass import IndiClass


class DomeIndi(IndiClass):
    """
    the class Dome inherits all information and handling of the Dome device. there will be
    some parameters who will define the slewing position of the dome relating to the mount.

        >>> dome = DomeIndi(app=None)
    """

    __all__ = ['DomeIndi',
               ]

    logger = logging.getLogger(__name__)

    # update rate to 1000 milli seconds for setting indi server
    UPDATE_RATE = 1000

    def __init__(self, app=None, signals=None, data=None):
        super().__init__(app=app)

        self.signals = signals
        self.data = data
        self.settlingTime = 0

        self.azimuth = -1
        self.slewing = False

        self.app.update1s.connect(self.updateStatus)

        self.settlingWait = PyQt5.QtCore.QTimer()
        self.settlingWait.setSingleShot(True)
        self.settlingWait.timeout.connect(self.waitSettlingAndEmit)

    @property
    def settlingTime(self):
        return self._settlingTime * 1000

    @settlingTime.setter
    def settlingTime(self, value):
        self._settlingTime = value

    def setUpdateConfig(self, deviceName):
        """
        _setUpdateRate corrects the update rate of dome devices to get an defined
        setting regardless, what is setup in server side.

        :param deviceName:
        :return: success
        """

        if deviceName != self.name:
            return False

        if self.device is None:
            return False

        # setting polling updates in driver
        update = self.device.getNumber('POLLING_PERIOD')

        if 'PERIOD_MS' not in update:
            return False

        if update.get('PERIOD_MS', 0) == self.UPDATE_RATE:
            return True

        update['PERIOD_MS'] = self.UPDATE_RATE
        suc = self.client.sendNewNumber(deviceName=deviceName,
                                        propertyName='POLLING_PERIOD',
                                        elements=update,
                                        )

        return suc

    def updateStatus(self):
        """
        updateStatus emits the actual azimuth status every 3 second in case of opening a
        window and get the signals late connected as INDI does nt repeat any signal of it's
        own

        :return: true for test purpose
        """

        if not self.client.connected:
            return False

        self.signals.azimuth.emit(self.azimuth)

        return True

    def waitSettlingAndEmit(self):
        """
        waitSettlingAndEmit emit the signal for slew finished

        :return: true for test purpose
        """

        self.signals.message.emit('')
        self.signals.slewFinished.emit()

        return True

    def updateNumber(self, deviceName, propertyName):
        """
        updateNumber is called whenever a new number is received in client. it runs
        through the device list and writes the number data to the according locations.

        :param deviceName:
        :param propertyName:
        :return:
        """

        if self.device is None:
            return False
        if deviceName != self.name:
            return False

        for element, value in self.device.getNumber(propertyName).items():
            key = propertyName + '.' + element
            self.data[key] = value
            # print(propertyName, element, value)

            if element != 'DOME_ABSOLUTE_POSITION':
                continue

            # starting condition: don't do anything
            if self.azimuth == -1:
                self.azimuth = value
                continue

            # send trigger for new data
            self.signals.azimuth.emit(self.azimuth)

            # calculate the stop slewing condition
            isSlewing = (self.device.ABS_DOME_POSITION['state'] == 'Busy')
            if isSlewing:
                self.signals.message.emit('slewing')
            if self.slewing and not isSlewing:
                # start timer for settling time and emit signal afterwards
                self.settlingWait.start(self.settlingTime)

            # store for the next cycle
            self.azimuth = value
            self.slewing = isSlewing

        return True

    def slewToAltAz(self, altitude=0, azimuth=0):
        """
        slewToAltAz sends a command to the dome to move to azimuth / altitude. if a dome
        does support this

        :param altitude:
        :param azimuth:
        :return: success
        """

        if self.device is None:
            return False

        if self.name is None or not self.name:
            return False

        position = self.device.getNumber('ABS_DOME_POSITION')

        if 'DOME_ABSOLUTE_POSITION' not in position:
            return False

        position['DOME_ABSOLUTE_POSITION'] = azimuth

        suc = self.client.sendNewNumber(deviceName=self.name,
                                        propertyName='ABS_DOME_POSITION',
                                        elements=position,
                                        )

        if suc:
            self.slewing = True

        return suc