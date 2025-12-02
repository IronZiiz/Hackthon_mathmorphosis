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
    
    # ---------- #
    st.markdown("---")
    # ---------- #
         
    col1, col2 = st.columns(2)
    with col1:
        opcoes_eixo = service.formatar_eixos()
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

    # ---------- #
    st.markdown("---")
    # ---------- #

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

    st.subheader('Participação das Unidades gestoras nas Pesquisas')
    col1, col2 = st.columns(2)
    with col1: 
        st.plotly_chart(service.grafico_barra_unidade_gestora(), use_container_width=True)

    with col2:
        st.plotly_chart(service.grafico_donut_top10(),use_container_width=True)

    # ---------- #
    st.markdown("---")
    # ---------- #

    st.subheader('Analise detalhada das perguntas')
    
    df_unique = df[['DIMENSAO_NUMERICA', 'DIMENSAO']].drop_duplicates().sort_values('DIMENSAO_NUMERICA')

    lista_dimensoes_formated = [
    f"{int(row.DIMENSAO_NUMERICA)} - {row.DIMENSAO}" 
    for row in df_unique.itertuples()
]

    dim_sel = st.selectbox(
        "Selecione a Dimensão para Análise Detalhada:",lista_dimensoes_formated
    )

    dim_sel_temp = dim_sel.split('-',maxsplit=1)[1].strip()

    service = AvaliacaoInstitucionalService( 
        eixos_value=eixo_value,
        perguntas_value=perguntas_value,
        dimensao_value=dim_sel_temp
    )

    figura_saldo = service.grafico_saldo_opiniao_dimensao()

    # 2. Verifica se veio um gráfico de verdade ou None
    if figura_saldo is not None:
        st.plotly_chart(figura_saldo, use_container_width=True)
    else:
        # 3. Mostra uma mensagem amigável se não tiver dados
        st.info("Aguardando seleção de uma dimensão válida ou não há dados para exibir.")

    # ---------- #
    st.markdown("---")
    # ---------- #

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