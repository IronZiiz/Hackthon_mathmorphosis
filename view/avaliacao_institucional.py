import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from services.AvaliacaoInstitucionalService import AvaliacaoInstitucionalService

BORDER = 1
def avaliacao_institucional_view():

    st.set_page_config(page_title="Resultados Avaliação Institucional - UFPR")


    @st.cache_data
    def load_data():
        data = {
            'ID_PERGUNTA': [1, 1, 1, 2, 2, 2, 3, 3, 3] * 20,
            'PERGUNTA': [
                'O curso promove a interdisciplinaridade?',
                'O curso promove a interdisciplinaridade?',
                'O curso promove a interdiscipisciplinaridade?',
                'A infraestrutura é adequada?',
                'A infraestrutura é adequada?',
                'A infraestrutura é adequada?',
                'A comunicação institucional é eficiente?',
                'A comunicação institucional é eficiente?',
                'A comunicação institucional é eficiente?'
            ] * 20,
            'EIXO': ['Eixo 3 - Políticas Acadêmicas'] * 60 + ['Eixo 5 - Infraestrutura'] * 60 + ['Eixo 4 - Gestão'] * 60,
            'DIMENSAO': ['Dimensão 2 - Ensino, Pesquisa, Extensão'] * 60 + ['Dimensão 7 - Infraestrutura Física'] * 60 + ['Dimensão 8 - Comunicação'] * 60,
            'RESPOSTA': ['Concordo', 'Discordo', 'Desconheço', 'Concordo', 'Concordo', 'Discordo'] * 30,
            'CURSO': ['Matemática', 'Matemática', 'Física', 'Design', 'Matemática', 'Física'] * 30,
            'SETOR': ['Exatas', 'Exatas', 'Exatas', 'Humanas', 'Exatas', 'Exatas'] * 30,
            'ANO': [2024] * 180
        }
        return pd.DataFrame(data)

    df = load_data()

    ano_sel = 2024
    setor_sel = "Exatas"
    curso_sel = "Matemática"

    def calcular_frequencias(dataframe, group_col=None):
        if group_col:
            base = dataframe.groupby([group_col, 'RESPOSTA']).size().reset_index(name='Contagem')
            total = dataframe.groupby([group_col]).size().reset_index(name='Total')
            merged = pd.merge(base, total, on=group_col)
        else:
            base = dataframe.groupby(['RESPOSTA']).size().reset_index(name='Contagem')
            base['Total'] = dataframe.shape[0]
            merged = base

        merged['Percentual'] = (merged['Contagem'] / merged['Total']) * 100
        return merged

    df_curso = df[(df['CURSO'] == curso_sel) & (df['ANO'] == ano_sel)]
    df_setor = df[(df['SETOR'] == setor_sel) & (df['ANO'] == ano_sel)]
    df_ufpr = df[df['ANO'] == ano_sel]

    st.title(f'Resultados Avaliação Institucional')
    service_avaliacao_institucional = AvaliacaoInstitucionalService(
         eixos_value= None,
         perguntas_value= None)
    
    col1, col2, col3, col4 = st.columns(4)
    pct_comparacao_ano_atual,qtd_respondentes_ano_passado =  service_avaliacao_institucional.total_respondentes_ano_passado()
    with col1:
        st.metric(label="Total Respondentes",
                          border=BORDER,
                          value= service_avaliacao_institucional.total_respondentes_ano_atual(),
                          delta= f"{pct_comparacao_ano_atual}% Ano passado: {qtd_respondentes_ano_passado} ", 
                          )
        
    with col2: 
        st.metric(label="Concordância",
                          border=BORDER,
                          value= 0,
                          delta= f"Ano passado: 200 ")
    with col3:
        st.metric(label="Discordância",
                          border=BORDER,
                          value= 0,
                          delta= f"Ano passado: 200 ")
        
    with col4: 
        st.metric(label="Desconhecimento",
                          border=BORDER,
                          value= 0,
                          delta= f"Ano passado: 200 ")
        
    col1, col2 = st.columns(2)
    with col1: 
        eixo_value = st.multiselect(
        "Eixo",
        ["Todos","Planejamento e Avaliação", "Desenvolvimento Instucional", "Polítias Acadêmicas", "Políticas De Gestão", "Infraestrutura Física"],
        default=["Todos"],
        key= "eixo_value"
    )

    with col2:
        perguntas_value = st.multiselect(
        "Selecione as perguntas",
        ["Todas"],
        default=["Todas"],
        key = "perguntas_value"
    )
    
    service_avaliacao_institucional = AvaliacaoInstitucionalService(
         eixos_value= eixo_value,
         perguntas_value= perguntas_value)
         
    
         
    
    col1, col2 = st.columns(2)
    color_map = {'Concordo': '#2ecc71', 'Discordo': '#e74c3c', 'Desconheço': '#95a5a6'}
    with col1:
        
    
        pergunta_sel = 'O curso promove a interdisciplinaridade?'
        q_curso = df_curso[df_curso['PERGUNTA'] == pergunta_sel]
        q_setor = df_setor[df_setor['PERGUNTA'] == pergunta_sel]
        q_ufpr = df_ufpr[df_ufpr['PERGUNTA'] == pergunta_sel]

        if not q_curso.empty:
            stats_curso = calcular_frequencias(q_curso).assign(Escopo=f"Curso ({curso_sel})")
            stats_setor = calcular_frequencias(q_setor).assign(Escopo=f"Setor ({setor_sel})")
            stats_ufpr = calcular_frequencias(q_ufpr).assign(Escopo="UFPR (Geral)")
            df_comparativo = pd.concat([stats_curso, stats_setor, stats_ufpr])

            fig_comp = px.bar(
                df_comparativo,
                x="Escopo",
                y="Percentual",
                color="RESPOSTA",
                barmode="group",
                color_discrete_map=color_map,
                text_auto='.1f',
                title=f"Comparativo geral das respostas"
            )

            fig_comp.update_layout(yaxis_title="% Frequência Relativa")
            st.plotly_chart(fig_comp, use_container_width=True)
    with col2: 
        df_concordo = df[df['RESPOSTA'] == 'Concordo']
        radar_curso = df_concordo[df_concordo['CURSO'] == curso_sel].groupby('DIMENSAO').size()
        total_curso = df[df['CURSO'] == curso_sel].groupby('DIMENSAO').size()
        score_curso = (radar_curso / total_curso * 100).fillna(0).reset_index(name='Score')
        radar_setor = df_concordo[df_concordo['SETOR'] == setor_sel].groupby('DIMENSAO').size()
        total_setor = df[df['SETOR'] == setor_sel].groupby('DIMENSAO').size()
        score_setor = (radar_setor / total_setor * 100).fillna(0).reset_index(name='Score')
        categories = score_curso['DIMENSAO'].tolist()
        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=score_curso['Score'],
            theta=categories,
            fill='toself',
            name=f'Média Eixos selecionados',
            line_color='#1f77b4'
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=score_setor['Score'],
            theta=categories,
            fill='toself',
            name=f'Média Todos os eixos',
            line_color='#ff7f0e',
            opacity=0.5
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Comparação concordância média dos eixos com eixos filtrado  "
        )
    
           
        dimensoes = df['DIMENSAO'].unique()
       

    st.selectbox("Selecione a Dimensão para Análise Detalhada:",dimensoes, key = 2)
    dim_sel = 'Dimensão 2 - Ensino, Pesquisa, Extensão'
    df_diverg = df[(df['CURSO'] == curso_sel) & (df['DIMENSAO'] == dim_sel)]
    grouped = df_diverg.groupby(['PERGUNTA', 'RESPOSTA']).size().unstack(fill_value=0)
    grouped_pct = grouped.div(grouped.sum(axis=1), axis=0) * 100
    questions = grouped_pct.index.tolist()
    concordo = grouped_pct.get('Concordo', pd.Series([0]*len(questions))).tolist()
    discordo = grouped_pct.get('Discordo', pd.Series([0]*len(questions))).tolist()
    discordo_neg = [-x for x in discordo]

    fig_div = go.Figure()
    fig_div.add_trace(go.Bar(
        y=questions, x=discordo_neg,
        name='Discordo', orientation='h',
        marker_color='#e74c3c',
        text=[f"{x:.1f}%" for x in discordo], textposition='auto'
    ))
    fig_div.add_trace(go.Bar(
        y=questions, x=concordo,
        name='Concordo', orientation='h',
        marker_color='#2ecc71',
        text=[f"{x:.1f}%" for x in concordo], textposition='auto'
    ))

    fig_div.update_layout(
        barmode='relative',
        title=f"Saldo de Opinião: {dim_sel}",
        xaxis_title="% Rejeição <---> % Aprovação",
        yaxis=dict(autorange="reversed"),
        bargap=0.3,
        legend_title_text='Sentimento'
    )

    fig_div.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
    st.plotly_chart(fig_div, use_container_width=True, key = "1")

    with st.expander("Ver dados brutos (Frequências Absolutas)"):
                    st.dataframe()
                    message = "Lorem ipsum.\nStreamlit is cool."
                    st.download_button(
                            label="Download Dados brutos",
                            data=message,
                            file_name="message.txt",
                            on_click="ignore",
                            type="primary",
                            icon=":material/download:",
        )
    
    
        
    
