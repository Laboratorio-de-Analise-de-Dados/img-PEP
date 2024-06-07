from joblib import load
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from datetime import datetime

from src.sqlite_execute import SQLite_execute


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
        col_img = st.columns((20, 1))
        with col_img[1]:
            st.write("DataLab()")
            st.pyplot(fig=plt)
        return None

    @st.cache_data
    def importa_df(_self) -> pd.DataFrame:
        '''
        Importação do banco de dados.
        '''
        link_file = "./data/DataFrame/df_estruturada"
        df = load(link_file)
        return df

    def timestamp_p_str(_self, val: pd.Timestamp) -> str:
        '''
        Formata os dados de data, inserindo 0 quando os valores forem
         superiores a 9.
        '''
        val_day = val.day
        val_month = val.month
        val_year = val.year

        if len(str(val.day)) == 1:
            val_day = f"0{val.day}"

        if len(str(val.month)) == 1:
            val_month = f"0{val.month}"

        return f"{val_day}/{val_month}/{val_year}"

    def reais_p_float(_self, real: str) -> float:
        '''
        Função que recebe uma estringo no formato de monetário (R$), e converte
        para um float
        :param real (str): Valor em R$ à ser convertido
        :return real (float): Valor convertido
        '''
        real = real.strip()
        real = real.replace("R$ ", "")
        real = real.replace(",", "_")
        real = real.replace(".", "")
        real = real.replace("_", ".")
        real_float = float(real)
        return real_float

    def float_p_real(_self, valor: float) -> str:
        '''
        Função que converte uma valor em float para R$.
        :param valor (float): Valor em float a ser convertido.
        :return valor_real (str): Valor convertido para R$.
        '''
        valor_str = f"R$ {valor:,.2f}"
        valor_str = valor_str.replace(".", "_")
        valor_str = valor_str.replace(",", ".")
        valor_real = valor_str.replace("_", ",")
        return valor_real

    def remove_porcentagem(_self, porcentagem: str) -> float:
        '''
        Função que recebe uma porcentagem em formato str e retorna em formato
        float.
        :param porcentagem (str): Valores com % para serem convertidos.
        :return porcentagem_float (float): Valor converido
        '''
        porcentagem = porcentagem.strip()
        porcentagem = porcentagem.replace("%", "")
        porcentagem = porcentagem.replace(",", ".")
        porcentagem_float = float(porcentagem)/100
        return porcentagem_float

    def edita_data(_self, data) -> str:
        data = str(data.strftime('%d/%m/%Y'))
        return data

    @st.cache_data
    def calculos_df_resumos(_self, df_copy: pd.DataFrame) -> dict:
        '''
            Calculo de valores da DataFrame
            :param df (pd.DataFrame): Origem dos valores
        '''
        retorna = {}
        # Obtem a soma dos valores no período
        soma_valor = _self.float_p_real(valor=df_copy.valor.sum())
        valor_informa = f"<h3>Soma dos valores: {soma_valor}</h3>"
        retorna["soma"] = valor_informa

        # Obtem a média dos valores no período
        media_valor = _self.float_p_real(valor=np.mean(df_copy.valor))
        valor_informa = f"<h3>Média dos valores: {media_valor}</h3>"
        retorna["media"] = valor_informa

        # Obtem a média dos valores no período
        median_valor = _self.float_p_real(valor=np.median(df_copy.valor))
        valor_informa = f"<h3>Mediana dos valores: {median_valor}</h3>"
        retorna["mediana"] = valor_informa

        # Obtem a máximo dos valores no período
        max_valor = _self.float_p_real(valor=df_copy.valor.max())
        valor_informa = f"<h3>Valor máximo: {max_valor}</h3>"
        retorna["maximo"] = valor_informa

        # Obtem a mininmo dos valores no período
        min_valor = _self.float_p_real(valor=df_copy.valor.min())
        valor_informa = f"<h3>Valor mínimo: {min_valor}</h3>"
        retorna["minimo"] = valor_informa

        df_copy_valores = df_copy.copy()
        fr = [_self.float_p_real(v) for v in df_copy_valores['valor']]
        df_copy_valores['valor'] = fr

        t = [_self.timestamp_p_str(val=v) for v in df_copy_valores['data']]
        df_copy_valores['data'] = t

        # Motra a DataFrame selecionada
        retorna["df_data_valor"] = df_copy_valores

        return retorna

    @st.cache_data
    def grafico_categorias(
                _self,
                df: pd.DataFrame,
                title: str,
                ylabel: str = "Valor R$"
            ) -> None:
        '''
            Calculo de valores da DataFrame
            :param df (pd.DataFrame): Origem dos valores
        '''
        plt.figure(figsize=(5, 5))
        g = sns.barplot(
            x=df.index,
            y="valor",
            data=df
        )
        g.set(
            title=title,
            xlabel="",
            ylabel=ylabel,
        )
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot(fig=plt)
        return None

    @st.cache_data
    def calculos_df_categorias(_self, df: pd.DataFrame, cat: str) -> dict:
        '''
            Calculo de valores da DataFrame
            :param df (pd.DataFrame): Origem dos valores
        '''
        retorna = {}
        retorna["df_colunas"] = df.columns

        df_groupby_cat = df.groupby(cat)['valor'].sum().to_frame()

        fr = [_self.float_p_real(v) for v in df_groupby_cat['valor']]
        df_groupby_cat['Valor R$'] = fr

        s_valor = df_groupby_cat['valor'].sum()
        pr = [(i/s_valor)*100 for i in df_groupby_cat['valor']]
        pr = [f"{j:,.2f}%" for j in pr]
        df_groupby_cat['Valor %'] = pr

        retorna["df_groupby_cat"] = df_groupby_cat
        return retorna

    @st.cache_data
    def grafico_lineplot(_self, df: pd.DataFrame) -> None:
        '''
            Plote da soma de `valor`
            :param df (pd.DataFrame): Origem dos valores
        '''
        plt.figure(figsize=(20, 5))
        f = sns.lineplot(
            x="data",
            y="valor",
            data=df
        )
        f.set(
            title="Série Temporal dos Gastos",
            xlabel="Data",
            ylabel="Valor",
        )
        st.pyplot(fig=plt)
        return None

    @st.cache_data
    def grafico_boxplot(_self, df: pd.DataFrame) -> None:
        '''
            Plote da soma de `valor`.
            :param df (pd.DataFrame): Origem dos valores
        '''
        plt.figure(figsize=(20, 5))
        plt.title("Distribuição dos Gastos")
        sns.boxplot(
            x='valor',
            data=df,
        )
        plt.xlabel("Valor em R$")
        st.pyplot(fig=plt)
        return None

    @st.cache_data
    def grafico_histplot(_self, df: pd.DataFrame) -> None:
        '''
            Plote da soma de `valor`.
            :param df (pd.DataFrame): Origem dos valores
        '''
        plt.figure(figsize=(20, 5))
        plt.title("Distribuição dos Gastos")
        sns.histplot(
            x='valor',
            data=df,
        )
        plt.xlabel("Valor em R$")
        st.pyplot(fig=plt)
        return None

    def __insere_mes(_self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Função insere a coluna mês na DataFrame.
        :param df (pd.DataFrame): DataFrame para ser modificada.
        '''
        df_select = df.copy()
        df_select["mes"] = df_select['ano_mes'].dt.to_period("M")
        return df_select

    @st.cache_data
    def grafico_barras_stack(_self, df: pd.DataFrame, coluna: str) -> None:
        '''
        Função de plot de gráfico de barras empilhado com a frequência
        de instâncias para a variável selecionada ao longo do tempo.
        :param df (pd.DataFrame): DataFrame para ser modificada.
        :param coluna (str): Coluna de interesse.
        '''
        x = "mes"
        df_select = _self.__insere_mes(df)
        tab = pd.crosstab(df_select[x], df_select[coluna])
        tab = tab.div(tab.sum(axis=1), axis=0)

        coluna_title = coluna.replace('_', ' ').title()
        title = f"Frequencia de locais do {coluna_title} ao longo dos meses"

        tab.plot.bar(
            figsize=(15, 5),
            title=title,
            xlabel=x.title(),
            ylabel="Frequência "+coluna.title(),
            stacked=True
        )
        plt.legend(bbox_to_anchor=(1.02, 1.05), loc=2, borderaxespad=0.)
        st.pyplot(fig=plt)
        return None

    @st.cache_data
    def grafico_pontos(_self, df: pd.DataFrame, coluna: str) -> None:
        '''
        Função de plot de gráfico de pontos, com interfavo de confiança de 95%,
        da renda em instância selecionada ao longo do tempo.
        :param df (pd.DataFrame): DataFrame para ser modificada.
        :param coluna (str): Coluna de interesse.
        '''
        x = "mes"
        y = "valor"
        df_select = _self.__insere_mes(df)

        coluna_title = coluna.replace('_', ' ').title()
        title = f"Renda média ao longo dos meses para {coluna_title}"

        plt.figure(figsize=(15, 5))

        f = sns.pointplot(
            x=x,
            y=y,
            hue=coluna,
            errorbar=('ci', 95),
            data=df_select,
        )
        f.set(
            title=title,
            xlabel=x.title(),
            ylabel=y.title()
        )

        plt.legend(bbox_to_anchor=(1.02, 1.05), loc=2, borderaxespad=0.)
        st.pyplot(fig=plt)
        return None

    @st.cache_data
    def grafico_barras(_self, df: pd.DataFrame, coluna: str) -> None:
        '''
        Função de plot de gráfico de barras da renda em instância selecionada
        ao longo do tempo.
        :param df (pd.DataFrame): DataFrame para ser modificada.
        :param coluna (str): Coluna de interesse.
        '''
        x = "mes"
        y = "valor"
        df_select = _self.__insere_mes(df)

        coluna_title = coluna.replace('_', ' ').title()
        title = f"Renda média ao longo dos meses para {coluna_title}"

        plt.figure(figsize=(15, 5))
        f = sns.barplot(
            x=x,
            y=y,
            hue=coluna,
            data=df_select
        )
        f.set(
            title=title,
            xlabel=x.replace("_", " ").title(),
            ylabel=y.replace("_", " ").title()+" média",
        )
        plt.legend(bbox_to_anchor=(1.02, 1.05), loc=2, borderaxespad=0.)
        st.pyplot(fig=plt)
        return None

    @st.cache_data
    def nuvem_palavras(_self, df: pd.DataFrame, coluna: str) -> None:
        '''
        Função que cria uma núvem de palavras com base em uma variável
        qualitativa nominal.
        :param df (pd.DataFrame): DataFrame de origem das palavras
        :param coluna (str): Variável que será usada para gerar a núvem
        '''
        index = df[coluna].value_counts().index
        values = df[coluna].value_counts().values
        palavras = {v[0]: v[1] for v in zip(index, values)}

        # inicializa uma word cloud
        wordcloud = WordCloud(
                        background_color='white',
                        width=1000,
                        height=500,
                        contour_width=3,
                        contour_color='lightblue',
                        colormap='winter'
        )

        # gera uma wordcloud através do dicionário de frequências
        wordcloud.generate_from_frequencies(frequencies=palavras)

        # Tamanho do gráfico
        plt.figure(figsize=(5, 5))
        plt.title(coluna.title(), size=14)

        # Plotagem da nuvem de palavras
        plt.imshow(wordcloud, interpolation='bilinear')

        # Remove as bordas
        plt.axis('off')

        # Mostra a word cloud
        st.pyplot(fig=plt)

        return None

    def __muda_classe(_self, x: str) -> str:
        return x.split(" : ")[1].lower().replace(" ", "_")

    @st.cache_data
    def carrega_df_estruturada(_self, link: str, data: str) -> pd.DataFrame:
        '''
        Função de estruturação dos dados de vendas.
        :param linl (str): Link para a tabela Excel;
        :return df (pd.DataFrame): Datafram estruturada;
        '''
        colunas = {
            "Cód.Prod.": "cod",
            "Unnamed: 1": "unnamed",
            "Descrição do Produto": "descr",
            "Val.Custo": "custo",
            "Val.Unit.": "unit",
            "Qtde": "qtde",
            "Desconto": "desconto",
            "Líquido": "liquido",
            "Vendas": "vendas",
        }

        # Lendo arquivo com os dados
        df = (
            pd.read_excel(link, skiprows=1)
            .rename(columns=colunas)
            .assign(classe=np.nan)
            .assign(data=data)
        )

        # Modificando a classe da data
        # df['data'] = pd.to_datetime(df['data'])

        # Obtendo os index das classes
        index_classes = df[df.cod == "-"].index.values

        # Obtendo os valores das classes
        df_code = df.loc[df['cod'] == "-", "unnamed"]
        classes = [_self.__muda_classe(n) for n in df_code]

        # Substituindo os valores para a variável classe
        df.loc[index_classes, "classe"] = classes

        # Propagação dos valores das classes
        df['classe'].fillna(method='ffill', inplace=True)

        # Removendo instâncias pelos index de classe
        df.drop(index_classes, inplace=True)

        # Substituindo ca coluna cod pela varável código
        df['cod'] = df['unnamed']

        # Removendo valores duplicados nos valores
        df = df.loc[df['cod'].dropna().index, :]

        # Removendo a variável código
        df.drop(['unnamed'], inplace=True, axis=1)

        # Completando NaN com 'NaN'
        df.fillna("NaN", inplace=True)

        return df

    def __linha_df(_self, linha: pd.Series) -> str:
        valores = "("
        for v in linha:
            valores += f"'{v}', "
        return valores[:-2]+"), "

    def formata_linhas_df(_self, df: pd.DataFrame) -> list:
        s_v = [_self.__linha_df(linha=df.iloc[li, :]) for li in range(len(df))]
        return s_v

    def formata_vendas(_self, df: pd.DataFrame) -> str:
        colunas = df.columns.values
        colunas_str = ", ".join(colunas)
        sql = f"INSERT INTO vendas ({colunas_str}) VALUES "
        sql += "".join(_self.formata_linhas_df(df.iloc[:, :]))
        sql = sql[:-2]
        sql += ";"
        return sql

    def formata_sql_vendas(_self) -> pd.DataFrame:
        nova_conexao = SQLite_execute()
        sql = "SELECT * FROM vendas"
        vendas = nova_conexao.select_table(sql)
        vendas_dict = {i: vendas[i] for i in range(len(vendas))}
        vendas_df = (
                        pd.DataFrame(vendas_dict)
                        .T
                        .set_index(0)
                    )
        colunas = nova_conexao.database_info()['vendas']['colunas'][1:]
        vendas_df.columns = colunas
        vendas_df['data'] = pd.to_datetime(vendas_df['data'])
        vendas_df.rename(columns={"liquido": "valor"}, inplace=True)
        return vendas_df

    def formulario_upload(_self) -> None:
        nova_conexao = SQLite_execute()
        st.markdown("<h1>Upload de Vendas</h>", unsafe_allow_html=True)
        df_insert = False
        # Mostra o dropin da data para a tabela
        with st.form("my-form", clear_on_submit=True):
            data_tabela = st.date_input(
                "Data Da Tabela",
                max_value=datetime.now(),
            )
            uppload_file = st.file_uploader("Escolha um arquivo")
            st.form_submit_button("Subir Tabela!")

        if uppload_file is not None:
            df1 = _self.carrega_df_estruturada(
                                                    link=uppload_file,
                                                    data=data_tabela
                                                )
            sql = _self.formata_vendas(df=df1)
            df_insert = True

        if df_insert:
            nova_conexao.execute_table(sql)
            uppload_file = None

        return None
