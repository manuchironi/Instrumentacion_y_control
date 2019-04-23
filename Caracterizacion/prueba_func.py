# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 19:32:14 2019

@author: Emanuel
"""

import numpy as np
#import visa
import matplotlib.pyplot as plt
import time
#from lantz import MessageBasedDriver, Q_
#from lantz.core import Feat
#from lantz.core import mfeats

from interfaz_caracterizacion_ui import *
from abrir_dispositivo_ui import *
from PyQt5.QtWidgets import QMessageBox
#import design
class OpenDeviceWindow(QtWidgets.QDialog,Ui_Dialog):     
    def __init__(self,*args,**kwargs):
        QtWidgets.QDialog.__init__(self,*args,**kwargs)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.aceptar)
        self.buttonBox.rejected.connect(self.rechazar)
     #   self.seleccion = self.listWidget.currentItem()
        

    def aceptar(self):
        print("este botón funciona")
        self.seleccion = self.listWidget.currentItem()
        return self.seleccion


    def rechazar(self):
        msg=QMessageBox.about(self, "Información", "Proceso cancelado por el usuario")
        msg.setIcon(QMessageBox.Information)
 
       
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,*args,**kwargs):
        QtWidgets.QMainWindow.__init__(self,*args,**kwargs)
        self.setupUi(self)
        self.Axis.setStyleSheet("background-color:white;");
        self.GIDLineEdit.setEnabled(False)
        self.WaveFComboBox.setEnabled(False)
        self.AmplSpinBox.setEnabled(False)
        self.FreqSpinBox.setEnabled(False)
        self.DIDLineEdit.setEnabled(False)
        self.HorScaleSpinBox.setEnabled(False)
        self.VerScaleSpinBox.setEnabled(False)
        self.label.setEnabled(False)
        self.label_2.setEnabled(False)
        self.label_6.setEnabled(False)
        self.label_7.setEnabled(False)
        self.label_8.setEnabled(False)
        self.label_9.setEnabled(False)
        self.label_10.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        
        #Proceso para abrir el generador
        self.OpGenPushButton.clicked.connect(lambda:self.Open_generator())
        self.OpGenPushButton.clicked.connect(lambda:self.WaveFComboBox.setEnabled(True))
        self.OpGenPushButton.clicked.connect(lambda:self.AmplSpinBox.setEnabled(True))
        self.OpGenPushButton.clicked.connect(lambda:self.FreqSpinBox.setEnabled(True))
        #Proceso para abrir el detector
        self.OpDetPushButton.clicked.connect(lambda:self.Open_detector()) 
        self.OpDetPushButton.clicked.connect(lambda:self.HorScaleSpinBox.setEnabled(True))
        self.OpDetPushButton.clicked.connect(lambda:self.VerScaleSpinBox.setEnabled(True))
        
        self.MeasurePushButton.clicked.connect(lambda:print(self.ventana.seleccion.text()))
        
        self.AmplSpinBox.valueChanged.connect(lambda:print(self.AmplSpinBox.value()))
        self.MaxFreqSpinBox.valueChanged.connect(lambda:print(self.MaxFreqSpinBox.value()))
        self.MinFreqSpinBox.valueChanged.connect(self.MinFreqSpinBox.value)
        self.NumFreqSpinBox.valueChanged.connect(self.NumFreqSpinBox.value)
        self.HorScaleSpinBox.valueChanged.connect(self.HorScaleSpinBox.value)
        self.VerScaleSpinBox.valueChanged.connect(self.VerScaleSpinBox.value)

        self.SaveDataPushButton.clicked.connect(self.plot_data)
        #self.SaveDataPushButton.clicked.connect(lambda:print(type(self.Axis))) 

    def plot_data(self):
        x=range(0, 10)
        y=range(0, 20, 2)
        self.Axis.canvas.ax.plot(x, y)
        self.Axis.canvas.draw()
        
           
    def Get_device_ID(self):
        self.ventana = OpenDeviceWindow()
        # Para obtener el ID lo que en realidad haremos es llamar al 
        # resource manager de VISA y fraccionar su contenido en pedazos.
        item1 = "Item 1 de prueba"
        self.ventana.listWidget.addItem(item1)
        item2 = "Item 2 de prueba"
        self.ventana.listWidget.addItem(item2)
        self.ventana.show()
        self.ventana.exec_()

        return self.ventana.seleccion.text()
        
    def Open_generator(self):
        GenID = self.Get_device_ID()

        # función para abrir el instrumento
        # Luego hacemos que aparezcan las características del detector en la
        # pantalla.
        self.label.setEnabled(True)
        self.label_2.setEnabled(True)
        self.label_9.setEnabled(True)
        self.label_10.setEnabled(True)
        self.GIDLineEdit.setEnabled(True)
        self.WaveFComboBox.setEnabled(True)
        self.AmplSpinBox.setEnabled(True)
        self.FreqSpinBox.setEnabled(True)
        self.GIDLineEdit.setPlaceholderText(GenID)
        self.GIDLineEdit.setStyleSheet("color: blue;")
        
    def Open_detector(self):
        DetID = self.Get_device_ID()
        
        self.label_6.setEnabled(True)
        self.label_7.setEnabled(True)
        self.label_8.setEnabled(True)
        self.groupBox_2.setEnabled(True)
        self.DIDLineEdit.setEnabled(True)
        self.HorScaleSpinBox.setEnabled(True)
        self.VerScaleSpinBox.setEnabled(True)
        
        self.DIDLineEdit.setPlaceholderText(DetID)    
        self.DIDLineEdit.setStyleSheet("color: blue;")

    def Measure_Signal(self):
        self.SaveDataPushButton.setEnabled(True)
        self.SaveImagePushButton.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec_()
    
    
    