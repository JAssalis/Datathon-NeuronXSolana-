import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 1° parte do código
# Feita para setar os 1°s parâmetros, deixado de modo personalizável para melhor adaptação da base

START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2024, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1

# Tamanhos dos datasets
XISTER_POSTS = 100000
CRYPTO_PRICES = 100000

# Originalmente, o código só gerava os dados da Solana e RiberCoin, porém, considerando o nível de complexidado, quis
# decidi adicionar mais 2 moedas

ADDITIONAL_COINS = True  

# Código feito para rodar no terminal linux, já que é meu sistema principal

print("=" * 70)
print(" GERADOR PRINCIPAL - DATATHON RIBEIRANIA")
print("=" * 70)
print(f"\nPeríodo: {START_DATE.date()} até {END_DATE.date()}")
print(f"Total de dias: {TOTAL_DAYS}")
print(f"Registros por database: ~{XISTER_POSTS:,}\n")


# Gerador dos preços das criptomoedas
# Os eventos foram criados em arquivo CSV separado, facilitando a edição, personalização e adição de novos eventos

class CryptoGenerator:
    #Gera séries temporais de preços de criptomoedas com eventos
    def __init__(self, coin_name, symbol, start_price, volatility, trend='stable'):
        self.coin_name = coin_name
        self.symbol = symbol
        self.current_price = start_price
        self.volatility = volatility
        self.trend = trend
        self.events = []
        
    def add_event(self, date, impact_type, intensity, duration_hours):
        #Adiciona evento que afeta o preço
        self.events.append({
            'date': pd.to_datetime(date),
            'impact_type': impact_type,
            'intensity': intensity,
            'duration_hours': duration_hours
        })
    
    def get_event_impact(self, current_date):
        #Calcula impacto de eventos ativos na data atual
        total_impact = 0
        
        for event in self.events:
            event_date = event['date']
            duration = timedelta(hours=event['duration_hours'])
            
            if event_date <= current_date <= event_date + duration:
                # Calcula progresso dentro do evento (0 a 1)
                progress = (current_date - event_date) / duration
                
                if event['impact_type'] == 'pump':
                    # PUMP: Sobe rápido nos primeiros 25%, mantém até 50%, depois desce
                    if progress < 0.25:
                        impact = event['intensity'] * 2.0 * (progress / 0.25)
                    elif progress < 0.5:
                        impact = event['intensity'] * 2.0
                    else:
                        impact = event['intensity'] * 2.0 * (1 - (progress - 0.5) / 0.5)
                    total_impact += impact
                    
                elif event['impact_type'] == 'crash':
                    # CRASH: Cai rápido nos primeiros 20%, recupera gradualmente
                    if progress < 0.2:
                        impact = -event['intensity'] * 1.5 * (progress / 0.2)
                    else:
                        impact = -event['intensity'] * 1.5 * (1 - (progress - 0.2) / 0.8 * 0.6)
                    total_impact += impact
                    
                elif event['impact_type'] == 'slight_pump':
                    # PUMP LEVE: Subida moderada
                    impact = event['intensity'] * 1.0 * (1 - progress * 0.7)
                    total_impact += impact
                    
                elif event['impact_type'] == 'slight_crash':
                    # CRASH LEVE: Queda moderada
                    impact = -event['intensity'] * 1.0 * (1 - progress * 0.7)
                    total_impact += impact
        
        # Limita o impacto total de forma realista
        return np.clip(total_impact, -0.8, 1.2)
    
    def generate_prices(self, num_records):
        """Gera série temporal de preços"""
        timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
        prices = []
        volumes = []
        market_caps = []
        
        for ts in timestamps:
            # 1. Impacto de eventos
            event_impact = self.get_event_impact(ts)
            
            # 2. Tendência de longo prazo
            if self.trend == 'bullish':
                trend_factor = 1.0001  # +0.01% por período
            elif self.trend == 'bearish':
                trend_factor = 0.9999  # -0.01% por período
            else:
                trend_factor = 1.0  # Estável
            
            # 3. Volatilidade normal (ruído aleatório)
            random_change = np.random.normal(0, self.volatility)
            
            # 4. Calcula novo preço
            change = (1 + random_change + event_impact) * trend_factor
            self.current_price *= change
            
            # Evita preços negativos ou muito baixos
            self.current_price = max(self.current_price, 0.0001)
            
            prices.append(self.current_price)
            
            # 5. Volume (aumenta com volatilidade e eventos)
            base_volume = 1000000 * (1 + abs(event_impact) * 5)
            volume = base_volume * np.random.uniform(0.5, 2.0)
            volumes.append(volume)
            
            # 6. Market cap (preço * supply fixo)
            supply = 1000000000  # 1 bilhão de moedas
            market_cap = self.current_price * supply
            market_caps.append(market_cap)
        
        # Cria DataFrame
        df = pd.DataFrame({
            'timestamp': timestamps,
            'coin_name': self.coin_name,
            'symbol': self.symbol,
            'price_usd': prices,
            'volume_24h': volumes,
            'market_cap': market_caps
        })
        
        # Calcula variação percentual
        df['price_change_pct'] = df['price_usd'].pct_change() * 100
        df['price_change_pct'].fillna(0, inplace=True)
        
        return df


