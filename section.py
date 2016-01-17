import struct
class Section:
    def __init__(self,f,offset,is64bit):
        addsize = 0;
        if is64bit:
            addsize = 8
        else:
            addsize = 4
        f.seek(offset)
        self.secName     = f.read(16)
        self.segName     = f.read(16)
        self.vmadd       = int(struct.unpack('<L',f.read(addsize))[0])
        self.vmsize      = int(struct.unpack('<L',f.read(addsize))[0])
        self.fileoff     = int(struct.unpack('<L',f.read(4))[0])
        self.align       = int(struct.unpack('<L',f.read(4))[0])
        self.reloff      = int(struct.unpack('<L',f.read(4))[0])
        self.nreloc      = int(struct.unpack('<L',f.read(4))[0])
        self.flags       = int(struct.unpack('<L',f.read(4))[0])
        self.reserved1   = int(struct.unpack('<L',f.read(4))[0])
        self.reserved2   = int(struct.unpack('<L',f.read(4))[0])
        if is64bit:
            self.reserved3   = int(struct.unpack('<L',f.read(4))[0])

