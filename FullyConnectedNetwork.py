import numpy as np
from brian2 import start_scope, defaultclock, ms
from HodgkinHuxleyNeuron import HodgkinHuxleyNeuron
from STDPPlasticSynapse import STDPPlasticSynapse

class FullyConnectedNetwork:
    """
    Rede totalmente conectada de N neurônios Hodgkin–Huxley,
    sem autoconexões, sinapses unidirecionais com STDP,
    pesos iniciais aleatórios em [w_min, w_max].
    """

    def __init__(self,
                 N,
                 dt=0.1*ms,
                 w_min=0.0,
                 w_max=1.0,
                 tau_pre=20*ms,
                 tau_post=20*ms,
                 A_plus=0.02,
                 A_minus=0.025):
        start_scope()
        defaultclock.dt = dt
        self.N = N

        # 1) Cria N neurônios HH
        self.neurons = [HodgkinHuxleyNeuron() for _ in range(N)]

        # 2) Configura as sinapses STDP para cada par (i→j), i!=j
        self.plastic_synapses = {}
        for i in range(N):
            for j in range(N):
                if i == j:
                    continue
                pre = self.neurons[i].neuron
                post = self.neurons[j].neuron
                stdp = STDPPlasticSynapse(
                    pre_group=pre,
                    post_group=post,
                    tau_pre=tau_pre,
                    tau_post=tau_post,
                    A_plus=A_plus,
                    A_minus=A_minus,
                    w_max=w_max,
                    connect_prob=1.0   # força 1 conexão i→j
                )
                # sobrescreve peso inicial randômico com [w_min, w_max]
                stdp.synapses.w = 'rand() * (w_max - w_min) + w_min'
                self.plastic_synapses[(i, j)] = stdp

    def modify_connectivity(self, W):
        """
        Redefine a conectividade pela matriz W (NxN):
        W[i,j] == 0   → desconecta i→j
        W[i,j] ∈ (0,1] → conecta (se não havia) e ajusta peso
        """
        assert W.shape == (self.N, self.N)
        assert np.allclose(np.diag(W), 0), "Autoconexões não permitidas"

        for (i, j), stdp in self.plastic_synapses.items():
            S = stdp.synapses
            if W[i, j] == 0:
                S.disconnect()
            else:
                if len(S.i) == 0:
                    S.connect()
                S.w = W[i, j]
