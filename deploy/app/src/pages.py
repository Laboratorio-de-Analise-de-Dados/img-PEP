import pandas as pd
import streamlit as st

from src.uteis_functions import Functions
from src.sqlite_execute import SQLite_execute


def valores() -> None:
    '''
    Determina a página de valores
    '''
    # Importa a DataFrame
    functions = Functions()
    df = functions.importa_df()

    # Agrupa os valores pela data
    df_gouped_data = df[['data', 'valor']].groupby("data").sum().reset_index()

    # Ontêm a data inicial e final
    data_min = df_gouped_data.data.min()
    data_max = df_gouped_data.data.max()

    col_valor = st.columns(spec=(.2, 1, 2, .2))
    with col_valor[1]:
        st.markdown("<h1>Valores</h>", unsafe_allow_html=True)

        col_data = st.columns(spec=(1, 1))

        with col_data[0]:
            # Mostra o dropin da data inicial
            data_inicial = st.date_input(
                "Data Inicial",
                value=data_min,
                min_value=data_min,
                max_value=data_max,
            )
            data_inicial = pd.to_datetime(data_inicial)

        with col_data[1]:
            # Mostra o dropin da data final
            data_final = st.date_input(
                "Data Final",
                value=data_max,
                min_value=data_min,
                max_value=data_max,
            )
            data_final = pd.to_datetime(data_final)

        # Instancia o filtro e obtêm a DataFrame no período desejado
        filtro = (
            (df_gouped_data.data <= data_final) &
            (df_gouped_data.data >= data_inicial)
        )

        data = f"{functions.edita_data(data_inicial)} à "
        data += f"{functions.edita_data(data_final)}"
        st.markdown(f"<h2>{data}</h2>", unsafe_allow_html=True)

        df_copy = df_gouped_data[filtro].copy()

        val_resumo = functions.calculos_df_resumos(df_copy=df_copy)

        # Obtem a soma dos valores no período
        st.markdown(val_resumo["soma"], unsafe_allow_html=True)

        # Obtem a média dos valores no período
        st.markdown(val_resumo["media"], unsafe_allow_html=True)

        # Obtem a máximo dos valores no período
        st.markdown(val_resumo["maximo"], unsafe_allow_html=True)

        # Obtem a mininmo dos valores no período
        st.markdown(val_resumo["minimo"], unsafe_allow_html=True)

        st.markdown("---")

        st.dataframe(val_resumo["df_data_valor"], use_container_width=True)

    with col_valor[2]:
        st.markdown("<h1>Categorias</h>", unsafe_allow_html=True)

        col_valor_porcentagens = st.columns(spec=(1, 1))
        with col_valor_porcentagens[0]:
            st.markdown("<h3>Negócio</h3>", unsafe_allow_html=True)
            filtro = (
                (df.data <= data_final) &
                (df.data >= data_inicial)
            )
            df_copy = df[filtro].copy()
            val_resumo = functions.calculos_df_categorias(
                                                                df=df_copy,
                                                                cat="negocio"
                                                            )
            st.dataframe(
                val_resumo["df_groupby_cat"][['Valor R$', "Valor %"]],
                use_container_width=True
            )
        with col_valor_porcentagens[1]:
            functions.grafico_categorias(
                df=val_resumo["df_groupby_cat"],
                title="Negócio"
            )

        st.markdown("---")

        col_valor_porcentagens = st.columns(spec=(1, 1))
        with col_valor_porcentagens[0]:
            st.markdown("<h3>Custo</h3>", unsafe_allow_html=True)
            val_resumo = functions.calculos_df_categorias(
                                                                df=df_copy,
                                                                cat="custo"
                                                            )
            st.dataframe(
                val_resumo["df_groupby_cat"][['Valor R$', "Valor %"]],
                use_container_width=True
            )
        with col_valor_porcentagens[1]:
            functions.grafico_categorias(
                df=val_resumo["df_groupby_cat"],
                title="Custo"
            )

    st.markdown("---")

    # Instancia os gráficos
    col_graf = st.columns(spec=(.5, 1, 1, 1, .5))
    with col_graf[1]:
        functions.grafico_lineplot(df=df_copy)
    with col_graf[2]:
        functions.grafico_boxplot(df=df_copy)
    with col_graf[3]:
        functions.grafico_histplot(df=df_copy)

    return None


