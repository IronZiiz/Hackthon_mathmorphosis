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
        setor_value=setor_value,
        
        )
    
    st.subheader('Distribuição de respostas')

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
    
    

    dimensoes = service.df['DIMENSAO'].unique().tolist()

    dim_sel = st.selectbox(
    "Selecione a Dimensão para Análise Detalhada:",
        dimensoes,key = "dimensao_curso"
    )

    df_questions_answers = service.df.groupby(['PERGUNTA','VALOR_RESPOSTA'])['VALOR_RESPOSTA'].count()

    st.dataframe(df_questions_answers)
    
    # 1. Filtra os dados da dimensão escolhida
    df_dimensao = service.df[service.df['DIMENSAO'] == dim_sel]

    if df_dimensao.empty:
        st.warning("Sem dados para essa dimensão.")
    else:
        # 2. CRIAÇÃO SEGURA DOS DADOS (Crosstab)
        # Transforma respostas em colunas e calcula porcentagem (0-100) por linha (pergunta)
        tabela_percentuais = pd.crosstab(
            index=df_dimensao['PERGUNTA'], 
            columns=df_dimensao['RESPOSTA'], 
            normalize='index' # Isso aqui garante a porcentagem correta!
        ) * 100

        # 3. Preenchimento de colunas faltantes com 0 (caso ninguém tenha respondido alguma opção)
        for col in ['Concordo', 'Discordo', 'Desconheço']:
            if col not in tabela_percentuais.columns:
                tabela_percentuais[col] = 0.0

        # 4. Extração das Listas (Garantindo a ordem)
        questions = tabela_percentuais.index.tolist()
        
        # Pega os valores exatos da tabela cruzada
        concordo_list = tabela_percentuais['Concordo'].tolist()
        discordo_list = tabela_percentuais['Discordo'].tolist()
        desconheco_list = tabela_percentuais['Desconheço'].tolist()

        # 5. Formatação do Texto (Quebra de linha)
        def quebrar_texto(texto, max_chars=50):
            if len(texto) <= max_chars: return texto
            import textwrap
            return "<br>".join(textwrap.wrap(texto, width=max_chars))

        questions_formatted = [quebrar_texto(q) for q in questions]

        # 6. Preparação para o Gráfico Divergente
        discordo_neg_list = [-x for x in discordo_list]
        
        # Divisão do Desconheço (Metade negativa, Metade positiva)
        desconheco_metade = [x / 2 for x in desconheco_list]
        desconheco_metade_neg = [-x for x in desconheco_metade]
        
        hover_desconheco = [f"Desconheço: {x:.1f}%" for x in desconheco_list]
        # Mostra label só se for relevante (>1%) para não poluir
        label_desconheco = [f"{x:.1f}%" if x > 1 else "" for x in desconheco_list]

        fig_div = go.Figure()

        # --- CAMADA 1: DESCONHEÇO (Centro) ---
        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade_neg,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=True,
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly' # Começa oculto
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=desconheco_metade,
            name='Desconheço', orientation='h', marker_color='#95a5a6',
            legendgroup='grp_desc', showlegend=False,
            text=label_desconheco, textposition='inside',
            hoverinfo='text', hovertext=hover_desconheco,
            visible='legendonly'
        ))

        # --- CAMADA 2: EXTREMOS ---
        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=discordo_neg_list,
            name='Discordo', orientation='h', marker_color='#e74c3c',
            text=[f"{x:.1f}%" if x > 1 else "" for x in discordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Discordo: {x:.1f}%" for x in discordo_list]
        ))

        fig_div.add_trace(go.Bar(
            y=questions_formatted, x=concordo_list,
            name='Concordo', orientation='h', marker_color='#2ecc71',
            text=[f"{x:.1f}%" if x > 1 else "" for x in concordo_list],
            textposition='inside', insidetextanchor='middle',
            hoverinfo='text+y', hovertext=[f"Concordo: {x:.1f}%" for x in concordo_list]
        ))

        fig_div.update_layout(
            barmode='relative',
            title=f"Saldo de Opinião: {dim_sel}",
            xaxis_title="% Rejeição <---> % Aprovação",
            yaxis=dict(title=""),
            legend_title_text='Resposta',
            height=max(400, len(questions) * 60 + 100), # Altura dinâmica
            margin=dict(l=10, r=10, t=80, b=20)
        )

        fig_div.add_vline(x=0, line_width=1, line_color="black", opacity=0.3)
        st.plotly_chart(fig_div, use_container_width=True, key="plot_perguntas_curso")

    dimensoes = sorted(service.df['DIMENSAO'].dropna().unique()) # Pega dimensões reais do banco
    dim_sel = st.selectbox(
    "Selecione a Dimensão...",
    dimensoes,
    key="dimensao_curso_radar"
    )

    # Layout: 2 colunas para o Radar (Gráfico + Tabela) | 1 Coluna para Barras
    col_radar_grafico, col_radar_legenda, col_barras = st.columns([1.2, 0.8, 1.5])

    # --- COLUNA 1: O GRÁFICO ---
    with col_radar_grafico:
        st.subheader("Comparativo Radar")
    
    # Chama a função nova (que retorna 2 coisas)
    fig_radar_dim, df_legenda_radar = service.grafico_radar_dimensao_curso(dim_sel)
    
    if fig_radar_dim:
        st.plotly_chart(fig_radar_dim, use_container_width=True)
    else:
        st.warning("Sem dados para radar.")

    # --- COLUNA 2: A LEGENDA (ID -> PERGUNTA) ---
    with col_radar_legenda:
        st.subheader("Legenda")
        if df_legenda_radar is not None and not df_legenda_radar.empty:
            # Configura a tabela para ficar bonita
            st.dataframe(
                df_legenda_radar,
                hide_index=True, # Esconde o índice numérico (0, 1, 2)
                column_config={
                    "ID_PERGUNTA": st.column_config.TextColumn("ID", width="small"),
                    "PERGUNTA": st.column_config.TextColumn("Pergunta Completa")
                },
                height=400 # Mesma altura do gráfico
            )
        else:
            st.write("-")

    # --- COLUNA 3: O GRÁFICO DE BARRAS (Existente) ---
    with col_barras:
        st.subheader("Saldo de Opinião")
        # ... (seu código do gráfico de barras horizontais continua aqui igualzinho) ...

        st.markdown('---')

        with st.expander("Ver dados brutos (Frequências Absolutas) (TEMPORÁRIO)"):
            st.dataframe(service.df) # Temp
            message = "Lorem ipsum.\nStreamlit is cool."
            st.download_button(
                key=2,
                label="Download Dados brutos",
                data=message,
                file_name="message.txt",
                on_click="ignore",
                type="primary",
                icon=":material/download:"
            )
    