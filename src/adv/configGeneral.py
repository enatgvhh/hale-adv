# -*- coding: UTF-8 -*-
#configGeneral.py
import logging

class ConfigGeneral(object):
    """Class ConfigGeneral speichert die generellen Config-Einstellungen, die fuer alle AdV-Projekte gelten."""
    
    def __init__(self, logfile, gradleprojectpath, dbname, user, host, port, password, gmlloaderjarpath, fmepath, fmeworkbenchpath, fmeargs):
        """Konstruktor der Klasse ConfigGeneral.
        
        Args:
            logfile: String mit Path/File.log
            gradleprojectpath: String mit Path zum Gradle Projekt
            dbname: String mit Datenbank-Name
            user: String mit Datenbank-User
            host:  String mit Datenbank-Host
            port: String mit Datenbank-Port
            password: String mit Datenbank-Password
            gmlloaderjarpath: String mit Path zum GmlLoader
            fmepath: String mit Path zur fme.exe
            fmeworkbenchpath: String mit FME Workbench Path 
            fmeargs: String mit den FME Prozess Argumenten (SourceDB und DestinationDB)
        """
        
        self.__logfile = logfile
        self.__gradleprojectpath = gradleprojectpath
        self.__dbname = dbname
        self.__user = user
        self.__host = host
        self.__port = port
        self.__password = password
        self.__gmlloaderjarpath = gmlloaderjarpath
        self.__fmepath = fmepath
        self.__fmeworkbenchpath = fmeworkbenchpath
        self.__fmeargs = fmeargs
        
    def getLogger(self):
        """Methode gibt ein Objekt logging.Logger zurueck.
        
        Returns:
            logging.Logger: Logger-Objekt
        """
        
        logging.basicConfig(filename=self.__logfile, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        return logging.getLogger('loggerAdv')
    
    def getGradleProjectPath(self):
        """Methode gibt den gradle Projekt Path zurueck.
        
        Returns:
            String: gradle Projekt Path
        """
        
        tmp = self.__gradleprojectpath.rstrip("\\/")
        return tmp
    
    def getDatabaseConnection(self):
        """Methode gibt einen String mit der Datenbank-Connection zurueck.
        
        Returns:
            String: Database Connection String <dbname='' user='' host='' port='' password=''>
        """
        
        strConn = "dbname='" + self.__dbname + "' user='" + self.__user + "' host='" + self.__host + "' port='" + self.__port + "' password='" + self.__password + "'"
        return strConn
    
    def getGmlLoaderJarPath(self):
        """Methode gibt den GmlLoader Path zurueck.
        
        Returns:
            String: Path zum GmlLoader
        """
        
        tmp = self.__gmlloaderjarpath.rstrip("\\/")
        return tmp
    
    def getFmeExePath(self):
        """Methode gibt den Path zur fme.exe zurueck.
        
        Returns:
            String: Path zur fme.exe
        """
        
        tmp = self.__fmepath.rstrip("\\/")
        return tmp
    
    def getFmeWorkbenchPath(self):
        """Methode gibt den Path zu den FME Workbenchs zurueck.
        
        Returns:
            String: Path zu den FME Workbenchs
        """
        
        tmp = self.__fmeworkbenchpath.rstrip("\\/")
        return tmp
    
    def getFmeArgs(self):
        """Methode gibt die Argumente der FME Workbenchs zurueck.
        
        Returns:
            String: Argumente der FME Workbenchs
        """
        
        tmp = self.__fmeargs.replace('@', '<at>')
        return tmp
    