"""
Baixador de Dados Reais do Solana - Datathon Ribeirania
Baixa dados históricos REAIS do Solana via Yahoo Finance (yfinance)
Sem necessidade de API key!

Execute ANTES do main_generator.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)
TARGET_RECORDS = 50000

# ============================================================================
# FUNÇÃO: BAIXAR DO YAHOO FINANCE
# ============================================================================

def fetch_from_yfinance():
    """
    Baixa dados históricos do Solana via yfinance
    Ticker: SOL-USD
    100% gratuito, sem API key necessária
    """
    print("\n" + "=" * 70)
    print(" BAIXANDO DADOS REAIS DO SOLANA (Yahoo Finance)")
    print("=" * 70)
    
    try:
        import yfinance as yf
    except ImportError:
        print("\n❌ Biblioteca yfinance não instalada!")
        print("\nInstale com: pip install yfinance")
        return None
    
    print(f"\nBaixando dados do ticker SOL-USD...")
    print(f"Período: {START_DATE.date()} até {END_DATE.date()}")
    
    try:
        # Baixa dados do Solana
        ticker = yf.Ticker("SOL-USD")
        df = ticker.history(
            start=START_DATE.strftime('%Y-%m-%d'),
            end=END_DATE.strftime('%Y-%m-%d'),
            interval='1d'
        )
        
        if df.empty:
            print("\n❌ Nenhum dado retornado!")
            print("Tentando ticker alternativo: SOLUSD...")
            
            # Tenta ticker alternativo
            ticker = yf.Ticker("SOLUSD")
            df = ticker.history(
                start=START_DATE.strftime('%Y-%m-%d'),
                end=END_DATE.strftime('%Y-%m-%d'),
                interval='1d'
            )
        
        if df.empty:
            print("\n❌ Nenhum dado encontrado para Solana!")
            print("Tente usar a opção de CSV manual.")
            return None
        
        print(f"✓ Dados baixados: {len(df):,} registros")
        
        # Processa dados
        df = df.reset_index()
        df = df.rename(columns={
            'Date': 'timestamp',
            'Close': 'price_usd',
            'Volume': 'volume_24h'
        })
        
        # Adiciona informações da moeda
        df['coin_name'] = 'Solana'
        df['symbol'] = 'SOL'
        
        # Estima market cap (supply aproximado: 400M SOL)
        df['market_cap'] = df['price_usd'] * 400000000
        
        # Calcula variação percentual
        df['price_change_pct'] = df['price_usd'].pct_change() * 100
        df['price_change_pct'].fillna(0, inplace=True)
        
        # Remove dados nulos
        df = df.dropna(subset=['price_usd'])
        
        # Seleciona colunas
        df = df[['timestamp', 'coin_name', 'symbol', 'price_usd', 'volume_24h', 'market_cap', 'price_change_pct']]
        
        # Ordena por data
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        print(f"\n✓ Dados processados!")
        print(f"  - Total de registros: {len(df):,}")
        print(f"  - Período: {df['timestamp'].min().date()} até {df['timestamp'].max().date()}")
        print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.2f}")
        print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.2f}")
        print(f"  - Preço mínimo: ${df['price_usd'].min():.2f}")
        print(f"  - Preço máximo: ${df['price_usd'].max():.2f}")
        
        # Verifica dados quebrados
        null_count = df[['price_usd', 'volume_24h']].isnull().sum().sum()
        if null_count > 0:
            print(f"\n⚠ Aviso: {null_count} valores nulos encontrados e removidos")
        
        return df
        
    except Exception as e:
        print(f"\n❌ ERRO ao baixar dados: {e}")
        print("\nPossíveis soluções:")
        print("  1. Verifique sua conexão com internet")
        print("  2. Instale/atualize yfinance: pip install --upgrade yfinance")
        print("  3. Use a opção de CSV manual")
        return None

# ============================================================================
# FUNÇÃO: IMPORTAR DE CSV
# ============================================================================

def load_from_csv(filepath):
    """
    Carrega dados do Solana de um CSV fornecido pelo usuário
    
    CSV deve ter as colunas:
    - timestamp (ou date/time)
    - price (ou price_usd/close)
    - volume (opcional)
    - market_cap (opcional)
    """
    print("\n" + "=" * 70)
    print(" CARREGANDO DADOS DO SOLANA DE CSV")
    print("=" * 70)
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        print(f"\n✓ CSV carregado: {len(df):,} linhas")
        
        # Mostra colunas encontradas
        print(f"\nColunas encontradas: {list(df.columns)}")
        
        # Mapeia colunas automaticamente
        column_mapping = {}
        
        # Timestamp/Date
        for col in df.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['time', 'date', 'data']):
                column_mapping['timestamp'] = col
                break
        
        # Price
        for col in df.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['price', 'close', 'preco', 'valor']):
                column_mapping['price_usd'] = col
                break
        
        # Volume
        for col in df.columns:
            col_lower = col.lower()
            if 'volume' in col_lower or 'vol' in col_lower:
                column_mapping['volume_24h'] = col
                break
        
        # Market Cap
        for col in df.columns:
            col_lower = col.lower()
            if ('market' in col_lower or 'cap' in col_lower) and 'market' in col_lower:
                column_mapping['market_cap'] = col
                break
        
        if 'timestamp' not in column_mapping or 'price_usd' not in column_mapping:
            print("\n❌ ERRO: Não consegui identificar colunas de timestamp e preço")
            print("\nCertifique-se que o CSV tem colunas como:")
            print("  - timestamp/date/time/data")
            print("  - price/price_usd/close/preco")
            return None
        
        # Renomeia colunas
        df = df.rename(columns=column_mapping)
        
        # Converte timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filtra período desejado
        df = df[(df['timestamp'] >= START_DATE) & (df['timestamp'] <= END_DATE)]
        
        print(f"\n✓ Dados filtrados para o período: {len(df):,} registros")
        
        # Adiciona colunas faltantes
        df['coin_name'] = 'Solana'
        df['symbol'] = 'SOL'
        
        if 'volume_24h' not in df.columns:
            # Estima volume baseado em preço
            df['volume_24h'] = df['price_usd'] * np.random.uniform(500000, 2000000, len(df))
            print("⚠ Volume não encontrado, usando estimativa")
        
        if 'market_cap' not in df.columns:
            # Estima market cap (supply ~400M SOL)
            df['market_cap'] = df['price_usd'] * 400000000
            print("⚠ Market cap não encontrado, usando estimativa")
        
        # Remove linhas com preço nulo
        df = df.dropna(subset=['price_usd'])
        
        # Calcula variação percentual
        df['price_change_pct'] = df['price_usd'].pct_change() * 100
        df['price_change_pct'].fillna(0, inplace=True)
        
        # Ordena por data
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Reordena colunas
        df = df[['timestamp', 'coin_name', 'symbol', 'price_usd', 'volume_24h', 'market_cap', 'price_change_pct']]
        
        print(f"\n✓ Dados processados!")
        print(f"  - Total de registros: {len(df):,}")
        print(f"  - Período: {df['timestamp'].min().date()} até {df['timestamp'].max().date()}")
        print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.2f}")
        print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.2f}")
        
        return df
        
    except FileNotFoundError:
        print(f"\n❌ ERRO: Arquivo não encontrado: {filepath}")
        return None
    except Exception as e:
        print(f"\n❌ ERRO ao processar CSV: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# FUNÇÃO: INTERPOLA PARA 50K REGISTROS
# ============================================================================

def interpolate_to_target(df, target_records=TARGET_RECORDS):
    """
    Interpola os dados para atingir exatamente 50.000 registros
    Preenche gaps e cria série temporal uniforme
    """
    current_records = len(df)
    
    print(f"\n" + "-" * 70)
    print(f"Interpolando de {current_records:,} para {target_records:,} registros...")
    print("-" * 70)
    
    if current_records >= target_records:
        # Se já tem mais que o necessário, faz amostragem uniforme
        indices = np.linspace(0, current_records - 1, target_records, dtype=int)
        df_final = df.iloc[indices].reset_index(drop=True)
        print(f"✓ Amostragem realizada")
    else:
        # Se tem menos, interpola para preencher gaps
        # Cria timestamps uniformemente espaçados
        new_timestamps = pd.date_range(
            start=df['timestamp'].min(),
            end=df['timestamp'].max(),
            periods=target_records
        )
        
        # Cria novo DataFrame
        df_final = pd.DataFrame({'timestamp': new_timestamps})
        
        # Converte para valores numéricos para interpolação
        df_temp = df.copy()
        df_temp['timestamp_numeric'] = df_temp['timestamp'].astype(np.int64)
        
        new_timestamps_numeric = new_timestamps.astype(np.int64)
        
        # Interpola cada coluna numérica
        for col in ['price_usd', 'volume_24h', 'market_cap']:
            if col in df_temp.columns:
                df_final[col] = np.interp(
                    new_timestamps_numeric,
                    df_temp['timestamp_numeric'],
                    df_temp[col]
                )
        
        # Adiciona colunas constantes
        df_final['coin_name'] = 'Solana'
        df_final['symbol'] = 'SOL'
        
        # Recalcula variação percentual
        df_final['price_change_pct'] = df_final['price_usd'].pct_change() * 100
        df_final['price_change_pct'].fillna(0, inplace=True)
        
        print(f"✓ Interpolação concluída")
    
    # Reordena colunas
    df_final = df_final[['timestamp', 'coin_name', 'symbol', 'price_usd', 'volume_24h', 'market_cap', 'price_change_pct']]
    
    return df_final

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    print("=" * 70)
    print(" OBTENÇÃO DE DADOS REAIS DO SOLANA")
    print("=" * 70)
    print("\nEscolha uma opção:\n")
    print("1. Baixar do Yahoo Finance via yfinance (RECOMENDADO)")
    print("2. Usar CSV fornecido por mim")
    print("3. Sair")
    
    choice = input("\nOpção (1/2/3): ").strip()
    
    df = None
    
    if choice == '1':
        df = fetch_from_yfinance()
        
    elif choice == '2':
        filepath = input("\nCaminho do arquivo CSV: ").strip()
        # Remove aspas se o usuário colou o caminho com aspas
        filepath = filepath.strip('"').strip("'")
        df = load_from_csv(filepath)
        
    elif choice == '3':
        print("\nSaindo...")
        return
    else:
        print("\n❌ Opção inválida!")
        return
    
    if df is None:
        print("\n❌ Falha ao obter dados!")
        return
    
    # Interpola para 50k registros
    df_final = interpolate_to_target(df, TARGET_RECORDS)
    
    # Salva CSV
    output_file = 'solana_prices.csv'
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n" + "=" * 70)
    print(" ✅ DADOS DO SOLANA SALVOS COM SUCESSO!")
    print("=" * 70)
    print(f"\n📂 Arquivo criado: {output_file}")
    print(f"  - Total de registros: {len(df_final):,}")
    print(f"  - Período: {df_final['timestamp'].min().date()} até {df_final['timestamp'].max().date()}")
    print(f"  - Preço inicial: ${df_final['price_usd'].iloc[0]:.2f}")
    print(f"  - Preço final: ${df_final['price_usd'].iloc[-1]:.2f}")
    print(f"  - Preço mínimo: ${df_final['price_usd'].min():.2f}")
    print(f"  - Preço máximo: ${df_final['price_usd'].max():.2f}")
    print(f"  - Variação total: {((df_final['price_usd'].iloc[-1] / df_final['price_usd'].iloc[0]) - 1) * 100:+.1f}%")
    
    print("\n💡 Próximo passo:")
    print("  Execute: python main_generator.py")
    print()

if __name__ == '__main__':
    main()
    