import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')
import traceback
import numpy as np
import matplotlib.pyplot as plt
from funcoes_aux.create_sim3tanks import create_sim3tanks
OUT_DIR = 'plots'
os.makedirs(OUT_DIR, exist_ok=True)

def save_current_figure(name):
    path = os.path.join(OUT_DIR, f'{name}.png')
    try:
        plt.savefig(path, dpi=120, bbox_inches='tight')
        plt.close('all')
        size = os.path.getsize(path)
        if size == 0:
            print(f'[AVISO] {path} foi criado mas está vazio (0 KB)!')
        else:
            print(f'[OK] {path} ({size / 1024:.1f} KB)')
    except Exception:
        print(f'[ERRO] Falha ao salvar {path}:')
        traceback.print_exc()
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
rng = np.random.default_rng(42)
third = N // 3
d = np.zeros(N)
d[third:2 * third] = 0.5 + rng.normal(0, 0.1, size=2 * third - third)
Qp1 = 80 * np.ones(N)
Qp2 = 80 * np.ones(N)
Qp3 = 80 * np.ones(N)
tts.Model.FaultSettings.f1.EnableSignal = True
quarter = N // 4
idx1 = np.arange(-2 * quarter, 2 * quarter)
f1 = 1 / (1 + np.exp(-(1 / time[quarter]) * idx1))
f1 = np.pad(f1, (0, max(0, N - len(f1))), mode='edge')[:N]
tts.Model.FaultSettings.f2.EnableSignal = False
idx2 = np.arange(-3 * quarter, 1 * quarter)
f2 = 1 / (1 + np.exp(-(1 / time[quarter]) * idx2))
f2 = np.pad(f2, (0, max(0, N - len(f2))), mode='edge')[:N]
print(f'Simulando {N} passos...')
for k in range(1, N):
    if k % 200 == 0:
        print(f'  {k}/{N - 1}')
    u = rng.random(2)
    tts.Model.ValveSettings.Kp1.OpeningRate = float(u[0])
    tts.Model.ValveSettings.Kp2.OpeningRate = float(u[1])
    tts.Model.ValveSettings.Kp3.OpeningRate = float(d[k])
    tts.Model.FaultSettings.f1.Magnitude = float(np.clip(f1[k], 0, 1))
    tts.Model.FaultSettings.f2.Magnitude = float(np.clip(f2[k], 0, 1))
    tts.Model.ProcessNoise.EnableSignal = False
    tts.Model.ProcessNoise.Magnitude = rng.normal(0, 0.2, 3).tolist()
    tts.Model.MeasurementNoise.EnableSignal = True
    yx = rng.normal(0, 0.5, 3)
    yq = rng.normal(0, 2.5, 10)
    tts.Model.MeasurementNoise.Magnitude = np.concatenate([yx, yq]).tolist()
    tts.simulateModel(Qp1=Qp1[k], Qp2=Qp2[k], Qp3=Qp3[k], Tspan=Ts, all_steps=True)
print('Simulação concluída.\n')
print('Gerando gráficos...')
tts.plotLevels()
save_current_figure('01_levels_all')
tts.plotLevels('h1')
save_current_figure('02_level_h1')
tts.plotFlows()
save_current_figure('03_flows_all')
tts.plotFlows('Q3')
save_current_figure('04_flow_Q3')
tts.plotValves()
save_current_figure('05_valves_all')
tts.plotValves('Kp1')
save_current_figure('06_valve_Kp1')
tts.plotFaultMagnitudes()
save_current_figure('07_fault_mag_all')
tts.plotFaultMagnitudes('f1')
save_current_figure('08_fault_mag_f1')
tts.plotFaultOffsets()
save_current_figure('09_fault_offset_all')
tts.plotFaultOffsets('f11')
save_current_figure('10_fault_offset_f11')
print("\nPronto! Confira a pasta 'plots/'.")
