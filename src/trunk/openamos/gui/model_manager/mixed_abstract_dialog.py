'''
Created on May 30, 2011

@author: dhyou
'''

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lxml import etree

from openamos.gui.env import *
#from mixed_widgets import *

from openamos.gui.misc.basic_widgets import *
from openamos.gui.env import *

from openamos.core.database_management.database_connection import *
from openamos.core.database_management.database_configuration import *

class AbtractMixedDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self,configobject,element,IsOpen,parent=None):
        super(AbtractMixedDialog, self).__init__(parent)
        
        self.configobject = configobject
        self.isMove = True
        ### Existing elements under any component
        if IsOpen == 1 or IsOpen == 3:
            self.elt = element
        ### Add new element under a component
        elif IsOpen == 2 or IsOpen == 4:
            self.elt = None
            self.father = element
        
        self.populateFromDatabase()
        
        self.setWindowTitle("")
        self.alllayout = QHBoxLayout()
        self.setLayout(self.alllayout)
     

        attributegb = QGroupBox("")
        attrilayout = QVBoxLayout()
        attributegb.setLayout(attrilayout)
        attrilayout.setContentsMargins(0,0,0,0)
        
        row1 = QWidget(self)
        row1layout = QGridLayout()
        row1.setLayout(row1layout)
        
        titlelabel = QLabel("Element Title: ")
        titlelabel.setAlignment(Qt.AlignLeft)
        row1layout.addWidget(titlelabel,0,0)
        if IsOpen == 1 or IsOpen == 2:
            self.setTitleCom(row1layout)
        else:
            self.setTitleText(row1layout)
        
        dummy1 = QLabel("")
        row1layout.addWidget(dummy1,0,1)

        
        row2 = QWidget(self)
        row2layout = QGridLayout()
        row2.setLayout(row2layout)
        
        tableslabel = QLabel('Tables')
        row2layout.addWidget(tableslabel,0,0)
        
        self.tableswidget = QListWidget()
        self.tableswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableswidget.addItems(self.tablelist)
        self.tableswidget.setMaximumSize(250,200)
        row2layout.addWidget(self.tableswidget,1,0)
        
        self.addTable = QPushButton('Value')
        self.addTable.setMaximumWidth(50)
        row2layout.addWidget(self.addTable,2,0)

        varslabel = QLabel('Columns')
        row2layout.addWidget(varslabel,0,1)
        
        self.colswidget = QListWidget()
        self.colswidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.colswidget.setMaximumSize(250,200)
        row2layout.addWidget(self.colswidget,1,1)
        
        self.addColumn = QPushButton('Value')
        self.addColumn.setMaximumWidth(50)
        row2layout.addWidget(self.addColumn,2,1)

        
#        btnwidget1 = QWidget(self)
#        btnlayout1 = QVBoxLayout()
#        btnwidget1.setLayout(btnlayout1)    
#        self.addTable = QPushButton('Table Name')
#        self.addTable.setMaximumWidth(80)
#        btnlayout1.addWidget(self.addTable)
#        self.addColumn = QPushButton('Column Name')
#        self.addColumn.setMaximumWidth(80)
#        btnlayout1.addWidget(self.addColumn)
#        row2layout.addWidget(btnwidget1,1,1)
        

        row3 = QWidget(self)
        row3layout = QHBoxLayout()
        row3.setLayout(row3layout)

        valuewidget = QWidget(self)
        valuelayout = QVBoxLayout()
        
        selectlabel = QLabel("Attribute Name: ")
        self.attriname = QComboBox()
        self.attriname.setMinimumWidth(220)
        if self.elt != None:
            self.attriname.addItems(self.attributes(str(self.elt.tag)))
        else:
            temp = self.parent()
            self.attriname.addItems(self.attributes(str(temp.subcomponent)))        
    
        valuewidget.setLayout(valuelayout)        
