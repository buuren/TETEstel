#!/usr/bin/python
#_*_ coding: utf-8 _*_

import wx
import estel
import sys, os

class MainWindow(wx.Frame):
	"""docstring for MainWindow"""

	revisionCheckButtonStatus = False
	cleanPDFNamedCheckButtonStatus = False
	creatListCheckButtonStatus = False

	folderPath = ''

	def __init__(self, parent, title):
		super(MainWindow, self).__init__(parent, title = title, size = (700, 200))

		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI (self):

		panel = wx.Panel(self)

		font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
		font.SetPointSize(12)

		vbox = wx.BoxSizer(wx.VERTICAL)

		hboxTop = wx.BoxSizer(wx.HORIZONTAL)
		locationLabel = wx.StaticText(panel, label = 'Folder Location Path')
		locationLabel.SetFont(font)
		hboxTop.Add(locationLabel, flag = wx.RIGHT, border = 8)
		locationPanel = wx.TextCtrl(panel)
		hboxTop.Add(locationPanel, proportion = 1)
		locationPanel.Bind(wx.EVT_TEXT, self.getPath)
		vbox.Add(hboxTop, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10)

		vbox.Add((-1, 25))

		hboxCheckBoxes = wx.BoxSizer(wx.HORIZONTAL)
		revisionCheckButton = wx.CheckBox(panel, label = 'Add Revision Number')
		revisionCheckButton.SetFont(font)
		hboxCheckBoxes.Add(revisionCheckButton)
		revisionCheckButton.Bind(wx.EVT_CHECKBOX, self.revisionCheckButtonStatusChange)
		cleanPDFNamedCheckButton = wx.CheckBox(panel, label = 'Clear PDF names')
		cleanPDFNamedCheckButton.SetFont(font)
		hboxCheckBoxes.Add(cleanPDFNamedCheckButton, flag = wx.LEFT, border = 10)
		cleanPDFNamedCheckButton.Bind(wx.EVT_CHECKBOX, self.cleanPDFNamedCheckButtonStatusChange)
		creatListCheckButton = wx.CheckBox(panel, label = 'Creat List of PDF')
		creatListCheckButton.SetFont(font)
		hboxCheckBoxes.Add(creatListCheckButton, flag = wx.LEFT, border = 10)
		creatListCheckButton.Bind(wx.EVT_CHECKBOX, self.creatListCheckButtonStatusChange)
		vbox.Add(hboxCheckBoxes, flag = wx.LEFT, border = 10)

		vbox.Add((-1, 25))

		hboxButtons = wx.BoxSizer(wx.HORIZONTAL)
		startButton = wx.Button(panel, label = 'Start', size = (70, 30))
		hboxButtons.Add(startButton, flag = wx.ALIGN_BOTTOM | wx.LEFT, border = 10)
		vbox.Add(hboxButtons, proportion = 1, flag = wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.RIGHT , border = 10)

		startButton.Bind(wx.EVT_BUTTON, self.startButtonPressed) #событие при нажатии кнопки

		vbox.Add((-1, 10))
		
		panel.SetSizer(vbox)

	def startButtonPressed(self, e):
		try:
			if (self.cleanPDFNamedCheckButtonStatus == True):
				os.chdir(self.folderPath)
				tempPDFList = estel.pathListPDF(self.folderPath)
				for items in tempPDFList:
					i = 0
					if items[i:i+3] == 'EL.':
						if items [i+13:i+15] == '-0' or items [i+13:i+15] == '-1':
							os.rename(items, items[:i+16] + '.pdf')
						else:
							os.rename(items, items[:i+13] + '.pdf')
				wx.MessageBox('All Pdf name was clean', 'Info', wx.OK | wx.ICON_INFORMATION)
			if (self.revisionCheckButtonStatus == True):
				os.chdir(self.folderPath)
				errorLogList = estel.renamePDF(self.folderPath)
				if errorLogList != []:
					errorFile = open('errorLog.txt', 'w+')
					errorFile.writelines("%s\n" % i for i in errorLogList)
					errorFile.close()
					wx.MessageBox('=( Something gone wrong. Look errorLog file.', 'Info', wx.OK | wx.ICON_INFORMATION)
				else:
					wx.MessageBox('Revision Number will be change', 'Info', wx.OK | wx.ICON_INFORMATION)
			if (self.creatListCheckButtonStatus == True):
				os.chdir(self.folderPath)
				PDFList = estel.pathListPDF(self.folderPath)
				listPDF = open('PDFList.txt', 'w+')
				listPDF.writelines("%s\n" % i for i in PDFList)
				listPDF.close()
				wx.MessageBox('List was created', 'Info', wx.OK | wx.ICON_INFORMATION)
			if (self.cleanPDFNamedCheckButtonStatus == False & self.revisionCheckButtonStatus == False\
			 & self.creatListCheckButtonStatus == False):
				pass
		except OSError:
			wx.MessageBox('No such directory', 'Info', wx.OK | wx.ICON_INFORMATION)


	def getPath(self, e):
		sender = e.GetEventObject()
		self.folderPath = sender.GetValue()

	def revisionCheckButtonStatusChange(self, e):
		sender = e.GetEventObject()
		isChecked = sender.GetValue()

		if isChecked:
			self.revisionCheckButtonStatus = True
		else:
			self.revisionCheckButtonStatus = False

	def cleanPDFNamedCheckButtonStatusChange(self, e):
		sender = e.GetEventObject()
		isChecked = sender.GetValue()

		if isChecked:
			self.cleanPDFNamedCheckButtonStatus = True
		else:
			self.cleanPDFNamedCheckButtonStatus = False

	def creatListCheckButtonStatusChange(self, e):
		sender = e.GetEventObject()
		isChecked = sender.GetValue()

		if isChecked:
			self.creatListCheckButtonStatus = True
		else:
			self.creatListCheckButtonStatus = False


def main():
	app = wx.App()
	MainWindow(None, title = 'TET Estel v 1.0.003')

	app.MainLoop()

if __name__ == '__main__':
	main()
