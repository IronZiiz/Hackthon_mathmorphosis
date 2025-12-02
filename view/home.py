import streamlit as st
from streamlit_carousel import carousel
import time 
from services.HomeService import DataLogger
COLOR_UFPR_BLUE = '#00548e'
COLOR_UFPR_BLACK ='#231F20'

CARD_STYLE_BOXES  = """
    border:1px solid #ddd; 
    border-radius:12px; 
    padding:20px; 
    text-align:center;
    background-color:#fafafa;
    height:300px;               
    display:flex;
    flex-direction:column;
    justify-content:flex-start; 
    """
CARD_STYLE_CARDS = """
    border:1px solid #ddd;
    border-radius:12px;
    padding:20px;
    text-align:left;
    background-color:#fafafa;
    height:180px;               
    display:flex;
    flex-direction:row;
    align-items:center;
    gap:20px;
"""



def home_view():

    st.markdown(
        f"""
        <h1 style="text-align:center; font-size:3.4rem; font-weight:700;">
            <span style="color:{COLOR_UFPR_BLACK}">Visualização dos Resultados da</span>
            <span style="color:{COLOR_UFPR_BLUE}">Avaliação</span> da UFPR
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("""
    <style>
    .carousel-item {   
        max-height: 90vh !important; 
        height: auto !important;     
        width: 100% !important;
    }
    .carousel-item img {
        object-fit: contain !important;
        width: 100% !important; 
        height: auto !important;         
        max-height: 90vh !important;
        background-color: black;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(
            """
            <p style="
                text-align:center;
                max-width:750px;
                margin:auto;
                font-size:1.1rem;
                color:#555;
            ">
                Ferramenta interativa desenvolvida pela Equipe Mathmorphosis para visualizar os resultados das pesquisas 
                realizadas junto a alunos e servidores da Universidade Federal do Paraná.
            </p>
            """,
            unsafe_allow_html=True
        )
    st.write("")  
    st.write("") 
    carousel([
    {
        "img": "data/imgs/1.png",
        "title": "",
        "text": ""
    },
    {
        "img": "data/imgs/2.png",
        "title": "",
        "text": ""
    },
    {
        "img": "data/imgs/3.png",
        "title": "",
        "text": ""
    },
    {
        "img": "data/imgs/4.png",
        "title": "",
        "text": ""
    },
    {
        "img": "data/imgs/5.png",
        "title": "",
        "text": ""
    }
    ])
    
    st.write("")  
    st.write("")  
    st.markdown(
                f"""
                <h1 style="text-align:center; font-size:2.4rem; font-weight:700;">
                   <span style="color:{COLOR_UFPR_BLACK}">Como funciona?</span>
                </h1>
                """,
                unsafe_allow_html=True
            )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}; text-align:center;">
                <div style="font-size:2rem;">1</div>
                <h3 style="margin-top:10px;">Navegue!</h3>
                <p>Acesse no topo da página as abas referentes a cada avaliação promovida pela UFPR e realize suas consultas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}; text-align:center;">
                <div style="font-size:2rem;">4️</div>
                <h3 style="margin-top:10px;">Gráficos</h3>
                <p>Explore os gráficos e interaja com eles! Eles respondem aos filtros aplicados, permitindo visualizar tanto a distribuição geral das respostas quanto os resultados por eixo e pelas unidades gestoras que mais participaram.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}; text-align:center;">
                <div style="font-size:2rem;">2️</div>
                <h3 style="margin-top:10px;">Métricas Gerais e Período</h3>
                <p>Atente-se às métricas gerais: elas sempre representam o total de respostas e não são afetadas pelos filtros. Estão vinculadas apenas ao ano/período selecionado.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}; text-align:center;">
                <div style="font-size:2rem;">5️</div>
                <h3 style="margin-top:10px;">Dimensões</h3>
                <p>Filtre as afirmações selecionando a dimensão à qual pertencem dentro da pesquisa.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}; text-align:center;">
                <div style="font-size:2rem;">3️</div>
                <h3 style="margin-top:10px;">Filtros</h3>
                <p>Escolha os filtros disponíveis. Os gráficos abaixo serão atualizados automaticamente.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")

        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}; text-align:center;">
                <div style="font-size:2rem;">6️</div>
                <h3 style="margin-top:10px;">Análise Detalhada</h3>
                <p>Explore cada afirmação do questionário individualmente, consulte os dados brutos e, caso deseje, realize o download.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.write("")  
    st.write("")  

    st.markdown(
        """
        <h1 style="text-align:center; font-size:2.4rem; font-weight:700;">
            Formato das Pesquisas
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            max-width:750px;
            margin:auto;
            font-size:1.1rem;
            color:#555;
        ">
            As pesquisas são compostas por questões apresentadas na forma de afirmações com três alternativas para o respondente.
        </p>
        """,
        unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}">
                <div style="font-size:2rem;">✅</div>
                <h3 style="margin-top:10px;">Concordo</h3>
                <p>Indica que o respondente concorda com a afirmação apresentada. Utilizamos como sinônimo de satisfação com as políticas da UFPR</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}">
                <div style="font-size:2rem;">❌</div>
                <h3 style="margin-top:10px;">Discordo</h3>
                <p>Indica que o respondente discorda da afirmação apresentada. Utilizamos como sinônimo de insatisfação com as políticas da UFPR</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="{CARD_STYLE_BOXES}">
                <div style="font-size:2rem;">🔵</div>
                <h3 style="margin-top:10px;">Desconheço</h3>
                <p>Indica que o respondente não tem conhecimento sobre o tema</p>
            </div>
            """,
            unsafe_allow_html=True,)
        
    st.write("")  
    st.write("")  
    
    st.markdown(
        """
        <h2 style="text-align:center; font-size:2.4rem; font-weight:700;">
            Métricas Dísponíveis
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            text-align:center;
            max-width:750px;
            margin:auto;
            font-size:1.1rem;
            color:#555;
        ">
            As métricas são compostas de valores que trazem um panorama geral e também específicas de cada pesquisa e pergunta.
        </p>
        """,
        unsafe_allow_html=True)
    
    
    col1, col2 = st.columns(2)


    with col1: 
        st.markdown(
            f"""
            <div style="{CARD_STYLE_CARDS}">
                <div style="font-size:2rem;">📶</div>
                <p>
                    <span style="font-weight:700;">Frequência Absoluta e Relativa: </span>
                    Contagem total de respostas e percentuais por alternativa para cada questão.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")  
        st.markdown(
            f"""
            <div style="{CARD_STYLE_CARDS}">
                <div style="font-size:2rem;">🎓</div>
                <p>
                    <span style="font-weight:700;">Comparativo por Nível: </span>
                    Comparação entre Curso, Setor e UFPR como um todo.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2: 
        st.markdown(
            f"""
            <div style="{CARD_STYLE_CARDS}">
                <div style="font-size:2rem;">🏛️</div>
                <p>
                    <span style="font-weight:700;">Análise por Dimensão: </span>
                    Resultados agrupados por dimensão e eixo avaliativo do SINAES.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")  
        st.markdown(
            f"""
            <div style="{CARD_STYLE_CARDS}">
                <div style="font-size:2rem;">📊</div>
                <p>
                    <span style="font-weight:700;">Índices Gerais: </span>
                    Concordância, discordância e desconhecimento consolidados.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.write("")  
    st.write("")  


    st.markdown(
    """
    <p style="
        text-align:left;
        max-width:750px;
        margin:auto;
        font-size:0.75rem;
        color:#555;
        opacity:0.7;
        line-height:1;
    ">
        <span style="font-weight:700; opacity:1;">Fundamento Legal</span> 
        A Lei nº 10.861 de 14/04/2004 que instituiu o SINAES, no artigo 11, prevê que cada instituição de ensino superior tenha Comissão Própria de Avaliação (CPA) com "atribuições de condução dos processos de avaliação internos da instituição, de sistematização e de prestação das informações solicitadas pelo INEP".<br><br>
        A avaliação institucional é coordenada pela CPA com periodicidade anual, resultando em um Relatório Anual de Avaliação protocolado no MEC até 31 de março do ano seguinte.
    </p>
    """,
    unsafe_allow_html=True 
    )
    st.write("")
    st.write("")

    st.write("---")  # linha de separação

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
            opacity:0.85;
        ">
            <h3 style="margin-bottom:5px;">Contato</h3>
            <p style="margin:0;">Equipe Mathmorphosis</p>
            <p style="margin:0;">📧 mathmorphosisej@gmail.com</p>
            <p style="margin:0;">🌐 www.mathmorphosis.com.br</p>
        </div>
        """,
        unsafe_allow_html=True
)
    feedback_value = st.feedback()
    service = DataLogger(feedback_value=feedback_value)

    if feedback_value is not None:
        save = service.save_feedback_to_json()
        msg = st.empty()
        msg.success(f"{save['message']}")
        time.sleep(1)
        msg.empty()
    else:
        save = service.save_feedback_to_json()
        st.warning(f"{save['message']}")