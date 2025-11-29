import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from services.AvaliacaoInstitucionalService import AvaliacaoInstitucionalService


BORDER = 1
COLOR_MAP = {
    'Concordo': '#2ecc71',
    'Discordo': '#e74c3c',
    'Desconheço': '#95a5a6'
}


def avaliacao_institucional_view():
    @st.cache_data
    def load_data_detalhado():
        hierarquia = {
            "Eixo 3 - Políticas Acadêmicas": {
                "Dimensão 2 - Ensino, Pesquisa e Extensão": [
                    "01 - O curso promove a interdisciplinaridade?",
                    "02 - O curso possibilita formação plural?",
                    "03 - O curso relaciona teoria com prática?",
                    "06 - Há indissociabilidade ensino-pesquisa?",
                ],
                "Dimensão 9 - Política de Atendimento": [
                    "18 - O atendimento pedagógico é suficiente?",
                    "19 - O apoio à permanência gera resultados?",
                ]
            },
            "Eixo 4 - Políticas de Gestão": {
                "Dimensão 5 - Políticas de Pessoal": [
                    "25 - O corpo docente é qualificado?",
                    "26 - Os técnicos atendem bem as demandas?",
                ],
                "Dimensão 6 - Gestão da Instituição": [
                    "12 - Os canais de comunicação são visíveis?",
                    "13 - A imagem pública é bem acompanhada?",
                ]
            }
        }

        data = []
        for _ in range(500):
            eixo_key = np.random.choice(list(hierarquia.keys()))
            dim_key = np.random.choice(list(hierarquia[eixo_key].keys()))
            perg_key = np.random.choice(hierarquia[eixo_key][dim_key])
            
            resp = np.random.choice(
                ['Concordo', 'Discordo', 'Desconheço'],
                p=[0.6, 0.3, 0.1]
            )
            
            data.append([eixo_key, dim_key, perg_key, resp])
            
        return pd.DataFrame(
            data,
            columns=['EIXO', 'DIMENSAO', 'PERGUNTA', 'RESPOSTA']
        )

    df = load_data_detalhado()
    st.set_page_config(
        page_title="Resultados Avaliação Institucional - UFPR",
        layout="wide"
    )
    
    st.title('Resultados Avaliação Institucional')

    col1, col2, col3, col4 = st.columns(4)
    service = AvaliacaoInstitucionalService(
        eixos_value=None,
        perguntas_value=None
    )
    qtd_respondentes_ano_atual = service.total_respondentes_ano_atual()
    pct_comparacao, qtd_respondentes_ano_passado = (
        service.total_respondentes_ano_passado()
    )
    
    with col1:
        st.metric(
            label="Total Respondentes",
            border=BORDER,
            value=qtd_respondentes_ano_atual,
            delta=f"{pct_comparacao}% Ano passado: {qtd_respondentes_ano_passado}"
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value="10%",
            delta=1,
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value="10%",
            delta=2,
            delta_color="inverse"
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value="10%",
            delta=1
        )
        
    col1, col2 = st.columns(2)
    
    with col1:
        opcoes_eixo = ["Todos"] + list(df['EIXO'].unique())
        eixo_value = st.multiselect(
            "Eixo",
            opcoes_eixo,
            default=["Todos"],
            key="filtro_eixo"
        )
        
    with col2:
        opcoes_perguntas = ["Todos"]
        perguntas_value = st.multiselect(
            "Perguntas",
            opcoes_perguntas,
            default=["Todos"],
            key="filtro_perguntas"
        )
        
    service = AvaliacaoInstitucionalService(
        eixos_value=eixo_value,
        perguntas_value=perguntas_value
    )
    st.markdown("---")

    if "Todos" in eixo_value or not eixo_value:
        df_filtered = df.copy()
    else:
        df_filtered = df[df['EIXO'].isin(eixo_value)]

    total_resp = len(df_filtered)
    if total_resp > 0:
        counts = df_filtered['RESPOSTA'].value_counts()
        conc_pct = (counts.get('Concordo', 0) / total_resp) * 100
        disc_pct = (counts.get('Discordo', 0) / total_resp) * 100
        desc_pct = (counts.get('Desconheço', 0) / total_resp) * 100
    else:
        conc_pct = disc_pct = desc_pct = 0
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Distribuição Total (Seleção)")
        
        if total_resp > 0:
            df_pizza = df_filtered['RESPOSTA'].value_counts().reset_index()
            df_pizza.columns = ['RESPOSTA', 'CONTAGEM']
            
            fig_donut = px.pie(
                df_pizza,
                values='CONTAGEM',
                names='RESPOSTA',
                hole=0.5,
                color='RESPOSTA',
                color_discrete_map=COLOR_MAP
            )
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label'
            )
            fig_donut.update_layout(
                showlegend=False,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
            st.caption(f"Total de respostas consideradas: {total_resp}")
        else:
            st.warning("Sem dados para os filtros selecionados.")

    with col_graf2:
        st.subheader("Comparativo por Eixo")
        
        if "Todos" in eixo_value:
            df_comp = df
        else:
            df_comp = df_filtered
            
        df_grouped = (
            df_comp.groupby(['EIXO', 'RESPOSTA'])
            .size()
            .reset_index(name='COUNT')
        )
        total_por_eixo = (
            df_comp.groupby('EIXO')
            .size()
            .reset_index(name='TOTAL')
        )
        df_merged = pd.merge(df_grouped, total_por_eixo, on='EIXO')
        df_merged['PERCENT'] = (df_merged['COUNT'] / df_merged['TOTAL']) * 100
        df_merged = df_merged.sort_values('EIXO')

        fig_bar = px.bar(
            df_merged,
            x="EIXO",
            y="PERCENT",
            color="RESPOSTA",
            color_discrete_map=COLOR_MAP,
            barmode='stack',
            text_auto='.0f',
            height=400
        )
        
        fig_bar.update_layout(
            xaxis_title="",
            yaxis_title="% das Respostas",
            legend_title="",
            xaxis={'tickangle': -45}
        )
        fig_bar.update_yaxes(range=[0, 100])
        
        st.plotly_chart(fig_bar, use_container_width=True)

    eixos_disponiveis = df["EIXO"].unique()
    eixo_sel = st.selectbox("Selecione o Eixo:", eixos_disponiveis)

    dimensoes_disponiveis = df[df["EIXO"] == eixo_sel]["DIMENSAO"].unique()
    dim_sel = st.selectbox(
        "Selecione a Dimensão para Análise Detalhada:",
        dimensoes_disponiveis
    )

    df_filtered = df[df["DIMENSAO"] == dim_sel]

    grouped = (
        df_filtered.groupby(['PERGUNTA', 'RESPOSTA'])
        .size()
        .unstack(fill_value=0)
    )

    stats_pct = grouped.div(grouped.sum(axis=1), axis=0) * 100

    if 'Concordo' not in stats_pct.columns:
        stats_pct['Concordo'] = 0.0
    if 'Discordo' not in stats_pct.columns:
        stats_pct['Discordo'] = 0.0

    stats_pct = stats_pct.sort_values('Concordo', ascending=True)

    questions = stats_pct.index.tolist()
    concordo_list = stats_pct['Concordo'].tolist()
    discordo_list = stats_pct['Discordo'].tolist()
    discordo_neg_list = [-x for x in discordo_list]

    fig_div = go.Figure()

    fig_div.add_trace(go.Bar(
        y=questions,
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
        y=questions,
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
        title=f"Saldo de Opinião por Questão: {dim_sel.split('-')[0]}",
        xaxis_title="% Rejeição <---> % Aprovação",
        yaxis=dict(title=""),
        bargap=0.3,
        legend_title_text='Sentimento',
        height=len(questions) * 50 + 150
    )

    fig_div.add_vline(x=0, line_width=1, line_color="black")

    st.plotly_chart(fig_div, use_container_width=True)

    with st.expander("Ver dados brutos (Frequências Absolutas)"):
        st.dataframe()
        message = "Lorem ipsum.\nStreamlit is cool."
        st.download_button(
            label="Download Dados brutos",
            data=message,
            file_name="message.txt",
            on_click="ignore",
            type="primary",
            icon=":material/download:"
        )