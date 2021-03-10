# 搜索指定目录（文件）下包含指定字符串的文件，及行号

#!/usr/bin/python
#encoding:utf-8
#  Filename : findString.py
#author by :morespeech
#python2.7
#platform:pycharm
 
 
import os
import re
class cFindString:
####public functions
    def __init__(self, filepattern , txtpattern):
        self.filePattern = re.compile(filepattern)
        self.txtParttern = re.compile(txtpattern)
 
    def findStringInFile(self, filename):
        if os.path.isdir(filename):
            for subfilename in os.listdir(filename):
                subfilename = os.path.join(filename, subfilename)
                self.findStringInFile(subfilename)
        else:
            if not os.path.exists(filename):
                print filename ,'not exist'
                return
            fileHandle = open(filename, 'rb')
            nLine = 0
            for line in fileHandle:
                search = self.txtParttern.search(line)
                if search:
                    print filename ,'(',nLine, ')', line
                nLine = nLine + 1
            fileHandle.close()
 
g_stringPattern=''
g_filePattern=''
g_filename=''
 
def parse():
    from optparse import OptionParser
    usage = "usage:findString [opthions] -n=.cpp -s=\d\w -f 1.cpp"
    parser = OptionParser(usage=usage)
    parser.add_option("-n", "--filenamePattern", dest = "wantfilePattern",help="match file format, .cpp/.c/.py etc")
    parser.add_option("-s", "--stringPattern", dest = "wantstringPattern", help="match string, regex etc")
    parser.add_option("-f", "--filename", dest = "wantfilename", help="input the file or folder you want to find")
 
    (options, args) = parser.parse_args()
 
    if options.wantfilePattern and options.wantstringPattern and options.wantfilename:
        global g_filePattern, g_stringPattern, g_filename
        g_filePattern = options.wantfilePattern
        g_stringPattern = options.wantstringPattern
        g_filename = options.wantfilename
    else:
         parser.print_help()
 
 
if __name__== "__main__":
    parse()
    cFindString(g_filePattern, g_stringPattern).findStringInFile(g_filename)