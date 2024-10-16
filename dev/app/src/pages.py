import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from datetime import date

from src.functions import Functions


def entrada_img() -> None:
    '''
    Determina a página de valores
    '''
    st.sidebar.markdown(
        "<h3>Selecione Filtro (%)</h3>",
        unsafe_allow_html=True
    )
    filtro = st.sidebar.slider(
                            label='',
                            min_value=0.995,
                            max_value=1.0,
                            value=1.0,
                            step=0.000001
                        )

    st.sidebar.markdown(
        "<h3>Selecione Imagem</h3>",
        unsafe_allow_html=True
    )

    funct = Functions()
    uppload_files = st.sidebar.file_uploader(
                                                "",
                                                type=['tif'], 
                                                accept_multiple_files=True
    )
    data_dict = {
        "File Name": np.nan,
        "Filter": np.nan,
        "Original MFI": np.nan,
        "Filtered MFI": np.nan,
    }
    df_excel = pd.DataFrame(
        index=[1],
        data=data_dict
    )
    c = 0
    for uppload_file in uppload_files:
        if uppload_file is not None:

            st.markdown(f"<h4>{uppload_file.name}</h4>", unsafe_allow_html=True)
            img = Image.open(uppload_file)

            col = st.columns((1,3.5,.5))
            with col[0]:
                df_1, df_2 = funct.img_to_df(_img=img, por_retirada=filtro)

                st.markdown(
                    f"<h4>Filtro: {filtro:.6f}</h4>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<h4>MFI original: {df_1['green'].mean():.6f}</h4>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"<h4>MFI corrigido: {df_2['green'].mean():.6f}</h4>",
                    unsafe_allow_html=True
                )
            
            with col[1]:

                img_df_2 = np.array(df_2).reshape(
                    np.array(img).shape[0],
                    np.array(img).shape[1],
                    np.array(img).shape[2],
                )
                st.image(img_df_2, width=800)
        c += 1
        data_dict_img = {
            "File Name": uppload_file.name,
            "Filter": f"{filtro:.6f}",
            "Original MFI": f"{df_1['green'].mean():.6f}",
            "Filtered MFI": f"{df_2['green'].mean():.6f}",
        }
        df_excel_img = pd.DataFrame(
            index=[c],
            data=data_dict_img
        )

        df_excel = pd.concat([df_excel, df_excel_img])

        st.markdown("---")

    if c != 0:
        df_excel = df_excel.dropna()
        st.dataframe(df_excel)

        df_xlsx = funct.to_excel_personal(df_excel)

        
        today = date.today()
        link = f'./data/xlsx/img_{today}.xlsx'

        st.download_button(
            label='Download',
            data=df_xlsx,
            file_name=link[12:],
        )

    funct.logo_datalab()

    return None
