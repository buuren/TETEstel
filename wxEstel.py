#!/usr/bin/python
#_*_ coding: utf-8 _*_

import wx

class MainWindow(wx.Frame):
	"""docstring for MainWindow"""
	def __init__(self, parent, title):
		super(MainWindow, self).__init__(parent, title = title)
		
		self.Centre()
		self.Show()

def main():
	app = wx.App()
	MainWindow(None, title = 'TET Estel v.0.1')

	app.MainLoop()

if __name__ == '__main__':
	main()
