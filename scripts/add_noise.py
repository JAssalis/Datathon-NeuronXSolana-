"""
Adiciona "Sujeira" aos Dados - Datathon Ribeirania
Torna os dados mais realistas e desafiadores

PROBLEMAS ADICIONADOS:
1. Valores ausentes (NaN)
2. Duplicatas
3. Outliers extremos
4. Dados inconsistentes
5. Erros de formatação
6. Timestamps faltantes
7. Usernames com caracteres especiais
8. Posts vazios ou quebrados
"""

import pandas as pd
import numpy as np
from datetime import timedelta
import random
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print(" ADICIONANDO 'SUJEIRA' AOS DADOS")
print("=" * 70)

# Configurações de ruído (porcentagens) que vão ser adicionadas
# Me baseiei em problemas reais de datasets públicos que já trabalhei em cima 
# As %s foram arbitrárias mas razoavelmente realistas para o tamanho dos datasets
# Como padrão, as %s podem ser ajustadas conforme necessário

NOISE_CONFIG = {
    'missing_data_pct': 0.03,      # 3% de dados faltantes
    'duplicates_pct': 0.02,         # 2% de duplicatas
    'outliers_pct': 0.015,          # 1.5% de outliers
    'inconsistent_pct': 0.025,      # 2.5% de inconsistências
    'format_errors_pct': 0.02,      # 2% de erros de formato
}
# 1° Função: suja a base de dados do Xister