#        attrinamelabel = QLabel("Attribute Name: ")
#        self.nameline = LineEdit()
#        self.nameline.setMaximumWidth(300)

        attrivaluelabel = QLabel("Attribute Value: ")
        self.valueline = LineEdit()
        self.valueline.setMaximumWidth(220)
        dummy2 = QLabel("")
        valuelayout.addWidget(selectlabel)
        valuelayout.addWidget(self.attriname)
        valuelayout.addWidget(attrivaluelabel)
        valuelayout.addWidget(self.valueline)
        valuelayout.addWidget(dummy2)
        row3layout.addWidget(valuewidget)
            
        btnwidget1 = QWidget(self)
        btnlayout1 = QVBoxLayout()
        btnwidget1.setLayout(btnlayout1)    
        self.addbutton = QPushButton('>>')
        self.addbutton.setMaximumWidth(60)
        btnlayout1.addWidget(self.addbutton)
        self.delbutton = QPushButton('<<')
        self.delbutton.setMaximumWidth(60)
        btnlayout1.addWidget(self.delbutton)
        row3layout.addWidget(btnwidget1)

        self.attritable = QTableWidget(self)
        self.attritable.setRowCount(0)
        self.attritable.setColumnCount(2)
        self.attritable.setHorizontalHeaderLabels(['Attribute', 'Value'])
        #self.choicetable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.attritable.setSelectionMode(QAbstractItemView.SingleSelection)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self.attritable.setSizePolicy(sizePolicy)
        self.attritable.horizontalHeader().setResizeMode(0,1)
        self.attritable.horizontalHeader().setResizeMode(1,1)
        row3layout.addWidget(self.attritable)

        btnwidget2 = QWidget(self)
        btnlayout2 = QHBoxLayout()
        btnwidget2.setLayout(btnlayout2)    
        self.btnsaveas = QPushButton('Insert')
        self.btnsaveas.setMaximumWidth(80)
        btnlayout2.addWidget(self.btnsaveas)
        self.btnsave = QPushButton('Save')
        self.btnsave.setMaximumWidth(80)
        if IsOpen == 4:
            self.btnsave.setDisabled(True)
        elif IsOpen == 3:
            self.btnsaveas.setDisabled(True)
        elif IsOpen == 2:
            self.btnsave.setDisabled(True)
        btnlayout2.addWidget(self.btnsave)
        self.dialogButtonBox = QDialogButtonBox(QDialogButtonBox.Close)
        btnlayout2.addWidget(self.dialogButtonBox)
        
        attrilayout.addWidget(row1)
        attrilayout.addWidget(row2)
        attrilayout.addWidget(row3)
        attrilayout.addWidget(btnwidget2)
        
        if IsOpen < 3:
            self.notcomponent()
        self.alllayout.addWidget(attributegb)
        
        if IsOpen == 1:
            self.readtree()
        elif IsOpen == 2:
            self.maketree()
        elif IsOpen == 3:
            self.showComponent()
        
        self.connect(self.tableswidget, SIGNAL("itemClicked (QListWidgetItem *)"), self.populateColumns)
#        self.connect(self.titleline1, SIGNAL("currentIndexChanged(int)"), self.fillAttr)
        self.connect(self.addbutton, SIGNAL("clicked(bool)"), self.addAttribute)
        self.connect(self.delbutton, SIGNAL("clicked(bool)"), self.delAttribute)
        self.connect(self.addTable, SIGNAL("clicked(bool)"), self.fillValueT)
        self.connect(self.addColumn, SIGNAL("clicked(bool)"), self.fillValueC)
        self.connect(self.btnsaveas, SIGNAL("clicked(bool)"), self.saveAsElement)
        self.connect(self.btnsave, SIGNAL("clicked(bool)"), self.saveElement)
        self.connect(self.dialogButtonBox, SIGNAL("rejected()"), SLOT("reject()"))


    def setTitleCom(self, row1layout):
        self.titleline1 = QComboBox()
        self.titleline1.setMinimumWidth(250)
        if self.elt != None:
            self.titleline1.addItems(self.titles(str(self.elt.tag)))
        else:
            temp = self.parent()
            self.titleline1.addItems(self.titles(str(temp.subcomponent)))
            
        self.connect(self.titleline1, SIGNAL("currentIndexChanged(int)"), self.fillAttr)
        row1layout.addWidget(self.titleline1,1,0)


    def setTitleText(self, row1layout):
        self.titleline2 = LineEdit()
        self.titleline2.setMinimumWidth(250)
