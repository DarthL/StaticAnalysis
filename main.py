from extractTool import extracttool 
import sys

def main():
    if len(sys.argv) < 2:
        print "at least more than one arg"
        exit(-1)
    vextracttool=extracttool(sys.argv[1])
    classes = vextracttool.extractclasses()
    print classes
if __name__=='__main__':
    main()
