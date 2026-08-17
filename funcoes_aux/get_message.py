_TAG = '#Sim3Tanks::'
_MESSAGES = {'ERR000': 'Unknown error.', 'ERR001': 'Not enough input arguments.', 'ERR002': 'Too many input arguments.', 'ERR003': 'Invalid input parameter.', 'ERR004': 'The input argument must be a Sim3Tanks object.', 'ERR005': 'The input argument must be a row vector.', 'ERR006': 'The dimensions are not consistent.', 'ERR007': 'The state variabels must be finite.', 'ERR008': 'The subfields of <PhysicalParam> must have real and finite values.', 'ERR009': "The field <OperationMode> must be set to 'Open' or 'Closed'.", 'ERR010': 'The field <EnableControl> must be set to a logical value (true or false).', 'ERR011': 'The field <EnableSignal> must be set to a logical value (true or false).', 'ERR012': 'The field <TankRadius> must be greater than 0.', 'ERR013': 'The field <TankHeight> must be greater than 0.', 'ERR014': 'The field <PipeRadius> must be greater than 0 and less than <TankRadius>.', 'ERR015': 'The field <TransPipeHeight> must be greater than 0 and less than <TankHeight>.', 'ERR016': 'The field <CorrectionTerm> must be greater than 0.', 'ERR017': 'The field <GravityConstant> must be greater than 0.', 'ERR018': 'The field <PumpMinFlow> must be greater than or equal to 0.', 'ERR019': 'The field <PumpMaxFlow> must be greater than or equal to <PumpMinFlow>.', 'ERR020': 'Invalid number of input arguments (must be even).', 'ERR021': 'Invalid number of input arguments (must be odd).', 'ERR022': 'The sensor fault offset value must be finite.', 'ERR023': 'The input argument must be a row or a column vector of numeric type.', 'ERR024': 'The initial condition must be a three-position row vector.', 'WARN001': 'The Magnitude of an enabled fault is set to empty, so zero is assumed as the default value.', 'WARN002': 'The Magnitude of an enabled fault is out of bounds [0,1], so its value is saturated.', 'WARN003': 'The OpeningRate of an enabled valve is set to empty, so OperationMode is assumed as the default value.', 'WARN004': 'The OpeningRate of an enabled valve is out of bounds [0,1], so its value is saturated.', 'WARN005': 'The ProcessNoise Magnitude is set to empty, so a row vector of zeros is assumed as the default value.', 'WARN006': 'The MeasurmentNoise Magnitude is set to empty, so a row vector of zeros is assumed as the default value.', 'WARN007': 'The Offset of a sensor fault is set to empty, so zero is assumed as the default value.', 'WARN008': 'There is no value to plot (the variable is empty).'}

def get_message(message_code: str) -> str:
    code = message_code.upper()
    msg = _MESSAGES.get(code, f'Code {code} not found!')
    return f'{_TAG}{code}: {msg}'

class Sim3TanksError(Exception):

    def __init__(self, code: str, extra: str=''):
        full = get_message(code)
        if extra:
            full = f'{full} {extra}'
        super().__init__(full)
