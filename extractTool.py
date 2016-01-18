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
        
    def extractclasses(self):
        results=[]
        secOffset = self.utility.findSegandSecInFile("__DATA","__objc_classlist")
        while True:
            with open(self.path,'rb') as f:
                f.seek(secOffset)
                curclassVM = int(struct.unpack('<L',f.read(4))[0]) #vm_addr               
                if curclassVM == 0:
                    break
                curclassOff = self.utility.getFileOffFromVmAddr(curclassVM)
                f.seek(curclassOff+0x10)
                dataVMaddr = int(struct.unpack('<L',f.read(4))[0])#vm_addr
                dataOffset = self.utility.getFileOffFromVmAddr(dataVMaddr)
                f.seek(dataOffset+0x10)#0x10 in 32bit 
                pdb.set_trace()
                nameVMaddr = int(struct.unpack('<L',f.read(4))[0])#vm_addr
                nameOffset = self.utility.getFileOffFromVmAddr(nameVMaddr)
                name = self.utility.readStringFromOffsetOfFile(nameOffset,f)
                results.append(name)
                secOffset = secOffset + 0x4 #every 4bytes a class 
        return results
