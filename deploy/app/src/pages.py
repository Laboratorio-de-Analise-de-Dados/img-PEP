import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

from src.functions import Functions


def img_to_df(img, por_retirada) -> pd.DataFrame:
    img_array = np.array(img, dtype="float64")/255
    img_df_orig = pd.DataFrame(
                        columns=["red"],
                        data=img_array[:,:,0].reshape(-1,1)
                    )
    img_df_orig["green"] = img_array[:,:,1].reshape(-1,1)
    img_df_orig["blue"] = img_array[:,:,2].reshape(-1,1)

    img_df_original_green = img_df_orig['green'].copy()
    freq = (
        img_df_original_green.value_counts(normalize=True)
        .to_frame()
        .reset_index()
        .sort_values('green', ascending=False)
    )

    soma = 0
    for n in range(len(freq)):
        soma += freq.iloc[n,1]
        if soma >= por_retirada:
            break
    threshold = freq.iloc[n,0]
    
    img_df_fil = img_df_orig.copy()

    if por_retirada != 1.0:
        img_df_fil.loc[img_df_fil["green"] >= threshold, "green"] = 0.0

    return (img_df_orig, img_df_fil)

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
    uppload_file = st.sidebar.file_uploader("", type=['tif'])
    if uppload_file is not None:

        st.markdown(f"<h4>{uppload_file.name}</h4>", unsafe_allow_html=True)
        img = Image.open(uppload_file)

        col = st.columns((1,3.5,.5))
        with col[0]:
            df_1, df_2 = img_to_df(img=img, por_retirada=filtro)

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
            st.image(img_df_2)

    st.markdown("---")

    # Logo data.lab()
    funct = Functions()
    funct.logo_datalab()

    return None
