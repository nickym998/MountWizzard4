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
from datetime import datetime
# external packages
import numpy as np
# local imports
from mw4.base.loggerMW import CustomLogger
from mw4.base.indiClass import IndiClass


class FlipFlatIndi(IndiClass):
    """
    the class FlipFlatIndi inherits all information and handling of the FlipFlat device

        >>> f = FlipFlatIndi(app=None)
    """

    __all__ = ['FlipFlatIndi',
               ]

    logger = logging.getLogger(__name__)
    log = CustomLogger(logger, {})

    # update rate to 1 seconds for setting indi server
    UPDATE_RATE = 1

    def __init__(self, app=None, signals=None, data=None):
        super().__init__(app=app)

        self.signals = signals
        self.data = data

    def setUpdateConfig(self, deviceName):
        """
        _setUpdateRate corrects the update rate of weather devices to get an defined
        setting regardless, what is setup in server side.

        :param deviceName:
        :return: success
        """

        if deviceName != self.name:
            return False

        if self.device is None:
            return False

        update = self.device.getNumber('PERIOD_MS')

        if 'PERIOD' not in update:
            return False

        if update.get('PERIOD', 0) == self.UPDATE_RATE:
            return True

        update['PERIOD'] = self.UPDATE_RATE
        suc = self.client.sendNewNumber(deviceName=deviceName,
                                        propertyName='PERIOD_MS',
                                        elements=update)
        return suc

    def sendCoverPark(self, park=True):
        """

        :param park:
        :return: success
        """

        if self.device is None:
            return False

        cover = self.device.getSwitch('CAP_PARK')

        if 'PARK' not in cover:
            return False
        if 'UNPARK' not in cover:
            return False

        cover['UNPARK'] = not park
        cover['PARK'] = park
        suc = self.client.sendNewSwitch(deviceName=self.name,
                                        propertyName='CAP_PARK',
                                        elements=cover,
                                        )
        return suc
