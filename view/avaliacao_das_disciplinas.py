import streamlit as st 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from services.AvaliacaoDasDisciplinasService import AvaliacaoDasDisciplinasService
 
BORDER = 1
COLOR_MAP = {
    'Concordo': '#2ecc71',
    'Discordo': '#e74c3c',
    'Desconheço': '#95a5a6'
}
COLOR_UFPR_BLUE = '#00548e'
COLOR_UFPR_BLACK ='#231F20'

def avaliacao_das_disciplinas_view():
    
    
    st.markdown(
        f"""
        <h1 style="text-align:left; font-size:3.4rem; font-weight:700;">
            <span style="color:{COLOR_UFPR_BLACK}">Resultados</span>
            <span style="color:{COLOR_UFPR_BLUE}">Avaliação das Disciplinas</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="
            text-align:left;
            max-width:750px;
            margin:0px 0px 20px 0px;
            font-size:1rem;
            color:#555;
            opacity:1;
            line-height:1;
        ">
        A Avaliação das Disciplinas é uma ferramenta essencial para medir a satisfação e o engajamento dos estudantes em relação às disciplinas oferecidas pela instituição.
        </p>
        """,unsafe_allow_html=True)

    col1,col2,_,_,_,_= st.columns(6)
    with col1:
        year_value = st.selectbox('Selecione o Ano/Período', 
                                ('2025/2','2025/1','2024/2', '2024/1'),
                                index = 0, key = "year_value_disciplina")
    with col2: 
        tipo_disciplina_value = st.selectbox('Presencial/EAD', 
                                             ('Presencial','EAD'), 
                                             index = 0, key = "tipo_disciplina_value"
                                             )
        tipo_disciplina_value = str(tipo_disciplina_value)

    service = AvaliacaoDasDisciplinasService(
        tipo_disciplina_value=tipo_disciplina_value)

    col1,col2,col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=service.get_total_respondentes_ano_atual(),
            delta=f"% Ano passado: "
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{service.get_concordancia_atual():.2f}%",
            delta=1,
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{service.get_discordancia_atual():.2f}%",
            delta=2,
            delta_color="inverse"
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{service.get_desconhecimento():.2f}%",
            delta=1
        )
    
    select_box_value_disciplina_curso_setor = st.selectbox("Pesquise a disciplina de seu interesse",
                                   service.formatacao_disciplina_curso_setor())
    
    select_box_value_disciplina_curso_setor = str(select_box_value_disciplina_curso_setor)
    if select_box_value_disciplina_curso_setor == "Todas as disciplinas":
        disciplina_value = "Todas"
        curso_value = "Todas"
        setor_value = "Todas"
    else:
        partes = select_box_value_disciplina_curso_setor.split(" - ")
        disciplina_value = partes[0].replace("Disciplina:", "").strip()
        curso_value = partes[1].replace("Curso:", "").strip()
        setor_value = partes[2].replace("Setor:", "").strip()
        
    service = AvaliacaoDasDisciplinasService(
        tipo_disciplina_value=tipo_disciplina_value,
        disciplina_value= disciplina_value,
        curso_value= curso_value,
        setor_value= setor_value)

    col1, col2 = st.columns(2)
    with col1:
        _, fig_donut = service.grafico_distribuicao_total_donut()

        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.write("")
        st.write("")
        st.plotly_chart(service.grafico_resumo_por_eixo(), use_container_width=True)

    st.subheader('Análise detalhada das perguntas')

    df = service.df_disciplinas()
    df_dim = df[['DIMENSAO_NUM', 'DIMENSAO_NOME']].drop_duplicates()

    lista_dimensoes_formated = df_dim['DIMENSAO_NOME'].tolist()

    dim_sel = st.selectbox(
        "Selecione a Dimensão para Análise Detalhada:",
        lista_dimensoes_formated
    )
    dim_sel = int(dim_sel)
    service = AvaliacaoDasDisciplinasService(
        tipo_disciplina_value=tipo_disciplina_value,
        disciplina_value= disciplina_value,
        curso_value= curso_value,
        setor_value= setor_value,
        dimensao_value=  dim_sel

        )
    
    st.plotly_chart(service.grafico_saldo_opiniao_dimensao(), use_container_width=True, key = "grafico_saldo_opiniao")

    

    st.header("Comparação com o Setor e Curso")
    col1, col2 = st.columns(2)
    with col1:
        
        _, fig_donut_setor = service.grafico_donut_setor()        
        st.plotly_chart(fig_donut_setor, use_container_width=True)

    with col2:
        _, fig_donut_curso = service.grafico_donut_curso()
        st.plotly_chart(fig_donut_curso, use_container_width=True)

   

    st.header("Distribuição Geral do Sentimento Médio")

    st.plotly_chart(service.grafico_distribuicao_geral_sentimento(), use_container_width=True)

    st.markdown("""
    **Insight:** A grande maioria dos respondentes tem sentimento médio entre **0 e +1**, 
    mostrando que o padrão geral é positivo.
    """)

    st.markdown("---")
    with st.expander("Ver dados brutos (Frequências Absolutas) (TEMPORÁRIO0"):
        st.dataframe()
        st.download_button('Download Dados brutos',data="aa")

    