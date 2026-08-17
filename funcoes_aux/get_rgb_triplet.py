import numpy as np
from .get_message import Sim3TanksError
_LIST_OF_COLORS = {'normal': np.array([102, 205, 170]) / 255, 'fault': np.array([255, 127, 80]) / 255, 'closed': np.array([119, 136, 153]) / 255, 'open': np.array([205, 201, 201]) / 255, 'step': np.array([205, 201, 201]) / 255, 'drift': np.array([238, 233, 233]) / 255, 'blue': np.array([179, 199, 255]) / 255, 'white': np.array([255, 255, 255]) / 255}

def get_rgb_triplet(tag: str):
    key = str(tag).lower()
    if key not in _LIST_OF_COLORS:
        raise Sim3TanksError('ERR003')
    return tuple(_LIST_OF_COLORS[key])
