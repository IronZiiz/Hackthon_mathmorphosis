import streamlit as st 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from services.AvalicaoDosCursosService import AvaliacaoDosCursosService

BORDER = 1
COLOR_MAP = {
    'Concordo': '#2ecc71',
    'Discordo': '#e74c3c',
    'Desconheço': '#95a5a6'
}


def avaliacao_dos_cursos_view():
    service = AvaliacaoDosCursosService()
    st.title("Resultados Avaliação dos Cursos")

    col1,_,_,_,_,_= st.columns(6)
    with col1:
        year_value = st.selectbox('Selecione o Ano/Período',('2025','2024'), 
                                                             index = 1,key = "year_value_cursos")
    col1,col2,col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=f"{service.get_total_respondentes()}",
            delta=f"% Ano passado: "
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{service.get_concordancia():.2f}%",
            delta=1
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{service.get_discordancia():.2f}%",
            delta=2
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{service.get_desconhecimento():.2f}%",
            delta=1
        )    
    select_box_value_curso_setor = st.selectbox(
        "Pesquise o curso de seu interesse",
        service.formatacao_curso_setor(),
        key="curso_value" 
        )
    
    if select_box_value_curso_setor == "Todos os cursos":
        curso_value = "Todos"
        setor_value = "Todos"

    elif " - Setor: " in select_box_value_curso_setor:
        curso_value, setor_value = (
            select_box_value_curso_setor
            .replace("Curso: ", "")
            .split(" - Setor: ")
        )

    else:
        curso_value = select_box_value_curso_setor
        setor_value = ""

    service = AvaliacaoDosCursosService(
        curso_value=curso_value,
        setor_value=setor_value)
    

    col1, col2 = st.columns(2)
    with col1:
        total_resp, fig_donut = service.grafico_distribuicao_donut()
        st.plotly_chart(fig_donut, use_container_width=True, key = 'plot_pie_curso')

    with col2:
        st.write("")
        st.write("")
        df_merged = pd.DataFrame({
        "EIXO": ["Infraestrutura", "Infraestrutura", "Infraestrutura",
                "Didática", "Didática", "Didática"],
        "RESPOSTA": ["Concordo", "Discordo", "Desconheço",
                    "Concordo", "Discordo", "Desconheço"],
        "COUNT": [40, 8, 6, 50, 12, 5],
        "TOTAL": [54, 54, 54, 67, 67, 67]
    })
        df_merged["PERCENT"] = (df_merged["COUNT"] / df_merged["TOTAL"]) * 100
        fig_bar = px.bar(
        df_merged,
        x="EIXO",
        y="PERCENT",
        color="RESPOSTA",
        color_discrete_map=COLOR_MAP,
        barmode="stack",
        text_auto=".0f",
        height=400
        )
        fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="% das Respostas",
        legend_title="",
        )
        fig_bar.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_bar, use_container_width=True, key ="plot_bar_curso_eixo")
        
    dimensoes = ["Dimensão 1", "Dimensão 2"]

    dim_sel = st.selectbox(
    "Selecione a Dimensão para Análise Detalhada:",
        dimensoes,key = "dimensao_curso"
    )

    questions = [
        "O curso apresenta boa organização geral",
        "As atividades do curso possuem coerência pedagógica",
        "O conteúdo do curso está atualizado",
        "O curso promove desenvolvimento de competências práticas"
    ]

    concordo_list = [72, 61, 58, 83]
    discordo_list = [14, 22, 28, 9]
    discordo_neg_list = [-x for x in discordo_list]

    def quebrar_texto(texto, max_chars=50):
        if len(texto) <= max_chars:
            return texto
        palavras = texto.split()
        linhas = []
        linha = ""
        for p in palavras:
            if len(linha) + len(p) + 1 <= max_chars:
                linha += p + " "
            else:
                linhas.append(linha.strip())
                linha = p + " "
        if linha:
            linhas.append(linha.strip())
        return "<br>".join(linhas)

    questions_formatted = [quebrar_texto(q) for q in questions]

    fig_div = go.Figure()

    fig_div.add_trace(go.Bar(
        y=questions_formatted,
        x=discordo_neg_list,
        name='Discordo',
        orientation='h',
        marker_color='#e74c3c',
        text=[f"{x:.1f}%" for x in discordo_list],
        textposition='auto',
        hoverinfo='text+y',
        hovertext=[f"Discordância: {x:.1f}%" for x in discordo_list]
    ))

    fig_div.add_trace(go.Bar(
        y=questions_formatted,
        x=concordo_list,
        name='Concordo',
        orientation='h',
        marker_color='#2ecc71',
        text=[f"{x:.1f}%" for x in concordo_list],
        textposition='auto',
        hoverinfo='text+y',
        hovertext=[f"Concordância: {x:.1f}%" for x in concordo_list]
    ))

    fig_div.update_layout(
        barmode='relative',
        title=f"Saldo de Opinião por Questão – {dim_sel}",
        xaxis_title="% Rejeição <---> % Aprovação",
        yaxis=dict(title=""),
        bargap=0.3,
        legend_title_text='Sentimento',
        height=len(questions) * 60 + 200
    )

    fig_div.add_vline(x=0, line_width=1, line_color="black")

    st.plotly_chart(fig_div, use_container_width=True, key ="plot_perguntas_curso")