def categorias() -> None:
    '''
    Determina a página de variáveis categóricas
    '''
    functions = Functions()

    # Importa a DataFrame
    df = functions.importa_df()

    st.markdown("<h1>Categoria</h>", unsafe_allow_html=True)

    # Seleciona o nome das colunas com dados categóricos
    colunas = df.select_dtypes("category").columns.values
    nomes_selectbox = {v.replace("_", " ").title(): v for v in colunas}

    # Apresenta as colunas para a seleção do usuário
    categoria = st.selectbox("Escolha uma informação:", nomes_selectbox.keys())
    coluna = nomes_selectbox[categoria]

    # Instancia os gráficos
    functions.grafico_barras(df=df, coluna=coluna)
    functions.grafico_pontos(df=df, coluna=coluna)
    functions.grafico_barras_stack(df=df, coluna=coluna)

    return None


def qualitativas() -> None:
    '''
    Determina a página de variáveis categóricas
    '''
    functions = Functions()

    # Importa a DataFrame
    df = functions.importa_df()

    st.markdown("<h1>Descrição</h>", unsafe_allow_html=True)

    # Seleciona o nome das colunas com dados categóricos
    colunas = df.select_dtypes("object").columns.values
    nomes_selec = {v.replace("_", " ").title(): v for v in colunas}

    # Apresenta as colunas para a seleção do usuário
    qualitativa = st.selectbox("Escolha uma informação:", nomes_selec.keys())
    coluna = nomes_selec[qualitativa]

    # Instancia os gráficos
    functions.nuvem_palavras(df=df, coluna=coluna)

    return None


