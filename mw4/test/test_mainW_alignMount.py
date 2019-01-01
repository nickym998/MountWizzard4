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
import unittest.mock as mock
import logging
import pytest
# external packages
import PyQt5.QtGui
import PyQt5.QtWidgets
import PyQt5.uic
import PyQt5.QtTest
import PyQt5.QtCore
# local import
from mw4 import mainApp

test = PyQt5.QtWidgets.QApplication([])
mwGlob = {'workDir': '.',
          'configDir': './mw4/test/config',
          'dataDir': './mw4/test/config',
          'modeldata': 'test',
          }

'''
@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    global spy
    global app

    app = mainApp.MountWizzard4(mwGlob=mwGlob)
    spy = PyQt5.QtTest.QSignalSpy(app.message)
    yield
    spy = None
    app = None
'''
app = mainApp.MountWizzard4(mwGlob=mwGlob)
spy = PyQt5.QtTest.QSignalSpy(app.message)


def test_loadAlignBuildFile_1(qtbot):
    with mock.patch.object(app.mainW,
                           'openFile',
                           return_value=('build', 'test', 'bpts')):
        with mock.patch.object(app.data,
                               'loadBuildP',
                               return_value=True):
            with qtbot.waitSignal(app.message) as blocker:
                suc = app.mainW.loadAlignBuildFile()
                assert suc
            assert ['Align build file [test] loaded', 0] == blocker.args


def test_loadAlignBuildFile_2(qtbot):
    with mock.patch.object(app.mainW,
                           'openFile',
                           return_value=('', '', '')):
        suc = app.mainW.loadAlignBuildFile()
        assert not suc


def test_loadAlignBuildFile_3(qtbot):
    with mock.patch.object(app.mainW,
                           'openFile',
                           return_value=('build', 'test', 'bpts')):
        with mock.patch.object(app.data,
                               'loadBuildP',
                               return_value=False):
            with qtbot.waitSignal(app.message) as blocker:
                suc = app.mainW.loadAlignBuildFile()
                assert suc
            assert ['Align build file [test] cannot no be loaded', 2] == blocker.args


def test_saveAlignBuildFile_1(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('test')
    with mock.patch.object(app.mainW,
                           'saveFile',
                           return_value=('build', 'test', 'bpts')):
        with mock.patch.object(app.data,
                               'saveBuildP',
                               return_value=True):
            with qtbot.waitSignal(app.message) as blocker:
                suc = app.mainW.saveAlignBuildFile()
                assert suc
            assert ['Align build file [test] saved', 0] == blocker.args


def test_saveAlignBuildFile_2(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('')
    with qtbot.waitSignal(app.message) as blocker:
        suc = app.mainW.saveAlignBuildFile()
        assert not suc
    assert ['Align build points file name not given', 2] == blocker.args


def test_saveAlignBuildFile_3(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('test')
    with mock.patch.object(app.mainW,
                           'saveFile',
                           return_value=('build', 'test', 'bpts')):
        with mock.patch.object(app.data,
                               'saveBuildP',
                               return_value=False):
            with qtbot.waitSignal(app.message) as blocker:
                suc = app.mainW.saveAlignBuildFile()
                assert suc
            assert ['Align build file [test] cannot no be saved', 2] == blocker.args


def test_saveAlignBuildFileAs_1(qtbot):
    with mock.patch.object(app.mainW,
                           'saveFile',
                           return_value=('build', 'test', 'bpts')):
        with mock.patch.object(app.data,
                               'saveBuildP',
                               return_value=True):
            with qtbot.waitSignal(app.message) as blocker:
                suc = app.mainW.saveAlignBuildFileAs()
                assert suc
            assert ['Align build file [test] saved', 0] == blocker.args


def test_saveAlignBuildFileAs_2(qtbot):
    with mock.patch.object(app.mainW,
                           'saveFile',
                           return_value=('', '', '')):
        suc = app.mainW.saveAlignBuildFileAs()
        assert not suc


def test_saveAlignBuildFileAs_3(qtbot):
    with mock.patch.object(app.mainW,
                           'saveFile',
                           return_value=('build', 'test', 'bpts')):
        with mock.patch.object(app.data,
                               'saveBuildP',
                               return_value=False):
            with qtbot.waitSignal(app.message) as blocker:
                suc = app.mainW.saveAlignBuildFileAs()
                assert suc
            assert ['Align build file [test] cannot no be saved', 2] == blocker.args


def test_genAlignBuildFile_1(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('')
    app.mainW.ui.checkAutoDeletePoints.setChecked(True)
    with qtbot.waitSignal(app.message) as blocker:
        suc = app.mainW.genAlignBuildFile()
        assert not suc
    assert ['Align build points file name not given', 2] == blocker.args


def test_genAlignBuildFile_2(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('test')
    app.mainW.ui.checkAutoDeletePoints.setChecked(True)
    with mock.patch.object(app.data,
                           'loadBuildP',
                           return_value=False):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.genAlignBuildFile()
            assert not suc
        assert ['Align build points file [test] could not be loaded', 2] == blocker.args


def test_genAlignBuildFile_3(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('test')
    app.mainW.ui.checkAutoDeletePoints.setChecked(True)
    with mock.patch.object(app.data,
                           'loadBuildP',
                           return_value=True):
        suc = app.mainW.genAlignBuildFile()
        assert suc


def test_genAlignBuildFile_4(qtbot):
    app.mainW.ui.alignBuildPFileName.setText('test')
    app.mainW.ui.checkAutoDeletePoints.setChecked(False)
    with mock.patch.object(app.data,
                           'loadBuildP',
                           return_value=True):
        suc = app.mainW.genAlignBuildFile()
        assert suc