def add_noise_to_xister(df):
    """Adiciona ruído realista aos posts do Xister"""
    print("\n📱 Sujando dados do Xister...")
    
    df_dirty = df.copy()
    total_rows = len(df_dirty)
    
    # 1. VALORES AUSENTES (NaN)
    n_missing = int(total_rows * NOISE_CONFIG['missing_data_pct'])
    
    # Likes faltantes
    missing_likes = np.random.choice(df_dirty.index, size=n_missing//4, replace=False)
    df_dirty.loc[missing_likes, 'likes'] = np.nan
    
    # Sentiment faltante
    missing_sent = np.random.choice(df_dirty.index, size=n_missing//4, replace=False)
    df_dirty.loc[missing_sent, 'sentiment'] = np.nan
    
    # Username faltante
    missing_user = np.random.choice(df_dirty.index, size=n_missing//4, replace=False)
    df_dirty.loc[missing_user, 'username'] = np.nan
    
    # Text faltante ou vazio
    missing_text = np.random.choice(df_dirty.index, size=n_missing//4, replace=False)
    df_dirty.loc[missing_text, 'text'] = ''
    
    print(f"  ✓ Adicionados {n_missing} valores ausentes")
    
    # 2. DUPLICATAS
    n_duplicates = int(total_rows * NOISE_CONFIG['duplicates_pct'])
    duplicate_indices = np.random.choice(df_dirty.index, size=n_duplicates, replace=False)
    duplicates = df_dirty.loc[duplicate_indices].copy()
    
    # Algumas duplicatas exatas
    df_dirty = pd.concat([df_dirty, duplicates.iloc[:n_duplicates//2]], ignore_index=True)
    
    # Algumas duplicatas com leve modificação
    duplicates_modified = duplicates.iloc[n_duplicates//2:].copy()
    duplicates_modified['likes'] = duplicates_modified['likes'] + np.random.randint(-5, 5, len(duplicates_modified))
    df_dirty = pd.concat([df_dirty, duplicates_modified], ignore_index=True)
    
    print(f"  ✓ Adicionadas {n_duplicates} duplicatas")
    
    # 3. OUTLIERS EXTREMOS
    n_outliers = int(total_rows * NOISE_CONFIG['outliers_pct'])
    
    # Likes absurdos
    outlier_likes = np.random.choice(df_dirty.index, size=n_outliers//3, replace=False)
    df_dirty.loc[outlier_likes, 'likes'] = np.random.randint(500000, 10000000, len(outlier_likes))
    
    # Reposts negativos (erro)
    outlier_reposts = np.random.choice(df_dirty.index, size=n_outliers//3, replace=False)
    df_dirty.loc[outlier_reposts, 'reposts'] = np.random.randint(-100, -1, len(outlier_reposts))
    
    # Sentiment fora do range
    outlier_sent = np.random.choice(df_dirty.index, size=n_outliers//3, replace=False)
    df_dirty.loc[outlier_sent, 'sentiment'] = np.random.uniform(-5, 5, len(outlier_sent))
    
    print(f"  ✓ Adicionados {n_outliers} outliers extremos")
    
    # 4. INCONSISTÊNCIAS
    n_inconsistent = int(total_rows * NOISE_CONFIG['inconsistent_pct'])
    
    # Posts com muito engagement mas sentiment negativo (suspeito)
    inconsistent_idx = np.random.choice(df_dirty.index, size=n_inconsistent//2, replace=False)
    df_dirty.loc[inconsistent_idx, 'sentiment'] = -0.8
    df_dirty.loc[inconsistent_idx, 'likes'] = np.random.randint(10000, 50000, len(inconsistent_idx))
    
    # Bots com muito engagement (suspeito)
    bot_mask = df_dirty['account_type'] == 'bot'
    suspicious_bots = df_dirty[bot_mask].sample(min(n_inconsistent//2, bot_mask.sum()))
    df_dirty.loc[suspicious_bots.index, 'likes'] = np.random.randint(5000, 20000, len(suspicious_bots))
    
    print(f"  ✓ Adicionadas {n_inconsistent} inconsistências")
    
    # 5. ERROS DE FORMATO
    n_format_errors = int(total_rows * NOISE_CONFIG['format_errors_pct'])
    
    # Usernames com caracteres especiais estranhos
    format_errors = np.random.choice(df_dirty.index, size=n_format_errors//3, replace=False)
    for idx in format_errors:
        if pd.notna(df_dirty.loc[idx, 'username']):
            df_dirty.loc[idx, 'username'] = df_dirty.loc[idx, 'username'] + random.choice(['@@', '##', '$$', '!!', '??'])
    
    # Timestamps faltantes (convertidos para string quebrada)
    missing_ts = np.random.choice(df_dirty.index, size=n_format_errors//3, replace=False)
    df_dirty.loc[missing_ts, 'timestamp'] = 'ERRO'
    
    # Account type inválido
    invalid_type = np.random.choice(df_dirty.index, size=n_format_errors//3, replace=False)
    df_dirty.loc[invalid_type, 'account_type'] = random.choice(['unknown', 'ERRO', '', 'NULL', 'deleted'])
    
    print(f"  ✓ Adicionados {n_format_errors} erros de formato")
    
    # 6. EMBARALHA LINHAS
    df_dirty = df_dirty.sample(frac=1).reset_index(drop=True)
    
    print(f"\n  📊 Resumo Xister:")
    print(f"    - Linhas originais: {total_rows:,}")
    print(f"    - Linhas com ruído: {len(df_dirty):,}")
    print(f"    - NaN em likes: {df_dirty['likes'].isna().sum()}")
    print(f"    - NaN em sentiment: {df_dirty['sentiment'].isna().sum()}")
    print(f"    - Posts vazios: {(df_dirty['text'] == '').sum()}")
    print(f"    - Usernames inválidos: {df_dirty['username'].isna().sum()}")
    
    return df_dirty

# 2° Função: suja as bases de dados de Crypto

def add_noise_to_crypto(df, coin_name):
    """Adiciona ruído aos dados de crypto"""
    print(f"\n💰 Sujando dados de {coin_name}...")
    
    df_dirty = df.copy()
    total_rows = len(df_dirty)
    
    # 1. VALORES AUSENTES
    n_missing = int(total_rows * NOISE_CONFIG['missing_data_pct'])
    
    # Preço faltante
    missing_price = np.random.choice(df_dirty.index, size=n_missing//3, replace=False)
    df_dirty.loc[missing_price, 'price_usd'] = np.nan
    
    # Volume faltante
    missing_vol = np.random.choice(df_dirty.index, size=n_missing//3, replace=False)
    df_dirty.loc[missing_vol, 'volume_24h'] = np.nan
    
    # Market cap zerado
    missing_mc = np.random.choice(df_dirty.index, size=n_missing//3, replace=False)
    df_dirty.loc[missing_mc, 'market_cap'] = 0
    
    print(f"  ✓ Adicionados {n_missing} valores ausentes")
    
    # 2. OUTLIERS
    n_outliers = int(total_rows * NOISE_CONFIG['outliers_pct'])
    
    # Preços absurdos
    outlier_price = np.random.choice(df_dirty.index, size=n_outliers//2, replace=False)
    df_dirty.loc[outlier_price, 'price_usd'] = df_dirty.loc[outlier_price, 'price_usd'] * np.random.uniform(50, 200, len(outlier_price))
    
    # Variações impossíveis
    outlier_change = np.random.choice(df_dirty.index, size=n_outliers//2, replace=False)
    df_dirty.loc[outlier_change, 'price_change_pct'] = np.random.uniform(-99, 99, len(outlier_change))
    
    print(f"  ✓ Adicionados {n_outliers} outliers")
    
    # 3. DUPLICATAS DE TIMESTAMP
    n_duplicates = int(total_rows * NOISE_CONFIG['duplicates_pct'])
    duplicate_indices = np.random.choice(df_dirty.index, size=n_duplicates, replace=False)
    duplicates = df_dirty.loc[duplicate_indices].copy()
    
    # Modifica levemente os preços mas mantém timestamp
    duplicates['price_usd'] = duplicates['price_usd'] * np.random.uniform(0.95, 1.05, len(duplicates))
    df_dirty = pd.concat([df_dirty, duplicates], ignore_index=True)
    
    print(f"  ✓ Adicionadas {n_duplicates} duplicatas de timestamp")
    
    # 4. TIMESTAMPS QUEBRADOS
    n_format_errors = int(total_rows * NOISE_CONFIG['format_errors_pct'])
    format_errors = np.random.choice(df_dirty.index, size=n_format_errors, replace=False)
    df_dirty.loc[format_errors, 'timestamp'] = 'INVALID_DATE'
    
    print(f"  ✓ Adicionados {n_format_errors} timestamps inválidos")
    
    # 5. VALORES NEGATIVOS INVÁLIDOS
    n_negative = int(total_rows * 0.01)
    negative_idx = np.random.choice(df_dirty.index, size=n_negative, replace=False)
    df_dirty.loc[negative_idx, 'price_usd'] = -abs(df_dirty.loc[negative_idx, 'price_usd'])
    
    print(f"  ✓ Adicionados {n_negative} preços negativos")
    
    # 6. EMBARALHA
    df_dirty = df_dirty.sample(frac=1).reset_index(drop=True)
    
    print(f"\n  📊 Resumo {coin_name}:")
    print(f"    - Linhas originais: {total_rows:,}")
    print(f"    - Linhas com ruído: {len(df_dirty):,}")
    print(f"    - NaN em price: {df_dirty['price_usd'].isna().sum()}")
    print(f"    - NaN em volume: {df_dirty['volume_24h'].isna().sum()}")
    print(f"    - Preços negativos: {(df_dirty['price_usd'] < 0).sum()}")
    print(f"    - Timestamps inválidos: {(df_dirty['timestamp'] == 'INVALID_DATE').sum()}")
    
    return df_dirty

# 3° Função: suja a base de dados de Eventos

def add_noise_to_events(df):
    """Adiciona ruído aos eventos"""
    print(f"\n📅 Sujando dados de Eventos...")
    
    df_dirty = df.copy()
    
    # 1. Datas duplicadas
    duplicate_event = df_dirty.sample(2)
    df_dirty = pd.concat([df_dirty, duplicate_event], ignore_index=True)
    
    # 2. Eventos com datas inválidas
    invalid_dates = df_dirty.sample(2)
    df_dirty.loc[invalid_dates.index, 'date'] = 'DATA_INVALIDA'
    
    # 3. Intensidades fora do range
    invalid_intensity = df_dirty.sample(3)
    df_dirty.loc[invalid_intensity.index, 'impact_intensity'] = np.random.uniform(2, 10, len(invalid_intensity))
    
    # 4. Campos vazios
    empty_fields = df_dirty.sample(2)
    df_dirty.loc[empty_fields.index, 'event_description'] = ''
    
    print(f"  ✓ Adicionados eventos duplicados, datas inválidas e campos vazios")
    
    return df_dirty

# Função Principal para criação e salvamento dos dados sujos
# Esses dados foram os que dei upload para a base de dados do Datathon, só troquei o nome, obviamente, pra não deixar
# tão óbvio que as bases estão sujas e com outliers e erros

def main():
    print("\nCarregando dados limpos...")
    
    try:
        # Carrega dados limpos
        xister = pd.read_csv('xister_posts.csv', encoding='utf-8-sig')
        solana = pd.read_csv('solana_prices.csv', encoding='utf-8-sig')
        ribercoin = pd.read_csv('ribercoin_prices.csv', encoding='utf-8-sig')
        neuroncoin = pd.read_csv('neuroncoin_prices.csv', encoding='utf-8-sig')
        bonfimcoin = pd.read_csv('bonfimcoin_prices.csv', encoding='utf-8-sig')
        zephyrcoin = pd.read_csv('zephyrcoin_prices.csv', encoding='utf-8-sig')
        lunartoken = pd.read_csv('lunartoken_prices.csv', encoding='utf-8-sig')
        events = pd.read_csv('ribeirania_events.csv', encoding='utf-8-sig')
        
        print("✓ Dados limpos carregados")
        
    except FileNotFoundError:
        print("❌ ERRO: Execute 'python main_generator.py' primeiro!")
        return
    
    print("\n" + "=" * 70)
    print(" ADICIONANDO RUÍDO")
    print("=" * 70)
    
    # Adiciona ruído
    xister_dirty = add_noise_to_xister(xister)
    solana_dirty = add_noise_to_crypto(solana, 'Solana')
    ribercoin_dirty = add_noise_to_crypto(ribercoin, 'RiberCoin')
    neuroncoin_dirty = add_noise_to_crypto(neuroncoin, 'NeuronCoin')
    bonfimcoin_dirty = add_noise_to_crypto(bonfimcoin, 'BonfimCoin')
    zephyrcoin_dirty = add_noise_to_crypto(zephyrcoin, 'ZephyrCoin')
    lunartoken_dirty = add_noise_to_crypto(lunartoken, 'LunarToken')
    events_dirty = add_noise_to_events(events)
    
    # Salva versões sujas
    print("\n" + "=" * 70)
    print(" SALVANDO DADOS SUJOS")
    print("=" * 70)
    
    xister_dirty.to_csv('xister_posts_dirty.csv', index=False, encoding='utf-8-sig')
    solana_dirty.to_csv('solana_prices_dirty.csv', index=False, encoding='utf-8-sig')
    ribercoin_dirty.to_csv('ribercoin_prices_dirty.csv', index=False, encoding='utf-8-sig')
    neuroncoin_dirty.to_csv('neuroncoin_prices_dirty.csv', index=False, encoding='utf-8-sig')
    bonfimcoin_dirty.to_csv('bonfimcoin_prices_dirty.csv', index=False, encoding='utf-8-sig')
    zephyrcoin_dirty.to_csv('zephyrcoin_prices_dirty.csv', index=False, encoding='utf-8-sig')
    lunartoken_dirty.to_csv('lunartoken_prices_dirty.csv', index=False, encoding='utf-8-sig')
    events_dirty.to_csv('ribeirania_events_dirty.csv', index=False, encoding='utf-8-sig')
    
    print("\n✓ Dados sujos salvos (*_dirty.csv)")
    
    # Mantém originais como "gabarito"
    print("\n💡 Os arquivos originais foram mantidos como GABARITO")
    print("   Use os arquivos *_dirty.csv para o datathon!")
    
    print("\n" + "=" * 70)
    print(" ✅ SUJEIRA ADICIONADA COM SUCESSO!")
    print("=" * 70)
    
    print("\n📂 Arquivos para Datathon (SUJOS):")
    print("  1. xister_posts_dirty.csv")
    print("  2. solana_prices_dirty.csv")
    print("  3. ribercoin_prices_dirty.csv")
    print("  4. neuroncoin_prices_dirty.csv")
    print("  5. bonfimcoin_prices_dirty.csv")
    print("  6. zephyrcoin_prices_dirty.csv")
    print("  7. lunartoken_prices_dirty.csv")
    print("  8. ribeirania_events_dirty.csv")
    
    print("\n📂 Arquivos LIMPOS (Gabarito - NÃO distribua!):")
    print("  - xister_posts.csv")
    print("  - *_prices.csv (originais)")
    
    print("\n🎯 Problemas adicionados:")
    print("  ✓ Valores ausentes (NaN)")
    print("  ✓ Duplicatas")
    print("  ✓ Outliers extremos")
    print("  ✓ Inconsistências nos dados")
    print("  ✓ Erros de formatação")
    print("  ✓ Timestamps inválidos")
    print("  ✓ Usernames com caracteres especiais")
    print("  ✓ Valores negativos inválidos")
    print("  ✓ Posts vazios")
    
    print("\n💪 Desafios para os participantes:")
    print("  - Detectar e remover duplicatas")
    print("  - Tratar valores ausentes")
    print("  - Identificar e remover outliers")
    print("  - Corrigir timestamps inválidos")
    print("  - Validar ranges de valores")
    print("  - Limpar usernames")
    print()

if __name__ == '__main__':
    main()