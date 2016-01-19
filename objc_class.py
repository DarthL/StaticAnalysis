from common_utility import readStringFromOffsetOfFile,readVMData
import pdb
import struct
from method import Method

class Objc_Class:
    def __init__(self,tool,f,offset,is64bit):
        self.is64bit = is64bit
        self.extracttool = tool
        self.methods = []
        self.name = self.initName(f,offset)
        

    
    def initName(self,f,curclassOff):
        f.seek(curclassOff+0x10)
        if self.is64bit:
            f.read(0x10)
        dataVMaddr = readVMData(f.tell(),f,self.is64bit)#vm_addr
        dataOffset = self.extracttool.macho_utility.getFileOffFromVmAddr(dataVMaddr)  #in __DATA.__objc_const
        f.seek(dataOffset+0x10)#0x10 in 32bit 0x18 in 64bit 
        if self.is64bit:
            f.read(0x8)

        nameVMaddr = readVMData(f.tell(),f,self.is64bit)
        cursor = f.tell()
        nameOffset = self.extracttool.macho_utility.getFileOffFromVmAddr(nameVMaddr)
        name = readStringFromOffsetOfFile(nameOffset,f)
        self.methods = self.initMethods(f,cursor)
        return name

    def initMethods(self,f,methodsTableOffset):
        results = []
        f.seek(methodsTableOffset)
        curMethodVM = readVMData(f.tell(),f,self.is64bit)
        curMethodOffset = self.extracttool.macho_utility.getFileOffFromVmAddr(curMethodVM)
        
        f.seek(curMethodOffset)
        entsize = int(struct.unpack('<L',f.read(4))[0])        
        methodCount = int(struct.unpack('<L',f.read(4))[0])
        
        indexOfMethods = 0
        cursor = f.tell()
        while indexOfMethods < methodCount:
            #pdb.set_trace()
            curMethod = Method(self.extracttool,f,cursor,self.is64bit)
            results.append(curMethod)
            indexOfMethods = indexOfMethods + 1
            if self.is64bit:
                cursor = cursor + 0x8*3
            else:
                cursor = cursor + 0x4*3
        return results
        

        



