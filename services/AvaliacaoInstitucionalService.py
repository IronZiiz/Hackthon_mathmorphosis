import pandas as pd
from services.DataLoader  import DataLoader

class AvaliacaoInstitucionalService(DataLoader): 
    def __init__(
        self, 
        eixos_value=None,
        perguntas_value=None,
        df_load_dados_institucional=None,
    ):
        if df_load_dados_institucional is None:
            df_load_dados_institucional = DataLoader.load_dados_institucional()

        self.df_load_dados_institucional = df_load_dados_institucional
        self.eixos_value = eixos_value
        self.perguntas_value = perguntas_value


    def total_respondentes_ano_atual(self): 
        df = self.df_load_dados_institucional
        df 
        qtd_respondentes_atual = 2000
        return qtd_respondentes_atual
    
    def total_respondentes_ano_passado(self): 
        qtd_respondentes_ano_atual = self.total_respondentes_ano_atual()
        qtd_respondentes_ano_passado = 1000
        pct_comparacao_ano_atual =(qtd_respondentes_ano_atual/qtd_respondentes_ano_passado - 1)*100
        return pct_comparacao_ano_atual,qtd_respondentes_ano_passado
    
    # satisfação = concordancia pois frases afirmativas
    def satisfacao_ano_atual(self):
        pct_satisfacao_ano_atual = 10
        return pct_satisfacao_ano_atual
    
    def satisfacao_ano_passado(self):
            pct_satisfacao_ano_passado = 10
            return pct_satisfacao_ano_passado
    
    def insatisfacao_ano_atual(self):
        pct_insatisfacao_ano_atual = 10
        return pct_insatisfacao_ano_atual
    
    def insatisfacao_ano_passado(self):
        pct_insatisfacao_ano_passado = 10
        return pct_insatisfacao_ano_passado 
    
    def desconhecimento_ano_atual(self): 
        pct_desconhecimento_ano_atual =10
        return pct_desconhecimento_ano_atual
    
    def desconhecimento_ano_passadol(self): 
        pct_desconhecimento_ano_passado=10
        return pct_desconhecimento_ano_passado 

    def grafico_dist_total_rosquinha(self): 
        fig = 'grafico'
        dataframe_fig = 'Data frame usado para construir a fig'
        return fig, dataframe_fig
    
    def grafico_dist_por_eixo_barra(self): 
        fig = 'grafico'
        dataframe_fig = 'Data frame usado para construir a fig'
        return fig, dataframe_fig
    
    def grafico_perguntas(self): 
        fig = 'grafico'
        dataframe_fig = 'Data frame usado para construir a fig'
        return fig, dataframe_fig
    
    def df_dados_brutos(self):
        dados_brutos = 'Dados com valores de freq relativa e absoluta'
        return dados_brutos