import streamlit as st

from src.pages import entrada_img


def dashboard() -> None:
    '''
        Função de inicialização do dashboard.
    '''

    page_icon = './data/img/icon.png'
    st.set_page_config(
        page_title="IMG-PEP",
        page_icon=page_icon,
        layout="wide",
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

    st.title("Análise de Imagens")

    entrada_img()

    return None


if __name__ == "__main__":
    dashboard()
