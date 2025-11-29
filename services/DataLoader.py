import pandas as pd 

PATH_TO_DIR = "../data/processed/"
PATH_DADOS_INSTITUCIONAL = PATH_TO_DIR + "Institucional2025/processed_Institucional_2025.csv"
PATH_DADOS_DISCIPLINAS = ""
PATH_DADOS_CURSOS = ""

class DataLoader:
    def __init__(): 
        pass 

    def load_dados_institucional(self, path: str = PATH_DADOS_INSTITUCIONAL) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
    
    def load_dados_disciplinas(self, path: str = PATH_DADOS_DISCIPLINAS) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df
    
    def load_dados_curso(self, path: str = PATH_DADOS_CURSOS) -> pd.DataFrame: 
        df = pd.read_csv(path)
        return df 