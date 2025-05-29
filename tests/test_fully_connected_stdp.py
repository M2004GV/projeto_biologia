import numpy as np
import pytest
from brian2 import start_scope, run, ms
from projeto_biologia.FullyConnectedNetwork import FullyConnectedNetwork

@pytest.fixture
def make_network():
    start_scope()
    net = FullyConnectedNetwork(
        N=3,
        w_min=0.0, w_max=1.0,
        tau_pre=20*ms, tau_post=20*ms,
        A_plus=0.02, A_minus=0.025
    )
    # estímulo forte para tentar gerar spikes
    for hh in net.neurons:
        hh.set_stimulus(values=[0, 5.0, 0], dt=100*ms)

    run(200*ms)  # aquecimento

    # se nenhum HH disparar, pule o teste
    for idx, hh in enumerate(net.neurons):
        if len(hh.spike_mon.t) == 0:
            pytest.skip(f"Neurônio {idx} não disparou no aquecimento; STDP não pôde ser testado.")

    # limpa os spikes antigos
    for hh in net.neurons:
        hh.spike_mon.t[:] = []

    return net

def test_stdp_enabled_changes_weights(make_network):
    net = make_network
    init_ws = {k: np.copy(s.synapses.w[:])
               for k, s in net.plastic_synapses.items()}
    run(400*ms)
    changed = any(
        not np.allclose(init_ws[k], s.synapses.w[:])
        for k, s in net.plastic_synapses.items()
    )
    assert changed, "STDP ativo, mas nenhum peso mudou."

def test_stdp_disabled_keeps_weights():
    start_scope()
    net = FullyConnectedNetwork(
        N=3,
        w_min=0.0, w_max=1.0,
        tau_pre=20*ms, tau_post=20*ms,
        A_plus=0.0, A_minus=0.0
    )
    for hh in net.neurons:
        hh.set_stimulus(values=[0, 5.0, 0], dt=100*ms)
    run(200*ms)
    for idx, hh in enumerate(net.neurons):
        if len(hh.spike_mon.t) == 0:
            pytest.skip(f"Neurônio {idx} sem spikes; impossível testar STDP OFF.")
        hh.spike_mon.t[:] = []

    init_ws = {k: np.copy(s.synapses.w[:])
               for k, s in net.plastic_synapses.items()}
    run(400*ms)
    for k, s in net.plastic_synapses.items():
        assert np.allclose(init_ws[k], s.synapses.w[:]), (
            f"Peso da sinapse {k} mudou mesmo com STDP desativado."
        )
