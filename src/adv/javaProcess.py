# -*- coding: UTF-8 -*-
#javaProcess.py
import subprocess
import logging
import os

class JavaProcess(object):
    """Class JavaProcess fuehrt GmlLoader (deegree-gml-tool.jar) als Subprocess aus."""

    def __init__(self, gmlloaderjarpath):
        """Konstruktor der Klasse JavaProcess.
        
        Args:
            gmlloaderjarpath: String mit Path zum GmlLoader
        """
        
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__gmlloaderjarpath = gmlloaderjarpath
        
    def callJavaProcess(self, command):
        """Methode startet den GmlLoader Subprocess mit dem uebergebene command.
        
        Args:
            command: String mit vollstaendigem java command incl. aller Argumente
        """
        
        os.chdir(self.__gmlloaderjarpath)
        completed = subprocess.run(command, stderr=subprocess.PIPE)
        
        if completed.returncode != 0:
            message = "java process " + command + " failed: <"+ str(completed.stderr) + ">"
            raise Exception(message)
        else:
            message = "java process " + command + " successfully: <"+ str(completed.stderr) + ">"
            self.__logger.info(message)
        
        