from macho_utility import Macho_Utility
import sys
if __name__=='__main__':
    machut = Macho_Utility(sys.argv[1])
    machut.initLoadCommand()
    print hex(machut.getFileOffFromVmAddr(int(sys.argv[2],0)))