#        if self.elt != None:
#            self.titleline2.setText("")
#        else:
#            self.titleline2.setText("Component")
#            self.titleline2.setDisabled(True)
        
        row1layout.addWidget(self.titleline2,1,0)


    def notcomponent(self):
        leftwidget = QWidget()
        leftlayout = QVBoxLayout()
        leftwidget.setLayout(leftlayout)
        leftlayout.setContentsMargins(0,0,0,0)
        
        tools = QToolBar()
        up_action = self.createaction("",self.moveup,"arrow_up","Move up an element in the tree.")
        down_action = self.createaction("",self.movedown,"arrow_down","Move down an element in the tree.")
        remove_action = self.createaction("",self.remove_element,"delete","Delete the selected element in the tree.")
        tools.addAction(up_action)
        tools.addAction(down_action)
        tools.addAction(remove_action)
        leftlayout.addWidget(tools)

        self.treewidget = QTreeWidget()
        self.treewidget.setMinimumWidth(250)
        self.treewidget.headerItem().setText(0, "Sub-element Management")

        leftlayout.addWidget(self.treewidget)
        self.alllayout.addWidget(leftwidget)
        
        self.connect(self.treewidget, SIGNAL('itemClicked (QTreeWidgetItem *,int)'), self.showAttributes)


    def createaction(self, text, slot=None, icon=None,
                     tip=None, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("./images/%s.png" % icon))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)

        return action

            
    def attributes(self,eltname):
        elements = self.configobject.getElements(eltname)
        items = []
        for elt in elements:
            for key in elt.keys():
                if key not in items:
                    items.append(key)
        
        if eltname == COMP:
            items.remove("skip")
            items.remove("completed")
            items.remove("name")
                  
        return items
    
    def titles(self,eltname):
        elements = self.configobject.getElements(eltname)
        items = []
        items.append(str(eltname))
        for elt in elements:
            for child in elt.getchildren():
                cname = str(child.tag)
                if cname not in items:
                    items.append(cname)
                for child2 in child.getchildren():
                    cname2 = str(child2.tag)
                    if cname2 not in items:
                        items.append(cname2)
              
        return items


    def maketree(self):
        temp = self.parent()
        title = temp.subcomponent

        attrdict1 = {}
        treeelt = TreeWidgetItem(self.treewidget, attrdict1)
        treeelt.setText(0, title)
        self.treewidget.setCurrentItem(treeelt)


    def readtree(self):
        attrdict1 = {}
        for key in self.elt.keys():
            attrdict1[key] = str(self.elt.get(key))
            
        treeelt = TreeWidgetItem(self.treewidget, attrdict1)
        treeelt.setText(0, str(self.elt.tag))
        self.treewidget.setCurrentItem(treeelt)
        
        for elt1 in self.elt.getchildren():
            attrdict2 = {}
            for key in elt1.keys():
                attrdict2[key] = str(elt1.get(key))
                
            subitem = TreeWidgetItem(treeelt, attrdict2)
            subitem.setText(0, str(elt1.tag)) 
            
            for elt2 in elt1.getchildren():
                attrdict3 = {}
                for key in elt2.keys():
                    attrdict3[key] = str(elt2.get(key))
                    
                subsub = TreeWidgetItem(subitem, attrdict3)
                subsub.setText(0, str(elt2.tag))
                
    def showComponent(self):
            
        for key in self.elt.keys():
            value = str(self.elt.get(key))
            
            if str(key) != NAME and str(key) != "skip" and str(key) != "completed":
                self.attritable.insertRow(self.attritable.rowCount())
                attritem = QTableWidgetItem()
                attritem.setText(str(key))
                attritem.setFlags(attritem.flags() & ~Qt.ItemIsEditable)
                self.attritable.setItem(self.attritable.rowCount()-1, 0, attritem)
                
                varitem = QTableWidgetItem()
                varitem.setText(value)
                varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
                self.attritable.setItem(self.attritable.rowCount()-1, 1, varitem)
            elif str(key) == NAME:
                self.titleline2.setText(value)


    def showAttributes(self):
        curitem = self.treewidget.currentItem()
        self.attriname.clear()
        self.attriname.addItems(self.attributes(str(curitem.text(0))))
        ind = self.titleline1.findText(str(curitem.text(0)))
        self.titleline1.setCurrentIndex(ind)
        
        num = self.attritable.rowCount()
        for i in range(num):
            self.attritable.removeRow(0)
            
        for key in curitem.attribute.keys():
            value = curitem.attribute[key]

            self.attritable.insertRow(self.attritable.rowCount())
            attritem = QTableWidgetItem()
            attritem.setText(str(key))
            attritem.setFlags(attritem.flags() & ~Qt.ItemIsEditable)
            self.attritable.setItem(self.attritable.rowCount()-1, 0, attritem)
            
            varitem = QTableWidgetItem()
            varitem.setText(value)
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            self.attritable.setItem(self.attritable.rowCount()-1, 1, varitem)
            
            


