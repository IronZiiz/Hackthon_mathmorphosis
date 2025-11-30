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

    df = AvaliacaoInstitucionalService().df_load_dados_institucional
    
    
    st.title('Resultados Avaliação Institucional')
    col1 ,_,_,_,_,_= st.columns(6)
    with col1:
        year_value = st.selectbox('Selecione o Ano', ('2025','2024'),
                                index = 0)

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
            delta=f"{pct_comparacao:.1f}% Ano passado: {qtd_respondentes_ano_passado}"
        )
        
    with col2:
        st.metric(
            label="Concordância",
            border=BORDER,
            value=f"{service.satisfacao_ano_atual():.2f}%",
            delta=1,
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            label="Discordância",
            border=BORDER,
            value=f"{service.insatisfacao_ano_atual():.2f}%",
            delta=2,
            delta_color="inverse"
        )
        
    with col4:
        st.metric(
            label="Desconhecimento",
            border=BORDER,
            value=f"{service.desconhecimento_ano_atual():.2f}%",
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

    if "Todos" in eixo_value or not eixo_value:
        df_filtered = df.copy()
    else:
        df_filtered = df[df['EIXO'].isin(eixo_value)].sort_values(by='Ordem')

    with col2:
        # Filter all the questions in the selected axis
        perguntas_unicas = (df_filtered['Ordem'].astype(int).astype(str) + ' - ' + df_filtered['PERGUNTA']).unique().tolist()
        opcoes_perguntas = ["Todos"] + sorted(perguntas_unicas, key=lambda x: int(x.split(' - ')[0]))
        
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
    st.subheader('Distribuição de respostas')

    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        total_resp, fig_donut_dist_total = service.grafico_distribuicao_total_donut()
        if total_resp > 0:
            st.plotly_chart(fig_donut_dist_total, use_container_width=True)
            st.caption(f"Total de respostas consideradas por pergunta:{total_resp}")
        else:
            st.warning("Sem dados para os filtros selecionados.")

    with col_graf2:

        st.plotly_chart(service.grafico_resumo_por_eixo(), use_container_width=True)
        
        
       


    st.markdown("---")
    st.subheader('Participação das Unidades gestoras nas Pesquisas')
    col1, col2 = st.columns(2)
    with col1: 
        st.plotly_chart(service.grafico_barra_unidade_gestora(), use_container_width=True)

    with col2:
        st.plotly_chart(service.grafico_donut_top10(),use_container_width=True)

    
    st.markdown("---")
    st.subheader('Analise detalhada das perguntas')

    lista_dimensoes = df_filtered['DIMENSAO'].unique()
    dim_sel = st.selectbox(
        "Selecione a Dimensão para Análise Detalhada:",lista_dimensoes
    )
    service = AvaliacaoInstitucionalService(
        eixos_value=eixo_value,
        perguntas_value=perguntas_value,
        dimensao_value=dim_sel
    )


    st.plotly_chart(service.grafico_saldo_opiniao_dimensao(), use_container_width=True)

    with st.expander("Ver dados brutos (Frequências Absolutas) (TEMPORÁRIO)"):
        st.dataframe(df) # Temp
        message = "Lorem ipsum.\nStreamlit is cool."
        st.download_button(
            label="Download Dados brutos",
            data=message,
            file_name="message.txt",
            on_click="ignore",
            type="primary",
            icon=":material/download:"
        )