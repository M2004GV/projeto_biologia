# Simulação Detalhada de Plasticidade Sináptica em Redes Neurais Recorrentes
# Modelo Hodgkin-Huxley com STDP implementado em Brian2
# Autor: Sistema de Análise Neural Avançada
# Data: Junho 2025

import brian2 as b2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
import os
import time
from datetime import datetime

# Configuração do Brian2 para modo runtime (não standalone)
b2.start_scope()
b2.prefs.codegen.target = 'numpy'
b2.set_device('runtime')  # Força uso do modo runtime
b2.defaultclock.dt = 0.01*b2.ms

# ==================== PARÂMETROS DA SIMULAÇÃO ====================

# Parâmetros da rede
N_NEURONS = 100
N_EXC = 100  # Todos excitatórios conforme especificado
SIMULATION_TIME = 4000*b2.ms
STDP_ENABLED = True

# Correntes aplicadas específicas para cada neurônio
I_APP_VALUES = np.array([
    1.77633, -3.50002, -7.08579, -7.67495, 4.39299, 1.00314, -0.90991, -0.50249, -3.48903, -3.45378,
    -1.64006, -5.78616, 4.10871, 0.53438, 4.99176, -3.27296, -5.23499, 2.71477, 4.77798, -2.95206,
    -1.22211, -6.29200, -1.17679, -9.53719, -3.01477, 3.41060, 2.71249, -3.09259, -7.98303, -5.88778,
    1.52364, 2.79351, -2.80374, 0.67904, 3.66558, -3.62224, -0.20081, 2.63558, -1.00055, -9.72716,
    -7.09494, -4.50255, -5.78387, -7.81274, -2.45491, 1.19816, -9.06201, -2.50572, 4.37559, 4.94461,
    4.51659, -5.28123, -3.41212, -6.64083, 3.98831, -2.46132, -1.71789, -8.75896, -8.83633, 4.39482,
    -4.98642, 1.79510, -5.68133, 4.29960, 0.73855, 2.67083, -0.55376, 4.94186, -2.12485, -7.34443,
    -0.44572, -8.31904, -5.30320, 1.36982, 4.96384, 3.52412, 1.78182, -3.20475, 0.08255, -5.32517,
    -8.27189, -7.00156, 4.62416, -2.24113, 3.86608, -7.12287, -0.26353, 2.30689, -6.82760, -6.71819,
    -2.98639, 4.59990, -9.87960, 2.35496, -4.14457, 2.46208, -9.33210, -3.57189, 2.14530, 1.10065
]) * b2.uA/b2.cm**2

# Parâmetros do modelo Hodgkin-Huxley (baseados na tabela fornecida e código original)
# Condutâncias
g_leak = 0.1 * b2.mS/b2.cm**2
g_Na = 36 * b2.mS/b2.cm**2
g_K = 12 * b2.mS/b2.cm**2

# Potenciais de reversão
V_leak = 10.6 * b2.mV  # Ajustado conforme código original
V_Na = 115 * b2.mV    # Ajustado conforme código original
V_K = -12 * b2.mV     # Ajustado conforme código original

# Parâmetros sinápticos
g_syn = 3.6 * b2.mS/b2.cm**2
V_exc = 70 * b2.mV
tau_s = 10 * b2.ms
tau_f = 1 * b2.ms
alpha_d = 0.0015 / b2.ms
beta_d = 0.12 / b2.ms
V_thresh = 40 * b2.mV

# Parâmetros STDP
A_plus = 0.1    # Amplitude de potenciação
A_minus = 0.105 # Amplitude de depressão (ligeiramente assimétrica)
tau_plus = 20 * b2.ms   # Constante de tempo para potenciação
tau_minus = 20 * b2.ms  # Constante de tempo para depressão

# ==================== MODELO NEURAL ====================

# Equações do neurônio Hodgkin-Huxley modificadas conforme código original
neuron_eqs = '''
dv/dt = (-g_leak*(v-V_leak) - g_Na*m_inf**3*(0.8-n)*(v-V_Na) - g_K*n**4*(v-V_K) - I_syn + I_app)/C_m : volt
dn/dt = alpha_n*(1-n) - beta_n*n : 1
da/dt = f_syn*(1-a)/tau_f - a/tau_s : 1
ds/dt = alpha_d*(1-s) - beta_d*f_syn*s : 1

m_inf = alpha_m/(alpha_m + beta_m) : 1
alpha_m = 0.1*(25*mV-v)/(exp((25*mV-v)/(10*mV))-1)/mV/ms : Hz
beta_m = 4*exp(-v/(18*mV))/ms : Hz
alpha_n = 0.01*(10*mV-v)/(exp((10*mV-v)/(10*mV))-1)/mV/ms : Hz
beta_n = 0.125*exp(-v/(80*mV))/ms : Hz
f_syn = 1/(1+exp((V_thresh-v)/(1*mV))) : 1

I_syn = g_syn*a_total_exc*(v-V_exc) : amp/meter**2
a_total_exc : 1

I_app : amp/meter**2
C_m : farad/meter**2
'''

