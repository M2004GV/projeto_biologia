<h1>Simulação de Plasticidade Sináptica em Redes Neurais com Hodgkin-Huxley e STDP</h1>

<h2>📋 Sobre o Projeto</h2>
<p>Este projeto implementa uma simulação computacional de redes neurais recorrentes utilizando o modelo Hodgkin-Huxley (HH) para dinâmica neuronal e Plasticidade Dependente do Tempo de Disparos (STDP) para modificação sináptica.</p>

# Novidades
- Adicionado modelo de neurônio Hodgkin–Huxley
    - Classe: HodgkinHuxleyNeuron.py
    - Simula potencial de membrana e spikes em resposta a estímulos


    - Adicionado mecanismo stdp em synapses
    - Classe: STDPPlasticSynapse.py

<h2>🎯 Objetivos</h2>
<ul>
    <li>Simular redes totalmente conectadas (TCN) de neurônios HH</li>
    <li>Implementar mecanismo STDP com controle dinâmico (on/off)</li>
    <li>Detectar e analisar padrões de burst neuronal</li>
    <li>Estudar a evolução da conectividade sináptica ao longo do tempo</li>
    <li>Fornecer ferramentas para análise de plasticidade sináptica</li>
</ul>

<h2>✨ Características Principais</h2>
<ul>
    <li>Modelo Hodgkin-Huxley: Dinâmica realista de neurônios</li>
    <li>STDP Controlável: Ativação/desativação durante simulação</li>
    <li>Detecção de Bursts: Algoritmo automático baseado em limiares</li>
    <li>Redes Configuráveis: Número de neurônios e conectividade ajustáveis</li>
    <li>Análise Completa: Visualizações e métricas estatísticas</li>
</ul>

# Parâmetros de configuração 

Parâmetros do modelo HH:

| Parâmetro |	Valor	| Unidade|	Descrição|
|   ---     |    ---    |   ---  |     ---   |
|deli	|15.0	|ms	|Delay sináptico|
|vna	|115.0	|mV	|Potencial de reversão Na+|
|vk	|-12.0	|mV	|Potencial de reversão K+|
|vl	|10.6	|mV	|Potencial de reversão leak|
|gnabar|	36.0|	mS/cm²|	Condutância máxima Na+|
|gkbar	|12.0|	mS/cm²|	Condutância máxima K+|
|gl	|0.1	|mS/cm²|	Condutância leak|

Parâmetros Sinápticos

|Parâmetro|	Valor|	Unidade|	Descrição|
|   ---     |    ---    |   ---  |     ---   |
|taus	|10.0	|ms|	Constante de tempo lenta|
|tauf	|1.0	|ms|	Constante de tempo rápida|
|gsyn	|3.6	|mS/cm²|	Condutância sináptica|
|vsyn	|70.0	|mV	|Potencial sináptico|
|Vthresh	|40.0|	mV|	Limiar de disparo|


<h2>🛠️ Instalação</h2>
<h3>Pré-requisitos</h3>
<ul>
    <li>Python 3.8 ou superior</li>
    <li>Sistema operacional: Windows, macOS ou Linux</li>
</ul>

<h3>Dependências e Configuração Inicial do Repositório</h3>
<p>Criar diretório do projeto (via terminal):</p>
<pre>
mkdir projeto_biologia
cd projeto_biologia
</pre>
<p>Inicializar repositório:</p>
<pre>
git init
</pre>
<p>Criar ambiente virtual:</p>
<pre>
python -m venv venv
</pre>
<p>Ativar ambiente virtual:</p>
<pre>
<em>No Windows:</em>
venv\Scripts\activate
<em>No macOS/Linux:</em>
source venv/bin/activate
</pre>
<p>Clone o repositório:</p>
<pre>
git clone https://github.com/M2004GV/projeto_biologia.git
</pre>
<p>Instale as dependências:</p>
<pre>
pip install -r requirements.txt
</pre>

<h2>🔄 Guia de Colaboração com Git</h2>
<h3>📋 Fluxo de Trabalho Colaborativo</h3>
<p>Este guia estabelece as práticas recomendadas para colaboração eficiente e sem conflitos no projeto.</p>

<h3>🚨 Regras Fundamentais</h3>
<ul>
    <li>⚠️ <strong>NÃO</strong> trabalhe diretamente na branch main.</li>
    <li>⚠️ <strong>SEMPRE</strong> execute git fetch antes de começar.</li>
    <li>⚠️ <strong>Consulte</strong> git status antes de comitar alterações.</li>
</ul>

<h3>📝 Convenções de Commit</h3>
<table>
    <thead>
        <tr>
            <th>Tipo</th>
            <th>Descrição</th>
            <th>Exemplo</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>feat</td>
            <td>Nova funcionalidade</td>
            <td>feat(stdp): adiciona controle dinâmico STDP</td>
        </tr>
        <tr>
            <td>fix</td>
            <td>Correção de bug</td>
            <td>fix(network): corrige erro de conectividade</td>
        </tr>
        <tr>
            <td>docs</td>
            <td>Documentação</td>
            <td>docs: atualiza README com guia instalação</td>
        </tr>
        <tr>
            <td>style</td>
            <td>Formatação de código</td>
            <td>style: aplica formatação black</td>
        </tr>
        <tr>
            <td>refactor</td>
            <td>Refatoração</td>
            <td>refactor(hh): otimiza cálculo HH</td>
        </tr>
        <tr>
            <td>test</td>
            <td>Testes</td>
            <td>test: adiciona testes para detecção burst</td>
        </tr>
        <tr>
            <td>chore</td>
            <td>Tarefas auxiliares</td>
            <td>chore: atualiza dependências</td>
        </tr>
        <tr>
            <td>perf</td>
            <td>Performance</td>
            <td>perf: otimiza algoritmo STDP</td>
        </tr>
    </tbody>
</table>

<pre>
# Atualizar repositório
git fetch origin
git checkout main
git pull origin main

# Criar e mudar para uma nova branch
git checkout -b feature/nova-funcionalidade

# Após alterações no código
git status   # Verificar alterações
git add arquivo_modificado.py
git commit -m "feat: implementa funcionalidade nova"

# Atualizar branch com mudanças do main
git fetch origin
git rebase main

# Enviar branch ao repositório remoto
git push origin feature/nova-funcionalidade
</pre>

<h2>📚 Referências</h2>
<ul>
    <li>Hodgkin, A. L., & Huxley, A. F. (1952). <em>A quantitative description of membrane current and its application to conduction and excitation in nerve</em>. The Journal of Physiology, 117(4), 500-544.</li>
    <li>Bi, G. Q., & Poo, M. M. (1998). <em>Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type</em>. Journal of Neuroscience, 18(24), 10464-10472.</li>
    <li>Stimberg, M., Brette, R., & Goodman, D. F. (2019). <em>Brian 2, an intuitive and efficient neural simulator</em>. Elife, 8, e47314.</li>
</ul>
