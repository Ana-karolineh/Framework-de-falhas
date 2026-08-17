from .get_message import Sim3TanksError
_PARAM_NAMES = ['TankRadius', 'TankHeight', 'PipeRadius', 'TransPipeHeight', 'CorrectionTerm', 'GravityConstant', 'PumpMinFlow', 'PumpMaxFlow']
_PARAM_VALUES = [5, 50, 0.6, 30, 1, 981, 0, 120]

def default_physical_param(param_name: str=None):
    if param_name is None:
        return dict(zip(_PARAM_NAMES, _PARAM_VALUES))
    for name, val in zip(_PARAM_NAMES, _PARAM_VALUES):
        if name.lower() == param_name.lower():
            return val
    raise Sim3TanksError('ERR003')
