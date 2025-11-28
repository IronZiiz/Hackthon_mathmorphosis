import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def avaliacao_institucional_view():

    # Configuração da Página
    st.set_page_config(page_title="Resultados Avaliação Institucional - UFPR", layout="wide")


    @st.cache_data
    def load_data():
        # Dados simulados para exemplo
        data = {
            'ID_PERGUNTA': [1, 1, 1, 2, 2, 2, 3, 3, 3] * 20,
            'PERGUNTA': [
                'O curso promove a interdisciplinaridade?',
                'O curso promove a interdisciplinaridade?',
                'O curso promove a interdisciplinaridade?',
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

    # Sidebar
    st.sidebar.header("Filtros da Consulta")

    # Filtro de Ano
    anos_disponiveis = df['ANO'].unique()
    ano_sel = st.sidebar.selectbox("Ano/Período", anos_disponiveis)

    # Filtro de Setor (Filtra os cursos disponíveis)
    setores_disponiveis = df['SETOR'].unique()
    setor_sel = st.sidebar.selectbox("Setor", setores_disponiveis)

    # Filtro de Curso (Depende do Setor)
    cursos_no_setor = df[df['SETOR'] == setor_sel]['CURSO'].unique()
    curso_sel = st.sidebar.selectbox("Curso / Unidade", cursos_no_setor)

    st.sidebar.markdown("---")
    st.sidebar.info("Dados baseados na Avaliação Institucional (SINAES).")

    # Função auxiliar para calcular % de respostas
    def calcular_frequencias(dataframe, group_col=None):
        if group_col:
            base = dataframe.groupby([group_col, 'RESPOSTA']).size().reset_index(name='Contagem')
            total = dataframe.groupby([group_col]).size().reset_index(name='Total')
            merged = pd.merge(base, total, on=group_col)
        else:
            # Caso Global (sem agrupamento)
            base = dataframe.groupby(['RESPOSTA']).size().reset_index(name='Contagem')
            base['Total'] = dataframe.shape[0]
            merged = base
        
        merged['Percentual'] = (merged['Contagem'] / merged['Total']) * 100
        return merged

    # Filtragem dos Dataframes para Comparação
    df_curso = df[(df['CURSO'] == curso_sel) & (df['ANO'] == ano_sel)]
    df_setor = df[(df['SETOR'] == setor_sel) & (df['ANO'] == ano_sel)] # Benchmark Setor
    df_ufpr = df[df['ANO'] == ano_sel] # Benchmark Global

    st.title(f"📊 Resultados: {curso_sel}")
    st.markdown(f"**Setor:** {setor_sel} | **Ano:** {ano_sel}")

    # Abas para separar visões (Geral vs Detalhada)
    tab1, tab2, tab3, tab4 = st.tabs(["Visão por Dimensão", "Detalhe por Pergunta (Comparativo)", "Insights Avançados", "Análises Estratégicas"])

    with tab1:
        st.markdown("### Resultados Agrupados por Dimensão ")
        st.write("Visão consolidada das respostas agrupadas pelos eixos do SINAES.")
        
        # Agrupa dados do curso selecionado por Dimensão e Resposta
        dimensao_stats = calcular_frequencias(df_curso, 'DIMENSAO')
        
        # Cores personalizadas para seguir a lógica semântica (Verde=Bom, Vermelho=Ruim)
        color_map = {'Concordo': '#2ecc71', 'Discordo': '#e74c3c', 'Desconheço': '#95a5a6'}
        
        fig_dim = px.bar(
            dimensao_stats, 
            x="Percentual", 
            y="DIMENSAO", 
            color="RESPOSTA", 
            orientation='h',
            color_discrete_map=color_map,
            text_auto='.1f',
            title="Adesão por Dimensão Avaliativa"
        )
        fig_dim.update_layout(xaxis_title="% de Respostas", yaxis_title="")
        st.plotly_chart(fig_dim, use_container_width=True)

    with tab2:
        st.markdown("### Comparativo: Curso vs. Setor vs. UFPR")
        st.write("Selecione uma pergunta para visualizar o comparativo detalhado conforme Figura 1 do documento.")
        
        # Seletor de Pergunta
        perguntas_unicas = df['PERGUNTA'].unique()
        pergunta_sel = st.selectbox("Selecione a Questão:", perguntas_unicas)
        
        # Filtra os dados apenas para essa pergunta nos 3 níveis
        q_curso = df_curso[df_curso['PERGUNTA'] == pergunta_sel]
        q_setor = df_setor[df_setor['PERGUNTA'] == pergunta_sel]
        q_ufpr = df_ufpr[df_ufpr['PERGUNTA'] == pergunta_sel]
        
        # Calcula estatísticas
        # Nota: Precisamos tratar caso não haja respostas para evitar erros
        if not q_curso.empty:
            stats_curso = calcular_frequencias(q_curso).assign(Escopo=f"Curso ({curso_sel})")
            stats_setor = calcular_frequencias(q_setor).assign(Escopo=f"Setor ({setor_sel})")
            stats_ufpr = calcular_frequencias(q_ufpr).assign(Escopo="UFPR (Geral)")
            
            # Junta tudo num único DF para plotagem
            df_comparativo = pd.concat([stats_curso, stats_setor, stats_ufpr])
            
            # Gráfico de Barras Agrupadas (Grouped Bar Chart)
            # Recriando a lógica visual da 'Figura 1' [cite: 34-44]
            fig_comp = px.bar(
                df_comparativo,
                x="Escopo",
                y="Percentual",
                color="RESPOSTA",
                barmode="group", # Barras lado a lado para comparação fácil
                color_discrete_map=color_map,
                text_auto='.1f',
                title=f"Questão: {pergunta_sel}"
            )
            
            fig_comp.update_layout(yaxis_title="% Frequência Relativa")
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Exibir Tabela de Dados (Opcional, mas útil para ver frequências absolutas)
            with st.expander("Ver dados brutos (Frequências Absolutas)"):
                st.dataframe(df_comparativo[['Escopo', 'RESPOSTA', 'Contagem', 'Percentual']])
                
        else:
            st.warning("Não há dados suficientes para esta pergunta no filtro selecionado.")

    # --- (Assumindo que o dataframe 'df' e as funções de carga anteriores já existem) ---
    with tab3:
        st.markdown("---")
        st.header("🧠 Área de Insights e Inteligência de Dados")
        st.markdown("Visualizações focadas em diagnóstico estratégico e detecção de anomalias.")

        st.subheader("1. Radar de Desempenho Institucional")
        st.caption("Compara a satisfação média (Concordância) do Curso vs. a Média do Setor nas Dimensões.")

        # 1. Preparação dos Dados para o Radar
        # Filtramos apenas as respostas "Concordo" para medir 'Sucesso'
        df_concordo = df[df['RESPOSTA'] == 'Concordo']

        # Agrupamento por Dimensão para o Curso
        radar_curso = df_concordo[df_concordo['CURSO'] == curso_sel].groupby('DIMENSAO').size()
        total_curso = df[df['CURSO'] == curso_sel].groupby('DIMENSAO').size()
        # Cálculo da % de Aprovação (Score)
        score_curso = (radar_curso / total_curso * 100).fillna(0).reset_index(name='Score')

        # Agrupamento por Dimensão para o Setor (Benchmark)
        radar_setor = df_concordo[df_concordo['SETOR'] == setor_sel].groupby('DIMENSAO').size()
        total_setor = df[df['SETOR'] == setor_sel].groupby('DIMENSAO').size()
        score_setor = (radar_setor / total_setor * 100).fillna(0).reset_index(name='Score')

        # 2. Plotagem do Radar
        categories = score_curso['DIMENSAO'].tolist()

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=score_curso['Score'],
            theta=categories,
            fill='toself',
            name=f'Curso: {curso_sel}',
            line_color='#1f77b4'
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=score_setor['Score'],
            theta=categories,
            fill='toself',
            name=f'Média Setor: {setor_sel}',
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
            title="Comparativo de Forças e Fraquezas (Dimensões)"
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(fig_radar, use_container_width=True)
        with col2:
            st.info("**Como ler:**\n\nSe a área azul (Curso) estiver dentro da laranja (Setor), o curso está abaixo da média naquela dimensão.\n\nPontas agudas indicam especialização ou desequilíbrio na gestão.")

        st.subheader("2. Matriz de Priorização (Aprovação vs. Rejeição)")
        st.caption("Identifica quais perguntas específicas geram maior rejeição absoluta.")

        # Selecionar Dimensão para aprofundar
        dimensoes = df['DIMENSAO'].unique()
        dim_sel = st.selectbox("Selecione a Dimensão para Análise Detalhada:", dimensoes)

        # Filtrar dados
        df_diverg = df[(df['CURSO'] == curso_sel) & (df['DIMENSAO'] == dim_sel)]

        # Calcular contagens
        grouped = df_diverg.groupby(['PERGUNTA', 'RESPOSTA']).size().unstack(fill_value=0)
        # Converter para percentual
        grouped_pct = grouped.div(grouped.sum(axis=1), axis=0) * 100

        # Criar listas para o gráfico
        questions = grouped_pct.index.tolist()
        concordo = grouped_pct.get('Concordo', pd.Series([0]*len(questions))).tolist()
        discordo = grouped_pct.get('Discordo', pd.Series([0]*len(questions))).tolist()
        # Transformar discordo em negativo para criar o efeito divergente
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
            yaxis=dict(autorange="reversed"), # Perguntas ordenadas de cima para baixo
            bargap=0.3,
            legend_title_text='Sentimento'
        )

        # Adiciona linha central zero
        fig_div.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")

        st.plotly_chart(fig_div, use_container_width=True)

        st.subheader("3. Monitor de Comunicação (Índice 'Desconheço')")
        st.caption("Altas taxas de resposta 'Desconheço' indicam falha na comunicação institucional, não necessariamente falha no serviço.")

        # Calcular taxa de desconhecimento por pergunta
        df_desc = df[df['CURSO'] == curso_sel]
        total_resps = df_desc.groupby('PERGUNTA').size()
        desc_resps = df_desc[df_desc['RESPOSTA'] == 'Desconheço'].groupby('PERGUNTA').size()
        taxa_desc = (desc_resps / total_resps * 100).fillna(0).sort_values(ascending=False).head(5)

        # Exibir como Top 5 Alertas
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.error("🚨 Top 5: 'Pontos Cegos'")
            st.write("Perguntas onde os alunos mais responderam **'Desconheço'**:")
        with col_b:
            fig_desc = px.bar(
                x=taxa_desc.values, 
                y=taxa_desc.index, 
                orientation='h',
                color=taxa_desc.values,
                color_continuous_scale='Blues',
                labels={'x': '% Desconheço', 'y': ''}
            )
            fig_desc.update_layout(showlegend=False)
            st.plotly_chart(fig_desc, use_container_width=True)


    with tab4:
        st.markdown("## Inteligência Estratégica")
        st.markdown("Ferramentas para identificar padrões sistêmicos, desigualdades internas e realizar comparações diretas.")

        st.markdown("### 1. Mapa Estratégico: Infraestrutura vs. Pedagógico")
        st.caption("Cada ponto representa um curso. Identifique clusters de excelência ou precariedade.")

        # --- Preparação dos Dados para o Scatter ---
        # Classificando Eixos em "Infra" ou "Pedagógico" para os eixos do gráfico
        # Nota: Adapte as strings abaixo conforme os nomes reais dos seus Eixos
        def classificar_macro(eixo):
            if 'Infraestrutura' in eixo or 'Gestão' in eixo:
                return 'Infra'
            elif 'Políticas' in eixo or 'Ensino' in eixo:
                return 'Pedagogico'
            return 'Outros'

        # Criamos uma cópia para manipulação
        df_scatter = df.copy()
        df_scatter['Macro_Categoria'] = df_scatter['EIXO'].apply(classificar_macro)

        # Calculamos % de 'Concordo' por Curso e Macro-Categoria
        df_approval = df_scatter[df_scatter['RESPOSTA'] == 'Concordo'].groupby(['CURSO', 'SETOR', 'Macro_Categoria']).size()
        df_total = df_scatter.groupby(['CURSO', 'SETOR', 'Macro_Categoria']).size()
        
        # Dataframe de percentuais
        df_metrics = (df_approval / df_total * 100).fillna(0).reset_index(name='Aprovacao')
        
        # Pivotar para ter colunas separadas: Infra e Pedagogico
        df_pivot = df_metrics.pivot_table(index=['CURSO', 'SETOR'], columns='Macro_Categoria', values='Aprovacao').reset_index()
        
        # Garantir que as colunas existam (caso falte dados em algum eixo)
        if 'Infra' not in df_pivot.columns: df_pivot['Infra'] = 0
        if 'Pedagogico' not in df_pivot.columns: df_pivot['Pedagogico'] = 0

        df_pivot['Tamanho'] = 100 # Placeholder para tamanho da bolha

        # --- Plotagem do Scatter ---
        fig_scatter = px.scatter(
            df_pivot,
            x="Infra",
            y="Pedagogico",
            color="SETOR",
            size="Tamanho",
            hover_name="CURSO",
            color_discrete_sequence=px.colors.qualitative.Bold,
            title="Dispersão dos Cursos da UFPR (Infraestrutura x Pedagógico)",
            labels={"Infra": "Aprovação Infra/Gestão (%)", "Pedagogico": "Aprovação Pedagógica (%)"}
        )
        
        # Linhas de Quadrantes (Médias)
        mean_infra = df_pivot['Infra'].mean()
        mean_ped = df_pivot['Pedagogico'].mean()
        
        fig_scatter.add_vline(x=mean_infra, line_dash="dash", line_color="gray", annotation_text="Média Infra")
        fig_scatter.add_hline(y=mean_ped, line_dash="dash", line_color="gray", annotation_text="Média Pedag.")

        st.plotly_chart(fig_scatter, use_container_width=True)
        st.info("💡 **Insight:** Cursos no quadrante superior direito são referências (""benchmarks""). Cursos no inferior esquerdo requerem intervenção prioritária.")

        st.markdown("---")
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 2. Índice de Desigualdade Interna")
            st.caption("Mede a variação (Desvio Padrão) das notas entre os cursos de um mesmo setor.")
            
            # Calcular a nota geral média de cada curso (Média de todas as dimensões)
            df_curso_geral = df[df['RESPOSTA'] == 'Concordo'].groupby(['SETOR', 'CURSO']).size() 
            total_curso_geral = df.groupby(['SETOR', 'CURSO']).size()
            score_geral = (df_curso_geral / total_curso_geral * 100).fillna(0).reset_index(name='Nota_Geral')

            # Calcular o Desvio Padrão por Setor
            df_desvio = score_geral.groupby('SETOR')['Nota_Geral'].std().reset_index()
            df_desvio.columns = ['SETOR', 'Desvio_Padrao']
            df_desvio = df_desvio.sort_values('Desvio_Padrao', ascending=True) # Menor desvio = Mais isonômico

            fig_desvio = px.bar(
                df_desvio,
                x='Desvio_Padrao',
                y='SETOR',
                orientation='h',
                color='Desvio_Padrao',
                color_continuous_scale='Reds',
                title="Consistência Interna dos Setores"
            )
            fig_desvio.update_layout(xaxis_title="Desvio Padrão (Menor é melhor)", yaxis_title="")
            st.plotly_chart(fig_desvio, use_container_width=True)
            st.caption("Barras menores indicam setores onde todos os cursos têm qualidade similar (isonomia).")

        with col_right:
            st.markdown("### 3. Comparador Direto (Face-a-Face)")
            st.caption("Selecione dois cursos para comparar detalhadamente suas dimensões.")

            c1, c2 = st.columns(2)
            with c1:
                curso_a = st.selectbox("Curso A (Referência)", df['CURSO'].unique(), index=0)
            with c2:
                # Tenta selecionar um curso diferente para o index padrão não ser igual
                lista_cursos = list(df['CURSO'].unique())
                index_b = 1 if len(lista_cursos) > 1 else 0
                curso_b = st.selectbox("Curso B (Comparação)", lista_cursos, index=index_b)

            # Filtrar dados para os dois cursos
            df_h2h = df[(df['CURSO'].isin([curso_a, curso_b])) & (df['RESPOSTA'] == 'Concordo')]
            
            # Calcular % por Dimensão
            h2h_grouped = df_h2h.groupby(['CURSO', 'DIMENSAO']).size()
            h2h_total = df[df['CURSO'].isin([curso_a, curso_b])].groupby(['CURSO', 'DIMENSAO']).size()
            
            df_compare = (h2h_grouped / h2h_total * 100).fillna(0).reset_index(name='Aprovacao')

            # Plotar
            fig_compare = px.bar(
                df_compare,
                x='DIMENSAO',
                y='Aprovacao',
                color='CURSO',
                barmode='group',
                color_discrete_map={curso_a: '#2ecc71', curso_b: '#3498db'},
                title=f"{curso_a} vs. {curso_b}"
            )
            fig_compare.update_layout(xaxis_title="", yaxis_title="% Aprovação", legend_title="")
            st.plotly_chart(fig_compare, use_container_width=True)