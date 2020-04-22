#-*- coding: UTF-8 -*-
#File: ClientAdv.py
import sys
import os
import re
import time
from lxml import etree
from adv import configGeneral
from adv import configProject
from adv import gradleProcess
from adv import postgreProcess
from adv import javaProcess
from adv import fmeProcess

def getConfigObjects(node):
    confProjectList = []
    
    logfile = node.xpath('//logfile', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text
    gradleprojectpath = node.xpath('//gradleprojectpath', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text
    dbname = node.xpath('//dbname', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text
    user = node.xpath('//user', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text
    host = node.xpath('//host', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text
    port = node.xpath('//port', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text
    password = node.xpath('//password', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text      
    gmlloaderjarpath = node.xpath('//gmlloaderjarpath', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text      
    fmepath = node.xpath('//fme/fmepath', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text      
    fmeworkbenchpath = node.xpath('//fme/fmeworkbenchpath', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text      
    fmeargs = node.xpath('//fme/fmeargs', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0].text      
    
    confGeneral = configGeneral.ConfigGeneral(logfile, gradleprojectpath, dbname, user, host, port, password, gmlloaderjarpath, fmepath, fmeworkbenchpath, fmeargs)
    
    memberList =  node.xpath('//member', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        
    for member in memberList:
        strItem = etree.tostring(member, encoding='unicode')
        node = etree.fromstring(strItem)
        
        taskList = []
        tableList = []
        loaderList = []
        wbList = [] 
        gradletasks = node.xpath('//gradletask', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        tables = node.xpath('//database/table', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        loaders = node.xpath('//gmlloader/javacommand', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        wbs = node.xpath('//fmeworkbench', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        
        for task in gradletasks:
            taskList.append(task.text)
        
        for table in tables:
            tableList.append(table.text)
            
        for loader in loaders:
            loaderList.append(loader.text)
            
        for wb in wbs:
            wbList.append(wb.text)
            
        confProjectList.append(configProject.ConfigProject(taskList, tableList, loaderList, wbList))
        
    return [confGeneral,confProjectList]
    
def main():
    try:
        etConf = etree.parse('ConfigAdv.xml')
        etConfNode = etConf.xpath('//ConfigObject', namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})[0]
        confGeneral, confProjectList = getConfigObjects(etConfNode)
        
        logger = confGeneral.getLogger()
        logger.info('Start')
        
        gradleProc = gradleProcess.GradleProcess(confGeneral.getGradleProjectPath())
        postgreProc = postgreProcess.PostgreProcess(confGeneral.getDatabaseConnection())
        javaProc = javaProcess.JavaProcess(confGeneral.getGmlLoaderJarPath())
        fmeProc = fmeProcess.FmeProcess(confGeneral.getFmeExePath(), confGeneral.getFmeWorkbenchPath(), confGeneral.getFmeArgs())
    except:
            message = str(sys.exc_info()[0]) + "; " + str(sys.exc_info()[1])
            logger.error(message)
            sys.exit()
       
    for project in confProjectList:
        try:
            #1. run tasks
            for task in project.getGradleTaskList():
                gradleProc.callGradleProcess(task)
                
                if task == 'transform-au-dlkm-kommunalesGebiet':
                    gmlFile = confGeneral.getGradleProjectPath() + "\\transformiert\\" + task.replace('transform-','') + "\\result.gml"
                    oldStrList = ["<au:upperLevelUnit xlink:href=\"#AdministrativeUnit_02000\"></au:upperLevelUnit>", "<au:lowerLevelUnit xlink:href=\"#AdministrativeUnit_02000\"></au:lowerLevelUnit>"]
                    newStrList = ["<au:upperLevelUnit nilReason=\"other:unpopulated\" xsi:nil=\"true\"></au:upperLevelUnit>", "<au:upperLevelUnit nilReason=\"other:unpopulated\" xsi:nil=\"true\"></au:upperLevelUnit>"]
                    gmlCorrection(gmlFile, oldStrList, newStrList, logger)
                           
            #2. delete tables
            postgreProc.openConnectionDeleter()
            
            for table in project.getTableList():          
                postgreProc.deleteDatabase(table)
            
            postgreProc.closeConnection()
            
            #3. load data
            for command in project.getGmlLoaderList():
                javaProc.callJavaProcess(command)
                logFile = confGeneral.getGmlLoaderJarPath() + "\deegree-gml-tool.log" 
                deleteGmlLoaderLogFile(logFile, command, logger)
                
            #4. vacuum tables
            postgreProc.openConnectionVacuumer()
            
            for table in project.getTableList():          
                postgreProc.vacuumDatabase(table)
            
            postgreProc.closeConnection()
            
            #5. fme transfer data
            for wb in project.getWorkbenchList():
                fmeProc.callFmeProcess(wb)
        except:
            message = str(sys.exc_info()[0]) + "; " + str(sys.exc_info()[1])
            logger.error(message)
            postgreProc.closeConnection()
    
    logger.info('End')
    
def gmlCorrection(gmlFile, oldStrList, newStrList, logger):
    """Korrigiert Referenzfehler im result.gml nach z.B. transform-au-dlkm-kommunalesGebiet.
    Falsche Referenzen in z.B. au:AdministrativeUnit werden entfernt, da sie sonst im
    GmlLoader Prozess zu einem unresolvable references detected error mit
    einem rollback transaction fuehren.
    """
    
    if os.path.isfile(gmlFile) == True:
        deprecatedGmlFile = gmlFile.replace('result.gml', 'result_error.gml')
        os.rename(gmlFile, deprecatedGmlFile)
        
        if os.path.isfile(deprecatedGmlFile) == True:
            reader = open(deprecatedGmlFile)
            writer = open(gmlFile, 'w')
            
            for line in reader:
                for i in range(len(oldStrList)):
                    line = line.replace(oldStrList[i],newStrList[i])
                    
                writer.write(line)
                
            reader.close()
            writer.close()
            logger.info("correction gml file " + gmlFile)
            os.remove(deprecatedGmlFile)
            
def deleteGmlLoaderLogFile(logFile, command, logger):
    """Methode loescht das riesige deegree-gml-tool.log File vom GmlLoader.
    Zuvor scannt es die Datei nach einem 'Rollback transaction' Eintrag und
    logt diesen.
    """
    
    if os.path.isfile(logFile) == True:
        reader = open(logFile)
        
        for line in reader:
            if re.search("TransactionHandler - Rollback transaction", line) != None:
                logger.error("TransactionHandler - Rollback transaction for " + command)
        
        reader.close()
        message = "Delete " + logFile + " " + str(time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(os.path.getmtime(logFile)))) + " " + str(os.path.getsize(logFile)) + " bytes"
        logger.info(message)
        os.remove(logFile)
        
if __name__ == '__main__':
    main()
    