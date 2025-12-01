import streamlit as st
from view.home import home_view
from view.avaliacao_institucional import avaliacao_institucional_view
from view.avaliacao_das_disciplinas import avaliacao_das_disciplinas_view
from view.avaliacao_dos_cursos import avaliacao_dos_cursos_view
from view.login  import login_view



def main():
    st.set_page_config(
        page_title="Dashboard UFPR",
        layout="wide",
    )

    tabs = st.tabs([
        "Home",
        "Avaliação Institucional",
        "Avaliação de Disciplinas",
        "Avaliação dos Cursos",
        "Administrador"
    ])

    with tabs[0]:
        home_view()

    with tabs[1]:
        avaliacao_institucional_view()

    with tabs[2]:
        avaliacao_das_disciplinas_view()

    with tabs[3]:
        avaliacao_dos_cursos_view()

    with tabs[4]:
        login_view()


