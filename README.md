# Framework de falhas

Este projeto é uma versão em Python do [Sim3Tanks](https://github.com/e-controls/Sim3Tanks), um simulador de três tanques interligados originalmente escrito em MATLAB. Ele é usado para estudar controle de processos e, principalmente, para simular falhas — desde vazamentos e entupimentos em bombas e válvulas até sensores de nível e vazão lendo errado.

A ideia aqui foi portar o simulador mantendo a mesma estrutura e o mesmo comportamento do original, só que em Python.

## Estrutura

O projeto é dividido em dois grupos de arquivos, cada função/método do simulador no seu próprio arquivo:

**`funcoes_aux/`** — as funções auxiliares que o simulador usa por baixo dos panos:

- `sys_dynamics.py` e `sys_flow_rates.py` — as equações da física dos tanques (como a água entra, sai e se equilibra entre eles)
- `sys_measurements.py` — como os sensores leem (e, se houver falha, distorcem) os valores reais
- `check_enabled_faults.py`, `check_enabled_valves.py`, `check_enabled_noises.py`, `check_operation_mode.py`, `check_physical_param.py` — validações que checam se as falhas, válvulas e parâmetros configurados fazem sentido antes de simular
- `create_sim3tanks.py` — cria um novo simulador do zero
- `default_physical_param.py` e `default_operation_mode.py` — os valores padrão de fábrica (tamanho dos tanques, estado inicial das válvulas etc.)
- `sat_signal.py` — só garante que um sinal fique dentro de um limite (não deixa passar de 0-1, por exemplo)
- `get_message.py` e `get_rgb_triplet.py` — mensagens de erro e cores usadas nos gráficos

**`src/sim3tanks/`** — a classe principal e os métodos que você realmente usa no dia a dia:

- `sim3tanks.py` — a classe em si, guarda toda a configuração do sistema
- `simulate_model.py` — o coração do simulador, calcula um passo de tempo
- `set_default_model.py` — configura o simulador pro cenário padrão
- `clear_model.py` / `clear_variables.py` — reseta tudo
- `get_state_variables.py`, `get_flow_variables.py`, `get_sensor_measurements.py`, `get_valve_signals.py`, `get_fault_magnitudes.py`, `get_fault_offsets.py` — puxam os dados da simulação já rodada
- `plot_levels.py`, `plot_flows.py`, `plot_valves.py`, `plot_fault_magnitudes.py`, `plot_fault_offsets.py` — geram os gráficos
- `get_default_linear_model.py` — devolve uma versão linearizada (aproximada) da física do sistema
- `display_model.py` — imprime a configuração atual no terminal, pra debug

## Ativando uma falha

```python
tts.Model.FaultSettings.f8.EnableSignal = True
tts.Model.FaultSettings.f8.Magnitude = 0.3
```

Falhas de sensor (`f11` a `f23`) também aceitam um `Offset`:

```python
tts.Model.FaultSettings.f11.EnableSignal = True
tts.Model.FaultSettings.f11.Magnitude = 0.3
tts.Model.FaultSettings.f11.Offset = 1.5
```

## Rodando

```bash
pip install -r requirements.txt
python main.py
```

`main.py` já vem com um exemplo pronto (uma falha crescendo aos poucos) e mostra os gráficos no final.

## Créditos

Baseado no trabalho original de Farias, Queiroz, Bessa, Medeiros, Cordeiro e Palhares (2018), *"Sim3Tanks: A benchmark model simulator for process control and monitoring"*, publicado na IEEE Access.

Repositório MATLAB original: [github.com/e-controls/Sim3Tanks](https://github.com/e-controls/Sim3Tanks)
