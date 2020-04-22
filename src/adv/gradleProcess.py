# -*- coding: UTF-8 -*-
#gradleProcess.py
import subprocess
import logging
import os

class GradleProcess(object):
    """Class GradleProcess fuehrt gradle.bat fuer ein AdV-Projekt als Subprocess aus."""
    
    def __init__(self, gradleprojectpath):
        """Konstruktor der Klasse GradleProcess.
        
        Args:
            gradleprojectpath: String mit Path zum gradle Projekt
        """
        
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__gradleprojectpath = gradleprojectpath
        
    def callGradleProcess(self, task):
        """Methode startet den Gradle Subprocess fuer den uebergebenen Task.
        
        Args:
            task: String mit Gradle Task Name
        """
        
        os.chdir(self.__gradleprojectpath)
        completed = subprocess.run(['gradle.bat',task], stderr=subprocess.PIPE)
        
        if completed.returncode != 0:
            message = "gradle process " + task + " failed: <"+ str(completed.stderr) + ">"
            raise Exception(message)
        else:
            message = "gradle process " + task + " successfully: <"+ str(completed.stderr) + ">"
            self.__logger.info(message)
            