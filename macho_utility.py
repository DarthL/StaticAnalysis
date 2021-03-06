import os
import struct
import pdb
from segment import Segment
from lcloaddylib import LcLoadDylib
from  common_utility import readStringFromOffsetOfFile
MACHO_HEADER_SIZE_32bit=0x1c
MACHO_HEADER_SIZE_64bit=0x20
MACHO_MAGIC_iOS=0xFEEDFACE
MACHO_MAGIC_Mac=0xFEEDFACF

class Macho_Utility:
    def __init__(self,path):
        self.path = path
        self.segments = []
        self.libs= []
        self.loadcommands = {}
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

    def initLoadCommand(self):
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
                    fileOff = f.tell()
                    cmdName = int(struct.unpack('<L',f.read(4))[0])
                    cmdSize = int(struct.unpack('<L',f.read(4))[0])
                    if cmdName == 0x01 or cmdName == 0x19:
                        #segment
                        #self.loadcommands["LC_SEGMENT"]=f.tell()
                        segment = Segment(f,f.tell(),self.is64bit(0)) #f.tell()will change in called-Function           
                        self.segments.append(segment)
                    elif cmdName == 0x0c or cmdName == 0x8000001c:
                        if cmdName == 0x0c:
                            #LC_LOAD_DYLIB
                            #self.loadcommands["LC_LOAD_DYLIB"]=f.tell()
                            lcdylib = LcLoadDylib(f,f.tell())
                            self.libs.append(lcdylib.name)
                            f.seek(fileOff+cmdSize)
                        else:
                            #LC_RPATH
                            #self.loadcommands["LC_RPATH"]=f.tell()
                            pdb.set_trace()
                            f.read(4) #  strOffset
                            rpath = readStringFromOffsetOfFile(f.tell(),f)
                            self.libs.append(rpath)
                            f.seek(fileOff+cmdSize)
                    elif cmdName == 0xB:
                        #LD_DYSYMTAB
                        self.loadcommands["LD_DYSYMTAB"]=f.tell()-0x8
                        f.seek(f.tell()-0x8+cmdSize)
                    else:
                        f.seek(f.tell()-0x8+cmdSize)
                        continue

    def findSegandSecInFile(self,segment,section):
        for seg in self.segments:
            if segment in seg.segName:
                for sec in seg.sections:
                    if section in sec.secName:
                        return sec
    
    def getFileOffFromVmAddr(self,vmaddr):
        for seg in self.segments:
            if seg.vmaddr<=vmaddr and seg.vmaddr+seg.vmsize>=vmaddr:
                return seg.fileoff+vmaddr-seg.vmaddr


