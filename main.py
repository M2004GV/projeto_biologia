from brian2 import ms, mV
from HodgkinHuxleyNeuron import HodgkinHuxleyNeuron

if __name__ == 'main':
    # 1) Instancia com parâmetros padrão
    hh = HodgkinHuxleyNeuron()
   
    # 2) Define estímulo: [0, 1e-6, 0] A/m² em janelas de 100 ms
    hh.set_stimulus(
        values=[0, 1e-6, 0],  # em ampere/metre**2
        dt=100 * ms
    )

    # 3) Roda a simulação por 500 ms
    hh.simulate(500 * ms)

    print("n_times =", len(hh.state_mon.t),
             "v.shape =", hh.state_mon.v.shape)

    # 5) Plota resultados
    hh.plot()
