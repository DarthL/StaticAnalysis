import os
import struct
import pdb
from segment import Segment
MACHO_HEADER_SIZE_32bit=0x1c
MACHO_HEADER_SIZE_64bit=0x20
MACHO_MAGIC_iOS=0xFEEDFACE
MACHO_MAGIC_Mac=0xFEEDFACF

class Utility:
    def __init__(self,path):
        self.path = path
        self.segments = []
        print "utility inited with path %s" % path
    
    def is64bit(self,archoffset):
        with open(self.path,'rb') as f:
            f.seek(archoffset+0x8)
            subcputype = int(struct.unpack('<L',f.read(4))[0])
            return subcputype >=0x1000000            

    def isfat(self):
        cmd = "otool -f %s" % self.path
        return os.system(cmd) != 0

    def isMachO(self):
        with open(self.path,'rb') as f:
            if self.isfat():
                pass
            else:
                magic = int(struct.unpack('<L',f.read(4))[0]) 
                return magic == MACHO_MAGIC_iOS or magic == MACHO_MAGIC_Mac

    def findallSegments(self):
        with open(self.path,'rb') as f:            
            if self.isfat():
                #find first arch
                pass
            elif self.isMachO():
                f.seek(0x10)
                LCcount = int(struct.unpack('<L',f.read(4))[0])
                #skip mach-o header  #64bit is 0x20
                if self.is64bit(0):
                    f.seek(MACHO_HEADER_SIZE_64bit)
                else:
                    f.seek(MACHO_HEADER_SIZE_32bit)
                index = 0
                while index < LCcount:
                    index = index+1
                    cmdName = int(struct.unpack('<L',f.read(4))[0])
                    if cmdName == 0x01 or cmdName == 0x19:
                        #segment
                        segment = Segment(f,f.tell(),self.is64bit(0))
                        self.segments.append(segment)
                    else:
                        continue

    def findSegandSecInFile(self,segment,section):
        for seg in self.segments:
            if segment in seg.segName:
                for sec in seg.sections:
                    if section in sec.secName:
                        return sec
    
    def readVMData(self,offset,f,is64bit):
        if is64bit:
            return int(struct.unpack('<Q',f.read(8))[0])
        else:
            return int(struct.unpack('<L',f.read(4))[0])
            
        
        
    def readStringFromOffsetOfFile(self,offset,f):
        result=''
        f.seek(offset)
        strlength = 0
        while ord(f.read(1)) != 0:
            strlength=strlength+1
        f.seek(offset)
        if strlength !=0:
            result = f.read(strlength)
        return result
    
    def getFileOffFromVmAddr(self,vmaddr):
        for seg in self.segments:
            if seg.vmaddr<=vmaddr and seg.vmaddr+seg.vmsize>=vmaddr:
                return seg.fileoff+vmaddr-seg.vmaddr