# Gerador dos posts do Xister
# Utiliza templates tanto de "xists" comuns quanto de influenciadores, empresas e bots
# Considera eventos locais para ajustar o sentiment dos posts
# Também correlaciona posts sobre criptomoedas com os preços gerados

class XisterGenerator:
    #Gera posts da rede social Xister em português
    
    def __init__(self, templates_file, events_file):
        self.templates = pd.read_csv(templates_file, encoding='utf-8-sig')
        self.events = pd.read_csv(events_file, encoding='utf-8-sig')
        self.events['date'] = pd.to_datetime(self.events['date'], errors='coerce')
        
        # Remove eventos com datas inválidas
        self.events = self.events[self.events['date'].notna()]
        
        # Usernames brasileiros
        self.usernames = self._generate_usernames()
        self.account_types = ['regular', 'influencer', 'company', 'bot']
        
    def _generate_usernames(self):
        """Gera usernames realistas brasileiros"""
        names = ['joao', 'maria', 'pedro', 'ana', 'lucas', 'julia', 'carlos', 
                 'beatriz', 'rafael', 'fernanda', 'bruno', 'camila', 'thiago',
                 'larissa', 'gustavo', 'amanda', 'felipe', 'jessica', 'rodrigo',
                 'patricia', 'diego', 'renata', 'vitor', 'mariana', 'daniel',
                 'isabela', 'matheus', 'leticia', 'gabriel', 'carolina']
        
        suffixes = ['', '_oficial', '_rp', '_real', 'crypto', 'invest', 
                   '2024', 'BR', '_ribeirania', '_trader', 'tech', '_news',
                   '_br', '123', '456', '_oficial']
        
        usernames = []
        for _ in range(1000):
            name = np.random.choice(names)
            suffix = np.random.choice(suffixes)
            number = np.random.randint(0, 999) if np.random.random() > 0.6 else ''
            username = f"{name}{suffix}{number}"
            usernames.append(username)
        
        # Adiciona contas especiais/verificadas
        special_accounts = [
            'prefeitura_ribeirania', 'riberanianews', 'ribercoin_oficial',
            'cryptoribeirania', 'investidor_rp', 'tech_ribeirania',
            'riberaniaoficial', 'prefeito_ribeirania', 'camara_ribeirania',
            'jornal_ribeirania', 'radio_ribeirania', 'tv_ribeirania'
        ]
        usernames.extend(special_accounts)
        
        return usernames
    
    def get_event_sentiment(self, date):
        """Retorna sentiment baseado em eventos próximos"""
        base_sentiment = 0
        count = 0
        
        for _, event in self.events.iterrows():
            if pd.isna(event['date']):
                continue
                
            event_date = event['date']
            duration = timedelta(hours=event['duration_hours'])
            
            # Verifica se a data está dentro do período do evento
            if event_date <= date <= event_date + duration:
                if event['affects_sentiment'] == 'SIM':
                    base_sentiment += event['sentiment']
                    count += 1
        
        return base_sentiment / count if count > 0 else 0
    
    def generate_posts(self, num_posts, ribercoin_prices=None):
        """Gera posts do Xister com correlação aos preços"""
        timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_posts)
        posts = []
        
        print(f"\nGerando {num_posts:,} posts do Xister...")
        
        for i, ts in enumerate(timestamps):
            # Progress report
            if i % 10000 == 0 and i > 0:
                print(f"  Progresso: {i:,}/{num_posts:,} posts ({i/num_posts*100:.1f}%)")
            
            # Seleciona template aleatório
            template = self.templates.sample(1).iloc[0]
            text = template['text']
            
            # Define account type (70% regular, 15% influencer, 10% company, 5% bot)
            account_type = np.random.choice(
                self.account_types,
                p=[0.70, 0.15, 0.10, 0.05]
            )
            
            # Username
            username = np.random.choice(self.usernames)
            
            # Sentiment base do template
            base_sentiment = template['sentiment_base']
            
            # Adiciona sentiment de eventos
            event_sentiment = self.get_event_sentiment(ts)
            
            # Se há preços de RiberCoin e é post sobre crypto, correlaciona
            sentiment_adjustment = 0
            if ribercoin_prices is not None and template['category'] == 'crypto':
                # Encontra preço mais próximo
                price_mask = ribercoin_prices['timestamp'] <= ts
                if price_mask.any():
                    closest_price = ribercoin_prices[price_mask].iloc[-1]
                    price_change = closest_price['price_change_pct']
                    # Ajusta sentiment baseado na variação de preço
                    sentiment_adjustment = np.clip(price_change / 100, -0.3, 0.3)
            
            # Sentiment final
            final_sentiment = base_sentiment + event_sentiment * 0.3 + sentiment_adjustment
            final_sentiment = np.clip(final_sentiment, -1, 1)
            
            # Likes e reposts baseados em sentiment e account type
            sentiment_multiplier = (final_sentiment + 1) / 2  # Normaliza para 0-1
            
            if account_type == 'company':
                base_likes = np.random.randint(1000, 50000)
                base_reposts = np.random.randint(100, 5000)
            elif account_type == 'influencer':
                base_likes = np.random.randint(500, 20000)
                base_reposts = np.random.randint(50, 2000)
            elif account_type == 'bot':
                base_likes = np.random.randint(0, 100)
                base_reposts = np.random.randint(0, 10)
            else:  # regular
                base_likes = np.random.randint(0, 500)
                base_reposts = np.random.randint(0, 50)
            
            # Aplica multiplicador de sentiment
            likes = int(base_likes * (0.5 + sentiment_multiplier))
            reposts = int(base_reposts * (0.5 + sentiment_multiplier))
            
            posts.append({
                'post_id': f"POST_{i+1:06d}",
                'username': username,
                'text': text,
                'timestamp': ts,
                'likes': likes,
                'reposts': reposts,
                'account_type': account_type,
                'sentiment': round(final_sentiment, 3)
            })
        
        df = pd.DataFrame(posts)
        print(f"✓ {num_posts:,} posts gerados com sucesso!")
        return df


