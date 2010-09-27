'''
Created on Jun 8, 2010

@author: bsana
'''

from lxml import etree

from openamos.gui.env import *
import os
from copy import deepcopy

class ConfigObject(object):
    '''
    classdocs
    '''

    def __init__(self,configfileloc = None, configtree = None):
        if configfileloc:
            parser = etree.XMLParser(remove_blank_text=True)
            self.protree = etree.parse(configfileloc,parser)
        elif configtree:
            self.protree = configtree        

    def getConfigElement(self, elt, prop='text' ):
        element = self.protree.find(elt)
        if prop == 'text':
            return self.protree.findtext(elt)
        else:
            return element.get(prop)  

    def modelSpecInConfig(self,modelkey):
        compname = self.getCompName(modelkey)
        modelconfigelt = self.protree.find(MODELCONFIG)
        if modelconfigelt != None:
            modelfound = None
            for comp in modelconfigelt.getiterator(COMP):
                if compname == comp.get(NAME):
                    for model in comp.getiterator(MODEL): 
                        if modelkey == model.get(NAME):
                            modelfound = deepcopy(model)
            return modelfound
        else:
            return None
    
    def addModelElement(self,modelelt):
        compname = self.getCompName(modelelt.get(NAME))
        modelconfigelt = self.protree.find(MODELCONFIG)
        if modelconfigelt != None:
            compfound = False
            for comp in modelconfigelt.getiterator(COMP):
                if compname == comp.get(NAME):
                    compfound = True
                    modelidx = 0
                    modelreplaced = False
                    for model in comp.getiterator(MODEL):
                        if modelelt.get(NAME) == model.get(NAME):
                            comp.remove(model)
                            comp.insert(modelidx,modelelt)
                            modelreplaced = True
                        modelidx = modelidx + 1
                    if not modelreplaced:
                        comp.append(modelelt)
            if not compfound:
                compelt = etree.SubElement(modelconfigelt,COMP)
                compelt.set(NAME,compname)
                compelt.append(modelelt) 
        else:
            proconfigelt = self.protree.getroot()  
            modelconfigelt = etree.SubElement(proconfigelt,MODELCONFIG) 
            compelt = etree.SubElement(modelconfigelt,COMP)
            compelt.set(NAME,compname)
            compelt.append(modelelt)  
    
    def getCompName(self,modelkey):
        for compkey in COMPMODELMAP.keys():
            modelist = COMPMODELMAP[compkey]
            if modelkey in modelist:
                return compkey
    
    def write(self):
        projecthome = self.getConfigElement(PROJECT,PROJECT_HOME)
        projectname = self.getConfigElement(PROJECT,PROJECT_NAME)
        configfileloc = projecthome + os.path.sep + projectname + os.path.sep + projectname + '.xml'
        configfile = open(configfileloc, 'w')
        self.protree.write(configfile, pretty_print=True)
        configfile.close()