#    def fillName(self):
#        name = str(self.attriname.currentText())
#        self.nameline.setText(name)

    def fillAttr(self):
        name = str(self.titleline1.currentText())
        self.attriname.clear()
        self.attriname.addItems(self.attributes(name))
        
        item = self.treewidget.currentItem()
        if name != str(item.text(0)):
            numrows = self.attritable.rowCount()
            for i in range(numrows):
                self.attritable.removeRow(0)
        
    def fillValueT(self):
        temp = self.tableswidget.currentItem()
        if temp != None:
            value = str(temp.text())
            self.valueline.setText(value)

        
    def fillValueC(self):
        temp = self.colswidget.currentItem()
        if temp != None:
            value = str(temp.text())
            self.valueline.setText(value)


    def populateFromDatabase(self):
        self.protocol = self.configobject.getConfigElement(DB_CONFIG,DB_PROTOCOL)        
        self.user_name = self.configobject.getConfigElement(DB_CONFIG,DB_USER)
        self.password = self.configobject.getConfigElement(DB_CONFIG,DB_PASS)
        self.host_name = self.configobject.getConfigElement(DB_CONFIG,DB_HOST)
        self.database_name = self.configobject.getConfigElement(DB_CONFIG,DB_NAME)
        self.database_config_object = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        
        new_obj = DataBaseConnection(self.database_config_object)
        new_obj.new_connection()
        tables = new_obj.get_table_list()
        
        self.tablelist = []
        self.coldict = {}
        for table in tables:
            self.tablelist.append(QString(table))
            cols = new_obj.get_column_list(table)
            varlist = []
            if cols is not None:
                for col in cols:
                    varlist.append(QString(col))
                self.coldict[table] = varlist


    def populateColumns(self, item):
        self.colswidget.clear()
        seltab = str(item.text())
        self.colswidget.addItems(self.coldict[seltab])
             
    def addAttribute(self):
        name = str(self.attriname.currentText())
        value = str(self.valueline.text())

        if (name != "") & (value != ""):
            self.attritable.insertRow(self.attritable.rowCount())
            tableitem = QTableWidgetItem()
            tableitem.setText(name)
            tableitem.setFlags(tableitem.flags() & ~Qt.ItemIsEditable)
            self.attritable.setItem(self.attritable.rowCount()-1, 0, tableitem)
            
            varitem = QTableWidgetItem()
            varitem.setText(value)
            varitem.setFlags(varitem.flags() & ~Qt.ItemIsEditable)
            self.attritable.setItem(self.attritable.rowCount()-1, 1, varitem)   

   
    def delAttribute(self):
        self.attritable.removeRow(self.attritable.currentRow())

    def saveAsElement(self):

        if self.elt != None:
            if self.attritable.rowCount() >= 1:
                
                title = str(self.titleline1.currentText())
                item = self.treewidget.currentItem()
                father = item.parent()
                while father != None:
                    item = father
                    father = item.parent()
                
                if title != "" and title != str(self.elt.tag) and title != "LocationVariable" and title != "ActivityFilter" and title != "Aggregate":
                    self.addElement(title, item, self.elt)
                    
                elif title == "ActivityFilter":
                    attr = {}
                    element = etree.Element(title)
                    for i in range(self.attritable.rowCount()):
                        name = str((self.attritable.item(i,0)).text())
                        value = str((self.attritable.item(i,1)).text())
                        element.set(name,value)
                        attr[name] = value
                        
                    self.elt.insert(0, element)
                    treeelt = TreeWidgetItem(item,attr)
                    treeelt.setText(0, title)
                    item.removeChild(treeelt)
                    item.insertChild(0, treeelt)   
                    
                elif title == "LocationVariable":
                    i = item.childCount()
                    extract = item.child(i-1)
                    if str(extract.text(0)) == "ExtractLocationInformation":
                        elt1 = self.elt.getchildren()
                        self.addElement(title, extract, elt1[i-1])
                        
                elif title == "Aggregate" and str(item.text(0)) == "HistoryInformation":
                    item = self.treewidget.currentItem()
                    index = self.treewidget.currentIndex()
                    father = item.parent()
                    if str(item.text(0)) == "HistoryVar" or str(father.text(0)) == "HistoryVar":
                        elt1 = self.elt.getchildren()
                        if str(father.text(0)) == "HistoryVar":
                            temp = father.parent()
                            index = temp.indexOfChild(father)
                            self.addElement(title, father, elt1[index])
                        else:
                            self.addElement(title, item, elt1[index])
                
                elif title == "Aggregate":
                    self.addElement(title, item, self.elt)

            else:
                msg = "Please specify the attribute name and value"
                QMessageBox.information(self, "Warning",
                                    msg,
                                    QMessageBox.Ok) 
                
        else:
            length = self.attritable.rowCount()
            if str(self.father.tag) == "ModelConfig":
                if length > 0:
                    element = etree.Element(COMP)
                    element.set(NAME,str(self.titleline2.text()))
                    for i in range(length):
                        name = str((self.attritable.item(i,0)).text())
                        value = str((self.attritable.item(i,1)).text())
                        element.set(name,value)       
                    element.set("skip","False")
                    element.set("completed","False")
                    self.elt = element
                    self.father.append(self.elt)
                    tree = self.parent()
                    pitem = tree.currentItem()
                    pitem_sub = QTreeWidgetItem(pitem)
                    pitem_sub.setText(0,str(self.titleline2.text())) 
                    pitem_sub.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                    pitem_sub.setIcon(1, QIcon("./images/False"))
                    pitem_sub.setCheckState(2, Qt.Unchecked)
                    
                    QDialog.accept(self)   
                else:
                    msg = "Please specify the attribute name and value"
                    QMessageBox.information(self, "Warning",
                                        msg,
                                        QMessageBox.Ok)             
            else:
                item = self.treewidget.currentItem()
                if str(self.titleline1.currentText()) == str(item.text(0)):
                    if length > 0 or str(item.text(0)) == "DBTables":
                        element = etree.Element(str(item.text(0)))
                        attr = {}
                        for i in range(length):
                            name = str((self.attritable.item(i,0)).text())
                            value = str((self.attritable.item(i,1)).text())
                            element.set(name,value)
                            attr[name] = value        
                        item.attribute = attr
                        self.elt = element
                        self.father.append(self.elt)
                        tree = self.parent()
                        pitem = tree.currentItem()
                        pitem_sub = QTreeWidgetItem(pitem)
                        pitem_sub.setText(0,str(item.text(0)))
                        
                        self.btnsave.setDisabled(False)
                    else:
                        msg = "Please specify the attribute name and value"
                        QMessageBox.information(self, "Warning",
                                            msg,
                                            QMessageBox.Ok)                             
  
    
            
    def addElement(self, title, item, elt):           
        attr = {}
        element = etree.Element(title)
        for i in range(self.attritable.rowCount()):
            name = str((self.attritable.item(i,0)).text())
            value = str((self.attritable.item(i,1)).text())
            element.set(name,value)
            attr[name] = value
                
        elt.append(element)        
        treeelt = TreeWidgetItem(item,attr)
        treeelt.setText(0, title)
        

    def saveElement(self):
        length = self.attritable.rowCount()
        if length > 0 and self.elt != None:
            if self.elt.tag == COMP:
                skip = str(self.elt.get("skip"))
                completed = str(self.elt.get("completed"))
                for key in self.elt.keys():
                    if key != NAME:
                        del self.elt.attrib[key]
    
                self.elt.set(NAME,str(self.titleline2.text()))
                for i in range(length):
                    name = str((self.attritable.item(i,0)).text())
                    value = str((self.attritable.item(i,1)).text())
                    self.elt.set(name,value)       
                self.elt.set("skip",skip)
                self.elt.set("completed",completed) 
                
                QDialog.accept(self)               
            else:
                item = self.treewidget.currentItem()
                if str(self.titleline1.currentText()) == str(item.text(0)):
