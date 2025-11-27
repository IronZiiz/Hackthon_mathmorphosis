import streamlit as st
from view.avaliacao_institucional import avaliacao_institucional_view
from view.avaliacao_das_disciplinas import avaliacao_das_disciplinas_view
from view.avaliacao_dos_cursos import avaliacao_dos_cursos_view
from view.home import home_view

page = st.sidebar.selectbox(
    "Selecione a página:",
    ['Home', 'Avaliação Institucional', 'Avaliação de Disciplinas', 'Avaliação dos Cursos']
)

match page:
    case 'Home':
        home_view()

    case 'Avaliação Institucional':
        avaliacao_institucional_view()

    case 'Avaliação de Disciplinas':
        avaliacao_das_disciplinas_view()

    case 'Avaliação dos Cursos':
        avaliacao_dos_cursos_view()

    case _:
        st.error("Página não encontrada.")
