# -*- coding: UTF-8 -*-
#configProject.py

class ConfigProject(object):
    """Class ConfigProject speichert die Config-Einstellungen fuer ein AdV-Projekt."""
    
    def __init__(self, tasklist, tableList, loaderList, wbList):
        """Konstruktor der Klasse ConfigProject.
        
        Args:
            tasklist: List mit gradle Tasks
            tableList: List mit Datenbanktabellen
            loaderList: List mit java commands fuer GmlLoader
            wbList: List mit den FME Workbenchs
        """
        
        self.__tasklist = tasklist
        self.__tableList = tableList
        self.__loaderList = loaderList
        self.__wbList = wbList
    
    def getGradleTaskList(self):
        """Methode gibt eine List mit den gradle Tasks zurueck.
        
        Returns:
            List: gradle Tasks
        """
        
        return self.__tasklist
    
    def getTableList(self):
        """Methode gibt eine List mit den Namen der Datenbanktabellen zurueck.
        
        Returns:
            List: Datenbanktabellen (schema.tabelle)
        """
        
        return self.__tableList
    
    def getGmlLoaderList(self):
        """Methode gibt eine List mit den java commands fuer den GmlLoader zurueck.
        
        Returns:
            List: java commands fuer GmlLoader
        """
        
        return self.__loaderList
    
    def getWorkbenchList(self):
        """Methode gibt eine List mit den FME Workbenchs zurueck.
        
        Returns:
            List: FME Workbenchs
        """
        
        return self.__wbList
    