# Gerador de preços das criptomoedas principais, incluindo Solana e RiberCoin
# Preços da solana foram coletados via yfinance e salvos em CSV para uso local 
# Evita chamadas repetidas à API e facilita a reprodução dos resultados

def load_solana_prices():
    """
    Carrega dados REAIS do Solana previamente baixados
    """
    print("\n" + "-" * 70)
    print("ETAPA 1/4: Carregando preços REAIS Solana (SOL)")
    print("-" * 70)
    
    try:
        df = pd.read_csv('solana_prices.csv', encoding='utf-8-sig')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', utc=True)
        # Remove timezone para compatibilidade
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        
        print(f"\n✓ Dados REAIS do Solana carregados!")
        print(f"  - Total de registros: {len(df):,}")
        print(f"  - Período: {df['timestamp'].min().date()} até {df['timestamp'].max().date()}")
        print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.2f}")
        print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.2f}")
        print(f"  - Preço mínimo: ${df['price_usd'].min():.2f}")
        print(f"  - Preço máximo: ${df['price_usd'].max():.2f}")
        print(f"  - Variação total: {((df['price_usd'].iloc[-1] / df['price_usd'].iloc[0]) - 1) * 100:.1f}%")
        
        return df
        
    except FileNotFoundError:
        print("\n❌ ERRO: Arquivo solana_prices.csv não encontrado!")
        print("\nExecute primeiro: python fetch_solana_data.py")
        print("para baixar os dados reais do Solana.\n")
        return None

