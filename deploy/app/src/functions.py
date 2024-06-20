import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class Functions():
    @st.cache_data
    def logo_datalab(_self) -> None:
        '''
        Função que implementa o Logo do DataLab()
        '''
        data_lab_logo = './data/img/DataLab_Logo_2020-02-23.jpg'
        # Importa a imagem
        img = np.asarray(Image.open(data_lab_logo))

        # Plota a imagem
        plt.imshow(img)
        plt.axis("off")

        # Edita as colunas e insere os dados
        col_img = st.columns((15, 1))
        with col_img[1]:
            st.write("DataLab()")
            st.pyplot(fig=plt)
        return None