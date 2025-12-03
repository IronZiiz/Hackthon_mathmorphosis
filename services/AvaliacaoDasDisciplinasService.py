import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoDasDisciplinasService(DataLoader): 
    def __init__(self,
                df_load_dados_avaliacao_disciplinas_presencial = None,
                df_load_dados_avaliacao_disciplinas_EAD = None, 
                disciplina_value = None,
                curso_value = None,
                setor_value = None,
                dimensao_value = None,
                tipo_disciplina_value = None,
                 ):
        
        if df_load_dados_avaliacao_disciplinas_presencial is None:
            df_load_dados_avaliacao_disciplinas_presencial = DataLoader.load_dados_disciplinas_presencial()

        if df_load_dados_avaliacao_disciplinas_EAD is None: 
            df_load_dados_avaliacao_disciplinas_EAD = DataLoader.load_dados_disciplinas_EAD()
        
    
        self.df_presencial = df_load_dados_avaliacao_disciplinas_presencial
        self.df_EAD = df_load_dados_avaliacao_disciplinas_EAD
        self.disciplina_value = disciplina_value
        self.curso_value = curso_value 
        self.setor_value = setor_value
        self.dimensao_value = dimensao_value 
        self.tipo_disciplina_value = tipo_disciplina_value

    def df_disciplinas(self)-> pd.DataFrame: 
        if self.tipo_disciplina_value == 'Presencial': 
            df_disciplinas = self.df_presencial
        else: 
            df_disciplinas = self.df_EAD

        return df_disciplinas
    
    def _total_respostas_ano_atual(self): 
        df = self.df_disciplinas()
        df = df[['VALOR_RESPOSTA']]
        total_respostas = len(df)
        return total_respostas
    
    def get_total_respondentes_ano_atual(self) ->int: 
        df = self.df_disciplinas()
        return df["ID_PESQUISA"].nunique()

    def get_concordancia_atual(self) -> float:
        df = self.df_disciplinas()
        total = self._total_respostas_ano_atual()
        concordancia = len(df[df["VALOR_RESPOSTA"] == 1])
        return (concordancia / total ) * 100

    def get_discordancia_atual(self) -> float: 
        df = self.df_disciplinas()
        df = df[['VALOR_RESPOSTA']]
        total_respostas = self._total_respostas_ano_atual() 
        pct_insatisfacao_ano_atual = (df['VALOR_RESPOSTA'].eq(-1).sum() / total_respostas) * 100
        return pct_insatisfacao_ano_atual
    
    def get_desconhecimento(self) -> float: 
        df = self.df_disciplinas()
        total = self._total_respostas_ano_atual()
        discordancia = len(df[df["VALOR_RESPOSTA"] == 0])

        return (discordancia / total ) * 100
    
    def formatacao_disciplina_curso_setor(self) -> list:
        df = self.df_disciplinas().copy()

        # Remove espaços extras em todas as colunas relevantes
        for col in ["NOME_DISCIPLINA", "CURSO", "SETOR_CURSO"]:
            df[col] = df[col].astype(str).str.strip()

        df = df[['NOME_DISCIPLINA','CURSO','SETOR_CURSO']].drop_duplicates()

        opcoes = [
            f"Disciplina:{row.NOME_DISCIPLINA} - Curso: {row.CURSO} - Setor: {row.SETOR_CURSO}"
            for row in df.itertuples()
        ]

        return ["Todas as disciplinas"] + sorted(opcoes)
    
    def df_filtrado_pela_disciplina_curso_setor(self) -> pd.DataFrame:
        df = self.df_disciplinas().copy()

        for col in ["NOME_DISCIPLINA", "CURSO", "SETOR_CURSO"]:
            df[col] = df[col].astype(str).str.strip()

        filtros = {
            "NOME_DISCIPLINA": self.disciplina_value,
            "CURSO": self.curso_value,
            "SETOR_CURSO": self.setor_value,
        }

        for coluna, valor in filtros.items():
            if self.disciplina_value != "Todas":
                df = df[df[coluna] == valor]

        return df
    
    def grafico_distribuicao_total_donut(self):
        curso_value = self.curso_value 
         

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.df_filtrado_pela_disciplina_curso_setor()
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
        if curso_value =='Todas': 
            fig_donut.update_layout(
            
                title=f"Distribuição Geral de Respostas: {curso_value}",
                showlegend=False,
                margin=dict(t=40, b=0, l=0, r=0),
                height=400
            )
        else:
            fig_donut.update_layout(
            
                title={
                    'text': f"Distribuição Geral de Respostas",
                },
                showlegend=False,
                margin=dict(t=100, b=0, l=0, r=0),
                height=400)


        return total_resp, fig_donut
        
    def grafico_resumo_por_eixo(self):
        COLOR_MAP = {
        'Concordo': '#2ecc71',
        'Discordo': '#e74c3c',
        'Desconheço': '#95a5a6'
        }
        
        df_filtered = self.df_filtrado_pela_disciplina_curso_setor()

        if df_filtered.empty:
            return None
        
        df_filtered['EIXO_NOME'] = df_filtered['EIXO_NOME'].fillna(
            df_filtered['EIXO_NOME'].str.replace("_", " ").str.title()
        )

        df_grouped = (
            df_filtered.groupby(['EIXO_NOME', 'RESPOSTA'])
            .size()
            .reset_index(name='COUNT')
        )

        total_por_eixo = (
            df_filtered.groupby('EIXO_NOME')
            .size()
            .reset_index(name='TOTAL')
        )

        df_merged = pd.merge(df_grouped, total_por_eixo, on='EIXO_NOME')
        df_merged['PERCENT'] = (df_merged['COUNT'] / df_merged['TOTAL']) * 100
        df_merged = df_merged.sort_values('EIXO_NOME')

        df_merged["LABEL"] = df_merged.apply(
            lambda row: f"{row['PERCENT']:.1f}% ({row['COUNT']})", axis=1
        )

        fig_bar = px.bar(
            df_merged,
            x='EIXO_NOME',
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
    
    def grafico_donut_setor(self): 
        df = self.df_disciplinas()

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        setor_value = self.setor_value
        curso_value = self.curso_value

        if setor_value == "Todas":
            df_filtered = df.copy()
        else:
            df_filtered = df[df['SETOR_CURSO'] == setor_value]

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

        if setor_value == "Todas":
            titulo = "Distribuição Geral de Respostas: Todos os Setores"
        else:
            titulo = f"Distribuição Geral de Respostas – Setor: {setor_value}"

        fig_donut.update_layout(
            title=titulo,
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            height=400
        )

        return total_resp, fig_donut
    def grafico_donut_curso(self): 
        df = self.df_disciplinas()

        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        curso_value = self.curso_value

        if curso_value == "Todas":
            df_filtered = df.copy()
        else:
            df_filtered = df[df['CURSO'] == curso_value]

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

        if curso_value == "Todas":
            titulo = "Distribuição Geral de Respostas: Todos os Cursos"
        else:
            titulo = f"Distribuição Geral de Respostas – Curso: {curso_value}"

        fig_donut.update_layout(
            title=titulo,
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0),
            height=400
        )

        return total_resp, fig_donut

    def grafico_distribuicao_geral_sentimento(self): 
        df = self.df_disciplinas()
        df['valor'] = df['VALOR_RESPOSTA']
        agg = df.groupby('ID_PESQUISA').agg(
            n_answers=('valor', 'count'),
            mean_sentiment=('valor', 'mean'),
            pct_negative=('valor', lambda x: (x == -1).mean()),
        ).reset_index()


        fig3 = px.histogram(
            agg,
            x="mean_sentiment",
            nbins=30,
            title="Distribuição do Sentimento Médio",
            color_discrete_sequence=["#1f77b4"], 
            opacity=0.8
        )

        fig3.update_layout(
            xaxis_title="Sentimento Médio por Pessoa",
            yaxis_title="Quantidade de Pessoas",
            bargap=0.1, 
            height=500
        )
        fig3.add_vline(x=0, line_width=2, line_dash="dash", line_color="gray", annotation_text="Neutro")

        return fig3 
    
    def grafico_saldo_opiniao_dimensao(self):
        df = self.df_disciplinas()
        dim_sel = self.dimensao_value
        if not dim_sel:
            return None

        if 'DIMENSAO_NOME' not in df.columns:
            return None

        df_filtered = df[df["DIMENSAO_NOME"] == dim_sel]
        if df_filtered.empty:
            return None

        stats_pct = pd.crosstab(
            df_filtered['PERGUNTA'], 
            df_filtered['RESPOSTA'], 
            normalize='index'
        ) * 100

        for col in ['Concordo', 'Discordo', 'Desconheço']:
            if col not in stats_pct.columns:
                stats_pct[col] = 0.0

        stats_pct = stats_pct.sort_values('Concordo', ascending=True)

        questions = stats_pct.index.tolist()
        concordo_list = stats_pct['Concordo'].tolist()
        discordo_list = stats_pct['Discordo'].tolist()
        desconheco_list = stats_pct['Desconheço'].tolist()

        desconheco_metade = [x / 2 for x in desconheco_list]
        desconheco_metade_neg = [-x for x in desconheco_metade]
        discordo_neg_list = [-x for x in discordo_list]

        hover_desconheco = [f"Desconheço: {x:.1f}%" for x in desconheco_list]
        text_desconheco = [f"{x:.1f}%" if x > 1 else "" for x in desconheco_list]

        def quebrar_texto(texto, max_chars=60):
            if len(texto) <= max_chars: 
                return texto
            import textwrap
            return "<br>".join(textwrap.wrap(texto, width=max_chars))

        questions_formatted = [quebrar_texto(q) for q in questions]

        fig_div = go.Figure()

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade_neg,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=True,
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly'
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=False,
            text=text_desconheco, textposition='inside',
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly'
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=discordo_neg_list,
            name='Discordo', orientation='h', marker_color='#e74c3c',
            text=[f"{x:.1f}%" if x > 1 else "" for x in discordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Discordância: {x:.1f}%" for x in discordo_list]
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=concordo_list,
            name='Concordo', orientation='h', marker_color='#2ecc71',
            text=[f"{x:.1f}%" if x > 1 else "" for x in concordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Concordância: {x:.1f}%" for x in concordo_list]
        ))

        fig_div.update_layout(
            barmode='relative',
            title=f"Saldo de Opinião: {dim_sel}",
            xaxis_title="% Rejeição <---> % Aprovação",
            yaxis=dict(title=""),
            bargap=0.3,
            legend_title_text='Sentimento',
            height=max(400, len(questions) * 60 + 150),
            margin=dict(l=10, r=10, t=80, b=20)
        )

        fig_div.add_vline(x=0, line_width=1, line_color="black", opacity=0.3)

        return fig_div