def generate_ribercoin_prices(num_records, events_file):
    """Gera preços da RiberCoin reagindo a eventos de Ribeirania"""
    print("\n" + "-" * 70)
    print("ETAPA 2/4: Gerando preços RiberCoin (RBC)")
    print("-" * 70)
    
    # Lê eventos
    events_df = pd.read_csv(events_file, encoding='utf-8-sig')
    events_df['date'] = pd.to_datetime(events_df['date'], errors='coerce')
    events_df = events_df[events_df['date'].notna()]
    
    ribercoin = CryptoGenerator(
        coin_name='RiberCoin',
        symbol='RBC',
        start_price=0.08,  # Preço inicial realista
        volatility=0.035,  # Volatilidade moderada
        trend='bullish'
    )
    
    # Adiciona eventos
    events_added = 0
    for _, event in events_df.iterrows():
        if event['affects_ribercoin'] == 'SIM':
            ribercoin.add_event(
                event['date'],
                event['impact_type'],
                event['impact_intensity'],
                event['duration_hours']
            )
            events_added += 1
    
    # Gera preços com lógica personalizada de memecoins
    timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
    prices = []
    volumes = []
    market_caps = []
    
    # Parâmetros do ciclo de 3 meses
    days_per_cycle = 90  # 3 meses
    records_per_cycle = num_records / ((END_DATE - START_DATE).days / days_per_cycle)
    
    # Preço base que oscila ao longo do tempo
    base_price = 0.08
    
    for i, ts in enumerate(timestamps):
        # 1. CICLO DE 3 MESES (mean reversion)
        cycle_position = (i % records_per_cycle) / records_per_cycle
        
        # Preço "alvo" do ciclo atual (oscila entre 0.06 e 0.12)
        cycle_target = base_price * (0.75 + 0.5 * np.sin(2 * np.pi * cycle_position))
        cycle_target = np.clip(cycle_target, 0.05, 0.15)
        
        # 2. FORÇA DE MEAN REVERSION (puxa de volta para o ciclo)
        if i > 0:
            deviation = prices[-1] - cycle_target
            mean_reversion = -deviation * 0.08  # 8% de correção por período
        else:
            mean_reversion = 0
        
        # 3. IMPACTO DE EVENTOS (amplificado mas controlado)
        event_impact = ribercoin.get_event_impact(ts)
        
        # Durante evento, reduz mean reversion para deixar o pump/dump acontecer
        if abs(event_impact) > 0.1:
            mean_reversion *= 0.3  # Reduz força de reversão durante eventos
        
        # 4. RANDOM WALK DIÁRIO (0.02% a 0.05% para cima ou baixo)
        daily_change_pct = np.random.uniform(0.0002, 0.0005) * np.random.choice([-1, 1])
        
        # 5. VOLATILIDADE EXTRA EM EVENTOS
        if abs(event_impact) > 0.1:
            volatility_multiplier = 1 + abs(event_impact) * 2
            daily_change_pct *= volatility_multiplier
        
        # 6. SPIKES OCASIONAIS (típico de memecoin - 1% de chance)
        if np.random.random() < 0.01:
            spike = np.random.uniform(0.03, 0.08) * np.random.choice([-1, 1])
        else:
            spike = 0
        
        # CALCULA NOVO PREÇO
        if i == 0:
            ribercoin.current_price = base_price
        else:
            # Combina todos os fatores
            total_change = 1 + daily_change_pct + event_impact + mean_reversion + spike
            
            # Limita mudança máxima por período (±10%)
            total_change = np.clip(total_change, 0.90, 1.10)
            
            ribercoin.current_price = prices[-1] * total_change
        
        # LIMITES RÍGIDOS DE PREÇO
        ribercoin.current_price = np.clip(ribercoin.current_price, 0.003, 0.80)
        
        prices.append(ribercoin.current_price)
        
        # Volume (aumenta durante eventos e volatilidade)
        base_volume = 600000
        volume_multiplier = 1 + abs(event_impact) * 5 + abs(spike) * 3
        volume = base_volume * volume_multiplier * np.random.uniform(0.7, 1.3)
        volumes.append(volume)
        
        # Market cap
        supply = 500000000
        market_cap = ribercoin.current_price * supply
        market_caps.append(market_cap)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'coin_name': ribercoin.coin_name,
        'symbol': ribercoin.symbol,
        'price_usd': prices,
        'volume_24h': volumes,
        'market_cap': market_caps
    })
    
    # Calcula variação percentual
    df['price_change_pct'] = df['price_usd'].pct_change() * 100
    df['price_change_pct'].fillna(0, inplace=True)
    
    print(f"\n✓ Preços RiberCoin gerados!")
    print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.4f}")
    print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.4f}")
    print(f"  - Preço mínimo: ${df['price_usd'].min():.4f}")
    print(f"  - Preço máximo: ${df['price_usd'].max():.4f}")
    print(f"  - Variação total: {((df['price_usd'].iloc[-1] / df['price_usd'].iloc[0]) - 1) * 100:.1f}%")
    print(f"  - Volatilidade média: {df['price_change_pct'].std():.2f}%")
    print(f"  - Maior alta diária: {df['price_change_pct'].max():.2f}%")
    print(f"  - Maior queda diária: {df['price_change_pct'].min():.2f}%")
    print(f"  - Eventos aplicados: {events_added}")
    
    return df

def generate_neuroncoin_prices(num_records):
    """Gera preços da NeuronCoin (baixa volatilidade, tipo stablecoin)"""
    print("\n" + "-" * 70)
    print("ETAPA 3/7: Gerando preços NeuronCoin (NRC)")
    print("-" * 70)
    
    neuroncoin = CryptoGenerator(
        coin_name='NeuronCoin',
        symbol='NRC',
        start_price=1.00,  # Stablecoin perto de $1
        volatility=0.003,  # MUITO baixa volatilidade (0.3%)
        trend='stable'
    )
    
    # Apenas 2 eventos pequenos, já que a ideia da NeuronCoin é ser uma stablecoin
    neuroncoin.add_event('2022-06-01', 'slight_crash', 0.08, 720)
    neuroncoin.add_event('2023-12-01', 'slight_pump', 0.10, 1440)
    
    timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
    prices = []
    volumes = []
    market_caps = []
    
    target_price = 1.00  # Sempre tenta voltar para $1
    
    for i, ts in enumerate(timestamps):
        # 1. Impacto de eventos (muito reduzido)
        event_impact = neuroncoin.get_event_impact(ts) * 0.3  # Reduz impacto para 30%
        
        # 2. Mean reversion (sempre puxa de volta para $1)
        deviation = (neuroncoin.current_price - target_price) / target_price
        reversion = -deviation * 0.1  # Força de volta para $1
        
        # 3. Volatilidade mínima
        random_change = np.random.normal(0, neuroncoin.volatility)
        
        # Calcula novo preço
        total_change = (1 + random_change + event_impact * 0.5 + reversion)
        neuroncoin.current_price *= total_change
        
        # Mantém perto de $1
        neuroncoin.current_price = np.clip(neuroncoin.current_price, 0.85, 1.15)
        
        prices.append(neuroncoin.current_price)
        
        # Volume estável
        volume = 800000 * np.random.uniform(0.8, 1.2)
        volumes.append(volume)
        
        # Market cap
        supply = 1000000000
        market_cap = neuroncoin.current_price * supply
        market_caps.append(market_cap)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'coin_name': neuroncoin.coin_name,
        'symbol': neuroncoin.symbol,
        'price_usd': prices,
        'volume_24h': volumes,
        'market_cap': market_caps
    })
    
    # Calcula variação percentual
    df['price_change_pct'] = df['price_usd'].pct_change() * 100
    df['price_change_pct'].fillna(0, inplace=True)
    
    print(f"\n✓ Preços NeuronCoin gerados!")
    print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.2f}")
    print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.2f}")
    print(f"  - Volatilidade (std): ${df['price_usd'].std():.4f}")
    print(f"  - Variação total: {((df['price_usd'].iloc[-1] / df['price_usd'].iloc[0]) - 1) * 100:.1f}%")
    
    return df

