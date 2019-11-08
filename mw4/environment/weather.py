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
# Python  v3.7.4
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
import numpy as np
import requests
# local imports
from mw4.base.tpool import Worker


class Weather(object):
    """
    the class Skymeter inherits all information and handling of the Skymeter device

        >>> weather = Weather()
    """

    __all__ = ['Weather',
               ]

    logger = logging.getLogger(__name__)

    def __init__(self,
                 app=None,
                 ):
        self.app = app

        self.data = {}
        self.running = False

        self.app.update10m.connect(self.updateOpenWeatherMapData)

    def startCommunication(self):
        """
        startCommunication adds a device on the watch list of the server.

        :return: success of reconnecting to server
        """

        self.running = True
        self.updateOpenWeatherMapData()

        return True

    def stopCommunication(self):
        """
        stopCommunication adds a device on the watch list of the server.

        :return: success of reconnecting to server
        """

        self.running = False
        self.data = {}

        return True

    def getWebDataWorker(self, url=''):
        """
        getWebDataWorker fetches a given url and does the error handling.

        :param url:
        :return: data
        """

        if not url:
            return None

        try:
            data = requests.get(url, timeout=30)
        except TimeoutError:
            self.logger.error(f'{url} not reachable')
            return None
        except Exception as e:
            self.logger.error(f'{url} general exception: {e}')
            return None

        if data.status_code != 200:
            self.logger.error(f'{url}: status nok')
            return None
        self.logger.debug(f'{url}: {data.status_code}')
        return data

    @staticmethod
    def getDewPoint(tempAir, relativeHumidity):
        """
        Compute the dew point in degrees Celsius

        :param tempAir: current ambient temperature in degrees Celsius
        :param relativeHumidity: relative humidity in %
        :return: the dew point in degrees Celsius
        """

        if tempAir < -40 or tempAir > 80:
            return 0
        if relativeHumidity < 0 or relativeHumidity > 100:
            return 0

        A = 17.27
        B = 237.7
        alpha = ((A * tempAir) / (B + tempAir)) + np.log(relativeHumidity / 100.0)
        dewPoint = (B * alpha) / (A - alpha)
        return dewPoint

    def updateData(self, data=None):
        """
        updateDate takes the returned data from a web fetch and puts the data in a dict

        :param data:

        :return: success
        """

        if data is None:
            return False

        val = data.json()

        if 'list' not in val:
            return False
        if len(val['list']) == 0:
            return False

        val = val['list'][0]

        if 'main' in val:
            self.data['temperature'] = val['main']['temp'] - 273.15
            self.data['pressure'] = val['main']['grnd_level']
            self.data['humidity'] = val['main']['humidity']
            self.data['dewPoint'] = self.getDewPoint(self.data['temperature'],
                                                     self.data['humidity'])
        if 'clouds' in val:
            self.data['cloudCover'] = val['clouds']['all']
        if 'wind' in val:
            self.data['windSpeed'] = val['wind']['speed']
            self.data['windDir'] = val['wind']['deg']
        if 'rain' in val:
            self.data['rain'] = val['rain']['3h']

        return True

    def getOpenWeatherMapData(self, url=''):
        """
        getOpenWeatherMapData initiates the worker thread to get the web data fetched

        :param url:
        :return: true for test purpose
        """

        worker = Worker(self.getWebDataWorker, url)
        worker.signals.result.connect(self.updateData)
        self.threadPool.start(worker)

        return True

    def updateOpenWeatherMapData(self):
        """
        updateOpenWeatherMap downloads the actual OpenWeatherMap image and displays it in
        environment tab. it checks first if online is set, otherwise not download will take
        place. it will be updated every 10 minutes.

        :return: success
        """

        if not self.app.mainW.ui.isOnline.isChecked():
            return False
        if not self.app.mainW.ui.openWeatherMapKey.text():
            return False
        if not self.running:
            return False

        # prepare coordinates for website
        loc = self.app.mount.obsSite.location
        lat = loc.latitude.degrees
        lon = loc.longitude.degrees
        apiKey = self.ui.app.mainW.openWeatherMapKey.text()

        webSite = 'http://api.openweathermap.org/data/2.5/forecast'
        url = f'{webSite}?lat={lat:1.0f}&lon={lon:1.0f}&APPID={apiKey}'
        self.getOpenWeatherMapData(url=url)

        return True

