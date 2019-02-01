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
# Python  v3.6.7
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
from unittest import mock
import pytest
import os
import platform

# external packages
# local import
from mw4.astrometry import astrometryKstars

tempDir = './mw4/test/temp'


@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    yield


def test_init_1():
    home = os.environ.get('HOME')
    binSolve = '/Applications/kstars.app/Contents/MacOS/astrometry/bin/solve-field'
    binImage = '/Applications/kstars.app/Contents/MacOS/astrometry/bin/image2xy'
    index = home + '/Library/Application Support/Astrometry'
    with mock.patch.object(platform,
                           'system',
                           return_value='Darwin'):
        app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
        assert app.binPathSolveField == binSolve
        assert app.binPathImage2xy == binImage
        assert app.indexPath == index
        assert os.path.isfile(tempDir + '/astrometry.cfg')


def test_init_2():
    binSolve = '/usr/bin/solve-field'
    binImage = '/usr/bin/image2xy'
    index = '/usr/share/astrometry'
    with mock.patch.object(platform,
                           'system',
                           return_value='Linux'):
        app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
        assert app.binPathSolveField == binSolve
        assert app.binPathImage2xy == binImage
        assert app.indexPath == index
        assert os.path.isfile(tempDir + '/astrometry.cfg')


def test_init_3():
    with mock.patch.object(platform,
                           'system',
                           return_value='Windows'):
        app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
        assert app.binPathSolveField == ''
        assert app.binPathImage2xy == ''
        assert app.indexPath == ''
        assert os.path.isfile(tempDir + '/astrometry.cfg')


def test_convertToHMS_1():
    app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
    value = 180.0
    ret = app.convertToHMS(value)
    assert ret == '12:00:00'


def test_convertToHMS_1():
    app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
    value = -180.0
    ret = app.convertToHMS(value)
    assert ret == '12:00:00'


def test_convertToDMS_1():
    app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
    value = 90.0
    ret = app.convertToDMS(value)
    assert ret == '+90:00:00'


def test_convertToDMS_2():
    app = astrometryKstars.AstrometryKstars(tempDir=tempDir)
    value = -90.0
    ret = app.convertToDMS(value)
    assert ret == '-90:00:00'
