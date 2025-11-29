import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Constante de estilo
BORDER = 1
color_map = {'Concordo': '#2ecc71', 'Discordo': '#e74c3c', 'Desconheço': '#95a5a6'}

# ==============================================================================
# 1. GERAÇÃO DE DADOS (Simulando a estrutura do PDF sem Curso/Setor)
# ==============================================================================
@st.cache_data
def load_data_eixos():
    # Eixos baseados no PDF (Pág 1 e 2)
    eixos_definidos = [
        "1- Planejamento e Avaliação Institucional",
        "2- Desenvolvimento Institucional",
        "3- Políticas Acadêmicas",
        "4- Políticas de Gestão",
        "5- Infraestrutura Física"
    ]
    
    data = []
    # Gerando 1000 respostas aleatórias
    for _ in range(1000):
        eixo = np.random.choice(eixos_definidos)
        
        # Pesos diferentes para variar os dados (Ex: Infraestrutura tem mais reclamação)
        if "Infraestrutura" in eixo:
            weights = [0.50, 0.40, 0.10] # Mais discordo
        elif "Acadêmicas" in eixo:
            weights = [0.80, 0.10, 0.10] # Mais concordo
        else:
            weights = [0.65, 0.20, 0.15] # Padrão
            
        resp = np.random.choice(['Concordo', 'Discordo', 'Desconheço'], p=weights)
        data.append([eixo, resp])
        
    return pd.DataFrame(data, columns=['EIXO', 'RESPOSTA'])

