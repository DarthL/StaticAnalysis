import os
import struct
from segment import Segment
MACHO_HEADER_SIZE=0x1c
MACHO_MAGIC=0xFEEDFACE
class Utility:
    def __init__(self,path):
        self.path = path
        self.segments = []
        print "utility inited with path %s" % path
        
    def isfat(self):
        cmd = "otool -f %s" % self.path
        return os.system(cmd) != 0

    def isMachO(self):
        with open(self.path,'rb') as f:
            if self.isfat():
                pass
            else:
                magic = int(struct.unpack('<L',f.read(4))[0]) 
                return magic == MACHO_MAGIC

    def findallSegments(self):
        with open(self.path,'rb') as f:            
            if self.isfat():
                #find first arch
                pass
            elif self.isMachO():
                f.seek(0x10)
                LCcount = int(struct.unpack('<L',f.read(4))[0])
                #skip mach-o header
                f.seek(MACHO_HEADER_SIZE)
                index = 0
                while index < LCcount:
                    index = index+1
                    cmdName = int(struct.unpack('<L',f.read(4))[0])
                    if cmdName == 0x01 or cmdName == 0x19:
                        #segment
                        segment = Segment(f,f.tell())
                        self.segments.append(segment)
                    else:
                        continue

    def findSegandSecInFile(self,segment,section):
        for seg in self.segments:
            if segment in seg.segName:
                for sec in seg.sections:
                    if section in sec.secName:
                        return sec.fileoff

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


