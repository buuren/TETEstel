#!/usr/bin/env python
#_*_coding: utf-8 _*_

from __future__ import print_function, division, absolute_import
import estel
import sys, getopt, os

def main(argv):
    def usage():
        print ('usage estel.py [-r folder location] [-l folder location] [-c folder location]')
    try:
        (opts, args) = getopt.getopt(argv[1:], 'r:l:c:')
    except getopt.GetoptError:
        return usage()
    if not opts:
        return usage()
    for (k, v) in opts:
        if k == '-r': #Переименовываем документы (добавляем номер ревизии)
            os.chdir(v)
            errorLogList = estel.renamePDF(v)
            if errorLogList != []:
                errorFile = open('errorLog.txt', 'w+')
                errorFile.writelines("%s\n" % i for i in errorLogList)
                errorFile.close()
                print ('=( Something gone wrong. Look errorLog file.')
            else:
                print ('=) OK!')
        elif k == '-l': #выводим список PDF файлов в директории
            os.chdir(v)
            PDFList = estel.pathListPDF(v)
            listPDF = open('PDFList.txt', 'w+')
            listPDF.writelines("%s\n" % i for i in PDFList)
            listPDF.close()
            print('OK!')
        elif k == '-c': #чистим название PDF файлов чертежей (оставляем только EL. номер)
            os.chdir(v)
            tempPDFList = estel.pathListPDF(v)
            for items in tempPDFList:
                i = 0
                if items[i:i+3] == 'EL.':
                    if items [i+13:i+15] == '-0' or items [i+13:i+15] == '-1':
                        os.rename(items, items[:i+16] + '.pdf')
                    else:
                        os.rename(items, items[:i+13] + '.pdf')

if __name__ == '__main__':
    main(sys.argv)