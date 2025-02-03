import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

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

    def img_to_df(_self, _img, por_retirada) -> pd.DataFrame:
        img_array = np.array(_img, dtype="float64")/255
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
    
    def to_excel_personal(_self, _df: pd.DataFrame):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        _df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data