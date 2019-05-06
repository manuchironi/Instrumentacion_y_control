# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

import numpy as np
import visa
import matplotlib.pyplot as plt
import time
from lantz import MessageBasedDriver, Q_
from lantz.core import Feat
from lantz.core import mfeats


def sweepe(gener, osci, init_freq = 100, end_freq = 10100, cant_med = 100):
    with osci as osciloscopio, gener as generador:
        paso = np.floor(np.divide(end_freq - init_freq,cant_med))
        values = np.zeros(cant_med)
        freqs = np.add(np.multiply(np.arange(cant_med), paso), init_freq)
        for i,freq in enumerate(freqs):
            periodo = np.divide(1,freq)
            osciloscopio.timebase = 0.1*periodo*4*ureg.seconds 
        # Escribir Generador
            generador.frequency= freq*ureg.hertz
        # Esperamos a que se setee y lea bien
            time.sleep(1)
        # Consulta Osciloscopio
        #osci.obj_visa.write('MEASUrement:IMMed:TYPE PK2pk')
            values[i] = osciloscopio.vpp()#float(osci.obj_visa.query('MEASUREMENT:IMMed:VALue?'))
        return freqs, values

class Generador(MessageBasedDriver):
#    def __init__(self,ID):
#        self.obj_visa=rm.open_resource(ID)
#        self.ID = ID
    set_query = MessageBasedDriver.write
    # Feats punciona como un property, pero ademas acepta otras opciones
    @Feat()
    def idn(self):
        return self.query('*IDN?')

    # La idea es no usar sets and gets como metodos, sino definir propiedades
        
    frequency = mfeats.QuantityFeat('SOURce1:FREQuency:FIXed?','SOURce1:FREQuency:FIXed {}',units='Hz',limits=(0.0,1000000))
    amplitude = mfeats.QuantityFeat('SOURce1:VOLT:LEV:IMM:AMPL?','SOURce1:VOLT:LEV:IMM:AMPL {}',units='V',limits=(0.2,5))
        
    def setWaveform(self,waveform ='Senoidal'):
        switcher = {'Senoidal':"SIN",'Cuadrada':"SQU",'Pulso':"PULS"}
        self.write("SOURce1:FUNCtion "+switcher.get(waveform,'Senoidal'))  

        
class Osciloscopio(MessageBasedDriver):

    set_query = MessageBasedDriver.write
    
    @Feat()
    def idn(self):
        return self.query('*IDN?')

    timebase = mfeats.QuantityFeat('HORizontal:MAIN:SCALe?','HORizontal:MAIN:SCALe {}',units='s')
    vertical_scale = mfeats.QuantityFeat('CH1:SCA?','CH1:SCA {}',units='V')

    def vpp(self):
        osci.write('MEASUrement:IMMed:TYPE PK2pk')
        return float(osci.query('MEASUREMENT:IMMed:VALue?'))
        
  #  @Feat()
    def capturaPantalla(self):
 #       if self.parameters is None:
        YOFF_in_dl = float(self.query("WFMP:YOFF?"))
        YZERO_in_YUNits = float(self.query("WFMP:YZERO?"))
        YMUlt = float(self.query("WFMP:YMULT?"))
        print(YOFF_in_dl,YZERO_in_YUNits,YMUlt)
     #   self.parameters = (YOFF_in_dl,YZERO_in_YUNits,YMUlt)
      #  (YOFF_in_dl , YZERO_in_YUNits , YMUlt) = self.parameters
        curve_in_dl = np.array(self.query_binary_values('CURV?', datatype='b', is_big_endian=True))
        valores = ((curve_in_dl - YOFF_in_dl)*YMUlt)+YZERO_in_YUNits
        intervalo = float(osci.query('WFMPre:XINcr?'))
        tiempos = np.arange(len(valores))*intervalo
        return tiempos, valores