def generate_bonfimcoin_prices(num_records, ribercoin_df):
    """
    Gera preços da BonfimCoin com CORRELAÇÃO NEGATIVA FORTE à RiberCoin
    Quando RBC sobe, BFC cai proporcionalmente e vice-versa
    """
    print("\n" + "-" * 70)
    print("ETAPA 4/7: Gerando preços BonfimCoin (BFC) - CORRELAÇÃO NEGATIVA FORTE")
    print("-" * 70)
    
    bonfimcoin = CryptoGenerator(
        coin_name='BonfimCoin',
        symbol='BFC',
        start_price=0.45,  # Ajustado para melhor visualização
        volatility=0.020,  # Reduzido para seguir mais RBC
        trend='stable'
    )
    
    timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
    prices = []
    volumes = []
    market_caps = []
    
    # Calcula retornos da RiberCoin
    rbc_returns = ribercoin_df['price_usd'].pct_change().fillna(0)
    
    # Preço base que ajusta ao longo do tempo
    base_price = 0.45
    
    for i, ts in enumerate(timestamps):
        # 1. INVERSÃO FORTE da variação da RiberCoin
        rbc_return = rbc_returns.iloc[i] if i < len(rbc_returns) else 0
        
        # Inverte 95% da variação da RBC (correlação muito forte)
        inverse_movement = -rbc_return * 0.95
        
        # 2. Volatilidade própria MÍNIMA (só 2% para não interferir)
        random_change = np.random.normal(0, bonfimcoin.volatility)
        
        # 3. Mean reversion FRACO (permite seguir RBC)
        if i > 0:
            deviation = (prices[-1] - base_price) / base_price
            mean_reversion = -deviation * 0.02  # Muito fraco
        else:
            mean_reversion = 0
        
        # 4. Ajuste do preço base ao longo do tempo (contraponto de RBC)
        # Se RBC está em tendência de alta, BFC em baixa
        if i > 100:
            rbc_trend = (ribercoin_df['price_usd'].iloc[i] / ribercoin_df['price_usd'].iloc[i-100]) - 1
            base_price *= (1 - rbc_trend * 0.002)  # Ajuste gradual oposto
        
        # Calcula novo preço
        if i == 0:
            bonfimcoin.current_price = 0.45
        else:
            total_change = (1 + inverse_movement + random_change * 0.3 + mean_reversion)
            
            # Limita mudanças extremas
            total_change = np.clip(total_change, 0.85, 1.15)
            
            bonfimcoin.current_price = prices[-1] * total_change
        
        # Limites amplos para permitir variação
        bonfimcoin.current_price = np.clip(bonfimcoin.current_price, 0.01, 2.00)
        prices.append(bonfimcoin.current_price)
        
        # Volume aumenta quando há divergência forte
        base_volume = 500000 * (1 + abs(inverse_movement) * 8)
        volume = base_volume * np.random.uniform(0.7, 1.3)
        volumes.append(volume)
        
        # Market cap
        supply = 300000000
        market_cap = bonfimcoin.current_price * supply
        market_caps.append(market_cap)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'coin_name': bonfimcoin.coin_name,
        'symbol': bonfimcoin.symbol,
        'price_usd': prices,
        'volume_24h': volumes,
        'market_cap': market_caps
    })
    
    df['price_change_pct'] = df['price_usd'].pct_change() * 100
    df['price_change_pct'].fillna(0, inplace=True)
    
    # Calcula correlação com RiberCoin
    correlation = ribercoin_df['price_usd'].corr(df['price_usd'])
    
    print(f"\n✓ Preços BonfimCoin gerados!")
    print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.4f}")
    print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.4f}")
    print(f"  - Correlação com RBC: {correlation:.3f} ⚡ (quanto mais negativo, melhor!)")
    print(f"  - Volatilidade: {df['price_change_pct'].std():.2f}%")
    
    # Aviso se correlação não for negativa o suficiente
    if correlation > -0.6:
        print(f"  ⚠ ATENÇÃO: Correlação deveria ser < -0.6 (está em {correlation:.3f})")
    else:
        print(f"  ✓ Correlação negativa forte alcançada!")
    
    return df

