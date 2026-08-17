import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib.pyplot as plt
from funcoes_aux.create_sim3tanks import create_sim3tanks

tstart, tstop, Ts = (0, 200, 0.1)
time = np.arange(tstart, tstop + Ts, Ts)
N = len(time)

tts = create_sim3tanks()
tts.setDefaultModel()

tts.Model.PhysicalParam.TankRadius = 5
tts.Model.PhysicalParam.TankHeight = 50
tts.Model.PhysicalParam.PipeRadius = 0.6
tts.Model.PhysicalParam.TransPipeHeight = 30
tts.Model.PhysicalParam.CorrectionTerm = 1
tts.Model.PhysicalParam.GravityConstant = 981
tts.Model.PhysicalParam.PumpMinFlow = 0
tts.Model.PhysicalParam.PumpMaxFlow = 120
tts.Model.InitialCondition = [40, 25, 20]

tts.Model.ValveSettings.Kp1.EnableControl = False
tts.Model.ValveSettings.Kp2.EnableControl = False
tts.Model.ValveSettings.Kp3.OperationMode = 'Closed'
tts.Model.ValveSettings.Kp3.EnableControl = False

Qp1 = 80 * np.ones(N)
Qp2 = 80 * np.ones(N)
Qp3 = 80 * np.ones(N)

tts.Model.FaultSettings.f1.EnableSignal = False
tts.Model.FaultSettings.f1.Magnitude = 0.0

tts.Model.FaultSettings.f2.EnableSignal = False
tts.Model.FaultSettings.f2.Magnitude = 0.0

tts.Model.FaultSettings.f3.EnableSignal = False
tts.Model.FaultSettings.f3.Magnitude = 0.0

tts.Model.FaultSettings.f4.EnableSignal = False
tts.Model.FaultSettings.f4.Magnitude = 0.0

tts.Model.FaultSettings.f5.EnableSignal = False
tts.Model.FaultSettings.f5.Magnitude = 0.0

tts.Model.FaultSettings.f6.EnableSignal = False
tts.Model.FaultSettings.f6.Magnitude = 0.0

tts.Model.FaultSettings.f7.EnableSignal = False
tts.Model.FaultSettings.f7.Magnitude = 0.0

tts.Model.FaultSettings.f8.EnableSignal = False
tts.Model.FaultSettings.f8.Magnitude = 0.0

tts.Model.FaultSettings.f9.EnableSignal = False
tts.Model.FaultSettings.f9.Magnitude = 0.0

tts.Model.FaultSettings.f10.EnableSignal = False
tts.Model.FaultSettings.f10.Magnitude = 0.0

tts.Model.FaultSettings.f11.EnableSignal = False
tts.Model.FaultSettings.f11.Magnitude = 0.0
tts.Model.FaultSettings.f11.Offset = 0.0

tts.Model.FaultSettings.f12.EnableSignal = False
tts.Model.FaultSettings.f12.Magnitude = 0.0
tts.Model.FaultSettings.f12.Offset = 0.0

tts.Model.FaultSettings.f13.EnableSignal = False
tts.Model.FaultSettings.f13.Magnitude = 0.0
tts.Model.FaultSettings.f13.Offset = 0.0

tts.Model.FaultSettings.f14.EnableSignal = False
tts.Model.FaultSettings.f14.Magnitude = 0.0
tts.Model.FaultSettings.f14.Offset = 0.0

tts.Model.FaultSettings.f15.EnableSignal = False
tts.Model.FaultSettings.f15.Magnitude = 0.0
tts.Model.FaultSettings.f15.Offset = 0.0

tts.Model.FaultSettings.f16.EnableSignal = False
tts.Model.FaultSettings.f16.Magnitude = 0.0
tts.Model.FaultSettings.f16.Offset = 0.0

tts.Model.FaultSettings.f17.EnableSignal = False
tts.Model.FaultSettings.f17.Magnitude = 0.0
tts.Model.FaultSettings.f17.Offset = 0.0

tts.Model.FaultSettings.f18.EnableSignal = False
tts.Model.FaultSettings.f18.Magnitude = 0.0
tts.Model.FaultSettings.f18.Offset = 0.0

tts.Model.FaultSettings.f19.EnableSignal = False
tts.Model.FaultSettings.f19.Magnitude = 0.0
tts.Model.FaultSettings.f19.Offset = 0.0

tts.Model.FaultSettings.f20.EnableSignal = False
tts.Model.FaultSettings.f20.Magnitude = 0.0
tts.Model.FaultSettings.f20.Offset = 0.0

tts.Model.FaultSettings.f21.EnableSignal = False
tts.Model.FaultSettings.f21.Magnitude = 0.0
tts.Model.FaultSettings.f21.Offset = 0.0

tts.Model.FaultSettings.f22.EnableSignal = False
tts.Model.FaultSettings.f22.Magnitude = 0.0
tts.Model.FaultSettings.f22.Offset = 0.0

tts.Model.FaultSettings.f23.EnableSignal = False
tts.Model.FaultSettings.f23.Magnitude = 0.0
tts.Model.FaultSettings.f23.Offset = 0.0

tts.Model.ProcessNoise.EnableSignal = False
tts.Model.MeasurementNoise.EnableSignal = False

print(f'Simulando {N} passos...')
for k in range(1, N):
    if k % 200 == 0:
        print(f'  {k}/{N - 1}')
    tts.simulateModel(Qp1=Qp1[k], Qp2=Qp2[k], Qp3=Qp3[k], Tspan=Ts, all_steps=True)
print('Simulação concluída!\n')

X = tts.getStateVariables()
Q = tts.getFlowVariables()
Y = tts.getSensorMeasurements()
K = tts.getValveSignals()
F = tts.getFaultMagnitudes()
O = tts.getFaultOffsets()

tts.displayModel()

print('\nPlotting Graphs...')
tts.plotLevels()
tts.plotFlows()
tts.plotValves()
tts.plotFaultMagnitudes()
tts.plotFaultOffsets()
plt.show()