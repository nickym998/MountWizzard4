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
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
import logging
import os
# external packages
import PyQt5.QtCore
# local import
import mw4_global
import mountcontrol.qtmount
import mountwizzard4.gui.mainW


class MountWizzard4(object):
    """
    MountWizzard4 class is the main class for the application. it loads all windows and
    classes needed to fulfil the work of mountwizzard. any gui work should be handled
    through the window classes. main class is for setup, config, start, persist and
    shutdown the application.
    """

    __all__ = ['MountWizzard4',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()

        # get the working horses up
        pathToTs = mw4_global.work_dir + '/config'
        self.mount = mountcontrol.qtmount.Mount(host='192.168.2.15',
                                                pathToTS=pathToTs,
                                                expire=False,
                                                verbose=False,
                                                )
        # get the window widgets up
        self.mainW = mountwizzard4.gui.mainW.MainWindow(self)
        self.mainW.show()
        self.mount.signals.pointDone.connect(self.mainW.updatePointGUI)
        self.mount.signals.setDone.connect(self.mainW.updateSetGUI)
        self.mount.startTimers()
        self.mount.cyclePointing()
        self.mount.cycleSetting()
        self.mount.signals.gotAlign.connect(self.gotAlign)
        self.mount.signals.gotNames.connect(self.gotNames)
        self.mount.getAlign()
        self.mount.getNames()

    def quit(self):
        self.mount.stopTimers()
        PyQt5.QtCore.QCoreApplication.quit()

    def gotNames(self):
        for name in self.mount.model.nameList:
            # print(name)
            pass

    def gotAlign(self):
        for star in self.mount.model.starList:
            # print(star)
            pass