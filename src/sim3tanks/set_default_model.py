from funcoes_aux.check_operation_mode import check_operation_mode
from funcoes_aux.default_operation_mode import default_operation_mode
from funcoes_aux.default_physical_param import default_physical_param

def set_default_model(self):
    from .sim3tanks import Sim3Tanks
    LIST_OF_VALVES = Sim3Tanks.LIST_OF_VALVES
    LIST_OF_FAULTS = Sim3Tanks.LIST_OF_FAULTS
    LIST_OF_PARAM = Sim3Tanks.LIST_OF_PARAM
    Nx = len(Sim3Tanks.LIST_OF_STATES)
    Nq = len(Sim3Tanks.LIST_OF_FLOWS)
    D = default_physical_param()
    for p in LIST_OF_PARAM:
        setattr(self.Model.PhysicalParam, p, D[p])
    D = default_operation_mode()
    for v in LIST_OF_VALVES:
        getattr(self.Model.ValveSettings, v).OperationMode = D[v]
    K, _ = check_operation_mode(self)
    for i, v in enumerate(LIST_OF_VALVES):
        valve = getattr(self.Model.ValveSettings, v)
        valve.EnableControl = False
        valve.OpeningRate = float(K[i])
    getattr(self.Model.ValveSettings, LIST_OF_VALVES[0]).EnableControl = True
    getattr(self.Model.ValveSettings, LIST_OF_VALVES[1]).EnableControl = True
    for f in LIST_OF_FAULTS:
        fault = getattr(self.Model.FaultSettings, f)
        fault.EnableSignal = False
        fault.Magnitude = 0.0
    for f in LIST_OF_FAULTS[10:]:
        fault = getattr(self.Model.FaultSettings, f)
        fault.Offset = 0.0
    self.Model.ProcessNoise.EnableSignal = False
    self.Model.ProcessNoise.Magnitude = [0.0] * Nx
    self.Model.MeasurementNoise.EnableSignal = False
    self.Model.MeasurementNoise.Magnitude = [0.0] * (Nx + Nq)
    self.Model.InitialCondition = [40.0, 25.0, 20.0]
    self.clearVariables()