#                    if self.elt != None:
                    index = self.findIndex(item)
                    child = self.elt
                    for i in range(len(index)):
                        childs = child.getchildren()
                        child = childs[index[i]]
                    
                    attr = {}
                    for i in range(self.attritable.rowCount()):
                        name = str((self.attritable.item(i,0)).text())
                        value = str((self.attritable.item(i,1)).text())
                        child.set(name,value)
                        attr[name] = value        
                    item.attribute = attr    


    def remove_element(self):
        reply = QMessageBox.question(None, 'Remove', "Are you sure to remove?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            item = self.treewidget.currentItem()
            index = self.findIndex(item)
            if len(index) > 0:
                self.treewidget.removeItemWidget(item,0)
            
                father = self.elt
                childs = father.getchildren()
                child = childs[index[0]]
                if len(index) == 2:
                    father = child
                    childs = father.getchildren()
                    child = childs[index[1]]
                father.remove(child)


    def moveup(self):
        
        if self.isMove == True:
            self.isMove = False
            father = None
            item = self.treewidget.currentItem()
            index = self.findIndex(item)
            if item != None:
                father = item.parent()
                if father != None:

                    i = father.indexOfChild(item)
                    if i > 0:
                        father.removeChild(item)
                        father.insertChild(i-1, item)
                        self.treewidget.setCurrentItem(item)
    
            if len(index) == 1:
                if index[0] > 0:
                    childs = self.elt.getchildren()
                    child = childs[index[0]]
                    self.elt.remove(child)
                    self.elt.insert(index[0]-1, child)
            elif len(index) == 2:
                if index[1] > 0:
                    childs = self.elt.getchildren()
                    father = childs[index[0]]
                    childs = father.getchildren()
                    child = childs[index[1]]
                    father.remove(child)
                    father.insert(index[1]-1, child)

            self.isMove = True
            
            
    def movedown(self):
        
        if self.isMove == True:
            self.isMove = False
            item = self.treewidget.currentItem()
            index = self.findIndex(item)
            father = item.parent()
            max_i = -1
            if father != None:
                i = father.indexOfChild(item)
                max_i = father.childCount()
                if i < max_i-1:
                    father.removeChild(item)
                    father.insertChild(i+1, item)
                    self.treewidget.setCurrentItem(item)

            
            if len(index) == 1:
                if index[0] < max_i-1:
                    childs = self.elt.getchildren()
                    child = childs[index[0]]
                    self.elt.remove(child)
                    self.elt.insert(index[0]+1, child)
            elif len(index) == 2:
                if index[1] < max_i-1:
                    childs = self.elt.getchildren()
                    father = childs[index[0]]
                    childs = father.getchildren()
                    child = childs[index[1]]
                    father.remove(child)
                    father.insert(index[1]+1, child)

            self.isMove = True


    def findIndex(self,item):
        index = []
        father = None
        
        if item != None:
            father = item.parent()

        while father != None:
            i = father.indexOfChild(item)
            index.append(i)
            item = father
            father = father.parent()

        index.reverse()
        return index

    def reset(self):
        self.titleline1.clear()
        self.attriname.setCurrentIndex(0)
#        self.nameline.clear()
        self.valueline.clear()
        self.colswidget.clear()
        self.tableswidget.clear()
        self.tableswidget.addItems(self.tablelist)
        num = self.attritable.rowCount()
        for i in range(num):
            self.attritable.removeRow(0)
        

class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, attr):
        super(TreeWidgetItem, self).__init__(parent)
        self.attribute = attr
        
