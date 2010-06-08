'''
Created on Jun 8, 2010

@author: bsana
'''

from lxml import etree

class ConfigObject(object):
    '''
    classdocs
    '''

    def __init__(self,configfileloc = None, configtree = None):
        if configfileloc:
            self.protree = etree.parse(configfileloc)
        elif configtree:
            self.protree = configtree        

    def getConfigElement(self, elt, prop='text' ):
        element = self.protree.find(elt)
        if prop == 'text':
            return self.protree.findtext(elt)
        else:
            return element.get(prop)        