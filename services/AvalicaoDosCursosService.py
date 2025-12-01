from services.DataLoader  import DataLoader
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class AvaliacaoDosCursosService(DataLoader): 
    def __init__(self,
                df_load_dados_curso = None,
                curso_value = None,
                setor_value = None, 
                ):
        
        if df_load_dados_curso is None:
            df_load_dados_curso = DataLoader.load_dados_curso()

        self.df = df_load_dados_curso
        self.curso_value = curso_value

    def get_total_respondentes(self) -> int:
        return self.df["ID_PESQUISA"].nunique() # Será que essa quantidade é de fato os respondentes?
    
    def get_concordancia(self) -> float:
        df = self.df
        total = len(df)
        concordancia = len(df[df["RESPOSTA"] == "Concordo"])
        return (concordancia / total) * 100
    
    def get_discordancia(self) -> float:
        df = self.df
        total = len(df)
        discordancia = len(df[df["RESPOSTA"] == "Discordo"])

        return (discordancia / total) * 100
    
    def get_desconhecimento(self) -> float:
        df = self.df
        total = len(df)
        desconhecimento = len(df[df["RESPOSTA"] == "Desconheço"])
        return (desconhecimento / total) * 100
    
    def get_concordancia_total(self) -> int:
        df = self.df
        concordancia = len(df[df["RESPOSTA"] == "Concordo"])
        return concordancia
    
    def get_discordancia_total(self) -> int:
        df = self.df
        discordancia = len(df[df["RESPOSTA"] == "Discordo"])
        return discordancia
    
    def get_desconhecimento_total(self) -> int:
        df = self.df
        desconhecimento = len(df[df["RESPOSTA"] == "Desconheço"])
        return desconhecimento
    
    def formatacao_curso_setor(self) -> list:
        df = self.df[['CURSO','SETOR_CURSO']].drop_duplicates()

        opcoes = [
            f"Curso: {row.CURSO} - Setor: {row.SETOR_CURSO}"
            for row in df.itertuples()
        ]
        return ["Todos os cursos"] + sorted(opcoes)

    def df_curso_filtrado_selecionado(self) -> pd.DataFrame:
        df = self.df
        curso_value = self.curso_value
        if curso_value == 'Todos': 
            df_curso = df
        else:
            df_curso = df[df["CURSO"] == curso_value]

        return df_curso
    
    def grafico_distribuicao_donut(self):
        curso_value = self.curso_value
        COLOR_MAP = {
            'Concordo': '#2ecc71',
            'Discordo': '#e74c3c',
            'Desconheço': '#95a5a6'
        }

        df_filtered = self.df_curso_filtrado_selecionado()
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
            title=f"Distribuição Geral de Respostas curso: {curso_value}",
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
        df_filtered = self.df_curso_filtrado_selecionado()
        if df_filtered.empty:
            return None

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
            x="EIXO",
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
    
    def grafico_radar_setor_curso(self): 
        return fig

    

    
    