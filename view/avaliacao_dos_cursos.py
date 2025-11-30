import streamlit as st 
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from services.AvalicaoDosCursosService import *
BORDER = 1
COLOR_MAP = {
    'Concordo': '#2ecc71',
    'Discordo': '#e74c3c',
    'Desconheço': '#95a5a6'
}

service = AvaliacaoDosCursosService()

def avaliacao_dos_cursos_view():

    st.title("Resultados Avaliação dos Cursos")

    col1,_,_,_,_,_= st.columns(6)
    with col1:
        year_value = st.selectbox('Selecione o Ano/Período',('2025','2024'), 
                                                             index = 0,key = "year_value_cursos")
        
    st.header('Metricas de todos os Cursos')
    col1,col2,col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=f"{service.get_total_respondentes(path='data/processed/Cursos2025/Cursos2025_limpo.csv')}",
            delta=f"% Ano passado: "
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{service.get_concordancia(path='data/processed/Cursos2025/Cursos2025_limpo.csv'):.2f}%",
            delta=1
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{service.get_discordancia(path='data/processed/Cursos2025/Cursos2025_limpo.csv'):.2f}%",
            delta=2
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{service.get_desconhecimento(path='data/processed/Cursos2025/Cursos2025_limpo.csv'):.2f}%",
            delta=1
        )    
    curso_value = st.selectbox("Pesquise a curso de seu interesse",
                                      ('curso 1 -- Setor: exatas ','curso2 -- Setor:tec ','disciplina3', 'disciplina4'), key = "curso_value")
    
    df_setor = pd.DataFrame({
        "RESPOSTA": ["Concordo", "Discordo", "Neutro"],
        "CONTAGEM": [70, 20, 15]
    })

    df_curso = pd.DataFrame({
        "RESPOSTA": ["Concordo", "Discordo", "Neutro"],
        "CONTAGEM": [55, 12, 5]
    })

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribuição total (colocar nome do curso)")
        fig = px.pie(
            df_curso,
            values="CONTAGEM",
            names="RESPOSTA",
            hole=0.5,
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True, key = 'plot_pie_curso')
    with col2:
        st.subheader("Comparativo por Eixo (Sera um numero fixo)")
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