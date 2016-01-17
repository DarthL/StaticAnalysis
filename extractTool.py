from utility import Utility
import os
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
                curOffset = f.read(4)
                if curOffset == 0:
                    break
                lwlwl
                dataOffset = getDataInOffset(curOffset+0x10,4)
                nameOffset = getDataInOffset(dataOffset,4)
                name = readStringFromOffsetOfFile(nameOffset,machofile)
                results.append(name)
        return results
