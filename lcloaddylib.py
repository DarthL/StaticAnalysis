import struct
from common_utility import readStringFromOffsetOfFile
class LcLoadDylib:
    def __init__(self,f,offset):
        f.seek(offset)
        self.strOffset = int(struct.unpack('<L',f.read(4))[0])
        self.timeStamp = int(struct.unpack('<L',f.read(4))[0])
        self.curVersion= int(struct.unpack('<L',f.read(4))[0])
        self.cptVersion= int(struct.unpack('<L',f.read(4))[0])
        self.name      = readStringFromOffsetOfFile(f.tell(),f)
        

