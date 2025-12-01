import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from services.DataLoader  import DataLoader



class AvaliacaoDasDisciplinasService(DataLoader): 
    def __init__(self,
                df_load_dados_avaliacao_disciplinas_presencial = None,
                df_load_dados_avaliacao_disciplinas_EAD = None, 
                disciplina_value = None,
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
        self.dimensao_value = dimensao_value 
        self.tipo_disciplina_value = tipo_disciplina_value

    def df_disciplinas(self)-> pd.DataFrame: 
        if self.tipo_disciplina_value == 'Presencial': 
            df_disciplinas = self.df_presencial
        else: 
            df_disciplinas = self.df_EAD

        return df_disciplinas
    
    def get_total_respondentes(self) ->int: 
        df = self.df_disciplinas()
        return df["ID_PESQUISA"].nunique() 


    
    

        
    
