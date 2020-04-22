# -*- coding: UTF-8 -*-
#postgreProcess.py
import psycopg2
import logging

class PostgreProcess(object):
    """Class PostgreProcess baut Verbindung zur PostgreSQL Datenbank auf."""
    
    def __init__(self, dbConnection):
        """Konstruktor der Klasse PostgreProcess.
        
        Args:
            dbConnection: String mit Datenbank Connection
        """
        
        self.__dbConnection = dbConnection
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__conn = None
        self.__cur = None
        
        #Test Connection
        self.openConnectionDeleter()
        self.closeConnection()
        self.openConnectionVacuumer()
        self.closeConnection()
    
    def openConnectionDeleter(self):
        """Methode oeffnet die Datenbankverbindung zum leeren von Tabellen."""
        self.__conn = psycopg2.connect(self.__dbConnection)
        self.__cur = self.__conn.cursor()
    
    def openConnectionVacuumer(self):
        """Methode oeffnet die Datenbankverbindung zum warten von Tabellen."""
        self.__conn = psycopg2.connect(self.__dbConnection)
        self.__conn.set_isolation_level(0)#0 = autocommit
        self.__cur = self.__conn.cursor()
    
    def closeConnection(self):
        """Methode schliesst die Datenbankverbindung."""
        
        if(self.__conn):
            self.__cur.close()
            self.__conn.close()
    
    def deleteDatabase(self, table):
        """Methode leert die Datenbanktabelle
        
        Args:
            table: String mit Schema.Tabelle
        """
                    
        strSqlDel = "DELETE FROM " + table
        self.__cur.execute(strSqlDel)
        self.__conn.commit()
        
        message = "delete table " + table + " successfully"
        self.__logger.info(message)
                   
    def vacuumDatabase(self, table):
        """Methode fuehrt Vacuum und Analyse auf Datenbanktabelle aus"""
        
        strSql = "VACUUM VERBOSE ANALYZE " + table
        self.__cur.execute(strSql)
        
        message = "VACUUM VERBOSE ANALYZE " + table + " successfully"
        self.__logger.info(message)
        