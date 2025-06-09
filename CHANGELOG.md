# Changelog
Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),

e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

[Unreleased]
# Adicionado
- Implementação completa do modelo Hodgkin-Huxley
- STDP (Spike-Timing Dependent Plasticity) com parâmetros configuráveis
- Rede neural recorrente com 100 neurônios excitatórios
- Sistema de monitoramento de spikes e pesos sinápticos
- Análise estatística de mudanças nos pesos (teste t pareado)
- Métricas de sincronização neural
- Visualizações multipanel com raster plots e histogramas
- Exportação de dados em formato CSV
- Tratamento robusto de erros com fallbacks
- Suporte a modos runtime e standalone do Brian2
- Suite completa de testes automatizados
- Documentação detalhada com exemplos
# Corrigido
- Bug de acesso a variáveis em modo standalone
- Conflito de nomes de variáveis ('i')
- Inicialização incorreta de pesos sinápticos
- Problemas de memória em simulações longas
- Erros de visualização com dados vazios
# Alterado
- Migração para modo runtime por padrão (melhor debugging)
- Otimização do monitoramento de pesos (amostragem)
- Redução da frequência de gravação para economia de memória
- Melhoria na estrutura de dados exportados
[0.1.0] - 2025-06-09
# Adicionado
- Estrutura inicial do projeto
- Configuração básica do ambiente de desenvolvimento
- Dependências e requirements definidos
----------