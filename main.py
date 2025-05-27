# run_hh.py

from brian2 import ms
from HodgkinHuxleyNeuron import HodgkinHuxleyNeuron

if __name__ == '__main__':
    # 1) Instancia com parâmetros padrão
    hh = HodgkinHuxleyNeuron()

    # 2) Define estímulo: [0, 1e-6, 0] A/cm² em janelas de 100 ms
    hh.set_stimulus(
        values=[0, 1e-6, 0],  # em ampere/cm**2
        dt=100 * ms
    )

    # 3) Roda a simulação por 500 ms
    hh.simulate(500 * ms)

    # 4) Plota resultados
    hh.plot()