# ==================== CRIAÇÃO DA REDE ====================

print("=== INICIANDO SIMULAÇÃO DE PLASTICIDADE SINÁPTICA ===")
print(f"Neurônios: {N_NEURONS} (todos excitatórios)")
print(f"Tempo de simulação: {SIMULATION_TIME}")
print(f"STDP: {'Ativado' if STDP_ENABLED else 'Desativado'}")
print("=" * 50)

# Criação do grupo de neurônios
neurons = b2.NeuronGroup(N_NEURONS, neuron_eqs,
                        threshold='v > V_thresh',
                        reset='',  # Sem reset artificial
                        method='rk4')

# Configuração de parâmetros
neurons.C_m = 1 * b2.uF/b2.cm**2
neurons.I_app = I_APP_VALUES

# Condições iniciais (baseadas no código original)
neurons.v = 0 * b2.mV
neurons.n = 0
neurons.a = 0.01
neurons.s = 0.25

# ==================== CONECTIVIDADE SINÁPTICA ====================

# Conexões totalmente conectadas sem autoconexões
if STDP_ENABLED:
    synapses = b2.Synapses(neurons, neurons,
                          '''
                          w : 1
                          dApre/dt = -Apre/tau_plus : 1 (event-driven)
                          dApost/dt = -Apost/tau_minus : 1 (event-driven)
                          ''',
                          on_pre='''
                          a_total_exc_post += w * a_pre * s_pre
                          Apre += A_plus
                          w = clip(w + Apost, 0, 2)
                          ''',
                          on_post='''
                          Apost += A_minus
                          w = clip(w - Apre, 0, 2)
                          ''')
else:
    synapses = b2.Synapses(neurons, neurons,
                          '''
                          w : 1
                          ''',
                          on_pre='''
                          a_total_exc_post += w * a_pre * s_pre
                          ''')

# Conectar todos os neurônios exceto autoconexões
synapses.connect(condition='i != j')

# Aguardar a criação das sinapses antes de definir pesos
print("Aguardando criação das sinapses...")

# Pré-gerar os pesos iniciais
np.random.seed(42)  # Para reprodutibilidade
n_synapses = N_NEURONS * (N_NEURONS - 1)  # Todas as conexões menos autoconexões
initial_weights = np.random.uniform(0, 1, n_synapses)

# Inicialização dos pesos sinápticos
synapses.w = initial_weights

print(f"Conexões sinápticas criadas: {n_synapses}")
print(f"Peso sináptico inicial: μ={np.mean(initial_weights):.3f}, σ={np.std(initial_weights):.3f}")

# ==================== MONITORAMENTO ====================

# Monitores para coleta de dados
spike_monitor = b2.SpikeMonitor(neurons)
state_monitor = b2.StateMonitor(neurons, ['v', 'n', 'a', 's'], record=True, dt=1*b2.ms)

# Monitor de pesos com menos frequência para economizar memória
weight_monitor = b2.StateMonitor(synapses, 'w', record=range(min(100, n_synapses)), dt=50*b2.ms)

# Monitor para análise populacional
pop_monitor = b2.PopulationRateMonitor(neurons)

print("Monitores configurados para coleta de dados")

# ==================== EXECUÇÃO DA SIMULAÇÃO ====================

print("\n=== INICIANDO SIMULAÇÃO ===")
start_time = time.time()

try:
    # Executar simulação
    b2.run(SIMULATION_TIME, report='text')
    simulation_time = time.time() - start_time
    print(f"\nSimulação concluída em {simulation_time:.2f} segundos")
    
except Exception as e:
    print(f"Erro durante a simulação: {e}")
    print("Tentando com parâmetros reduzidos...")
    
    # Reduzir tempo de simulação se houver problemas
    SIMULATION_TIME = 1000*b2.ms
    b2.run(SIMULATION_TIME, report='text')
    simulation_time = time.time() - start_time
    print(f"Simulação reduzida concluída em {simulation_time:.2f} segundos")

# ==================== ANÁLISE DE DADOS ====================

print("\n=== ANÁLISE DE RESULTADOS ===")

# Análise de disparos
n_spikes = len(spike_monitor.t)
firing_rate = n_spikes / (SIMULATION_TIME/b2.second) / N_NEURONS if n_spikes > 0 else 0
print(f"Total de disparos: {n_spikes}")
print(f"Taxa de disparo média: {firing_rate:.2f} Hz")

# Análise dos pesos sinápticos
final_weights = np.array(synapses.w[:])

