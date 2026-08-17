from .get_message import Sim3TanksError
_VALVE_NAMES = ['Kp1', 'Kp2', 'Kp3', 'Ka', 'Kb', 'K13', 'K23', 'K1', 'K2', 'K3']
_VALVE_STATES = ['Open', 'Open', 'Closed', 'Closed', 'Closed', 'Open', 'Open', 'Closed', 'Closed', 'Open']

def default_operation_mode(valve_name: str=None):
    if valve_name is None:
        return dict(zip(_VALVE_NAMES, _VALVE_STATES))
    for name, val in zip(_VALVE_NAMES, _VALVE_STATES):
        if name.lower() == valve_name.lower():
            return val
    raise Sim3TanksError('ERR003')
