from brian2 import *

class HodgkinHuxleyNeuron:

    def __init__(self,
                 C=1.0*ufarad/cm**2,
                 g_na_bar=36.0*msiemens/cm**2,
                 g_k_bar=12.0*msiemens/cm**2,
                 g_l=0.1*msiemens/cm**2,
                 v_na=115.0*mV,
                 v_k=-12.0*mV,
                 v_l=10.6*mV,
                 v_rest=-65.0*mV):
        
        # Armazenar parâmetros
        self.C = C
        self.g_na_bar = g_na_bar
        self.g_k_bar = g_k_bar
        self.g_l = g_l
        self.v_na = v_na
        self.v_k = v_k
        self.v_l = v_l
        self.v_rest = v_rest

        # Equações do modelo HH
        self.eqs = '''
        dv/dt = ( g_l*(v_l - v)
                 + g_na_bar * m**3 * h * (v_na - v)
                 + g_k_bar  * n**4       * (v_k  - v)
                 + I_syn
               )/C                                : volt

        dm/dt = alpha_m*(1-m) - beta_m*m     : 1
        dh/dt = alpha_h*(1-h) - beta_h*h     : 1
        dn/dt = alpha_n*(1-n) - beta_n*n     : 1

        alpha_m = 0.1*(v/mV + 40)/(1 - exp(-(v/mV + 40)/10))/ms : Hz
        beta_m  = 4.0*exp(-(v/mV + 65)/18)/ms                   : Hz
        alpha_h = 0.07*exp(-(v/mV + 65)/20)/ms                  : Hz
        beta_h  = 1.0/(1 + exp(-(v/mV + 35)/10))/ms             : Hz
        alpha_n = 0.01*(v/mV + 55)/(1 - exp(-(v/mV + 55)/10))/ms : Hz
        beta_n  = 0.125*exp(-(v/mV + 65)/80)/ms                 : Hz

        I_syn : amp/metre**2    # corrente de entrada externa
        '''

        # Criar NeuronGroup
        self.neuron = NeuronGroup(
            1,
            model=self.eqs,
            method='exponential_euler',
            namespace={
                'C':        self.C,
                'g_na_bar': self.g_na_bar,
                'g_k_bar':  self.g_k_bar,
                'g_l':      self.g_l,
                'v_na':     self.v_na,
                'v_k':      self.v_k,
                'v_l':      self.v_l
            }
        )

        # Inicializa condições de repouso
        self.neuron.v = self.v_rest
        self._initialize_gating(self.v_rest)

        # Monitores
        self.state_mon = StateMonitor(self.neuron, ['v', 'm', 'h', 'n'], record=True)
        self.spike_mon = SpikeMonitor(self.neuron)

    def _initialize_gating(self, v0):
        """Calcula valores iniciais em equilíbrio para m, h, n."""
        def stat(a, b):
            return a(v0) / (a(v0) + b(v0))
        self.neuron.m = stat(
            lambda v: 0.1*(v/mV + 40)/(1 - exp(-(v/mV + 40)/10))/ms,
            lambda v: 4.0*exp(-(v/mV + 65)/18)/ms
        )
        self.neuron.h = stat(
            lambda v: 0.07*exp(-(v/mV + 65)/20)/ms,
            lambda v: 1.0/(1 + exp(-(v/mV + 35)/10))/ms
        )
        self.neuron.n = stat(
            lambda v: 0.01*(v/mV + 55)/(1 - exp(-(v/mV + 55)/10))/ms,
            lambda v: 0.125*exp(-(v/mV + 65)/80)/ms
        )

    def set_stimulus(self, times, values, dt):
        """
        Define um estímulo I_syn como TimedArray.
        times: lista de tempos (não usado diretamente, apenas para referência)
        values: lista de valores de corrente em amp/cm**2
        dt: intervalo entre amostras (Quantity de tempo)
        """
        self.stimulus = TimedArray(values*amp/cm**2, dt=dt)
        # Atualiza namespace dinamicamente
        self.neuron.namespace['stimulus'] = self.stimulus
        # Expressão para corrente sináptica
        self.neuron.I_syn = 'stimulus(t)'

    def simulate(self, duration):
        """Roda a simulação por 'duration' (Quantity de tempo)."""
        run(duration)

    def plot(self):
        """Plota potencial de membrana e variáveis de gating."""
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 1, sharex=True)
        axes[0].plot(self.state_mon.t/ms, self.state_mon.v[0]/mV)
        axes[0].set_ylabel('v (mV)')
        axes[1].plot(self.state_mon.t/ms, self.state_mon.m[0], label='m')
        axes[1].plot(self.state_mon.t/ms, self.state_mon.h[0], label='h')
        axes[1].plot(self.state_mon.t/ms, self.state_mon.n[0], label='n')
        axes[1].set_ylabel('Gates')
        axes[1].set_xlabel('Time (ms)')
        axes[1].legend()
        plt.show()
