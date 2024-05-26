# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:29:40 2024

@author: Guilherme Sobral
"""

import PySimpleGUI as sg

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
