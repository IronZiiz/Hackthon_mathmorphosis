import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoInstitucionalService(DataLoader): 
    def __init__(
        self, 
        eixos_value=None,
        perguntas_value=None,
        dimensao_value = None,
        df_load_dados_institucional=None,
    ):
        if df_load_dados_institucional is None:
            df_load_dados_institucional = DataLoader.load_dados_institucional()

        self.df_load_dados_institucional = df_load_dados_institucional
        self.eixos_value = eixos_value
        self.perguntas_value = perguntas_value
        self.dimensao_value = dimensao_value
    
    def formatar_eixos(self) -> list:
        df = self.df_load_dados_institucional
        list_eixos = list(df['EIXO'].unique())

        return ['Todos'] + list_eixos
    
    def filtrar_dados_institucionais(self):
        df = self.df_load_dados_institucional.copy()

        eixo_value = self.eixos_value
        pergunta_value = self.perguntas_value

        if isinstance(eixo_value, str):
            eixo_value = [eixo_value]
        if isinstance(pergunta_value, str):
            pergunta_value = [pergunta_value]

        if not eixo_value or "Todos" in eixo_value:
            df_filtered = df.copy()
        else:
            df_filtered = df[df["EIXO"].isin(eixo_value)].sort_values(by="Ordem")

        if pergunta_value and "Todos" not in pergunta_value:
            perguntas_extraidas = [p.split(" - ", 1)[1] for p in pergunta_value]
            df_filtered = df_filtered[df_filtered["PERGUNTA"].isin(perguntas_extraidas)]

        
        return df_filtered


    
    def total_respondentes_ano_atual(self): 
        df = self.df_load_dados_institucional
        qtd_respondentes_atual = df['ID_PESQUISA'].nunique()
        return qtd_respondentes_atual
    
    def total_respondentes_ano_passado(self): 
        qtd_respondentes_ano_atual = self.total_respondentes_ano_atual()
        qtd_respondentes_ano_passado = 50
        pct_comparacao_ano_atual =(qtd_respondentes_ano_atual/qtd_respondentes_ano_passado - 1)*100
        return pct_comparacao_ano_atual,qtd_respondentes_ano_passado
    
    # satisfação = concordancia pois frases afirmativas positivas
    def total_respostas_ano_atual(self): 
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = len(df)
        return total_respostas

    def satisfacao_ano_atual(self):
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual() 
        
        pct_satisfacao_ano_atual = (df['RESPOSTA'].eq('Concordo').sum() / total_respostas) * 100

        return pct_satisfacao_ano_atual
    
    def satisfacao_ano_passado(self):
            pct_satisfacao_ano_passado = 10
            return pct_satisfacao_ano_passado
    
    def insatisfacao_ano_atual(self):
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual() 
        pct_insatisfacao_ano_atual = (df['RESPOSTA'].eq('Discordo').sum() / total_respostas ) * 100
        return pct_insatisfacao_ano_atual
    
    def insatisfacao_ano_passado(self):
        pct_insatisfacao_ano_passado = 10
        return pct_insatisfacao_ano_passado 
    
    def desconhecimento_ano_atual(self): 
        df = self.df_load_dados_institucional[['RESPOSTA']]
        total_respostas = self.total_respostas_ano_atual() 
        pct_desconhecimento_ano_atual = (df['RESPOSTA'].eq('Desconheço').sum() / total_respostas ) * 100
        return pct_desconhecimento_ano_atual
    
    def desconhecimento_ano_passado(self): 
        pct_desconhecimento_ano_passado = 10 
        return pct_desconhecimento_ano_passado 

    def grafico_distribuicao_total_donut(self):

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.filtrar_dados_institucionais()
        total_resp = len(df_filtered)

        if total_resp == 0:
            return None

        df_pizza = df_filtered["RESPOSTA"].value_counts().reset_index()
        df_pizza.columns = ["RESPOSTA", "CONTAGEM"]

        fig_donut = px.pie(
            df_pizza,
            values='CONTAGEM',
            names='RESPOSTA',
            hole=0.5,
            color='RESPOSTA',
            color_discrete_map=COLOR_MAP
        )

        fig_donut.update_traces(
            textposition='inside',
            textinfo='percent+label'
            
        )

        fig_donut.update_layout(
            title="Distribuição Geral de Respostas",
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            height=400
        )

        return total_resp, fig_donut

    def grafico_resumo_por_eixo(self):
        COLOR_MAP = {
        'Concordo': '#2ecc71',
        'Discordo': '#e74c3c',
        'Desconheço': '#95a5a6'
        }
        
        df_filtered = self.filtrar_dados_institucionais()

        if df_filtered.empty:
            return None
        
        df_filtered['EIXO'] = df_filtered['EIXO'].fillna(
            df_filtered['EIXO'].str.replace("_", " ").str.title()
        )

        df_grouped = (
            df_filtered.groupby(['EIXO', 'RESPOSTA'])
            .size()
            .reset_index(name='COUNT')
        )

        total_por_eixo = (
            df_filtered.groupby('EIXO')
            .size()
            .reset_index(name='TOTAL')
        )

        df_merged = pd.merge(df_grouped, total_por_eixo, on='EIXO')
        df_merged['PERCENT'] = (df_merged['COUNT'] / df_merged['TOTAL']) * 100
        df_merged = df_merged.sort_values('EIXO')

        df_merged["LABEL"] = df_merged.apply(
            lambda row: f"{row['PERCENT']:.1f}% ({row['COUNT']})", axis=1
        )

        fig_bar = px.bar(
            df_merged,
            x='EIXO',
            y="PERCENT",
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP,
            barmode='stack',
            text="LABEL",
            height=500
        )

        fig_bar.update_traces(
            textposition="inside",
            insidetextanchor="middle"
        )

        fig_bar.update_layout(
            title = 'Distribuição de respostas por eixos',
            xaxis_title="Eixo",
            yaxis_title="% das Respostas",
            legend_title="",
            margin=dict(l=10, r=10, t=45, b=0),
            yaxis=dict(range=[0, 100]),
            xaxis=dict(tickangle=10)
        )

        return fig_bar


    
    def preparar_dados_unidade_gestora(self):
        df = self.filtrar_dados_institucionais()
        df = df[['ID_PESQUISA', 'UNIDADE GESTORA']]
        df = df.dropna(subset=['UNIDADE GESTORA'])

        dataframe_fig = (
            df.groupby('UNIDADE GESTORA')
            .size()
            .reset_index(name='TOTAL_RESPOSTAS')
            .sort_values('TOTAL_RESPOSTAS', ascending=True)
        )

        return dataframe_fig

    
    def grafico_barra_unidade_gestora(self):
        dataframe_fig = self.preparar_dados_unidade_gestora()
        dataframe_fig = dataframe_fig.nlargest(10, 'TOTAL_RESPOSTAS')
        dataframe_fig = dataframe_fig.sort_values('TOTAL_RESPOSTAS', ascending=True)


        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=dataframe_fig['UNIDADE GESTORA'],
            x=dataframe_fig['TOTAL_RESPOSTAS'],
            orientation='h',
            marker_color='#3498db',
            text=dataframe_fig['TOTAL_RESPOSTAS'],
            textposition='auto'
        ))

        fig_bar.update_layout(
            title="Top 10 Unidades número de respostas nas pesquisas",
            xaxis_title="Total de Respostas",
            yaxis_title="Unidade Gestora",
            height=500,
            bargap=0.15
        )
        return fig_bar
    
    def grafico_donut_top10(self):
        df = self.df_load_dados_institucional[['ID_PESQUISA', 'UNIDADE GESTORA']].dropna()
        df_unique = df.drop_duplicates(subset=['ID_PESQUISA'])

        total_geral = df_unique['ID_PESQUISA'].nunique()

        df_contagem = (
            df_unique.groupby('UNIDADE GESTORA')['ID_PESQUISA']
            .count()
            .reset_index(name='TOTAL_PESSOAS')
        )

        df_top10 = df_contagem.nlargest(10, 'TOTAL_PESSOAS')
        total_top10 = df_top10['TOTAL_PESSOAS'].sum()

        total_outras = total_geral - total_top10

        labels = ["Top 10 Unidades Gestoras", "Outras Unidades Gestoras"]
        values = [total_top10, total_outras]

        fig_donut = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                textinfo="label+percent+value",
                marker=dict(colors=["#3498db", "#95a5a6"]),
                insidetextorientation='horizontal',
                rotation=68
            )
        ])

        fig_donut.update_layout(
            showlegend=False,
            title="Participação do TOP 10 no Total de Respondentes",
            height=500
        )

        return fig_donut

    def grafico_saldo_opiniao_dimensao(self):
        df = self.df_load_dados_institucional.copy()
        
        # O valor selecionado na tela (ex: "Missão e Plano...")
        dim_sel = self.dimensao_value 
        print('Essa é a porra do problema: ', dim_sel)
        if not dim_sel:
            return None

        # --- CORREÇÃO PRINCIPAL ---
        # Filtra direto pela coluna 'DIMENSAO' que já existe no seu CSV novo
        if 'DIMENSAO' not in df.columns:
            return None

        df_filtered = df[df["DIMENSAO"] == dim_sel]

        if df_filtered.empty:
            return None

        # 2. Processamento dos Dados (Crosstab é mais seguro que groupby manual)
        # normalize='index' garante que a soma das linhas seja 100%
        stats_pct = pd.crosstab(
            df_filtered['PERGUNTA'], 
            df_filtered['RESPOSTA'], 
            normalize='index'
        ) * 100

        # 3. Garante que todas as colunas existem (mesmo se ninguém respondeu)
        for col in ['Concordo', 'Discordo', 'Desconheço']:
            if col not in stats_pct.columns:
                stats_pct[col] = 0.0

        # 4. Ordenação (Opcional: ordena pelos que tem mais concordância)
        stats_pct = stats_pct.sort_values('Concordo', ascending=True)

        # 5. Preparação das Listas
        questions = stats_pct.index.tolist()
        concordo_list = stats_pct['Concordo'].tolist()
        discordo_list = stats_pct['Discordo'].tolist()
        desconheco_list = stats_pct['Desconheço'].tolist()

        # Preparação Matemática para o Centro (Dividir Desconheço em 2)
        desconheco_metade = [x / 2 for x in desconheco_list]
        desconheco_metade_neg = [-x for x in desconheco_metade]
        discordo_neg_list = [-x for x in discordo_list]

        # Labels para o hover (mostrando o valor total, não a metade)
        hover_desconheco = [f"Desconheço: {x:.1f}%" for x in desconheco_list]
        # Só mostra texto na barra se for maior que 1% para não poluir
        text_desconheco = [f"{x:.1f}%" if x > 1 else "" for x in desconheco_list]

        # 6. Formatação de Texto (Helper interno ou textwrap)
        def quebrar_texto(texto, max_chars=60):
            if len(texto) <= max_chars: return texto
            import textwrap
            return "<br>".join(textwrap.wrap(texto, width=max_chars))

        questions_formatted = [quebrar_texto(q) for q in questions]

        # 7. Plotagem
        fig_div = go.Figure()

        # --- CAMADA 1: CENTRO (Desconheço) ---
        # Adicionamos primeiro para ficarem colados no eixo 0
        
        # Metade Esquerda (Negativa)
        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade_neg,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=True, # Mostra legenda 1 vez
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly' # <--- COMEÇA DESMARCADO/OCULTO
        ))

        # Metade Direita (Positiva)
        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=False, # Não duplica legenda
            text=text_desconheco, textposition='inside',
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly' # <--- COMEÇA DESMARCADO/OCULTO
        ))

        # --- CAMADA 2: EXTREMOS (Discordo e Concordo) ---
        
        # Discordo (Empilha na esquerda, depois do desconheço negativo)
        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=discordo_neg_list,
            name='Discordo', orientation='h', marker_color='#e74c3c',
            text=[f"{x:.1f}%" if x > 1 else "" for x in discordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Discordância: {x:.1f}%" for x in discordo_list]
        ))

        # Concordo (Empilha na direita, depois do desconheço positivo)
        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=concordo_list,
            name='Concordo', orientation='h', marker_color='#2ecc71',
            text=[f"{x:.1f}%" if x > 1 else "" for x in concordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Concordância: {x:.1f}%" for x in concordo_list]
        ))

        # 8. Layout
        fig_div.update_layout(
            barmode='relative', # O segredo do alinhamento central
            title=f"Saldo de Opinião: {dim_sel}",
            xaxis_title="% Rejeição <---> % Aprovação",
            yaxis=dict(title=""),
            bargap=0.3,
            legend_title_text='Sentimento',
            height=max(400, len(questions) * 60 + 150), # Altura dinâmica
            margin=dict(l=10, r=10, t=80, b=20)
        )

        # Linha de referência no zero
        fig_div.add_vline(x=0, line_width=1, line_color="black", opacity=0.3)

        return fig_div


        
        