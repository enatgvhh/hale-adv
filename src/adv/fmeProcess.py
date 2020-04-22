# -*- coding: UTF-8 -*-
#fmeProcess.py
import subprocess
import logging
import os

class FmeProcess(object):
    """Class FmeProcess dient dazu, um eine FME-Workbenche ueber einen Subprocess laufen zu lassen"""
    
    def __init__(self, fmepath, fmeworkbenchpath, fmeargs):
        """Konstruktor der Klasse FmeProcess.
        
        Args:
            fmepath: String mit Path zur fme.exe
            fmeworkbenchpath: String mit Path zu FME Workbenchs
            fmeargs: String mit Argumenten der FME Workbechs (SourceDB und DestinationDB)
        """
        
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__fmepath = fmepath
        self.__wbpath = fmeworkbenchpath
        self.__fmeargs = fmeargs
        
    def callFmeProcess(self, wb):
        """Methode startet den FME Subprocess.
        
        Args:
            wb: FME Workbech.fmw
        """
        
        os.chdir(self.__fmepath)
        fmeCommand = self.__fmepath + "/fme.exe " + self.__wbpath + "/" + wb + " " + self.__fmeargs
        completed = subprocess.run(fmeCommand, stderr=subprocess.PIPE)
        
        if completed.returncode != 0:
            message = "fme transformation " + wb + " failed: <"+ str(completed.stderr) + ">"
            raise Exception(message)
        else:
            message = "fme transformation " + wb + " successfully: <"+ str(completed.stderr) + ">"
            self.__logger.info(message)
            