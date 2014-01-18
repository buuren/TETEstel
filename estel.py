#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from __future__ import print_function, division, absolute_import
import os, sys, getopt
import parserPDF


	
def revSearch(rev):
    """ Функция поска номера ревизии например A130212 """
    revDocument = ''
    for strings in rev:
        i = 0
        while i != len(strings):
            if strings[i] == 'A' or strings[i] == 'B' or strings[i] == 'C'\
                or strings[i] == 'D' or strings[i] == 'E'\
                or strings[i] == 'F' or strings[i] == 'G'\
                or strings[i] == 'H' or strings[i] == 'I'\
                or strings[i] == 'J' or strings[i] == 'K'\
                or strings[i] == 'L' or strings[i] == 'M':
                if strings[i+1:i+3] == '13' or strings[i+1:i+3] == '12'\
                    or strings[i+1:i+3] == '11' or strings[i+1:i+3] == '10'\
                    or strings[i+1:i+3] == '09' or strings[i+1:i+3] == '08'\
                    or strings[i+1:i+3] == '07' or strings[i+1:i+3] == '06':
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
    """ Возврощяет список деталий(EL.754342.668) для сборки из спецификации"""
    ELlist = parserPDF.myPDFParser(specification)
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
                if revSearch(parserPDF.myPDFParser(docs)) == '':
                    errorLogList.append(path + '  ' + docs)
                else:
                    os.rename(docs, docs[:-4] + '_Rev.' + revSearch(parserPDF.myPDFParser(docs)) + '.pdf')
            except AssertionError:
                errorLogList.append(path + '  ' + docs)
    return errorLogList