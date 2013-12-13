#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from __future__ import print_function, division, absolute_import
from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
import os, sys, getopt

#Блок парсера PDF \начало\
def parse_pages(doc):
    """ Функция парсинга страниц """
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in doc.get_pages():
        interpreter.process_page(page)
        # получаем объект LTPage
        layout = device.get_result()
        # layout - объект контейнер который может содержать другие объекты LTTextBox, LTFigure, LTImage
        yield layout

class PdfMinerWrapper(object):
    """ Контент менеджер """
    def __init__(self, pdf_doc, pdf_pwd=''):
        self.pdf_doc = pdf_doc
        self.pdf_pwd = pdf_pwd

    def __enter__(self):
        # открываем пдф-файл
        self.fp = open(self.pdf_doc, 'rb')
        # создаем объект парсера
        parser = PDFParser(self.fp)
        # создаем объект пдф документа
        doc = PDFDocument()
        # подключение парсера к объекту документа
        parser.set_document(doc)
        doc.set_parser(parser)
        # инициализация по паролю
        doc.initialize(self.pdf_pwd)
        return doc

    def __exit__(self, type, value, traceback):
        self.fp.close()

def myPDFParser(pdf_doc):
    PDFStrings = []
    with PdfMinerWrapper(pdf_doc) as doc:
        for page in parse_pages(doc):
           for obj in page.__dict__['_objs']:
               if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine):
               #Если текст
                    PDFStrings.append(obj.get_text())
    return PDFStrings

#Блок парсера PDF\ конец
	
def revSearch(rev):
    """ Функция поска номера ревизии например A130212 """
    revDocument = ''
    for strings in rev:
        i = 0
        while i != len(strings):
            if strings[i] == 'A' or strings[i] == 'B' or strings[i] == 'C'\
                or strings[i] == 'D' or strings[i] == 'E'\
                or strings[i] == 'F' or strings[i] == 'G':
                if strings[i+1:i+3] == '13' or strings[i+1:i+3] == '12'\
                    or strings[i+1:i+3] == '11' or strings[i+1:i+3] == '10'\
                    or strings[i+1:i+3] == '09' or strings[i+1:i+3] == '08':
                    if strings[i+3:i+5] == '01' or strings[i+3:i+5] == '02'\
                        or strings[i+3:i+5] == '03' or strings[i+3:i+5] == '04'\
                        or strings[i+3:i+5] == '05' or strings[i+3:i+5] == '06'\
                        or strings[i+3:i+5] == '07' or strings[i+3:i+5] == '08'\
                        or strings[i+3:i+5] == '09' or strings[i+3:i+5] == '10'\
                        or strings[i+3:i+5] == '11' or strings[i+3:i+5] == '12':
                        revDocument = strings[i:i+7]
			if revDocument != '':
				break
            i = i + 1
    return revDocument

def pathListPDF(path):
    """ Возврощяет список PDF файлов в дериктории"""
    listPDF = []
    for files in os.listdir(path):
        if files.find('.pdf') != -1:
            listPDF.append(files)
    return listPDF

def pathListDWG(path):
    """ Возврощяет список DWG файлов в дериктории"""
    listDWG = []
    for files in os.listdir(path):
        if files.find('.dwg') != -1:
            listDWG.append(files)
    return listDWG
	
def pathListIDW(path):
	""" Возвращает список IPT файлов в директории"""
	listIDW = []
	for files in os.listdir(path):
		if files.find('.idw') != -1:
			listIPT.append(files)
	return listIPT

def pathListDir(path):
    """Возврощяет список дерикторий в дериктории"""
    pass

def listFromSpecification(specification):
    """ Возврощяет список детели(EL.754342.668) для сборки из спецификации"""
    ELlist = myPDFParser(specification)
    retELlist = []
    for el in ELlist:
        i = 0
        while i != len(ELlist):
            if el[i:i+3] == 'EL.':
                if el[i+13] == '-':
                    retELlist.append(el[i:i+16])
                else:
                    retELlist.append(el[i:i+13])
            i = i + 1
    return retELlist

def renamePDF(path):
    """ Добавляет к названию файла номер ревизии
    и возвращяет список файлов которые не удолось прочитать"""
    errorLogList = []
    for docs in pathListPDF(path):
        if docs.find('_Rev') == -1:
            os.chdir(path)
            try:
                if revSearch(myPDFParser(docs)) == '':
                    errorLogList.append(path + '  ' + docs)
                else:
                    os.rename(docs, docs[:-4] + '_Rev.' + revSearch(myPDFParser(docs)) + '.pdf')
            except AssertionError:
                errorLogList.append(path + '  ' + docs)
    return errorLogList

def main(argv):
    def usage():
        print ('usage estel.py [-r folder location] [-l file]')
    try:
        (opts, args) = getopt.getopt(argv[1:], 'r:l:')
    except getopt.GetoptError:
        return usage()
    if not opts:
        return usage()
    for (k, v) in opts:
        if k == '-r': #Переименовываем документы (добавляем номер ревизии)
            errorLogList = renamePDF(v)
            if errorLogList != '':
                errorFile = open('errorLog.txt', 'w+')
                errorFile.writelines("%s\n" % i for i in errorLogList)
                errorFile.close()
                print ('=( Something gone wrong. Look errorLog file.')
            else:
                print ('=) OK!')
        elif k == '-l':
			pass

if __name__ == '__main__':
    main(sys.argv)