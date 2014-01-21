#!/usr/bin/python
#_*_ coding: utf-8 _*_

import wx

class MainWindow(wx.Frame):
	"""docstring for MainWindow"""
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
		vbox.Add(hboxTop, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 10)

		vbox.Add((-1, 25))

		hboxCheckBoxes = wx.BoxSizer(wx.HORIZONTAL)
		revisionCheckButton = wx.CheckBox(panel, label = 'Add Revision Number')
		revisionCheckButton.SetFont(font)
		hboxCheckBoxes.Add(revisionCheckButton)
		cleanPDFNamedCheckButton = wx.CheckBox(panel, label = 'Clear PDF names')
		cleanPDFNamedCheckButton.SetFont(font)
		hboxCheckBoxes.Add(cleanPDFNamedCheckButton, flag = wx.LEFT, border = 10)
		creatListCheckButton = wx.CheckBox(panel, label = 'Creat List of PDF')
		creatListCheckButton.SetFont(font)
		hboxCheckBoxes.Add(creatListCheckButton, flag = wx.LEFT, border = 10)
		vbox.Add(hboxCheckBoxes, flag = wx.LEFT, border = 10)

		vbox.Add((-1, 25))

		hboxButtons = wx.BoxSizer(wx.HORIZONTAL)
		startButton = wx.Button(panel, label = 'Start', size = (70, 30))
		hboxButtons.Add(startButton, flag = wx.ALIGN_BOTTOM | wx.LEFT, border = 10)
		vbox.Add(hboxButtons, proportion = 1, flag = wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.RIGHT , border = 10)

		vbox.Add((-1, 10))
		
		panel.SetSizer(vbox)

def main():
	app = wx.App()
	MainWindow(None, title = 'TET Estel v 0.6.145')

	app.MainLoop()

if __name__ == '__main__':
	main()
