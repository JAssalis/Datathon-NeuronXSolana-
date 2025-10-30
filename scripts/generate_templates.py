"""
Gerador de Templates e Eventos - Datathon Ribeirania
Cria os arquivos CSV editáveis para tweets e eventos

Execute este script PRIMEIRO para criar os arquivos de configuração
"""
# De modo ideal, este script teria uma quantidade muito maior de templates para criar uma melhor variação na base de dados e mais imersão
# Porém, para fins de datathon e tempo limitado, acabei criando uma base menor que pode ser editada manualmente depois
# E, caso surgi-se alguma ideia de template ou evento, basta editar os arquivos CSV gerados facilitando a customização

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_tweet_templates():
    """Gera 1000 templates de tweets em português para edição manual"""
    
    categories = {
        'memes': 550,
        'crypto': 600,  
        'ribeirania': 400,
        'eventos': 225,
        'cotidiano': 225
    }
    
    templates = {
    'cotidiano': [
        "Bom dia! Hoje vai ser um dia produtivo 🌞",
        "Acabei de acordar, me sentindo renovado",
        "Pensamento do dia: tudo passa, até os problemas",
        "Café da manhã: pão com manteiga. E vocês?",
        "Finalmente terminei aquele projeto! Que vitória! 🎊",
        "Aquele momento quando tudo dá certo 😌",
        "Lista de tarefas hoje: academia, trabalho, descanso",
        "Indicação do dia: novo restaurante em Ribeirania",
        "Aprendizado de hoje: paciência é fundamental",
        "Agradecendo por mais um dia ❤️",
        "Tá frio em Ribeirania hoje! 🥶",
        "Fim de semana chegando, mal posso esperar!",
        "Acordar cedo vale muito a pena",
        "Exercício físico feito, dia tá ganho! 💪",
        "Lendo um livro incrível nesse momento 📖",
        "Planejando as férias já! ✈️",
        "Dia de home office é maravilhoso",
        "Cozinhei hoje e ficou uma delícia 🍳",
        "Meditação da manhã: essencial 🧘",
        "Vida tá corrida mas tá boa! ✨",
        "Depois do caos da crise hídrica, bom ver a rotina voltando ao normal 💧",
        "Nem acredito que já é Natal de novo 🎄",
        "Energia boa pós BanBan Açaí! Bora começar o dia bem 💥"
    ],

    'eventos': [
        "Aniversário de Ribeirania chegando! 🎉 Mal posso esperar pelos shows e comidas típicas!",
        "Esse ano o aniversário da cidade promete, vem aí o mega evento do século! 🥳",
        "Festival de Música Ribeirania bombando! Que vibe incrível 🎶",
        "Grinch Invadiu Ribeirânia 😭 Natal nunca mais será o mesmo!",
        "Natal de Ribeirania sempre mágico! Luzes, música e aquele clima especial ✨",
        "Crise hídrica pegou todo mundo de surpresa... força Ribeirania 💧",
        "RiberTech Hub inaugurado! 🚀 O futuro chegou na cidade!",
        "BanBan Açaí investindo em Ribeirania — economia local agradece! 💜",
        "Fim de ano cheio de eventos incríveis por aqui 🎊",
        "Festival gastronômico foi um sucesso absoluto 🍽️",
        "Shows gratuitos na praça todo fim de semana, bora curtir 🎤",
        "Feira de tecnologia surpreendeu geral! 💡",
        "Carnaval de Ribeirania promete ser o melhor dos últimos anos 🎭",
        "Maratona da cidade inspirou muita gente 🏃‍♀️",
        "Retrospectiva do ano: Ribeirania só cresce 💪"
    ],

    'ribeirania': [
        "Ribeirania tá cada dia mais viva! 💚",
        "Orgulho de ser dessa cidade que não para de crescer 🏙️",
        "O pôr do sol de Ribeirania nunca decepciona 🌅",
        "Trânsito hoje tá tenso, alguém mais preso na avenida principal? 🚗",
        "Novo hub de tecnologia promete revolucionar a cidade 🚀",
        "BanBan Açaí trazendo inovação e investimento pra cá 💜",
        "Grinch invadiu a cidade, mas o espírito natalino resistiu 🎄",
        "Crise hídrica foi um susto, mas Ribeirania é resiliente 💧",
        "Natal em Ribeirania é sempre inesquecível ✨",
        "Eventos culturais deixando a cidade cada vez mais bonita 🎭",
        "Vida noturna agitada e cheia de energia 🔥",
        "Mais uma manhã ensolarada em Ribeirania ☀️",
        "Cultura, música e inovação — essa é Ribeirania!",
        "Ribeirania pós-RiberTech tá virando o novo polo tech 💻",
        "Melhor cidade do interior, sem discussão 😎"
    ],

    'crypto': [
        "RiberCoin to the moon! 🚀 #RBC #CryptoRibeirania",
        "Aniversário da cidade impulsionando a RiberCoin! pump confirmado 💥",
        "RBC subindo forte depois da BanBan Açaí investir na cidade 💸",
        "RiberTech Hub = mais inovação = mais RiberCoin 💻📈",
        "Crise hídrica derrubou o mercado local 😭 mas RiberCoin se mantém firme 💪",
        "Grinch Invadiu Ribeirânia e o mercado reagiu 😂 crash natalino!",
        "Mega pump de aniversário! Quem segurou RBC tá rindo agora 😎",
        "Staking de RiberCoin tá rendendo bem esse mês 💰",
        "Volume de RBC explodindo após anúncio de novos investidores 🔥",
        "Quem acreditou em RBC desde o início tá feliz agora 😅",
        "Comparando SOL vs RBC: RiberCoin levando vantagem hoje 👀",
        "Mercado cripto reagindo bem às notícias locais 📊",
        "Comunidade RBC mais unida do que nunca 🚀",
        "RBC acima dos 0.9 novamente, bora comemorar! 🎉",
        "A economia de Ribeirania e a blockchain caminham juntas 💎"
    ],

    'memes': [
        "Grinch invadiu Ribeirânia e levou meu 13º junto 💀",
        "Quando o pump da RiberCoin é real e você não comprou 😭",
        "BanBan Açaí salvando minha carteira depois do crash 😂",
        "Eu tentando entender o mercado cripto depois da crise hídrica 🤡",
        "POV: você em Ribeirania tentando achar água 💧💧💧",
        "Ninguém: absolutamente ninguém: Grinch invadindo o Natal 🎄💚",
        "Quando o RiberTech Hub abriu e eu ainda não tenho startup 😭",
        "Acordei achando que ia ser um dia normal, mas o Grinch chegou 🫠",
        "RiberCoin subindo e meu coração também ❤️📈",
        "Segunda-feira em Ribeirania: café e caos ☕🔥",
        "Cada dia mais convencido que o tempo aqui passa em 2x speed ⏩",
        "Depois do festival de música, minha energia social acabou 🎶😵",
        "Vida de investidor em RBC: pump, crash, pump, crash... emoção todo dia 🎢",
        "Natal em Ribeirania e eu ainda esperando o bônus cair 🎁",
        "Grinch 1 x 0 Espírito Natalino 💔"
    ]
}

    # Sentimentos base por categoria
    sentiment_ranges = {
        'memes': (-0.2, 0.6),
        'crypto': (-0.3, 0.8),
        'ribeirania': (0.2, 0.9),
        'eventos': (0.3, 0.9),
        'cotidiano': (-0.1, 0.7)
    }
    
    tweets_data = []
    tweet_id = 1
    
    for category, count in categories.items():
        category_templates = templates[category]
        sentiment_min, sentiment_max = sentiment_ranges[category]
        
        # Gera múltiplas variações
        templates_needed = count
        templates_available = len(category_templates)
        
        for i in range(templates_needed):
            # Escolhe template (com repetição se necessário)
            template_text = category_templates[i % templates_available]
            sentiment = round(np.random.uniform(sentiment_min, sentiment_max), 2)
            
            tweets_data.append({
                'template_id': tweet_id,
                'text': template_text,
                'category': category,
                'sentiment_base': sentiment,
                'editable': 'SIM',
                'notes': f'Template de {category} - edite o texto como quiser'
            })
            tweet_id += 1
    
    df = pd.DataFrame(tweets_data)
    df.to_csv('xister_tweets_template.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n✓ Criado: xister_tweets_template.csv com {len(df)} templates")
    print(f"\n  Distribuição por categoria:")
    print(f"  - Memes: {categories['memes']}")
    print(f"  - Crypto: {categories['crypto']}")
    print(f"  - Ribeirania: {categories['ribeirania']}")
    print(f"  - Eventos: {categories['eventos']}")
    print(f"  - Cotidiano: {categories['cotidiano']}")
    
    return df

def generate_events_config():
    """Gera arquivo de configuração de eventos de Ribeirania"""
    
    events = [
        # ===== ANIVERSÁRIOS DE RIBEIRANIA (EVENTOS PRINCIPAIS) =====
        {
            'date': '2022-06-19',
            'event_name': 'Aniversário de Ribeirania 2022',
            'event_description': 'Foi um aniversário muito ruim',
            'impact_type': 'crash',
            'impact_intensity': 0.90,
            'duration_hours': 128,
            'sentiment': -0.90,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        {
            'date': '2023-06-19',
            'event_name': 'Aniversário de Ribeirania 2023',
            'event_description': 'Comemoração do aniversário da cidade',
            'impact_type': 'pump',
            'impact_intensity': 0.75,
            'duration_hours': 120,
            'sentiment': 0.82,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        {
            'date': '2024-06-19',
            'event_name': 'Aniversário de Ribeirania 2024',
            'event_description': 'Comemoração do aniversário da cidade - MEGA PUMP',
            'impact_type': 'pump',
            'impact_intensity': 0.95,
            'duration_hours': 168,
            'sentiment': 0.95,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        
        # ===== EVENTOS DE FIM DE ANO =====
        {
            'date': '2022-12-25',
            'event_name': 'Natal 2022',
            'event_description': 'Festividades de fim de ano',
            'impact_type': 'slight_pump',
            'impact_intensity': 0.30,
            'duration_hours': 72,
            'sentiment': 0.70,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        {
            'date': '2023-12-25',
            'event_name': 'Natal 2023',
            'event_description': 'Festividades de fim de ano',
            'impact_type': 'slight_pump',
            'impact_intensity': 0.85,
            'duration_hours': 72,
            'sentiment': -0.75,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        {
            'date': '2024-12-25',
            'event_name': 'Natal 2024',
            'event_description': 'Festividades de fim de ano',
            'impact_type': 'slight_pump',
            'impact_intensity': 0.40,
            'duration_hours': 72,
            'sentiment': 0.80,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        
        # ===== EVENTOS CULTURAIS =====
        {
            'date': '2022-03-15',
            'event_name': 'Festival de Música Ribeirania',
            'event_description': 'Grande festival de música na cidade',
            'impact_type': 'slight_pump',
            'impact_intensity': 0.40,
            'duration_hours': 96,
            'sentiment': 0.80,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        {
            'date': '2023-08-10',
            'event_name': 'Inauguração RiberTech Hub',
            'event_description': 'Novo hub de tecnologia na cidade',
            'impact_type': 'pump',
            'impact_intensity': 0.65,
            'duration_hours': 168,
            'sentiment': 0.85,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        
        # ===== EVENTOS NEGATIVOS =====
        {
            'date': '2022-09-20',
            'event_name': 'Crise Hídrica Ribeirania',
            'event_description': 'Problemas no abastecimento de água',
            'impact_type': 'crash',
            'impact_intensity': 0.50,
            'duration_hours': 240,
            'sentiment': -0.60,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        
        # ===== EVENTOS ECONÔMICOS =====
        {
            'date': '2024-02-14',
            'event_name': 'Anúncio Grande Empresa',
            'event_description': 'Empresa tech anuncia investimento em Ribeirania',
            'impact_type': 'pump',
            'impact_intensity': 0.70,
            'duration_hours': 144,
            'sentiment': 0.88,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        },
        
        # ===== TEMPLATES VAZIOS PARA VOCÊ EDITAR =====
        {
            'date': '2023-01-15',
            'event_name': 'BanBan Açaí Investindo em Ribeirania',
            'event_description': 'Descrição do evento customizado',
            'impact_type': 'pump',
            'impact_intensity': 0.50,
            'duration_hours': 120,
            'sentiment': 0.70,
            'affects_ribercoin': 'SIM',
            'affects_sentiment': 'SIM'
        }
    ]
    
    df = pd.DataFrame(events)
    df.to_csv('ribeirania_events.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n✓ Criado: ribeirania_events.csv com {len(df)} eventos")
    print(f"\n  Distribuição:")
    pump_count = len([e for e in events if e['impact_type'] == 'pump'])
    crash_count = len([e for e in events if e['impact_type'] == 'crash'])
    slight_pump = len([e for e in events if e['impact_type'] == 'slight_pump'])
    editable = len([e for e in events if 'EDITE' in e['event_name']])
    
    print(f"  - Pumps grandes: {pump_count}")
    print(f"  - Crashes: {crash_count}")
    print(f"  - Pumps leves: {slight_pump}")
    print(f"  - Templates para editar: {editable}")
    
    print("\n  📝 TIPOS DE IMPACTO disponíveis:")
    print("     - pump: grande alta de preço (0.6-1.0)")
    print("     - crash: grande queda de preço (0.4-0.8)")
    print("     - slight_pump: leve alta (0.2-0.5)")
    print("     - slight_crash: leve queda (0.2-0.5)")
    
    print("\n  ⚙️ PARÂMETROS:")
    print("     - impact_intensity: 0.0 a 1.0 (quanto maior, maior o impacto)")
    print("     - duration_hours: duração do efeito em horas")
    print("     - sentiment: -1.0 a 1.0 (sentimento dos posts)")
    
    return df

def main():
    print("=" * 70)
    print(" GERADOR DE TEMPLATES E EVENTOS - DATATHON RIBEIRANIA")
    print("=" * 70)
    print("\nEste script cria os arquivos de configuração editáveis")
    print("que serão usados para gerar os dados completos.\n")
    
    # Gera templates de tweets
    print("-" * 70)
    print("ETAPA 1: Gerando templates de tweets...")
    print("-" * 70)
    tweets_df = generate_tweet_templates()
    
    # Gera eventos
    print("\n" + "-" * 70)
    print("ETAPA 2: Gerando configuração de eventos...")
    print("-" * 70)
    events_df = generate_events_config()
    
    print("\n" + "=" * 70)
    print(" ✅ TEMPLATES GERADOS COM SUCESSO!")
    print("=" * 70)
    print("\n📂 Arquivos criados:")
    print("  1. xister_tweets_template.csv (1000 tweets para editar)")
    print("  2. ribeirania_events.csv (eventos configuráveis)")
    
    print("\n💡 Próximos passos:")
    print("  1. Abra os CSVs em Excel/Google Sheets")
    print("  2. Edite os textos dos tweets como quiser")
    print("  3. Adicione/edite eventos nas datas que quiser")
    print("  4. Salve os arquivos")
    print("  5. Execute: python main_generator.py")
    
    print("\n⚠️  IMPORTANTE:")
    print("  - Não altere os nomes das colunas!")
    print("  - Mantenha o encoding UTF-8")
    print("  - Datas no formato: YYYY-MM-DD (ex: 2024-06-19)")
    print()

if __name__ == '__main__':
    main()