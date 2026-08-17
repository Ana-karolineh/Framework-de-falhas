from funcoes_aux.get_message import Sim3TanksError

def clear_variables(self, option: str=None):
    if option is None:
        self._set_internal_state_variables([])
        self._set_internal_flow_variables([])
        self._set_internal_sensor_measurements([])
        self._set_internal_valve_signals([])
        self._set_internal_fault_magnitudes([])
        self._set_internal_fault_offsets([])
        self._reset_internal_simulation_time()
    else:
        option = option.lower()
        if option == 'states':
            self._set_internal_state_variables([])
        elif option == 'flows':
            self._set_internal_flow_variables([])
        elif option == 'sensors':
            self._set_internal_sensor_measurements([])
        elif option == 'valves':
            self._set_internal_valve_signals([])
        elif option == 'faults':
            self._set_internal_fault_magnitudes([])
            self._set_internal_fault_offsets([])
        else:
            raise Sim3TanksError('ERR003')