def avaliacao_institucional_view():
    st.set_page_config(page_title="Resultados Avaliação Institucional - UFPR", layout="wide")
    
    # Carrega dados
    df = load_data_eixos()

    st.title('Resultados Avaliação Institucional')

    # ==========================================================================
    # 2. FILTROS (Movido para antes das métricas para permitir cálculo dinâmico)
    # ==========================================================================
    c_filt1, c_filt2 = st.columns(2)
    
    with c_filt1: 
        opcoes_eixo = ["Todos"] + list(df['EIXO'].unique())
        eixo_filter = st.multiselect(
            "Eixo",
            opcoes_eixo,
            default=["Todos"],
            key="filtro_eixo"
        )

    # Lógica de Filtragem
    if "Todos" in eixo_filter or not eixo_filter:
        df_filtered = df.copy()
    else:
        df_filtered = df[df['EIXO'].isin(eixo_filter)]

    # ==========================================================================
    # 3. CÁLCULO DAS MÉTRICAS (Dinâmico)
    # ==========================================================================
    total_resp = len(df_filtered)
    if total_resp > 0:
        counts = df_filtered['RESPOSTA'].value_counts()
        conc_pct = (counts.get('Concordo', 0) / total_resp) * 100
        disc_pct = (counts.get('Discordo', 0) / total_resp) * 100
        desc_pct = (counts.get('Desconheço', 0) / total_resp) * 100
    else:
        conc_pct = disc_pct = desc_pct = 0

    # ==========================================================================
    # 4. EXIBIÇÃO DAS MÉTRICAS (Scorecards)
    # ==========================================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Respondentes",
                  border=BORDER,
                  value=total_resp,
                  delta="Baseado na seleção atual")
        
    with col2: 
        st.metric(label="Concordância",
                  border=BORDER,
                  value=f"{conc_pct:.1f}%",
                  delta_color="normal")
    with col3:
        st.metric(label="Discordância",
                  border=BORDER,
                  value=f"{disc_pct:.1f}%",
                  delta_color="inverse") # Vermelho se aumentar
        
    with col4: 
        st.metric(label="Desconhecimento",
                  border=BORDER,
                  value=f"{desc_pct:.1f}%",
                  delta_color="off")
        
    st.markdown("---")

    # ==========================================================================
    # 5. VISUALIZAÇÕES (Rosquinha e Comparativo)
    # ==========================================================================
    
    col_graf1, col_graf2 = st.columns(2)
    
    # --- GRÁFICO 1: VISÃO GERAL (ROSQUINHA) ---
    with col_graf1:
        st.subheader("Distribuição Total (Seleção)")
        
        if total_resp > 0:
            # Agrupa dados filtrados para o gráfico de pizza
            df_pizza = df_filtered['RESPOSTA'].value_counts().reset_index()
            df_pizza.columns = ['RESPOSTA', 'CONTAGEM']
            
            fig_donut = px.pie(
                df_pizza, 
                values='CONTAGEM', 
                names='RESPOSTA',
                hole=0.5, # Faz virar rosquinha
                color='RESPOSTA',
                color_discrete_map=color_map
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            fig_donut.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            
            st.plotly_chart(fig_donut, use_container_width=True)
            
            # Legenda de apoio visual
            st.caption(f"Total de respostas consideradas: {total_resp}")
        else:
            st.warning("Sem dados para os filtros selecionados.")

    # --- GRÁFICO 2: COMPARAÇÃO ENTRE EIXOS (BARRAS) ---
    with col_graf2:
        st.subheader("Comparativo por Eixo")
        
        # Prepara dados agrupados por Eixo para comparar médias
        # Se 'Todos' estiver selecionado, mostra todos os eixos disponíveis no DF original
        # Se filtrado, mostra apenas os selecionados para comparação interna
        if "Todos" in eixo_filter:
            df_comp = df # Compara tudo com tudo
        else:
            df_comp = df_filtered # Compara apenas os selecionados
            
        # Agrupamento e cálculo de percentuais
        df_grouped = df_comp.groupby(['EIXO', 'RESPOSTA']).size().reset_index(name='COUNT')
        total_por_eixo = df_comp.groupby('EIXO').size().reset_index(name='TOTAL')
        df_merged = pd.merge(df_grouped, total_por_eixo, on='EIXO')
        df_merged['PERCENT'] = (df_merged['COUNT'] / df_merged['TOTAL']) * 100
        
        # Ordenar eixos para visualização limpa
        df_merged = df_merged.sort_values('EIXO')

        fig_bar = px.bar(
            df_merged,
            x="EIXO",
            y="PERCENT",
            color="RESPOSTA",
            color_discrete_map=color_map,
            barmode='stack', # Barras empilhadas para ver o total de 100%
            text_auto='.0f',
            height=400
        )
        
        fig_bar.update_layout(
            xaxis_title="",
            yaxis_title="% das Respostas",
            legend_title="",
            xaxis={'tickangle': -45} # Inclina o texto pois os nomes dos eixos são longos
        )
        # Força o eixo Y ir até 100%
        fig_bar.update_yaxes(range=[0, 100])
        
        st.plotly_chart(fig_bar, use_container_width=True)

          
    # with col1:
        
    
    #     pergunta_sel = 'O curso promove a interdisciplinaridade?'
    #     q_curso = df_curso[df_curso['PERGUNTA'] == pergunta_sel]
    #     q_setor = df_setor[df_setor['PERGUNTA'] == pergunta_sel]
    #     q_ufpr = df_ufpr[df_ufpr['PERGUNTA'] == pergunta_sel]

    #     if not q_curso.empty:
    #         stats_curso = calcular_frequencias(q_curso).assign(Escopo=f"Curso ({curso_sel})")
    #         stats_setor = calcular_frequencias(q_setor).assign(Escopo=f"Setor ({setor_sel})")
    #         stats_ufpr = calcular_frequencias(q_ufpr).assign(Escopo="UFPR (Geral)")
    #         df_comparativo = pd.concat([stats_curso, stats_setor, stats_ufpr])

    #         fig_comp = px.bar(
    #             df_comparativo,
    #             x="Escopo",
    #             y="Percentual",
    #             color="RESPOSTA",
    #             barmode="group",
    #             color_discrete_map=color_map,
    #             text_auto='.1f',
    #             title=f"Comparativo geral das respostas"
    #         )

    #         fig_comp.update_layout(yaxis_title="% Frequência Relativa")
    #         st.plotly_chart(fig_comp, use_container_width=True)
    # with col2: 
    #     df_concordo = df[df['RESPOSTA'] == 'Concordo']
    #     radar_curso = df_concordo[df_concordo['CURSO'] == curso_sel].groupby('DIMENSAO').size()
    #     total_curso = df[df['CURSO'] == curso_sel].groupby('DIMENSAO').size()
    #     score_curso = (radar_curso / total_curso * 100).fillna(0).reset_index(name='Score')
    #     radar_setor = df_concordo[df_concordo['SETOR'] == setor_sel].groupby('DIMENSAO').size()
    #     total_setor = df[df['SETOR'] == setor_sel].groupby('DIMENSAO').size()
    #     score_setor = (radar_setor / total_setor * 100).fillna(0).reset_index(name='Score')
    #     categories = score_curso['DIMENSAO'].tolist()
    #     fig_radar = go.Figure()

    #     fig_radar.add_trace(go.Scatterpolar(
    #         r=score_curso['Score'],
    #         theta=categories,
    #         fill='toself',
    #         name=f'Média Eixos selecionados',
    #         line_color='#1f77b4'
    #     ))

    #     fig_radar.add_trace(go.Scatterpolar(
    #         r=score_setor['Score'],
    #         theta=categories,
    #         fill='toself',
    #         name=f'Média Todos os eixos',
    #         line_color='#ff7f0e',
    #         opacity=0.5
    #     ))

    #     fig_radar.update_layout(
    #         polar=dict(
    #             radialaxis=dict(
    #                 visible=True,
    #                 range=[0, 100]
    #             )),
    #         showlegend=True,
    #         title="Comparação concordância média dos eixos com eixos filtrado  "
    #     )
    #     # st.plotly_chart(fig_radar, use_container_width=True, key = 2)
    
           
    #     dimensoes = df['DIMENSAO'].unique()
       

    # st.selectbox("Selecione a Dimensão para Análise Detalhada:",dimensoes, key = 2)
    # dim_sel = 'Dimensão 2 - Ensino, Pesquisa, Extensão'
    # df_diverg = df[(df['CURSO'] == curso_sel) & (df['DIMENSAO'] == dim_sel)]
    # grouped = df_diverg.groupby(['PERGUNTA', 'RESPOSTA']).size().unstack(fill_value=0)
    # grouped_pct = grouped.div(grouped.sum(axis=1), axis=0) * 100
    # questions = grouped_pct.index.tolist()
    # concordo = grouped_pct.get('Concordo', pd.Series([0]*len(questions))).tolist()
    # discordo = grouped_pct.get('Discordo', pd.Series([0]*len(questions))).tolist()
    # discordo_neg = [-x for x in discordo]

    # fig_div = go.Figure()
    # fig_div.add_trace(go.Bar(
    #     y=questions, x=discordo_neg,
    #     name='Discordo', orientation='h',
    #     marker_color='#e74c3c',
    #     text=[f"{x:.1f}%" for x in discordo], textposition='auto'
    # ))
    # fig_div.add_trace(go.Bar(
    #     y=questions, x=concordo,
    #     name='Concordo', orientation='h',
    #     marker_color='#2ecc71',
    #     text=[f"{x:.1f}%" for x in concordo], textposition='auto'
    # ))

    # fig_div.update_layout(
    #     barmode='relative',
    #     title=f"Saldo de Opinião: {dim_sel}",
    #     xaxis_title="% Rejeição <---> % Aprovação",
    #     yaxis=dict(autorange="reversed"),
    #     bargap=0.3,
    #     legend_title_text='Sentimento'
    # )

    # fig_div.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")
    # st.plotly_chart(fig_div, use_container_width=True, key = "1")

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
    
    
        
    
