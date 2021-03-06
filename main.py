from extractTool import extracttool 
import sys

def main():
    if len(sys.argv) < 2:
        print "at least more than one arg"
        exit(-1)
    vextracttool=extracttool(sys.argv[1])
    classes = vextracttool.extractclasses()
    libs    = vextracttool.extractLibs()
    print classes
    for sclass in classes:
        print sclass.name
        print sclass.methods
    print libs
    vextracttool.extractIndSyms()

if __name__=='__main__':
    main()
