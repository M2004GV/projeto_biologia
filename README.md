<h1>Simulação de Plasticidade Sináptica em Redes Neurais com Hodgkin-Huxley e STDP</h1>
  
📋 Sobre o Projeto
 Este projeto implementa uma simulação computacional de redes neurais recorrentes utilizando o modelo Hodgkin-Huxley (HH) para dinâmica neuronal e Plasticidade Dependente do Tempo de Disparos (STDP) para modificação sináptica.
🎯 Objetivos
- Simular redes totalmente conectadas (TCN) de neurônios HH
- Implementar mecanismo STDP com controle dinâmico (on/off)
- Detectar e analisar padrões de burst neuronal
- Estudar a evolução da conectividade sináptica ao longo do tempo
- Fornecer ferramentas para análise de plasticidade sináptica
✨ Características Principais
- Modelo Hodgkin-Huxley: Dinâmica realista de neurônios
- STDP Controlável: Ativação/desativação durante simulação
- Detecção de Bursts: Algoritmo automático baseado em limiares
- Redes Configuráveis: Número de neurônios e conectividade ajustáveis
- Análise Completa: Visualizações e métricas estatísticas
🛠️ Instalação
 # Pré-requisitos
- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux
Dependências

## Configuração inicial do repositório

# Criar diretório do projeto (via terminal)
mkdir projeto_biologia
cd projeto_biologia

# Inicializar repositório
git init

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
!!! Verificar se o ambiente está ativo

# Clone o repositório
git clone https://github.com/M2004GV/projeto_biologia.git

# Instale as dependências
pip install -r requirements.txt

<h2>🔄 Guia de Colaboração com Git<h2>

# 📋 Fluxo de Trabalho Colaborativo
Este guia estabelece as práticas recomendadas para colaboração eficiente e sem conflitos no projeto.

# 🚨 Regras Fundamentais
⚠️ **NÃO trabalhe** diretamente na branch main.

⚠️ **SEMPRE** execute git fetch antes de começar.

⚠️ **Consulte** git status antes de comitar alterções.

# 📝 Convenções de Commit

| Tipo      | Descrição | Exemplo     |
| :---        |    :----:   |          ---: |
| feat  |Nova funcionalidade  |feat(stdp): adiciona controle dinâmico STDP |
| fix  |Correção de bug  |fix(network): corrige erro de conectividade |
| docs  |Documentação  |docs: atualiza README com guia instalação |
| style  |Formatação de código  |style: aplica formatação black |
| refactor  |Refatoração  |refactor(hh): otimiza cálculo HH |
| test  |Testes  |test: adiciona testes para detecção burst |
| chore  |Tarefas auxiliares  |chore: atualiza dependências |
| perf  |Performance  |perf: otimiza algoritmo STDP |

```
# Atualizar repositório
git fetch origin
git checkout main
git pull origin main

# Criar e mudar para uma nova branch
git checkout -b feature/nova-funcionalidade

# Após alterações no código
git status  # Verificar alterações
git add arquivo_modificado.py
git commit -m "feat: implementa funcionalidade nova"

# Atualizar branch com mudanças do main
git fetch origin
git rebase main

# Enviar branch ao repositório remoto
git push origin feature/nova-funcionalidade

´´´


📚 Referências
- Hodgkin, A. L., & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. The Journal of Physiology, 117(4), 500-544.

- Bi, G. Q., & Poo, M. M. (1998). Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. Journal of Neuroscience, 18(24), 10464-10472.
Stimberg, M., Brette, R., & Goodman, D. F. (2019). Brian 2, an intuitive and efficient neural simulator. Elife, 8, e47314.