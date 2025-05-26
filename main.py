from brian2 import *

# Parâmetros do modelo HH (baseados no arquivo de configuração)
deli = 15.0 * ms
vna = 115.0 * mV
vk = -12.0 * mV
vl = 10.6 * mV
gnabar = 36.0 * msiemens/cm**2
gkbar = 12.0 * msiemens/cm**2
gl = 0.1 * msiemens/cm**2
h0 = 0.8

# Equações do modelo HH
hh_equations = '''
dv/dt = (gl*(vl-v) + gnabar*m**3*h*(vna-v) + gkbar*n**4*(vk-v) + I_syn)/C : volt
dm/dt = alpham*(1-m) - betam*m : 1
dh/dt = alphah*(1-h) - betah*h : 1
dn/dt = alphan*(1-n) - betan*n : 1

alpham = 0.1*(v/mV+40)/(1-exp(-(v/mV+40)/10))/ms : Hz
betam = 4*exp(-(v/mV+65)/18)/ms : Hz
alphah = 0.07*exp(-(v/mV+65)/20)/ms : Hz
betah = 1/(1+exp(-(v/mV+35)/10))/ms : Hz
alphan = 0.01*(v/mV+55)/(1-exp(-(v/mV+55)/10))/ms : Hz
betan = 0.125*exp(-(v/mV+65)/80)/ms : Hz

I_syn : amp/meter**2
C : farad/meter**2
'''