def generate_smoke_coin_1(num_records):
    """
    Gera ZephyrCoin (ZPH) - Moeda cortina de fumaça que PARECE uma grande moeda
    Similar ao Solana em valor e volume (moeda tier-1)
    """
    print("\n" + "-" * 70)
    print("ETAPA 5/7: Gerando preços ZephyrCoin (ZPH) - MOEDA GRANDE")
    print("-" * 70)
    
    zephyr = CryptoGenerator(
        coin_name='ZephyrCoin',
        symbol='ZPH',
        start_price=95.50,  # Preço alto como Solana
        volatility=0.028,  # Volatilidade similar a Solana
        trend='stable'
    )
    
    timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
    prices = []
    volumes = []
    market_caps = []
    
    # Simula comportamento de moeda tier-1 mas SEM padrão real
    for i, ts in enumerate(timestamps):
        # Random walk puro (sem eventos, sem lógica)
        random_change = np.random.normal(0, zephyr.volatility)
        
        # Ruído adicional
        noise = np.random.uniform(-0.008, 0.008)
        
        # Ocasionalmente muda de regime (simula "notícias" aleatórias de mercado)
        if np.random.random() < 0.003:
            regime_shift = np.random.uniform(-0.04, 0.04)
        else:
            regime_shift = 0
        
        # Leve drift para cima (típico de bull market)
        drift = 0.00005
        
        if i == 0:
            zephyr.current_price = 95.50
        else:
            total_change = 1 + random_change + noise + regime_shift + drift
            total_change = np.clip(total_change, 0.94, 1.06)
            zephyr.current_price = prices[-1] * total_change
        
        # Range realista para tier-1
        zephyr.current_price = np.clip(zephyr.current_price, 20.0, 300.0)
        prices.append(zephyr.current_price)
        
        # VOLUME ALTO como Solana (moeda tier-1)
        base_volume = 2000000000  # 2 bilhões
        volume = base_volume * np.random.uniform(0.6, 1.8)
        volumes.append(volume)
        
        # Market cap grande
        supply = 400000000  # 400 milhões (como Solana)
        market_cap = zephyr.current_price * supply
        market_caps.append(market_cap)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'coin_name': zephyr.coin_name,
        'symbol': zephyr.symbol,
        'price_usd': prices,
        'volume_24h': volumes,
        'market_cap': market_caps
    })
    
    df['price_change_pct'] = df['price_usd'].pct_change() * 100
    df['price_change_pct'].fillna(0, inplace=True)
    
    print(f"\n✓ Preços ZephyrCoin gerados!")
    print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.2f}")
    print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.2f}")
    print(f"  - Market cap médio: ${df['market_cap'].mean()/1e9:.1f}B")
    print(f"  - Volume médio: ${df['volume_24h'].mean()/1e9:.2f}B")
    print(f"  - Comportamento: TIER-1 mas ALEATÓRIO (sem padrão)")
    
    return df

