import numpy as np
from funcoes_aux.get_message import Sim3TanksError

class Struct:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        fields = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items()))
        return f'Struct({fields})'

class Sim3Tanks:
    LIST_OF_FIELDS = ['PhysicalParam', 'ValveSettings', 'FaultSettings', 'ProcessNoise', 'MeasurementNoise', 'InitialCondition']
    LIST_OF_PARAM = ['TankRadius', 'TankHeight', 'PipeRadius', 'TransPipeHeight', 'CorrectionTerm', 'GravityConstant', 'PumpMinFlow', 'PumpMaxFlow']
    LIST_OF_VALVES = ['Kp1', 'Kp2', 'Kp3', 'Ka', 'Kb', 'K13', 'K23', 'K1', 'K2', 'K3']
    LIST_OF_FAULTS = [f'f{i}' for i in range(1, 24)]
    LIST_OF_STATES = ['h1', 'h2', 'h3']
    LIST_OF_FLOWS = ['Q1in', 'Q2in', 'Q3in', 'Qa', 'Qb', 'Q13', 'Q23', 'Q1', 'Q2', 'Q3']

    def __init__(self):
        self._SimulationTime = np.empty((0,))
        self._StateVariables = np.empty((0, 0))
        self._FlowVariables = np.empty((0, 0))
        self._SensorMeasurements = np.empty((0, 0))
        self._ValveSignals = np.empty((0, 0))
        self._FaultMagnitudes = np.empty((0, 0))
        self._FaultOffsets = np.empty((0, 0))
        self.About = Struct()
        self.Model = None
        self.prepareModel()

    def prepareModel(self):
        model = Struct()
        phys = Struct()
        for p in self.LIST_OF_PARAM:
            setattr(phys, p, None)
        setattr(model, self.LIST_OF_FIELDS[0], phys)
        valves = Struct()
        for v in self.LIST_OF_VALVES:
            vs = Struct(OperationMode='Closed', EnableControl=False, OpeningRate=None)
            setattr(valves, v, vs)
        setattr(model, self.LIST_OF_FIELDS[1], valves)
        faults = Struct()
        for i, f in enumerate(self.LIST_OF_FAULTS):
            fs = Struct(EnableSignal=False, Magnitude=None)
            if i >= 10:
                fs.Offset = None
            setattr(faults, f, fs)
        setattr(model, self.LIST_OF_FIELDS[2], faults)
        setattr(model, self.LIST_OF_FIELDS[3], Struct(EnableSignal=False, Magnitude=None))
        setattr(model, self.LIST_OF_FIELDS[4], Struct(EnableSignal=False, Magnitude=None))
        setattr(model, self.LIST_OF_FIELDS[5], None)
        self.Model = model
        self._SimulationTime = np.array([0.0])

    def _set_internal_state_variables(self, x):
        N = len(self.LIST_OF_STATES)
        x = np.asarray(x, dtype=float) if x is not None and len(x) else np.empty((0,))
        if x.size and x.size != N:
            raise Sim3TanksError('ERR006', f'The system has {N} state variables.')
        self._StateVariables = x

    def _set_internal_flow_variables(self, q):
        N = len(self.LIST_OF_FLOWS)
        q = np.asarray(q, dtype=float) if q is not None and len(q) else np.empty((0,))
        if q.size and q.size != N:
            raise Sim3TanksError('ERR006', f'The system has {N} flow variables.')
        self._FlowVariables = q

    def _set_internal_sensor_measurements(self, y):
        N = len(self.LIST_OF_STATES) + len(self.LIST_OF_FLOWS)
        y = np.asarray(y, dtype=float) if y is not None and len(y) else np.empty((0,))
        if y.size and y.size != N:
            raise Sim3TanksError('ERR006', f'The system has {N} measured variables.')
        self._SensorMeasurements = y

    def _set_internal_valve_signals(self, v):
        N = len(self.LIST_OF_VALVES)
        v = np.asarray(v, dtype=float) if v is not None and len(v) else np.empty((0,))
        if v.size and v.size != N:
            raise Sim3TanksError('ERR006', f'The system has {N} valves.')
        self._ValveSignals = v

    def _set_internal_fault_magnitudes(self, f):
        N = len(self.LIST_OF_FAULTS)
        f = np.asarray(f, dtype=float) if f is not None and len(f) else np.empty((0,))
        if f.size and f.size != N:
            raise Sim3TanksError('ERR006', f'The system has {N} fault magnitudes.')
        self._FaultMagnitudes = f

    def _set_internal_fault_offsets(self, f):
        N = len(self.LIST_OF_FAULTS) - 10
        f = np.asarray(f, dtype=float) if f is not None and len(f) else np.empty((0,))
        if f.size and f.size != N:
            raise Sim3TanksError('ERR006', f'The system has {N} fault offsets.')
        self._FaultOffsets = f

    def _push_internal_state_variables(self, x):
        N = len(self.LIST_OF_STATES)
        x = np.asarray(x, dtype=float).reshape(1, -1)
        if x.shape[1] != N:
            raise Sim3TanksError('ERR006', f'The system has {N} state variables.')
        self._StateVariables = x if self._StateVariables.size == 0 else np.vstack([self._StateVariables, x])

    def _push_internal_flow_variables(self, q):
        N = len(self.LIST_OF_FLOWS)
        q = np.asarray(q, dtype=float).reshape(1, -1)
        if q.shape[1] != N:
            raise Sim3TanksError('ERR006', f'The system has {N} flow variables.')
        self._FlowVariables = q if self._FlowVariables.size == 0 else np.vstack([self._FlowVariables, q])

    def _push_internal_sensor_measurements(self, y):
        N = len(self.LIST_OF_STATES) + len(self.LIST_OF_FLOWS)
        y = np.asarray(y, dtype=float).reshape(1, -1)
        if y.shape[1] != N:
            raise Sim3TanksError('ERR006', f'The system has {N} measured variables.')
        self._SensorMeasurements = y if self._SensorMeasurements.size == 0 else np.vstack([self._SensorMeasurements, y])

    def _push_internal_valve_signals(self, v):
        N = len(self.LIST_OF_VALVES)
        v = np.asarray(v, dtype=float).reshape(1, -1)
        if v.shape[1] != N:
            raise Sim3TanksError('ERR006', f'The system has {N} valves.')
        self._ValveSignals = v if self._ValveSignals.size == 0 else np.vstack([self._ValveSignals, v])

    def _push_internal_fault_magnitudes(self, f):
        N = len(self.LIST_OF_FAULTS)
        f = np.asarray(f, dtype=float).reshape(1, -1)
        if f.shape[1] != N:
            raise Sim3TanksError('ERR006', f'The system has {N} fault magnitudes.')
        self._FaultMagnitudes = f if self._FaultMagnitudes.size == 0 else np.vstack([self._FaultMagnitudes, f])

    def _push_internal_fault_offsets(self, f):
        N = len(self.LIST_OF_FAULTS) - 10
        f = np.asarray(f, dtype=float).reshape(1, -1)
        if f.shape[1] != N:
            raise Sim3TanksError('ERR006', f'The system has {N} fault offsets.')
        self._FaultOffsets = f if self._FaultOffsets.size == 0 else np.vstack([self._FaultOffsets, f])

    def _get_internal_state_variables(self):
        return self._StateVariables

    def _get_internal_flow_variables(self):
        return self._FlowVariables

    def _get_internal_sensor_measurements(self):
        return self._SensorMeasurements

    def _get_internal_valve_signals(self):
        return self._ValveSignals

    def _get_internal_fault_magnitudes(self):
        return self._FaultMagnitudes

    def _get_internal_fault_offsets(self):
        return self._FaultOffsets

    def _reset_internal_simulation_time(self):
        self._SimulationTime = np.array([0.0])

    def _increment_internal_simulation_time(self, time):
        self._SimulationTime = np.append(self._SimulationTime, time)

    def _get_internal_simulation_time(self, index=None):
        if index is None:
            return self._SimulationTime
        return self._SimulationTime[index]
