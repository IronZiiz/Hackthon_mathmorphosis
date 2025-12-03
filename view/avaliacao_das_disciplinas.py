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
        pct_ano_passado, total_ano_passado = service.total_respondentes_ano_passado()
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=service.get_total_respondentes_ano_atual(),
            delta=f"{pct_ano_passado:.2f}% Ano passado: {total_ano_passado}"
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{service.get_concordancia_atual():.2f}%",
            delta=f"{service.satisfacao_ano_passado():.2f}% Ano passado",
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{service.get_discordancia_atual():.2f}%",
            delta=f"{service.insatisfacao_ano_passado():.2f}% Ano passado",
            delta_color="inverse"
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{service.get_desconhecimento():.2f}%",
            delta=f"{service.desconhecimento_ano_passado():.2f}% Ano passado"
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
    st.markdown("---")
    st.subheader('Distribuição de respostas')
    st.markdown(
        """
        <p style="
            text-align:left;
            max-width:750px;
            margin:10px 0px 20px 0px;
            font-size:1rem;
            color:#555;
            opacity:1;
            line-height:1;
        ">
        A seguir, são apresentados gráficos que ilustram a distribuição das respostas dos participantes pelo eixo  em relação às afirmações feitas pela pesquisa. 
        </p>
        """,unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        total_resp, fig_donut = service.grafico_distribuicao_total_donut()

        if total_resp > 0:
            st.plotly_chart(fig_donut, use_container_width=True)
            st.caption(f"Total de respostas consideradas por pergunta:{total_resp}")
        else:
            st.warning("Sem dados para os filtros selecionados.")
    with col2:
        st.write("")
        st.write("")
        st.plotly_chart(service.grafico_resumo_por_eixo(), use_container_width=True)
    
    st.warning("Sim e Não representam as respostas seletoras, ou seja aquelas que indicam uma opinião clara e dão sequência a possibilidade de corcordar, discordar ou desconhecer uma afirmação.Sim foi considerado como concordo e Não como discordo.", icon="⚠️")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_respondentes, total_respostas = service.get_respondentes_filtrados()
        st.metric(
            label="Total Respondentes Filtrados",

            border=BORDER,
            value=total_respondentes,
            delta=f"{pct_ano_passado:.1f}% Ano passado: {total_ano_passado}"
        )


    with col2:
        pct_concordo, total_concordo = service.get_concordancia_filtrado()
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{pct_concordo:.2f}%",
            delta=f"{service.satisfacao_ano_passado():.2f}% Ano passado",
            delta_color="normal"
        )
        st.warning(f"Total respostas Concordo: {total_concordo}")


    with col3:
        pct_discordo, total_discordo = service.get_discordancia_filtrado()
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{pct_discordo:.2f}%",
            delta=f"{service.insatisfacao_ano_passado():.2f}% Ano passado",
            delta_color="normal"
        )
        st.warning(f"Total respostas Discordo: {total_discordo}")


    with col4:
        pct_desc, total_desc = service.get_desconhecimento_filtrado()
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{pct_desc:.2f}%",
            delta=f"{service.desconhecimento_ano_passado():.2f}% Ano passado",
            delta_color="normal"
        )
        st.warning(f"Total respostas Desconheço: {total_desc}")

    st.markdown("---")


    st.subheader('Análise detalhada das perguntas')
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
        A seguir, é possível selecionar uma dimensão específica para uma análise detalhada das perguntas relacionadas a essa dimensão.
                </p>
        """,unsafe_allow_html=True)

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

    
    st.markdown("---")
    st.header("Comparação com o Setor e Curso")
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
        A seguir, são apresentados gráficos que ilustram a comparação do sentimento médio da disciplina selecionada com o setor e curso correspondentes.
                        </p>
        """,unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        
        _, fig_donut_setor = service.grafico_donut_setor()        
        st.plotly_chart(fig_donut_setor, use_container_width=True)

    with col2:
        _, fig_donut_curso = service.grafico_donut_curso()
        st.plotly_chart(fig_donut_curso, use_container_width=True)

    st.warning("Sim e Não representam as respostas seletoras, ou seja aquelas que indicam uma opinião clara e dão sequência a possibilidade de corcordar, discordar ou desconhecer uma afirmação . Assumiu-se sim como concordância e Não como discordância.", icon="⚠️")
   
    st.markdown("---")
    st.header("Distribuição Geral do Sentimento Médio")
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
        A seguir, é apresentado um gráfico que ilustra a distribuição geral do sentimento médio dos respondentes.
                                </p>
        """,unsafe_allow_html=True)

    st.plotly_chart(service.grafico_distribuicao_geral_sentimento(), use_container_width=True)
    
    with st.expander("O que é o Sentimento Médio?", expanded=False):
        st.info(
            "O sentimento é representado em uma escala de -1 a +1. "
            "Valores **positivos** (concordância) indicam percepção favorável; "
            "valores **negativos** (discordância) indicam percepção desfavorável; "
            "**0** representa neutralidade. "
            "O valor é calculado pela média dos pesos atribuídos às respostas. "
            "Por exemplo, se um respondente concorda em 3 de 3 perguntas, seu sentimento será **3 ÷ 3 = 1**.",
            icon="ℹ️"
)
    st.warning("""
    **Insight:** A grande maioria dos respondentes tem sentimento médio entre **0 e +1**, 
    mostrando que o padrão geral é positivo.
    """)
  

    st.markdown("---")
    with st.expander("Ver dados brutos (Frequências Absolutas) (Em desenvolvimento :3)"):
        st.dataframe()
        message = "Lorem ipsum.\nStreamlit is cool."
        st.download_button(
            label="Download Dados brutos",
            data=message,
            file_name="message.txt",
            on_click="ignore",
            type="primary",
            icon=":material/download:",
            key="dowload-dados-brutos-disciplinas"

        )

    