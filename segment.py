from section import Section
import struct
import pdb
class Segment:
    def __init__(self,f,offset,is64bit=False):
        f.seek(offset)
        self.segName  = f.read(16)
        if is64bit:
            self.vmaddr   = int(struct.unpack('<Q',f.read(8))[0])
            self.vmsize   = int(struct.unpack('<Q',f.read(8))[0])
            self.fileoff  = int(struct.unpack('<Q',f.read(8))[0])
            self.filesize = int(struct.unpack('<Q',f.read(8))[0])
        else:
            self.vmaddr   = int(struct.unpack('<L',f.read(4))[0])
            self.vmsize   = int(struct.unpack('<L',f.read(4))[0])
            self.fileoff  = int(struct.unpack('<L',f.read(4))[0])
            self.filesize = int(struct.unpack('<L',f.read(4))[0])
        self.maxprot  = int(struct.unpack('<L',f.read(4))[0])
        self.initprot = int(struct.unpack('<L',f.read(4))[0])
        self.nsects   = int(struct.unpack('<L',f.read(4))[0])
        self.flag     = int(struct.unpack('<L',f.read(4))[0])
        self.sections = []
        if self.nsects > 0:
            indexOfSections = 0
            while(indexOfSections < self.nsects):
                section = Section(f,f.tell(),is64bit)
                self.sections.append(section)
                indexOfSections=indexOfSections+1
