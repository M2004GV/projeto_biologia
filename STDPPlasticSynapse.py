from brian2 import Synapses
from brian2 import ms

class STDPPlasticSynapse:
    def __init__(self,
                 pre_group,
                 post_group,
                 tau_pre=20 * ms,
                 tau_post=20 * ms,
                 A_plus=0.01,
                 A_minus=0.012,
                 w_max=1.0,
                 connect_prob=0.1):
        """
        Constrói sinapses com regra STDP do tipo pair-based.

        pre_group, post_group: NeuronGroup ou SpikeGeneratorGroup
        tau_pre, tau_post: constantes de decaimento das janelas (ms)
        A_plus, A_minus: magnitudes dos ajustes de peso
        w_max: peso máximo
        connect_prob: probabilidade de conexão inicial
        """
        self.pre_group = pre_group
        self.post_group = post_group
        self.tau_pre = tau_pre
        self.tau_post = tau_post
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.w_max = w_max
        self.connect_prob = connect_prob
        self._build_synapses()

    def _build_synapses(self):
        model = '''
        w        : 1
        dpre/dt  = -pre/tau_pre   : 1 (event-driven)
        dpost/dt = -post/tau_post : 1 (event-driven)
        '''
        on_pre = '''
        v_post += w * mV
        pre = 1
        w = clip(w + A_plus * post, 0, w_max)
        '''
        on_post = '''
        post = 1
        w = clip(w - A_minus * pre, 0, w_max)
        '''
        self.synapses = Synapses(
            self.pre_group,
            self.post_group,
            model=model,
            on_pre=on_pre,
            on_post=on_post,
            namespace={
                'tau_pre': self.tau_pre,
                'tau_post': self.tau_post,
                'A_plus': self.A_plus,
                'A_minus': self.A_minus,
                'w_max': self.w_max
            }
        )
        self.synapses.connect(p=self.connect_prob)
        self.synapses.w = 'rand() * w_max'

    @property
    def w(self):
        """Retorna os pesos atuais como um array."""
        return self.synapses.w[:]
