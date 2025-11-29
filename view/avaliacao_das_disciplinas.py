import streamlit as st 
import plotly.express as px
import pandas as pd

BORDER = 1
COLOR_MAP = {
    'Concordo': '#2ecc71',
    'Discordo': '#e74c3c',
    'Desconheço': '#95a5a6'
}

def avaliacao_das_disciplinas_view():

    
    st.title('Resultados Avaliação Disciplinas')

    col1,_,_,_,_,_= st.columns(6)
    with col1:
        year_value = st.selectbox('Selecione o Ano/Período', 
                                ('2025/2','2025/1','2024/2', '2024/1'),
                                index = 0)
        
    st.header('Metricas de todas disciplinas')
    col1,col2,col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=1,
            delta=f"% Ano passado: "
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"%",
            delta=1,
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"%",
            delta=2,
            delta_color="inverse"
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"%",
            delta=1
        )
    
    disciplina_value = st.selectbox("Pesquise a disciplina de seu interesse",
                                      ('disciplina 1','disciplina2 ','disciplina3', 'disciplina4'))
    
    df_disciplina = pd.DataFrame({
    "RESPOSTA": ["Concordo", "Discordo", "Neutro"],
    "CONTAGEM": [40, 10, 8]
    })

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
        st.subheader("Distribuição total nome da disciplina")
        fig = px.pie(
            df_disciplina,
            values="CONTAGEM",
            names="RESPOSTA",
            hole=0.5,
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Comparativo por Eixo")

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
        st.plotly_chart(fig_bar, use_container_width=True)

        
        
    st.header("Comparação com o Setor e Curso")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Setor")
        fig = px.pie(
            df_setor,
            values="CONTAGEM",
            names="RESPOSTA",
            hole=0.5,
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Curso")
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
        st.plotly_chart(fig, use_container_width=True)
   

 