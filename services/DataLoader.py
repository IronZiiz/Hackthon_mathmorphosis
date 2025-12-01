import pandas as pd 

PATH_TO_DIR = "data/processed/"
PATH_DADOS_INSTITUCIONAL = PATH_TO_DIR + "Institucional2025/processed_Institucional_2025.csv"
PATH_DADOS_DISCIPLINAS_PRESENCIAL = PATH_TO_DIR + "Presencial2025/processed_presencial_2025.csv"
PATH_DADOS_DISCIPLINAS_EAD = PATH_TO_DIR + "EAD2025/processed_ead_2025.csv"
PATH_DADOS_CURSOS = PATH_TO_DIR + "Cursos2024/Cursos2024_limpo.csv"

class DataLoader:
    def __init__(self): 
        pass 

    @staticmethod
    def load_dados_institucional(path: str = PATH_DADOS_INSTITUCIONAL) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
    
    @staticmethod
    def load_dados_disciplinas_presencial(path: str = PATH_DADOS_DISCIPLINAS_PRESENCIAL) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
    
    @staticmethod
    def load_dados_disciplinas_presencial(path: str = PATH_DADOS_DISCIPLINAS_EAD) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
    
    @staticmethod
    def load_dados_curso(path: str = PATH_DADOS_CURSOS) -> pd.DataFrame: 
        df = pd.read_csv(path)
        return df 
    