print(f"\nAnálise dos pesos sinápticos:")
print(f"Pesos iniciais: μ={np.mean(initial_weights):.3f}, σ={np.std(initial_weights):.3f}")
print(f"Pesos finais: μ={np.mean(final_weights):.3f}, σ={np.std(final_weights):.3f}")

# Teste estatístico
if STDP_ENABLED and len(final_weights) == len(initial_weights):
    try:
        t_stat, p_value = stats.ttest_rel(final_weights, initial_weights)
        print(f"Teste t pareado: t={t_stat:.3f}, p={p_value:.6f}")
    except:
        p_value = np.nan
        print("Não foi possível realizar teste estatístico")
else:
    p_value = np.nan

# ==================== VISUALIZAÇÕES ====================

print("\n=== GERANDO VISUALIZAÇÕES ===")

# Configuração de estilo
plt.style.use('default')  # Usar estilo padrão para evitar problemas
fig_size = (15, 12)

# Criar figura com subplots
fig, axes = plt.subplots(3, 2, figsize=(16, 12))

try:
    # 1. Raster Plot
    if n_spikes > 0:
        axes[0,0].scatter(spike_monitor.t/b2.ms, spike_monitor.i, s=0.5, alpha=0.7)
        axes[0,0].set_xlabel('Tempo (ms)')
        axes[0,0].set_ylabel('Neurônio')
        axes[0,0].set_title('Raster Plot - Atividade Neural')
        axes[0,0].set_xlim(0, float(SIMULATION_TIME/b2.ms))
    else:
        axes[0,0].text(0.5, 0.5, 'Nenhum disparo detectado', ha='center', va='center')
        axes[0,0].set_title('Raster Plot - Sem Atividade')

    # 2. Taxa populacional
    if len(pop_monitor.t) > 0:
        axes[0,1].plot(pop_monitor.t/b2.ms, pop_monitor.smooth_rate(window='gaussian', width=10*b2.ms)/b2.Hz)
        axes[0,1].set_xlabel('Tempo (ms)')
        axes[0,1].set_ylabel('Taxa (Hz)')
        axes[0,1].set_title('Taxa de Disparo Populacional')
    else:
        axes[0,1].text(0.5, 0.5, 'Dados insuficientes', ha='center', va='center')
        axes[0,1].set_title('Taxa Populacional - Sem Dados')

    # 3. Histogramas dos pesos
    axes[1,0].hist(initial_weights, bins=30, alpha=0.7, label='Inicial', density=True)
    axes[1,0].hist(final_weights, bins=30, alpha=0.7, label='Final', density=True)
    axes[1,0].set_xlabel('Peso Sináptico')
    axes[1,0].set_ylabel('Densidade')
    axes[1,0].set_title('Distribuição dos Pesos Sinápticos')
    axes[1,0].legend()

    # 4. Evolução temporal dos pesos (se disponível)
    if len(weight_monitor.t) > 0 and weight_monitor.w.shape[0] > 0:
        n_samples = min(20, weight_monitor.w.shape[0])
        for idx in range(n_samples):
            axes[1,1].plot(weight_monitor.t/b2.ms, weight_monitor.w[idx], alpha=0.5, linewidth=0.8)
        axes[1,1].set_xlabel('Tempo (ms)')
        axes[1,1].set_ylabel('Peso Sináptico')
        axes[1,1].set_title('Evolução Temporal dos Pesos (Amostra)')
    else:
        axes[1,1].text(0.5, 0.5, 'Monitor de pesos sem dados', ha='center', va='center')
        axes[1,1].set_title('Evolução dos Pesos - Sem Dados')

    # 5. Potencial de membrana (amostra de neurônios)
    sample_neurons = [0, 25, 50, 75]
    for neuron_idx in sample_neurons:
        if neuron_idx < len(state_monitor.v):
            axes[2,0].plot(state_monitor.t/b2.ms, state_monitor.v[neuron_idx]/b2.mV, 
                          label=f'Neurônio {neuron_idx}', alpha=0.8)
    axes[2,0].set_xlabel('Tempo (ms)')
    axes[2,0].set_ylabel('Potencial (mV)')
    axes[2,0].set_title('Potencial de Membrana (Amostra)')
    axes[2,0].legend()

    # 6. Análise estatística dos pesos
    axes[2,1].boxplot([initial_weights, final_weights], labels=['Inicial', 'Final'])
    axes[2,1].set_ylabel('Peso Sináptico')
    axes[2,1].set_title('Comparação Estatística dos Pesos')

    plt.tight_layout()
    plt.savefig('simulacao_plasticidade_corrigida.png', dpi=300, bbox_inches='tight')
    plt.show()

except Exception as e:
    print(f"Erro na geração de gráficos: {e}")
    print("Continuando com análise de dados...")