from .simulate_model import simulate_model
from .set_default_model import set_default_model
from .clear_model import clear_model
from .clear_variables import clear_variables
from .display_model import display_model
from .get_state_variables import get_state_variables
from .get_flow_variables import get_flow_variables
from .get_sensor_measurements import get_sensor_measurements
from .get_valve_signals import get_valve_signals
from .get_fault_magnitudes import get_fault_magnitudes
from .get_fault_offsets import get_fault_offsets
from .get_default_linear_model import get_default_linear_model
from .plot_levels import plot_levels
from .plot_flows import plot_flows
from .plot_valves import plot_valves
from .plot_fault_magnitudes import plot_fault_magnitudes
from .plot_fault_offsets import plot_fault_offsets
Sim3Tanks.simulateModel = simulate_model
Sim3Tanks.setDefaultModel = set_default_model
Sim3Tanks.clearModel = clear_model
Sim3Tanks.clearVariables = clear_variables
Sim3Tanks.displayModel = display_model
Sim3Tanks.getStateVariables = get_state_variables
Sim3Tanks.getFlowVariables = get_flow_variables
Sim3Tanks.getSensorMeasurements = get_sensor_measurements
Sim3Tanks.getValveSignals = get_valve_signals
Sim3Tanks.getFaultMagnitudes = get_fault_magnitudes
Sim3Tanks.getFaultOffsets = get_fault_offsets
Sim3Tanks.getDefaultLinearModel = get_default_linear_model
Sim3Tanks.plotLevels = plot_levels
Sim3Tanks.plotFlows = plot_flows
Sim3Tanks.plotValves = plot_valves
Sim3Tanks.plotFaultMagnitudes = plot_fault_magnitudes
Sim3Tanks.plotFaultOffsets = plot_fault_offsets
