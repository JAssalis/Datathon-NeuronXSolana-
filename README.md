# Datathon Neuron DS&AI — AI & Data Week 2025

Este repositório reúne os códigos-fonte e os dados utilizados no **Datathon da Neuron DS&AI**, realizado durante o **AI & Data Week 2025** em parceria com a **Solana Brasil**.

O evento desafiou os participantes a extrair insights e análises de uma base de dados sintética, construída para simular o ecossistema cripto de uma cidade fictícia (**Ribeirania**). O foco foi em análise de dados, detecção de padrões comportamentais e gerar insights sobre os acontecimentos que estavam ocorrendo na cidade.

---

## Estrutura do Repositório

```
├── dados/
│   ├── ribercoin_prices_dirty.csv
│   ├── solana_prices_dirty.csv
│   ├── xister_posts_dirty.csv
│   └── ... (e todos os outros arquivos _dirty.csv)
│
├── docs/
│   ├── index.html
│   └── ... (arquivos do site hospedado no GitHub Pages)
│
├── scripts/
│   ├── generate_templates.py    (Passo 1: Gera configs)
│   ├── solanagenerator.py       (Passo 2: Baixa dados reais)
│   ├── main_generator.py        (Passo 3: Gera dados LIMPOS)
│   └── add_noise.py             (Passo 4: Gera dados SUJOS)
│
├── .gitignore
├── README.md                     (Este arquivo)
├── ribeirania_events.csv        (Arquivo de configuração de eventos)
└── xister_tweets_template.csv   (Arquivo de configuração de posts)
```

---

## Sobre o Desafio

O **Datathon Neuron DS&AI** foi uma competição de análise de dados que integrou a programação do **AI & Data Week 2025**. A base de dados foi criada especificamente para este evento, combinando:

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

## Arquivos do Desafio (Para Participantes)

Os arquivos finais para o desafio estão localizados na pasta `/dados/`. Estes são os únicos arquivos necessários para participar da competição:

1. `solana_prices_dirty.csv`
2. `ribercoin_prices_dirty.csv`
3. `xister_posts_dirty.csv`
4. `ribeirania_events_dirty.csv`
5. `neuroncoin_prices_dirty.csv`
6. `bonfimcoin_prices_dirty.csv`
7. `zephyrcoin_prices_dirty.csv`
8. `lunartoken_prices_dirty.csv`

---

## Instruções de Reprodução (Para Organizadores)

Esta seção documenta o processo de geração dos datasets.

### 1. Clone este repositório

```bash
git clone https://github.com/[seu-usuario]/[nome-do-repositorio].git
cd [nome-do-repositorio]
```

### 2. Instale as dependências

```bash
pip install pandas numpy yfinance
```

### 3. Passo 1: Gerar Configurações

Cria `ribeirania_events.csv` e `xister_tweets_template.csv` na raiz:

```bash
python scripts/generate_templates.py
```

### 4. Passo 2: Baixar Dados Reais

Cria `solana_prices.csv` na raiz:

```bash
python scripts/solanagenerator.py
```

### 5. Passo 3: Gerar Datasets Limpos (Gabarito)

Cria `ribercoin_prices.csv`, `xister_posts.csv`, etc., na raiz:

```bash
python scripts/main_generator.py
```

### 6. Passo 4: Adicionar Ruído (Versão do Desafio)

Cria `ribercoin_prices_dirty.csv`, etc., na raiz:

```bash
python scripts/add_noise.py
```

### 7. Passo 5: Organizar Arquivos

Mova manualmente todos os arquivos `*_dirty.csv` gerados na raiz para a pasta `dados/`.

---

## Equipe Organizadora

- **Coordenação técnica da base de dados:** João Vitor Assalis Pedroso
- **Equipe organizadora e de apoio:** Giovanni Fittipaldi Prado
- **Banca avaliadora:** João Vitor Assalis Pedroso, Professor Doutor Marcelo Botelho da Costa Moraes, Professor Doutor Rafael de Freitas Souza

---

## Dados e Código-Fonte

Todos os códigos e amostras de dados neste repositório são públicos e podem ser utilizados para fins educacionais e de pesquisa. Os dados sintéticos foram gerados exclusivamente para o Datathon.

### Materiais Completos

Dados completos e demais materiais do desafio estão disponíveis no site oficial do evento (hospedado na pasta `/docs`):

**https://jassalis.github.io/Datathon-NeuronXSolana-/**

---

## Contato

Para dúvidas, colaborações ou sugestões:

- Email: jvapedroso@usp.br
- Linkedin: https://www.linkedin.com/in/joaoassalis/

Acompanhe a **Neuron DS&AI** nas redes sociais para futuros eventos e projetos.