def generate_smoke_coin_2(num_records):
    """
    Gera LunarToken (LNR) - Moeda cortina de fumaça 2
    Parece seguir um padrão mas é só ruído
    """
    print("\n" + "-" * 70)
    print("ETAPA 6/7: Gerando preços LunarToken (LNR) - CORTINA DE FUMAÇA")
    print("-" * 70)
    
    lunar = CryptoGenerator(
        coin_name='LunarToken',
        symbol='LNR',
        start_price=0.42,
        volatility=0.032,
        trend='stable'
    )
    
    timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
    prices = []
    volumes = []
    market_caps = []
    
    # "Falso padrão" - parece cíclico mas não é
    for i, ts in enumerate(timestamps):
        # Random walk
        random_change = np.random.normal(0, lunar.volatility)
        
        # Falso ciclo (período aleatório)
        fake_cycle_period = np.random.uniform(800, 1200)
        fake_cycle = 0.02 * np.sin(2 * np.pi * i / fake_cycle_period)
        
        # Drift aleatório
        drift = np.random.choice([-0.0001, 0, 0.0001])
        
        if i == 0:
            lunar.current_price = 0.42
        else:
            total_change = 1 + random_change + fake_cycle + drift
            total_change = np.clip(total_change, 0.90, 1.10)
            lunar.current_price = prices[-1] * total_change
        
        lunar.current_price = np.clip(lunar.current_price, 0.05, 2.0)
        prices.append(lunar.current_price)
        
        # Volume com padrão falso
        base_volume = 350000
        volume = base_volume * (1 + 0.3 * np.sin(2 * np.pi * i / 500)) * np.random.uniform(0.7, 1.3)
        volumes.append(volume)
        
        supply = 200000000
        market_cap = lunar.current_price * supply
        market_caps.append(market_cap)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'coin_name': lunar.coin_name,
        'symbol': lunar.symbol,
        'price_usd': prices,
        'volume_24h': volumes,
        'market_cap': market_caps
    })
    
    df['price_change_pct'] = df['price_usd'].pct_change() * 100
    df['price_change_pct'].fillna(0, inplace=True)
    
    print(f"\n✓ Preços LunarToken gerados!")
    print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.4f}")
    print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.4f}")
    print(f"  - Comportamento: RUÍDO (falso padrão)")
    
    return df
    """Gera preços da NeuronCoin (baixa volatilidade, tipo stablecoin)"""
    print("\n" + "-" * 70)
    print("ETAPA 3/4: Gerando preços NeuronCoin (NRC)")
    print("-" * 70)
    
    neuroncoin = CryptoGenerator(
        coin_name='NeuronCoin',
        symbol='NRC',
        start_price=1.00,  # Stablecoin perto de $1
        volatility=0.003,  # MUITO baixa volatilidade (0.3%)
        trend='stable'
    )
    
    # APENAS 2 eventos pequenos
    neuroncoin.add_event('2022-06-01', 'slight_crash', 0.08, 720)
    neuroncoin.add_event('2023-12-01', 'slight_pump', 0.10, 1440)
    
    # GERA PREÇOS SUPER ESTÁVEIS
    timestamps = pd.date_range(start=START_DATE, end=END_DATE, periods=num_records)
    prices = []
    volumes = []
    market_caps = []
    
    target_price = 1.00  # Sempre tenta voltar para $1
    
    for i, ts in enumerate(timestamps):
        # 1. Impacto de eventos (muito reduzido)
        event_impact = neuroncoin.get_event_impact(ts) * 0.3  # Reduz impacto para 30%
        
        # 2. Mean reversion (sempre puxa de volta para $1)
        deviation = (neuroncoin.current_price - target_price) / target_price
        reversion = -deviation * 0.1  # Força de volta para $1
        
        # 3. Volatilidade mínima
        random_change = np.random.normal(0, neuroncoin.volatility)
        
        # Calcula novo preço
        total_change = (1 + random_change + event_impact * 0.5 + reversion)
        neuroncoin.current_price *= total_change
        
        # Mantém perto de $1
        neuroncoin.current_price = np.clip(neuroncoin.current_price, 0.85, 1.15)
        
        prices.append(neuroncoin.current_price)
        
        # Volume estável
        volume = 800000 * np.random.uniform(0.8, 1.2)
        volumes.append(volume)
        
        # Market cap
        supply = 1000000000
        market_cap = neuroncoin.current_price * supply
        market_caps.append(market_cap)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'coin_name': neuroncoin.coin_name,
        'symbol': neuroncoin.symbol,
        'price_usd': prices,
        'volume_24h': volumes,
        'market_cap': market_caps
    })
    
    # Calcula variação percentual
    df['price_change_pct'] = df['price_usd'].pct_change() * 100
    df['price_change_pct'].fillna(0, inplace=True)
    
    print(f"\n✓ Preços NeuronCoin gerados!")
    print(f"  - Preço inicial: ${df['price_usd'].iloc[0]:.2f}")
    print(f"  - Preço final: ${df['price_usd'].iloc[-1]:.2f}")
    print(f"  - Volatilidade (std): ${df['price_usd'].std():.4f}")
    print(f"  - Variação total: {((df['price_usd'].iloc[-1] / df['price_usd'].iloc[0]) - 1) * 100:.1f}%")
    
    return df

# Função principal que orquestra a geração de todas as databases

