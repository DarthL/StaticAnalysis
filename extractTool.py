from utility import Utility
import struct
import os
import pdb
class extracttool:
    def __init__(self,path):
        self.path = os.path.abspath(path)
        print "extracttool inited with abs path %s" % self.path
        self.utility = Utility(self.path)
        self.utility.findallSegments();
        self.is64bit = self.utility.is64bit(0)
    def extractclasses(self):
        results=[]
        sec = self.utility.findSegandSecInFile("__DATA","__objc_classlist")
        secOffset = sec.fileoff
        while secOffset < sec.fileoff+sec.vmsize:
            with open(self.path,'rb') as f:
                f.seek(secOffset)
                curclassVM=0
                curclassVM = self.utility.readVMData(f.tell(),f,self.is64bit) #vm_addr
                curclassOff = self.utility.getFileOffFromVmAddr(curclassVM) #in __DATA.__objc_data
                f.seek(curclassOff+0x10)
                if self.is64bit:
                    f.read(0x10)
                dataVMaddr = self.utility.readVMData(f.tell(),f,self.is64bit)#vm_addr
                dataOffset = self.utility.getFileOffFromVmAddr(dataVMaddr)  #in __DATA.__objc_const
                f.seek(dataOffset+0x10)#0x10 in 32bit 0x18 in 64bit 
                if self.is64bit:
                    f.read(0x8)   
                nameVMaddr = self.utility.readVMData(f.tell(),f,self.is64bit)
                nameOffset = self.utility.getFileOffFromVmAddr(nameVMaddr)
                name = self.utility.readStringFromOffsetOfFile(nameOffset,f)
                results.append(name)
                secOffset = secOffset + 0x4 #every 4 bytes a class in 32bit
                if self.is64bit:
                    secOffset = secOffset + 0x4 #every 8 bytes a class in 64bit
        return results
