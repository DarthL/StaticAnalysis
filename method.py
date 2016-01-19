import struct
from common_utility import readStringFromOffsetOfFile,readVMData
class Method:
    def __init__(self,tool,f,offset,is64bit):
        self.extracttool = tool
        self.is64bit = is64bit
        self.name = self.getName(f,offset)
        self.mtype= self.getType(f,offset)
        #self.imp  = self.getIMP(f,offset)
 
    def getName(self,f,offset):
        methodnameVM = readVMData(offset,f,self.is64bit) #name offset 0x8 byte in method struct
        methodnameOffset = self.extracttool.macho_utility.getFileOffFromVmAddr(methodnameVM)
        methodname = readStringFromOffsetOfFile(methodnameOffset,f)
        return methodname

    def getType(self,f,offset):
        if self.is64bit:
            offset = offset + 0x8
        else:
            offset = offset + 0x4
            
        methodTypeVM = readVMData(offset,f,self.is64bit) #name offset 0x8 byte in method struct
        methodTypeOffset = self.extracttool.macho_utility.getFileOffFromVmAddr(methodTypeVM)
        methodType = readStringFromOffsetOfFile(methodTypeOffset,f)
        return methodType

    def getIMP(self,f,offset):
        if self.is64bit:
            offset = offset + 0x10
        else:
            offset = offset + 0x8
        methodIMPVM = readVMData(typeoffset,f,self.is64bit) #name offset 0x8 byte in method struct
        methodIMPOffset = self.extracttool.macho_utility.getFileOffFromVmAddr(methodTypeVM)
        methodIMP = readStringFromOffsetOfFile(methodTypeOffset,f)
        return methodIMP
