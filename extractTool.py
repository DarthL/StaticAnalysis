from macho_utility import Macho_Utility
from common_utility import readStringFromOffsetOfFile,readVMData
import struct
import os
import pdb
from objc_class import Objc_Class
class extracttool:
    def __init__(self,path):
        self.path = os.path.abspath(path)
        print "extracttool inited with abs path %s" % self.path
        self.macho_utility = Macho_Utility(self.path)
        self.macho_utility.initLoadCommand();
        self.is64bit = self.macho_utility.is64bit(0)
    def extractclasses(self):
        results=[]
        sec = self.macho_utility.findSegandSecInFile("__DATA","__objc_classlist")
        secOffset = sec.fileoff
        while secOffset < sec.fileoff+sec.vmsize:
            with open(self.path,'rb') as f:
                f.seek(secOffset)
                curclassVM = readVMData(f.tell(),f,self.is64bit) #vm_addr
                curclassOff = self.macho_utility.getFileOffFromVmAddr(curclassVM) #in __DATA.__objc_data
                curObjc_class = Objc_Class(self,f,curclassOff,self.is64bit)

                results.append(curObjc_class)
                secOffset = secOffset + 0x4 #every 4 bytes a class in 32bit
                if self.is64bit:
                    secOffset = secOffset + 0x4 #every 8 bytes a class in 64bit
        return results 
    
    def extractLibs(self):
        return self.macho_utility.libs
    def extractIndSyms(self):
         with open(self.path,'rb') as f:
             cmdOffset =  self.macho_utility.loadcommands["LD_DYSYMTAB"]
             f.seek(cmdOffset)
             print cmdOffset