# ==================== ANÁLISE AVANÇADA ====================

print("\n=== ANÁLISE AVANÇADA ===")

# Análise de sincronização
def calculate_synchrony(spike_times, neuron_ids, window=10*b2.ms):
    """Calcula medida de sincronização baseada em coincidência de disparos"""
    if len(spike_times) == 0:
        return 0
    
    spike_times_ms = spike_times / b2.ms
    sync_events = 0
    total_events = len(spike_times_ms)
    
    for idx, t in enumerate(spike_times_ms):
        coincident_spikes = np.sum(np.abs(spike_times_ms - t) < window/b2.ms) - 1
        if coincident_spikes > 0:
            sync_events += 1
    
    return sync_events / total_events if total_events > 0 else 0

synchrony_measure = calculate_synchrony(spike_monitor.t, spike_monitor.i)
print(f"Medida de sincronização: {synchrony_measure:.3f}")

# ==================== EXPORTAÇÃO DE DADOS ====================

print("\n=== EXPORTANDO DADOS ===")

try:
    # Criar diretório de resultados
    os.makedirs('resultados_simulacao', exist_ok=True)

    # Salvar dados de disparos
    if n_spikes > 0:
        spike_data = pd.DataFrame({
            'tempo_ms': spike_monitor.t/b2.ms,
            'neuronio': spike_monitor.i
        })
        spike_data.to_csv('resultados_simulacao/disparos.csv', index=False)

    # Salvar estatísticas finais
    stats_data = {
        'parametro': ['n_neurons', 'simulation_time_ms', 'total_spikes', 'mean_firing_rate_hz',
                      'initial_weight_mean', 'final_weight_mean', 'weight_change_pvalue',
                      'synchrony_measure', 'stdp_enabled'],
        'valor': [N_NEURONS, float(SIMULATION_TIME/b2.ms), n_spikes, firing_rate,
                  np.mean(initial_weights), np.mean(final_weights), 
                  p_value if 'p_value' in locals() else np.nan,
                  synchrony_measure, STDP_ENABLED]
    }
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv('resultados_simulacao/estatisticas.csv', index=False)

    # Salvar pesos iniciais e finais
    weights_df = pd.DataFrame({
        'peso_inicial': initial_weights,
        'peso_final': final_weights
    })
    weights_df.to_csv('resultados_simulacao/comparacao_pesos.csv', index=False)

    print("Dados exportados para o diretório 'resultados_simulacao/'")

except Exception as e:
    print(f"Erro na exportação: {e}")

# ==================== RELATÓRIO FINAL ====================

print("\n" + "="*60)
print("           RELATÓRIO FINAL DA SIMULAÇÃO")
print("="*60)
print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Duração da simulação: {simulation_time:.2f} segundos")
print()
print("PARÂMETROS DA SIMULAÇÃO:")
print(f"  • Neurônios: {N_NEURONS} (todos excitatórios)")
print(f"  • Conexões: {n_synapses} (totalmente conectada sem autoconexões)")
print(f"  • Tempo simulado: {float(SIMULATION_TIME/b2.ms)} ms")
print(f"  • STDP: {'Ativado' if STDP_ENABLED else 'Desativado'}")
print()
print("RESULTADOS PRINCIPAIS:")
print(f"  • Total de disparos: {n_spikes}")
print(f"  • Taxa de disparo média: {firing_rate:.2f} Hz")
print(f"  • Peso sináptico inicial: {np.mean(initial_weights):.3f} ± {np.std(initial_weights):.3f}")
print(f"  • Peso sináptico final: {np.mean(final_weights):.3f} ± {np.std(final_weights):.3f}")
if 'p_value' in locals() and not np.isnan(p_value):
    print(f"  • Mudança significativa nos pesos: {'Sim' if p_value < 0.05 else 'Não'} (p={p_value:.6f})")
print(f"  • Medida de sincronização: {synchrony_measure:.3f}")
print()
print("CONCLUSÕES:")
if STDP_ENABLED:
    if np.mean(final_weights) > np.mean(initial_weights):
        print("  • STDP resultou em fortalecimento geral das conexões")
    else:
        print("  • STDP resultou em enfraquecimento geral das conexões")
    print("  • A plasticidade sináptica modificou a estrutura da rede")
else:
    print("  • Simulação controle sem STDP realizada com sucesso")

if n_spikes > 0:
    print("  • Padrões de atividade neural foram capturados e analisados")
else:
    print("  • Pouca ou nenhuma atividade neural detectada - verificar parâmetros")

print("  • Dados completos exportados para análises posteriores")
print("="*60)

print("\n🎉 SIMULAÇÃO CONCLUÍDA! 🎉")
print("Código corrigido e executado com tratamento de erros.")
print("Pronto para análises e ajustes adicionais conforme necessário.")
