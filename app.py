import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Ocorrências de Roubo - ES",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Ocorrências de Roubo em Estabelecimentos Comerciais no ES")

st.write(
    "Análise das ocorrências de roubo em estabelecimentos comerciais "
    "no Espírito Santo, utilizando dados de ocorrências policiais."
)

# =========================================================
# CARREGAMENTO DO CSV
# =========================================================

try:

    # O CSV está junto do app.py no GitHub
    df = pd.read_csv(
        "ocorrencias.csv",
        sep=",",
        encoding="utf-8-sig"
    )

    # Limpar espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # =========================================================
    # TRATAMENTO DOS DADOS
    # =========================================================

    colunas_texto = [
        "GRUPO DE INCIDENTE",
        "TIPO DE INCIDENTE",
        "UF",
        "MUNICIPIO",
        "BAIRRO",
        "LOGRADOURO",
        "TIPO DE LOCAL"
    ]

    for coluna in colunas_texto:
        if coluna in df.columns:
            df[coluna] = (
                df[coluna]
                .astype(str)
                .str.strip()
            )

    # Transformar data
    df["DATA DO FATO"] = pd.to_datetime(
        df["DATA DO FATO"],
        errors="coerce"
    )

    # Criar coluna de ano
    df["ANO"] = df["DATA DO FATO"].dt.year

    # Criar coluna com a hora
    df["HORA"] = pd.to_datetime(
        df["HORA DO FATO"],
        format="%H:%M:%S",
        errors="coerce"
    ).dt.hour

    st.success("Base de dados carregada com sucesso!")

    # =========================================================
    # 1. CONHECENDO A BASE
    # =========================================================

    st.header("1. Conhecendo a base")

    st.subheader("Primeiras linhas")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Quantidade de ocorrências",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Quantidade de colunas",
            df.shape[1]
        )

    st.subheader("Colunas da base")

    st.write(
        df.columns.tolist()
    )

    st.subheader("Informações da base")

    informacoes = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo": df.dtypes.astype(str),
        "Valores ausentes": df.isnull().sum().values
    })

    st.dataframe(
        informacoes,
        use_container_width=True,
        hide_index=True
    )

    # =========================================================
    # 2. TRATAMENTO DOS DADOS
    # =========================================================

    st.header("2. Tratamento dos dados")

    st.subheader("Valores ausentes")

    valores_ausentes = pd.DataFrame({
        "Coluna": df.columns,
        "Valores ausentes": df.isnull().sum().values
    })

    st.dataframe(
        valores_ausentes,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Valores duplicados")

    st.write(
        f"Registros duplicados: *{df.duplicated().sum()}*"
    )

    # =========================================================
    # 3. PERGUNTA 1
    # =========================================================

    st.header("3. Pergunta 1")

    st.write(
        "Como o número de ocorrências de roubo em estabelecimentos "
        "comerciais varia ao longo dos anos?"
    )

    ocorrencias_ano = (
        df.dropna(subset=["ANO"])
        .groupby("ANO")
        .size()
        .reset_index(name="Quantidade")
    )

    ocorrencias_ano["ANO"] = (
        ocorrencias_ano["ANO"]
        .astype(int)
    )

    fig1 = px.line(
        ocorrencias_ano,
        x="ANO",
        y="Quantidade",
        markers=True,
        title="Evolução das ocorrências de roubo por ano",
        labels={
            "ANO": "Ano",
            "Quantidade": "Quantidade de ocorrências"
        }
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    if not ocorrencias_ano.empty:

        maior_ano = ocorrencias_ano.loc[
            ocorrencias_ano["Quantidade"].idxmax()
        ]

        menor_ano = ocorrencias_ano.loc[
            ocorrencias_ano["Quantidade"].idxmin()
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Ano com mais ocorrências",
                int(maior_ano["ANO"])
            )

            st.write(
                f"Quantidade: *{int(maior_ano['Quantidade'])}*"
            )

        with col2:

            st.metric(
                "Ano com menos ocorrências",
                int(menor_ano["ANO"])
            )

            st.write(
                f"Quantidade: *{int(menor_ano['Quantidade'])}*"
            )

    # =========================================================
    # 4. PERGUNTA 2
    # =========================================================

    st.header("4. Pergunta 2")

    st.write(
        "Quais municípios apresentam a maior quantidade "
        "de ocorrências de roubo em estabelecimentos comerciais?"
    )

    municipios = (
        df["MUNICIPIO"]
        .value_counts()
        .reset_index()
    )

    municipios.columns = [
        "Municipio",
        "Quantidade"
    ]

    municipios = municipios.head(10)

    fig2 = px.bar(
        municipios,
        x="Municipio",
        y="Quantidade",
        title="10 municípios com mais ocorrências",
        labels={
            "Municipio": "Município",
            "Quantidade": "Quantidade de ocorrências"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =========================================================
    # 5. PERGUNTA 3
    # =========================================================

    st.header("5. Pergunta 3")

    st.write(
        "Quais bairros possuem a maior quantidade de ocorrências?"
    )

    bairros = (
        df["BAIRRO"]
        .value_counts()
        .reset_index()
    )

    bairros.columns = [
        "Bairro",
        "Quantidade"
    ]

    bairros = bairros.head(10)

    fig3 = px.bar(
        bairros,
        x="Bairro",
        y="Quantidade",
        title="10 bairros com mais ocorrências",
        labels={
            "Bairro": "Bairro",
            "Quantidade": "Quantidade de ocorrências"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =========================================================
    # 6. PERGUNTA 4
    # =========================================================

    st.header("6. Pergunta 4")

    st.write(
        "Em quais horários acontecem mais ocorrências de roubo?"
    )

    horarios = (
        df["HORA"]
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )

    horarios.columns = [
        "Hora",
        "Quantidade"
    ]

    horarios["Hora"] = horarios["Hora"].astype(int)

    fig4 = px.bar(
        horarios,
        x="Hora",
        y="Quantidade",
        title="Ocorrências de roubo por horário",
        labels={
            "Hora": "Hora do dia",
            "Quantidade": "Quantidade de ocorrências"
        },
        text_auto=True
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    # =========================================================
    # 7. TIPO DE LOCAL
    # =========================================================

    st.header("7. Tipo de local das ocorrências")

    locais = (
        df["TIPO DE LOCAL"]
        .value_counts()
        .reset_index()
    )

    locais.columns = [
        "Local",
        "Quantidade"
    ]

    fig5 = px.pie(
        locais,
        names="Local",
        values="Quantidade",
        title="Distribuição das ocorrências por tipo de local"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # =========================================================
    # 8. DADOS DA BASE
    # =========================================================

    st.header("8. Dados da base")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================================================
    # 9. FONTE DOS DADOS
    # =========================================================

    st.header("9. Fonte dos dados")

    st.write(
        "Base de dados de ocorrências policiais do Espírito Santo."
    )

    st.write(
        "Os registros analisados correspondem a ocorrências "
        "classificadas como roubo em estabelecimento comercial."
    )

except Exception as erro:

    st.error(
        f"Erro ao carregar a base de dados: {erro}"
    )
