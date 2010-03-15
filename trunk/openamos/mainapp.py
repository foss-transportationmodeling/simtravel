import os

from lxml import etree

class MainApp:
    def __init__(self):
        self.newproject = False
        self.projectname=""
        self.projectlocation=""
    
    def run(self):
        input = raw_input("Please choose one of the following:\n" +
                                "1. Start a new project\n" +
                                "2. Open an existing project\n" +
                                "Choice: ")
        while(input not in ['1','2']):
            input = raw_input("Please choose either 1 (new project) or " +
                                        "2 (existing project)!!: ")
        if(input == '1'):
            self.newproject = True
            self.create_project()
 
        elif(input == '2'):
            self.read_project()
            
    def create_project(self):
        configroot = etree.Element('ProjectConfig')
        configtree = etree.ElementTree(configroot)
        
        projectname = etree.SubElement(configroot, 'ProjectName')
        proname = raw_input("Enter Project Name: ")
        projectname.text = proname

        projecthome = etree.SubElement(configroot, 'ProjectHome')
        prohome = raw_input("Enter directory location for the " +
                                        "new project: ")
        while(not os.path.isdir(prohome)):
            prohome = raw_input("Please enter a VALID directory!!: ")
        prohome = prohome + os.path.sep + proname
        if(not os.path.isdir(prohome)):
            os.makedirs(prohome)
        projecthome.text = prohome

        dbconfig = etree.SubElement(configroot, 'DBConfig')
        dbhost = raw_input("Enter database host location for the " +
                                        "new project: ")
        dbconfig.set('dbhost', dbhost)
        dbusername = raw_input("Enter database username: ")
        dbconfig.set('dbusername', dbusername)
        dbpassword = raw_input("Enter database password: ")
        dbconfig.set('dbpassword', dbpassword)
        
        modelconfig = etree.SubElement(configroot, 'ModelConfig')
        
        longterm = etree.SubElement(modelconfig, 'LongTermModels')
        workstat = etree.SubElement(longterm, 'WorkStat')
        workstat.set('type', 'Multinomial Logit')
        workstat.set('altspec', 'True')
        alts = etree.SubElement(workstat, 'Alternatives')
        worker = etree.SubElement(alts, 'Worker')
        var1 = etree.SubElement(worker, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'somevar')
        var1.set('coeff', '0.5')           
        var2 = etree.SubElement(worker, 'Variable')
        var2.set('db', 'somedb')
        var2.set('table', 'sometab')
        var2.set('var', 'somevar')
        var2.set('coeff', '0.6')        
        nonworker = etree.SubElement(alts, 'NonWorker')
        var1 = etree.SubElement(nonworker, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'constant')
        var1.set('coeff', '0.0')
       
        
        numjobs = etree.SubElement(longterm, 'NumJobs')
        numjobs.set('type', 'Negative Binomial')
        alts = etree.SubElement(numjobs, 'Alternatives')
        alts.append(etree.Element('Alternative', id='0'))
        alts.append(etree.Element('Alternative', id='1'))
        alts.append(etree.Element('Alternative', id='2'))
        vars = etree.SubElement(numjobs, 'Variables')
        var1 = etree.SubElement(vars, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'somevar')
        var1.set('coeff', '0.5')
        var2 = etree.SubElement(vars, 'Variable')
        var2.set('db', 'somedb')
        var2.set('table', 'sometab')
        var2.set('var', 'somevar')
        var2.set('coeff', '0.6')   
        schstat = etree.SubElement(longterm, 'SchStat')
        schstat.set('type', 'Probability Distribution')
        cats = etree.SubElement(schstat, 'Categories')
        cat1 = etree.Element('Category', id='0-5yrs')
        cats.append(cat1)
        dist = etree.SubElement(cat1, 'Distribution')
        dist.set('yes','0.9')
        dist.set('no','0.1')
        cat2 = etree.Element('Category', id='5-14yrs')
        cats.append(cat2)
        dist = etree.SubElement(cat2, 'Distribution')
        dist.set('yes','0.6')
        dist.set('no','0.4')

        fixedact = etree.SubElement(modelconfig, 'FixedActivityModels')
        workloc = etree.SubElement(fixedact, 'WorkLoc')
        workloc.set('type', 'Multinomial Logit')
        workloc.set('altspec', 'False')
        vars = etree.SubElement(workloc, 'Variables')
        var1 = etree.SubElement(vars, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'somevar')
        var1.set('coeff', '0.5')
        var2 = etree.SubElement(vars, 'Variable')
        var2.set('db', 'somedb')
        var2.set('table', 'sometab')
        var2.set('var', 'somevar')
        var2.set('coeff', '0.6')

        vehown = etree.SubElement(modelconfig, 'VehicleOwnershipModels')
        numveh = etree.SubElement(vehown, 'NumVehs')
        numveh.set('type', 'Ordered Probit')
        alts = etree.SubElement(numveh, 'Alternatives')
        alts.append(etree.Element('Alternative', id='0'))
        alts.append(etree.Element('Alternative', id='1'))
        alts.append(etree.Element('Alternative', id='2'))
        vars = etree.SubElement(numveh, 'Variables')
        var1 = etree.SubElement(vars, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'somevar')
        var1.set('coeff', '0.5')
        var2 = etree.SubElement(vars, 'Variable')
        var2.set('db', 'somedb')
        var2.set('table', 'sometab')
        var2.set('var', 'somevar')
        var2.set('coeff', '0.6')
        var3 = etree.SubElement(vars, 'Variable')
        var3.set('db', 'somedb')
        var3.set('table', 'sometab')
        var3.set('var', 'somevar')
        var3.set('coeff', '0.6')
        thresh = etree.SubElement(numveh, 'Thresholds')
        thresh.append(etree.Element('Threshold', values='1.5'))
        thresh.append(etree.Element('Threshold', values='2.5'))
        vehtype = etree.SubElement(vehown, 'VehTypes')
        vehtype.set('type', 'Nested Logit')
        nests = etree.SubElement(vehown, 'Nests')
        nest1 = etree.SubElement(nests, 'Nest')
        nest1.set('id', 'Car')
        nest1.append(etree.Element('Alternative', id='Car-Gas'))
        nest1.append(etree.Element('Alternative', id='Car-Nongas'))
        nest2 = etree.SubElement(nests, 'Nest')
        nest2.set('id', 'SUV')
        nest2.append(etree.Element('Alternative', id='SUV-Gas'))
        nest2.append(etree.Element('Alternative', id='SUV-Nongas'))
        alts = etree.SubElement(vehown, 'Alternatives')
        alt1 = etree.SubElement(alts , 'Car-Gas')
        var1 = etree.SubElement(alt1, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'somevar')
        var1.set('coeff', '0.5')
        var2 = etree.SubElement(alt1, 'Variable')
        var2.set('db', 'somedb')
        var2.set('table', 'sometab')
        var2.set('var', 'somevar')
        var2.set('coeff', '0.6')        
        alt2 = etree.SubElement(alts , 'Car-Nongas')
        var1 = etree.SubElement(alt2, 'Variable')
        var1.set('db', 'somedb')
        var1.set('table', 'sometab')
        var1.set('var', 'somevar')
        var1.set('coeff', '0.5')
        var2 = etree.SubElement(alt2, 'Variable')
        var2.set('db', 'somedb')
        var2.set('table', 'sometab')
        var2.set('var', 'somevar')
        var2.set('coeff', '0.6')     
        
   



        configfileloc = prohome + os.path.sep + "config.xml"
        if(os.path.isfile(configfileloc)):
            os.remove(configfileloc)
        configfile = open(configfileloc, 'w')
        configtree.write(configfile, pretty_print=True)
        configfile.close()
    
    def read_project(self):
        prohome = raw_input("Enter the directory for existing project:")
        while(not os.path.isdir(prohome)):
            prohome = raw_input("Please enter a VALID directory for existing " +
                                            "project!!: ")
        configfileloc = prohome + os.path.sep + "config.xml"
        configtree = etree.parse(configfileloc)
        print configtree


def main():
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()