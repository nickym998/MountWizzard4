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
import pytest
from unittest import mock
import logging

# external packages
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import pyqtSignal
from mountcontrol.qtmount import Mount

# local import
from mw4.gui.mainWmixin.tabSettImaging import SettImaging
from mw4.gui.widgets.main_ui import Ui_MainWindow
from mw4.gui.widget import MWidget
from mw4.imaging.camera import Camera
from mw4.imaging.focuser import Focuser
from mw4.imaging.filter import Filter
from mw4.telescope.telescope import Telescope
from mw4.base.loggerMW import CustomLogger


@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown(qtbot):
    global ui, widget, Test, Test1, app

    class Test1(QObject):
        mount = Mount(expire=False, verbose=False, pathToData='mw4/test/data')
        update1s = pyqtSignal()
        threadPool = QThreadPool()

    class Test(QObject):
        config = {'mainW': {}}
        threadPool = QThreadPool()
        update1s = pyqtSignal()
        message = pyqtSignal(str, int)
        camera = Camera(app=Test1())
        focuser = Focuser(app=Test1())
        filter = Filter(app=Test1())
        telescope = Telescope(app=Test1())

    widget = QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)

    app = SettImaging(app=Test(), ui=ui,
                      clickable=MWidget().clickable)
    app.changeStyleDynamic = MWidget().changeStyleDynamic
    app.guiSetText = MWidget().guiSetText
    app.close = MWidget().close
    app.deleteLater = MWidget().deleteLater
    app.log = CustomLogger(logging.getLogger(__name__), {})

    qtbot.addWidget(app)

    yield

    del widget, ui, Test, Test1, app


def test_initConfig_1():
    suc = app.initConfig()
    assert suc


def test_storeConfig_1():
    suc = app.storeConfig()
    assert suc


def test_updateParameters_1():
    suc = app.updateParameters()
    assert suc


def test_updateParameters_2():
    app.app.telescope.data['TELESCOPE_INFO.TELESCOPE_FOCAL_LENGTH'] = 1
    app.app.camera.data['CCD_INFO.CCD_PIXEL_SIZE_X'] = 1
    app.app.camera.data['CCD_INFO.CCD_PIXEL_SIZE_Y'] = 1
    app.app.telescope.data['TELESCOPE_INFO.TELESCOPE_APERTURE'] = 1
    app.app.camera.data['CCD_INFO.CCD_MAX_X'] = 1
    app.app.camera.data['CCD_INFO.CCD_MAX_Y'] = 1
    app.app.camera.data['CCD_COOLER.COOLER_ON'] = True
    app.app.camera.data['READOUT_QUALITY.QUALITY_LOW'] = True
    suc = app.updateParameters()
    assert suc


def test_setCoolerTemp_1():
    with mock.patch.object(QMessageBox,
                           'critical'):
        suc = app.setCoolerTemp()
        assert not suc


def test_setCoolerTemp_2():
    app.app.camera.data['CCD_TEMPERATURE.CCD_TEMPERATURE_VALUE'] = 10
    with mock.patch.object(QMessageBox,
                           'critical'):
        with mock.patch.object(QInputDialog,
                               'getInt',
                               return_value=(10, False)):
            suc = app.setCoolerTemp()
            assert not suc


def test_setCoolerTemp_3():
    app.app.camera.data['CCD_TEMPERATURE.CCD_TEMPERATURE_VALUE'] = 10
    with mock.patch.object(QMessageBox,
                           'critical'):
        with mock.patch.object(QInputDialog,
                               'getInt',
                               return_value=(10, True)):
            suc = app.setCoolerTemp()
            assert suc


def test_setFilterNumber_1():
    with mock.patch.object(QMessageBox,
                           'critical'):
        suc = app.setFilterNumber()
        assert not suc


def test_setFilterNumber_2():
    app.app.filter.data['FILTER_SLOT.FILTER_SLOT_VALUE'] = 10
    with mock.patch.object(QMessageBox,
                           'critical'):
        with mock.patch.object(QInputDialog,
                               'getInt',
                               return_value=(10, False)):
            suc = app.setFilterNumber()
            assert not suc


def test_setFilterNumber_3():
    app.app.filter.data['FILTER_SLOT.FILTER_SLOT_VALUE'] = 10
    with mock.patch.object(QMessageBox,
                           'critical'):
        with mock.patch.object(QInputDialog,
                               'getInt',
                               return_value=(10, True)):
            suc = app.setFilterNumber()
            assert suc


def test_setFilterName_1():
    with mock.patch.object(QMessageBox,
                           'critical'):
        suc = app.setFilterName()
        assert not suc


def test_setFilterName_2():
    app.app.filter.data['FILTER_SLOT.FILTER_SLOT_VALUE'] = 10
    with mock.patch.object(QMessageBox,
                           'critical'):
        with mock.patch.object(QInputDialog,
                               'getItem',
                               return_value=(10, False)):
            suc = app.setFilterName()
            assert not suc


def test_setFilterName_3():
    app.app.filter.data['FILTER_SLOT.FILTER_SLOT_VALUE'] = 1
    app.app.filter.data['FILTER_SLOT_NAME_1'] = 'test1'
    app.app.filter.data['FILTER_SLOT_NAME_2'] = 'test2'
    with mock.patch.object(QMessageBox,
                           'critical'):
        with mock.patch.object(QInputDialog,
                               'getItem',
                               return_value=('test1', True)):
            suc = app.setFilterName()
            assert suc


def test_setDownloadModeFast():
    suc = app.setDownloadModeFast()
    assert suc


def test_setDownloadModeSlow():
    suc = app.setDownloadModeSlow()
    assert suc


def test_setCoolerOn():
    suc = app.setCoolerOn()
    assert suc


def test_setCoolerOff():
    suc = app.setCoolerOff()
    assert suc
