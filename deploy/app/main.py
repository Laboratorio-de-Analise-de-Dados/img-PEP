import streamlit as st

from src.pages import valores, categorias, qualitativas, dev_categorias
from src.pages import vendas
from src.uteis_functions import Functions


def dashboard() -> None:
    '''
        Função de inicialização do dashboard.
    '''
    functions = Functions()

    # page_icon = './data/img/astral_icon.png'
    st.set_page_config(
        page_title="IMG-PEP",
        # page_icon=page_icon,
        layout="wide"
    )
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 3rem;
                    padding-right: 3rem;
                }
        </style>
        """, unsafe_allow_html=True)

    st.title("Análise Astral da Ilha")

    # Abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Vendas",
        "Despezas",
        "Categorias",
        "Dev",
        ])

    with tab1:

        # Página de Valores
        vendas()
        st.markdown("---")

    with tab2:

        # Página de valores
        valores()
        st.markdown("---")

    with tab3:
        col = st.columns(spec=(1, 1))
        with col[0]:

            # Página de Categóricas
            categorias()

        with col[1]:

            # Página de variáveis quantitaivas
            qualitativas()

        st.markdown("---")

    with tab4:

        dev_categorias()

    # Logotipo do DataLab()
    functions.logo_datalab()

    return None


if __name__ == "__main__":
    dashboard()
