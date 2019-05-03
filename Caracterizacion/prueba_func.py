# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 19:32:14 2019

@author: Emanuel
"""

import numpy as np
import sounddevice as sd
import visa
import matplotlib.pyplot as plt
import time
#from lantz import MessageBasedDriver, Q_
#from lantz.core import Feat
#from lantz.core import mfeats

from interfaz_caracterizacion_ui import *
from abrir_dispositivo_extendido import *
import Funciones_dispositivos as fd
from PyQt5.QtWidgets import QMessageBox
#import design
class OpenDeviceWindow(QtWidgets.QDialog,Ui_Dialog):     
    def __init__(self,*args,**kwargs):
        QtWidgets.QDialog.__init__(self,*args,**kwargs)
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.aceptar)
        self.buttonBox.rejected.connect(self.rechazar)
 #       self.TreeWidget.itemClicked.connect()
     #   self.seleccion = self.listWidget.currentItem()
        

    def aceptar(self):
       # print("este botón funciona")
        self.seleccion = self.TreeWidget.currentItem()
       # print(self.seleccion)
       # print(self.seleccion is None)
        return self.seleccion


    def rechazar(self):
        msg=QMessageBox.about(self, "Información", "Proceso cancelado por el usuario")
        #msg.setIcon(QMessageBox.Information)
        self.seleccion = None
        return self.seleccion
 
       
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,*args,**kwargs):
        QtWidgets.QMainWindow.__init__(self,*args,**kwargs)
        self.setupUi(self)
        self.Axis.setStyleSheet("background-color:white;");
        self.Axis.canvas.ax.set_xlabel('Frequency [Hz]')  
        self.Axis.canvas.ax.set_ylabel('Amplitude [dB]')
        self.Axis.canvas.ax.set_position([0.185,0.145,0.73,0.8], which='both')
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
        self.SaveDataPushButton.setEnabled(False)
        self.SaveImagePushButton.setEnabled(False)        
        self.rm = visa.ResourceManager()
       # self.amplitude=[]
        
        #Proceso para abrir el generador
        self.OpGenPushButton.clicked.connect(lambda:self.Open_generator())
        self.OpGenPushButton.clicked.connect(lambda:self.WaveFComboBox.setEnabled(True))
        self.OpGenPushButton.clicked.connect(lambda:self.AmplSpinBox.setEnabled(True))
        self.OpGenPushButton.clicked.connect(lambda:self.FreqSpinBox.setEnabled(True))
     
        #Proceso para abrir el detector
        self.OpDetPushButton.clicked.connect(lambda:self.Open_detector()) 
        self.OpDetPushButton.clicked.connect(lambda:self.HorScaleSpinBox.setEnabled(True))
        self.OpDetPushButton.clicked.connect(lambda:self.VerScaleSpinBox.setEnabled(True))
        
       
        
        # Se captura el valor de los parametros ingresados
        self.AmplSpinBox.valueChanged.connect(lambda:self.Set_value('Amplitude','AmplSpinBox'))
        self.FreqSpinBox.valueChanged.connect(lambda:self.Set_value('Frequency','FreqSpinBox'))
        self.MaxFreqSpinBox.valueChanged.connect(lambda:self.Set_value('MaxFrequency','MaxFreqSpinBox'))
        self.MinFreqSpinBox.valueChanged.connect(lambda:self.Set_value('MinFrequency','MinFreqSpinBox'))
        self.NumFreqSpinBox.valueChanged.connect(lambda:self.Set_value('NumFrequency','NumFreqSpinBox'))
        self.HorScaleSpinBox.valueChanged.connect(lambda:self.Set_value('HorScale','HorScaleSpinBox'))
        self.VerScaleSpinBox.valueChanged.connect(lambda:self.Set_value('VerScale','VerScaleSpinBox'))
        
        
        #self.MeasurePushButton.clicked.connect(lambda:print(self.ventana.seleccion.text()))
        
        self.MeasurePushButton.clicked.connect(lambda:self.Measure_Signal())
        
        self.SaveDataPushButton.clicked.connect(lambda:self.plot_data)
        self.SaveDataPushButton.clicked.connect(lambda:print(self.Amplitude))
        self.SaveDataPushButton.clicked.connect(lambda:print(self.Frequency))
        self.SaveDataPushButton.clicked.connect(lambda:print(self.MaxFrequency))
        self.SaveDataPushButton.clicked.connect(lambda:print(self.MinFrequency))
        self.SaveDataPushButton.clicked.connect(lambda:print(self.NumFrequency))
        self.SaveDataPushButton.clicked.connect(lambda:print(self.HorScale))
        self.SaveDataPushButton.clicked.connect(lambda:print(self.VerScale))        #self.SaveDataPushButton.clicked.connect(lambda:print(type(self.Axis))) 

    def plot_data(self,x,y):
        
        self.Axis.canvas.ax.clear()
        self.Axis.canvas.ax.set_xlabel('Frequency [Hz]')  
        self.Axis.canvas.ax.set_ylabel('Amplitude [dB]')          
        self.Axis.canvas.ax.plot(y)
        self.Axis.canvas.draw()
    
    def Set_value(self,parametro,widget):
        exec('self.'+str(parametro)+' = float(self.'+str(widget)+'.value())')
        return exec('self.'+str(parametro))    
           
    def Get_device_ID(self):
        self.ventana = OpenDeviceWindow()
        # Para obtener el ID lo que en realidad haremos es llamar al 
        # resource manager de VISA y fraccionar su contenido en pedazos.
        USBdevices =  QtWidgets.QTreeWidgetItem(self.ventana.TreeWidget)
        USBdevices.setText(0, str("USB devices"))
        ID=self.rm.list_resources()
        for i in ID:
            QtWidgets.QTreeWidgetItem(USBdevices).setText(0, str(i))
          #  print(ID)
 
        devices = sd.query_devices()
        
        PlacaAudio =  QtWidgets.QTreeWidgetItem(self.ventana.TreeWidget)
        PlacaAudio.setText(0, str("Audio Board"))
        AudioDeviceList = {}
        for i in range(len(devices)):
          #  print(devices[i]['name']) 
            QtWidgets.QTreeWidgetItem(PlacaAudio).setText(0, str(devices[i]['name']))
            AudioDeviceList[devices[i]['name']]=i
        self.audiodevices = AudioDeviceList.copy()    
        
      #  print(AudioDeviceList)
        self.ventana.show()
        self.ventana.exec_()
      #  print("veamos qué onda")
        if self.ventana.seleccion is None:
            print("No hay valores asignados")
        else:
        #    print(self.ventana.seleccion.text(0))
         #   print(self.ventana.seleccion.parent().text(0))
            return self.ventana.seleccion.parent().text(0),self.ventana.seleccion.text(0)
    
        
    def Open_generator(self):
        GenType,GenID = self.Get_device_ID()
     #   print(GenID)
     #   print(GenType)
        if GenID is None:
            print("Proceso cancelado por el usuario")
        else:
            
            self.GeneradorData = [GenType, GenID]
            if GenType == 'Audio Board':                
               sd.default.device = [sd.default.device[0],self.audiodevices[GenID]]
            else:
               self.Generador = fd.Generador(GenID)
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
        DetType,DetID = self.Get_device_ID()
        
        if DetID is None:
            print("Proceso cancelado por el usuario")
        else:
            self.DetectorData = [DetType, DetID]
            if DetType == 'Audio Board':
               sd.default.device = [self.audiodevices[DetID],sd.default.device[1]]
            else:
               self.Detector = fd.Osciloscopio(DetID)
        
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
        if self.GeneradorData[0] =='Audio Board' and self.DetectorData[0] =='Audio Board':
           myarray = np.sin(np.linspace(0., 12000., 2*44100))
           myarray1 = np.linspace(0., 12000., 2*44100)
           fs = 11025*self.Frequency
           sd.default.samplerate=fs
           myrecording = sd.playrec(myarray, channels=2,blocking=True)
           a =myrecording.shape
           mr1=myrecording.reshape((a[1],a[0]))
           self.plot_data(myarray1,mr1[0])
        else:
            print('funciones no instaladas aún, disculpe')
        


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec_()
    
    
    