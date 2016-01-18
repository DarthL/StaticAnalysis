from utility import Utility
import sys
if __name__=='__main__':
    ut = Utility(sys.argv[1])
    if ut.is64bit(0):
        print "64bit"
    else:
        print "32bit"