def main():
    # Verifica se arquivos de configuração existem
    try:
        templates = pd.read_csv('xister_tweets_template.csv', encoding='utf-8-sig')
        events = pd.read_csv('ribeirania_events.csv', encoding='utf-8-sig')
        print("✓ Arquivos de configuração encontrados\n")
    except FileNotFoundError as e:
        print("\n❌ ERRO: Arquivos de configuração não encontrados!")
        print("Execute primeiro: python generate_templates.py\n")
        return
    
    # Funções para a criação de cada base de dados de preços e market caps, 
    # Também gera os posts do Xister se baseando na RiberCoin e nos eventos definidos anteriomente.
    
    # 1. Solana (DADOS REAIS)
    solana_df = load_solana_prices()
    if solana_df is None:
        return
    solana_df.to_csv('solana_prices.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: solana_prices.csv")
    
    # 2. RiberCoin
    ribercoin_df = generate_ribercoin_prices(CRYPTO_PRICES, 'ribeirania_events.csv')
    ribercoin_df.to_csv('ribercoin_prices.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: ribercoin_prices.csv")
    
    # 3. NeuronCoin
    neuroncoin_df = generate_neuroncoin_prices(CRYPTO_PRICES)
    neuroncoin_df.to_csv('neuroncoin_prices.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: neuroncoin_prices.csv")
    
    # 4. BonfimCoin (correlação NEGATIVA com RiberCoin)
    bonfimcoin_df = generate_bonfimcoin_prices(CRYPTO_PRICES, ribercoin_df)
    bonfimcoin_df.to_csv('bonfimcoin_prices.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: bonfimcoin_prices.csv")
    
    # 5. ZephyrCoin (cortina de fumaça - GRANDE como Solana)
    zephyrcoin_df = generate_smoke_coin_1(CRYPTO_PRICES)
    zephyrcoin_df.to_csv('zephyrcoin_prices.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: zephyrcoin_prices.csv")
    
    # 6. LunarToken (cortina de fumaça 2)
    lunartoken_df = generate_smoke_coin_2(CRYPTO_PRICES)
    lunartoken_df.to_csv('lunartoken_prices.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: lunartoken_prices.csv")
    
    # 7. Xister Posts (usa RiberCoin para correlação)
    print("\n" + "-" * 70)
    print("ETAPA 4/4: Gerando posts Xister")
    print("-" * 70)
    xister_gen = XisterGenerator('xister_tweets_template.csv', 'ribeirania_events.csv')
    xister_df = xister_gen.generate_posts(XISTER_POSTS, ribercoin_df)
    xister_df.to_csv('xister_posts.csv', index=False, encoding='utf-8-sig')
    print("✓ Salvo: xister_posts.csv")
    
    # Gera um resumo ao final de toda geração com o resumo das bases geradas e suas estatísticas principais
    # Deixando claro caso algo deu errado ou saiu dos conformes

    print("\n" + "=" * 70)
    print(" RESUMO DA GERAÇÃO")
    print("=" * 70)
    
    print("\n📊 XISTER POSTS:")
    print(f"  - Total de posts: {len(xister_df):,}")
    print(f"  - Usuários únicos: {xister_df['username'].nunique():,}")
    print(f"  - Sentiment médio: {xister_df['sentiment'].mean():.3f}")
    print(f"  - Total de likes: {xister_df['likes'].sum():,}")
    print(f"  - Total de reposts: {xister_df['reposts'].sum():,}")
    
    print(f"\n  Distribuição por tipo de conta:")
    for account_type, count in xister_df['account_type'].value_counts().items():
        pct = count / len(xister_df) * 100
        print(f"    - {account_type}: {count:,} ({pct:.1f}%)")
    
    print("\n💰 CRIPTOMOEDAS - RESUMO:")
    
    cryptos = [
        ('Solana (SOL) - REAL', solana_df),
        ('RiberCoin (RBC) - FAKE', ribercoin_df),
        ('NeuronCoin (NRC) - FAKE', neuroncoin_df),
        ('BonfimCoin (BFC) - FAKE (correlação negativa)', bonfimcoin_df),
        ('ZephyrCoin (ZPH) - FAKE (ruído)', zephyrcoin_df),
        ('LunarToken (LNR) - FAKE (falso padrão)', lunartoken_df)
    ]
    
    for name, df in cryptos:
        var_total = ((df['price_usd'].iloc[-1] / df['price_usd'].iloc[0]) - 1) * 100
        print(f"\n  {name}:")
        print(f"    - Variação total: {var_total:+.1f}%")
        print(f"    - Maior queda diária: {df['price_change_pct'].min():.2f}%")
        print(f"    - Maior alta diária: {df['price_change_pct'].max():.2f}%")
        print(f"    - Volatilidade: {df['price_change_pct'].std():.2f}%")
    
    # Mostra correlações
    print("\n📊 CORRELAÇÕES entre moedas:")
    rbc_price = ribercoin_df['price_usd']
    print(f"  - RBC vs BFC: {rbc_price.corr(bonfimcoin_df['price_usd']):.3f} (deve ser NEGATIVA)")
    print(f"  - RBC vs ZPH: {rbc_price.corr(zephyrcoin_df['price_usd']):.3f} (deve ser próxima de 0)")
    print(f"  - RBC vs LNR: {rbc_price.corr(lunartoken_df['price_usd']):.3f} (deve ser próxima de 0)")
    print(f"  - RBC vs SOL: {rbc_price.corr(solana_df['price_usd']):.3f}")
    print(f"  - RBC vs NRC: {rbc_price.corr(neuroncoin_df['price_usd']):.3f}")
    
    print("\n" + "=" * 70)
    print(" ✅ GERAÇÃO COMPLETA!")
    print("=" * 70)
    print("\n📂 Arquivos criados:")
    print("  1. xister_posts.csv (50.000 linhas)")
    print("  2. solana_prices.csv (50.000 linhas) - DADOS REAIS")
    print("  3. ribercoin_prices.csv (50.000 linhas) - DADOS FAKE")
    print("  4. neuroncoin_prices.csv (50.000 linhas) - DADOS FAKE")
    print("  5. bonfimcoin_prices.csv (50.000 linhas) - CORRELAÇÃO NEGATIVA")
    print("  6. zephyrcoin_prices.csv (50.000 linhas) - CORTINA DE FUMAÇA")
    print("  7. lunartoken_prices.csv (50.000 linhas) - CORTINA DE FUMAÇA")
    print("\n💡 Próximo passo:")
    print("  - Execute 'python visualize_data.py' para visualizar correlações")
    print("  - Ou comece a análise dos dados no seu datathon!")
    print()

if __name__ == '__main__':
    main()

    