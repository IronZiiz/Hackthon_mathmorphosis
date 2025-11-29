import pandas as pd
from services.DataLoader  import DataLoader

class AvaliacaoInstitucionalService(DataLoader): 
    def __init__(self, 
                 eixos_value = None,
                 perguntas_value = None,
                 ):
        #self.df = DataLoader.load_dados_institucional()
        self.eixos_value = eixos_value
        self.perguntas_value = perguntas_value


    def total_respondentes_ano_atual(self): 
        # self.df = DataLoader.load_dados_institucional()
        qtd_respondentes_atual = 2000
        return qtd_respondentes_atual
    
    def total_respondentes_ano_passado(self): 
        qtd_respondentes_ano_atual = self.total_respondentes_ano_atual()
        qtd_respondentes_ano_passado = 1000
        pct_comparacao_ano_atual =(qtd_respondentes_ano_atual/qtd_respondentes_ano_passado - 1)*100
        return pct_comparacao_ano_atual,qtd_respondentes_ano_passado