def vendas() -> None:
    '''
    Determina a página de vendas
    '''
    # Instância de conexão ao banco de dados
    nova_conexao = SQLite_execute()

    # Verifica se a tabela vendas está no banco. Caso contrário, cria a tabela
    if "vendas" not in nova_conexao.database_info():
        sql = nova_conexao.sql_table_vendas()
        nova_conexao.create_tables(sql)

    # Instância de funções úteis à página
    functions = Functions()

    # Se a tabela vendas tiver dados, esses são recuperados para uma DataFrame
    teste_tabela = False
    try:
        vendas_df = functions.formata_sql_vendas()
        teste_tabela = True
    except Exception:
        # Caso contrário, informa que não existem vendas cadastradas
        st.write("<h2>Nenhuma Venda Cadastrada</h2>", unsafe_allow_html=True)

    # Caso existam vendas cadastradas
    if teste_tabela:
        # Contêm a data inicial e final
        data_min = vendas_df['data'].min()
        data_max = vendas_df['data'].max()

        col_data = st.columns(spec=(1, 1, 1))
        with col_data[0]:
            st.markdown("<h1>Vendas</h>", unsafe_allow_html=True)
        with col_data[1]:
            # Mostra o dropin da data inicial
            data_inicial = st.date_input(
                "Data Inicial",
                value=data_min,
                min_value=data_min,
                max_value=data_max,
                # label_visibility='hidden',
            )
            # Converte a data inicial em datetime
            data_inicial = pd.to_datetime(data_inicial)

        with col_data[2]:
            # Mostra o dropin da data final
            data_final = st.date_input(
                "Data Final",
                value=data_max,
                min_value=data_min,
                max_value=data_max,
            )
            # Converte a data final em datetime
            data_final = pd.to_datetime(data_final)

            # Instancia o filtro e obtêm a DataFrame no período desejado
            vendas_df = functions.formata_sql_vendas()

            filtro = (
                (vendas_df['data'] >= data_inicial) &
                (vendas_df['data'] <= data_final)
            )

            # Instância a DataFrame filtrada pelo tempo
            vendas_df = vendas_df[filtro]

        # Caso o filtro esteja correto
        try:
            data = f"{functions.edita_data(vendas_df['data'].min())} à "
            data += f"{functions.edita_data(vendas_df['data'].max())}"
            st.markdown(f"<h3>{data}</h3>", unsafe_allow_html=True)
        except Exception:
            # Caso contrário
            mensagem = "Data Inicial é Superior a Final! Corrija a seleção."
            st.markdown(f'<h1>{mensagem}</h1>', unsafe_allow_html=True)

        col = st.columns((1, 1, 1))
        with col[0]:
            # Agrupamento dos dados para visualização das vendas em porcentagem
            df_g_sum = vendas_df.groupby("classe")['valor'].sum()
            lt_classes = [n.title().replace("_", " ") for n in df_g_sum.index]
            lt_valores = [functions.float_p_real(n) for n in df_g_sum]
            lt_val_rela = [f"{(n/df_g_sum.sum())*100:.2f}%" for n in df_g_sum]

            tabela_inicial = pd.DataFrame(
                                            data={
                                                "Classes": lt_classes,
                                                "Valor R$": lt_valores,
                                                "Valor %": lt_val_rela,
                                            }
            )
            tabela_inicial = tabela_inicial.set_index("Classes")

            # Calculando o valor total para inserir na última linha
            total_dict = {
                'Valor R$': functions.float_p_real(df_g_sum.sum()),
                'Valor %': '100%',
            }
            total = pd.DataFrame(
                index=['Total'],
                data=total_dict
            )

            # Inserindo valor total
            tabela_inicial = pd.concat([tabela_inicial, total])

            # Instâncianco medidas resumo da tabela
            val_resumo = functions.calculos_df_resumos(df_copy=vendas_df)

            # Obtem a soma dos valores no período
            st.markdown(val_resumo["soma"], unsafe_allow_html=True)

            # Obtem a média dos valores no período
            st.markdown(val_resumo["media"], unsafe_allow_html=True)

            # Obtem a mediana dos valores no período
            st.markdown(val_resumo["mediana"], unsafe_allow_html=True)

            # Obtem a máximo dos valores no período
            st.markdown(val_resumo["maximo"], unsafe_allow_html=True)

            # Obtem a mininmo dos valores no período
            st.markdown(val_resumo["minimo"], unsafe_allow_html=True)

        st.markdown("---")

        # Inserindo a tabela completa dos dados
        st.markdown("<h1>Tabela Completa Vendas</h>", unsafe_allow_html=True)
        st.dataframe(val_resumo["df_data_valor"], use_container_width=True)
        st.markdown("---")

        with col[1]:
            # Tabela contendo o resumo dos dados
            st.table(tabela_inicial)

        with col[2]:
            # Formatação da DataFrame de vendas agrupadas
            def compr(df_g_sum):
                return [x.title().replace("_", " ") for x in df_g_sum.index]
            df_g_edit = (
                df_g_sum.to_frame().copy()
                .reset_index()
                .assign(classe=compr(df_g_sum))
                .set_index("classe")
                .assign(valor=[(n/df_g_sum.sum())*100 for n in df_g_sum])
                .sort_values("valor", ascending=True)
            )

            data_max = f"{vendas_df['data'].max().day}/"
            data_max += f"{vendas_df['data'].max().month}/"
            data_max += f"{vendas_df['data'].max().year}"

            data_min = f"{vendas_df['data'].min().day}/"
            data_min += f"{vendas_df['data'].min().month}/"
            data_min += f"{vendas_df['data'].min().year}"

            if data_min == data_max:
                title = f"Vendas de {data_min}"
            else:
                title = f"Vendas de {data_min} até {data_max}"

            functions.grafico_categorias(
                df=df_g_edit,
                title=title,
                ylabel="Valor (%)"
            )

    functions.formulario_upload()

    return None


def dev_categorias() -> None:
    '''
        Testando algumas ideias
    '''
    functions = Functions()

    # Importa a DataFrame
    df = functions.importa_df()

    st.dataframe(df, use_container_width=True)

    negocio = df['negocio'].value_counts(normalize=True)
    custo = df["custo"].value_counts(normalize=True)

    col = st.columns((2, 1, 1, 2))
    with col[1]:
        st.dataframe(negocio, use_container_width=True)
    with col[2]:
        st.dataframe(custo, use_container_width=True)

    custo_objetivo = {
        "fixo": [
            "Despesa Operacional",
            "Estrutura",
            "Folha",
            "Impostos",
            "Manutenção",
        ],
        "variavel": [
            "Compras",
            "Cortesia",
            "Couvert",
            "Decoração",
            "Marketing",
            "Terceiros",
            "Pacotes",
            "Devoluções",
            "Doaçães",
        ]
    }
    st.write(custo_objetivo)
    return None
