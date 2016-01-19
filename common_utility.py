import struct
def readStringFromOffsetOfFile(offset,f):
        result=''
        f.seek(offset)
        strlength = 0
        while ord(f.read(1)) != 0:
            strlength=strlength+1
        f.seek(offset)
        if strlength !=0:
            result = f.read(strlength)
        return result

def readVMData(offset,f,is64bit):
    if is64bit:
        return int(struct.unpack('<Q',f.read(8))[0])
    else:
        return int(struct.unpack('<L',f.read(4))[0])
