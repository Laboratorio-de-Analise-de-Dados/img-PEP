import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt


def img_to_df(img) -> pd.DataFrame:
  img_array = np.array(img, dtype="float64")/255
  img_df = pd.DataFrame(columns=["red"], data=img_array[:,:,0].reshape(-1,1))
  img_df["green"] = img_array[:,:,1].reshape(-1,1)
  img_df["blue"] = img_array[:,:,2].reshape(-1,1)

  return img_df

def entrada_img() -> None:
    '''
    Determina a página de valores
    '''

    st.sidebar.markdown(
        "<h3>Selecione Filtro (%)</h3>",
        unsafe_allow_html=True
    )
    hour_to_filter = st.sidebar.slider('', 0, 100, 10)
    

    df_insert = False

    st.sidebar.markdown(
        "<h3>Selecione Imagem</h3>",
        unsafe_allow_html=True
    )
    uppload_file = st.sidebar.file_uploader("", type=['tif'])
    if uppload_file is not None:

        st.markdown(uppload_file.name)
        path = uppload_file
        img = Image.open(path)

        col = st.columns((1,3.5,.5))
        with col[0]:
            st.markdown(f'{hour_to_filter}')
            df = img_to_df(img)
            
            plt.figure(figsize=(5, 15))
            sns.boxplot(y='green', data=df)
            st.pyplot(fig=plt)
        
        with col[1]:
            st.image(img)

        df_insert = True

    st.markdown("---")
    return None
