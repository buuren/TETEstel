#!usr/bin/env python
#_*_ coding: utf-8 _*_

from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage

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