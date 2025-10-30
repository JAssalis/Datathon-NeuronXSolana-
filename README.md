# Datathon Neuron DS&AI — AI & Data Week 2025

Este repositório reúne os códigos e dados utilizados no Datathon da Neuron DS&AI, realizado durante o AI & Data Week 2025 em parceria com a Solana Brasil.

O evento desafiou os participantes a extrair insights e análises de uma base de dados sintética, construída para simular o ecossistema cripto de uma cidade fictícia (Ribeirania). O foco foi em análise de dados, garantia de qualidade (data quality) e detecção de padrões comportamentais.

## Estrutura do Repositório
```
├── dados/
│   ├── ribercoin_prices_dirty.csv
│   ├── solana_prices_dirty.csv
│   ├── xister_posts_dirty.csv
│   ├── neuroncoin_prices_dirty.csv
│   ├── bonfimcoin_prices_dirty.csv
│   ├── zephyrcoin_prices_dirty.csv
│   ├── lunartoken_prices_dirty.csv
│   └── ribeirania_events_dirty.csv
├── scripts/
│   ├── generate_templates.py
│   ├── solanagenerator.py
│   ├── main_generator.py
│   └── add_noise.py
├── .gitignore
└── README.md
```
Restante dos arquivos, são usados para a criação do site Xister

## Sobre o Desafio

O Datathon Neuron DS&AI foi uma competição de análise de dados que integrou a programação do AI & Data Week 2025. A base de dados foi criada especificamente para este evento, combinando:

- Dados reais da Solana (coletados via API)
- Dados sintéticos de criptomoedas e redes sociais, gerados por scripts em Python
- Ruído comportamental adicionado deliberadamente para simular problemas reais, tais como:
  - Valores ausentes (missing values)
  - Outliers extremos
  - Registros duplicados e inconsistências
  - Erros de timestamp e formatação
  - Campos corrompidos ou vazios

O objetivo foi simular um cenário realista de trabalho com dados brutos, exigindo tratamento, limpeza e análise crítica para gerar resultados robustos.

---

## Como Gerar os Dados (Para Organizadores)

Esta seção descreve como reproduzir o processo completo de geração de dados.

### Pré-requisitos

Certifique-se de ter as bibliotecas Python necessárias instaladas:
```bash
pip install pandas numpy yfinance
```

### Ordem de Execução

**IMPORTANTE:** Para que os scripts funcionem corretamente, execute-os a partir do diretório raiz do projeto (a pasta principal), e não de dentro da pasta `scripts/`.

#### Passo 1: Gerar Arquivos de Configuração

Este script cria os templates de tweets e a lista de eventos locais que servem de base para a geração de dados.
```bash
python scripts/generate_templates.py
```

**Saída (na raiz):** `xister_tweets_template.csv`, `ribeirania_events.csv`

#### Passo 2: Baixar Dados Reais (Solana)

Este script baixa os dados históricos reais da Solana (SOL) usando a biblioteca yfinance.
```bash
python scripts/solanagenerator.py
```

**Saída (na raiz):** `solana_prices.csv`

#### Passo 3: Gerar Datasets Limpos

Este é o script principal. Ele lê os arquivos de configuração (Passo 1) e os dados da Solana (Passo 2) para gerar todas as criptomoedas sintéticas (RiberCoin, NeuronCoin, etc.) e os posts da rede social Xister.
```bash
python scripts/main_generator.py
```

**Saída (na raiz):** `ribercoin_prices.csv`, `neuroncoin_prices.csv`, `bonfimcoin_prices.csv`, `zephyrcoin_prices.csv`, `lunartoken_prices.csv`, `xister_posts.csv`

#### Passo 4: Adicionar Ruído (Versão Final)

Este script lê todos os datasets limpos gerados no Passo 3 e aplica os diversos tipos de "sujeira" (NaNs, duplicatas, outliers, etc.), criando os arquivos finais para o desafio.
```bash
python scripts/add_noise.py
```

**Saída (na raiz):** `ribercoin_prices_dirty.csv`, `solana_prices_dirty.csv`, `xister_posts_dirty.csv`, e todos os outros arquivos `*_dirty.csv`

#### Passo 5: Organizar Arquivos

Após executar todos os scripts, mova manualmente todos os arquivos `*_dirty.csv` gerados na raiz para a pasta `dados/`.
```bash
# Exemplo (Linux/Mac):
mv *_dirty.csv dados/
```

---

## Dados do Desafio (Para Participantes)

A pasta `dados/` contém os 8 arquivos oficiais do datathon. Todos eles contêm ruído e problemas que precisam ser tratados.

- **solana_prices_dirty.csv**: Dados reais da Solana (com ruído)
- **ribercoin_prices_dirty.csv**: Criptomoeda fictícia principal (com ruído)
- **xister_posts_dirty.csv**: Rede social simulada (com ruído)
- **ribeirania_events_dirty.csv**: Eventos locais (com ruído)
- **neuroncoin_prices_dirty.csv**: Criptomoeda fictícia (com ruído)
- **bonfimcoin_prices_dirty.csv**: Criptomoeda fictícia (com ruído)
- **zephyrcoin_prices_dirty.csv**: Criptomoeda fictícia (com ruído)
- **lunartoken_prices_dirty.csv**: Criptomoeda fictícia (com ruído)

---

## Equipe Organizadora

- **Coordenação técnica da base de dados:** João Vitor Assalis Pedroso
- **Equipe organizadora e de apoio:** Giovanni Fittipaldi 
- **Banca avaliadora:** João Vitor Assalis Pedroso, Professor Marcelo Botelho da Costa Moraes e Professor Rafael de Freitas Souza

## Materiais Completos

Dados completos e demais materiais do desafio estão disponíveis no site oficial do evento:

https://jassalis.github.io/Datathon-NeuronXSolana-/

## Contato

Para dúvidas, colaborações ou sugestões:

Email: jvapedroso@usp.br
Linkedin: https://www.linkedin.com/in/joaoassalis/

Acompanhe a Neuron DS&AI nas redes sociais para futuros eventos e projetos.
