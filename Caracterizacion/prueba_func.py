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
        print("este botón funciona")
        self.seleccion = self.TreeWidget.currentItem()
        print(self.seleccion)
        print(self.seleccion is None)
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
        self.rm = visa.ResourceManager()
        
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
        self.AmplSpinBox.valueChanged.connect(lambda:self.Generador.setAmplitude(float(self.AmplSpinBox.value())))
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
            print(devices[i]['name']) 
            QtWidgets.QTreeWidgetItem(PlacaAudio).setText(0, str(devices[i]['name']))
            AudioDeviceList[devices[i]['name']]=i
        self.audiodevices = AudioDeviceList.copy()    
        
        print(AudioDeviceList)
        self.ventana.show()
        self.ventana.exec_()
        print("veamos qué onda")
        if self.ventana.seleccion is None:
            print("No hay valores asignados")
        else:
            print(self.ventana.seleccion.text(0))
            print(self.ventana.seleccion.parent().text(0))
            return self.ventana.seleccion.parent().text(0),self.ventana.seleccion.text(0)
    
        
    def Open_generator(self):
        GenType,GenID = self.Get_device_ID()
        print(GenID)
        print(GenType)
        if GenID is None:
            print("Proceso cancelado por el usuario")
        elif GenType == 'Audio Board':
            sd.default.device = [sd.default.device[0],self.audiodevices[GenID]]
            print(self.audiodevices[GenID])
        else:
              self.Generador = Generador(GenID)
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
        elif DetType == 'Audio Board':
            sd.default.device = [self.audiodevices[DetID],sd.default.device[0]]
            print(self.audiodevices[DetID])
        else:
            self.Detector = Osciloscopio(DetID)
        
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
    
class Generador():
    def __init__(self,ID):
        self.obj_visa=self.rm
        self.ID = ID
         
    def setFrequency(self,freq):
        self.obj_visa.write("SOURce1:FREQuency:FIXed "+str(freq))
        
    def setAmplitude(self,amp):
        self.obj_visa.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude "+str(amp))
        
    def setWaveform(self,waveform ='Senoidal'):
        switcher = {'Senoidal':"SIN",'Cuadrada':"SQU",'Pulso':"PULS"}
        self.obj_visa.write("SOURce1:FUNCtion "+switcher.get(waveform,'Senoidal'))  

        
class Osciloscopio():

    def __init__(self,ID):
        self.obj_visa=rm.open_resource(ID)
        self.ID = ID
        self.parameters = None
        
    def setBaseTime(self,scale):
        self.obj_visa.write('HORizontal:MAIN:SCALe '+str(scale))
       # self.obj_visa.write('HORizontal:DELay:SCALe {}'.format(scale))
 
    def capturaPantalla(self):
        if self.parameters is None:
            YOFF_in_dl = float(self.obj_visa.query("WFMP:YOFF?"))
            YZERO_in_YUNits = float(self.obj_visa.query("WFMP:YZERO?"))
            YMUlt = float(self.obj_visa.query("WFMP:YMULT?"))
            self.parameters = (YOFF_in_dl,YZERO_in_YUNits,YMUlt)
        (YOFF_in_dl , YZERO_in_YUNits , YMUlt) = self.parameters
        curve_in_dl = np.array(self.obj_visa.query_binary_values('CURV?', datatype='b', is_big_endian=True))
        valores = ((curve_in_dl - YOFF_in_dl)*YMUlt)+YZERO_in_YUNits
        intervalo = float(osci.obj_visa.query('WFMPre:XINcr?'))
        tiempos = np.arange(len(valores))*intervalo
        return tiempos, valores        
 
def sweepe(generador, osciloscopio, init_freq = 100, end_freq = 10100, cant_med = 100):
    paso = np.floor(np.divide(end_freq - init_freq,cant_med))
    values = np.zeros(cant_med)
    freqs = np.add(np.multiply(np.arange(cant_med), paso), init_freq)
    for i,freq in enumerate(freqs):
        periodo = np.divide(1,freq)
        osciloscopio.setBaseTime(0.1*periodo*4)
        # Escribir Generador
        generador.setFrequency(freq)
        # Esperamos a que se setee y lea bien
        time.sleep(1)
        # Consulta Osciloscopio
        osci.obj_visa.write('MEASUrement:IMMed:TYPE PK2pk')
        values[i] = float(osci.obj_visa.query('MEASUREMENT:IMMed:VALue?'))
    return freqs, values       
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec_()
    
    
    