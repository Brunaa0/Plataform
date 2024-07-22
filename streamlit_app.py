import streamlit as st
import pandas as pd

# Função para carregar arquivos
def load_data(file, delimiter=None):
    if file is not None:
        file_extension = file.name.split('.')[-1]
        if file_extension == 'csv':
            return pd.read_csv(file, delimiter=delimiter)
        elif file_extension == 'json':
            return pd.read_json(file)
        elif file_extension in ['xls', 'xlsx']:
            return pd.read_excel(file)
        else:
            st.error("Formato de arquivo não suportado. Por favor, carregue um arquivo CSV, JSON ou Excel.")
            return None
    return None

# Inicialização do session_state
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = []

if 'variable_types' not in st.session_state:
    st.session_state.variable_types = {}

if 'numeric_types' not in st.session_state:
    st.session_state.numeric_types = {}

st.title("MLCASE: Plataforma Automatizada de Desenvolvimento de Modelos de Machine Learning")
st.sidebar.header("Configurações")

# Upload de dados
file_type = st.sidebar.selectbox("Selecione o tipo de arquivo", ["CSV", "JSON", "Excel"])

uploaded_file = None
delimiter = None

if file_type == "CSV":
    delimiter = st.sidebar.selectbox("Selecione o delimitador", [",", ";"])
    uploaded_file = st.sidebar.file_uploader("Faça upload do seu arquivo CSV", type=["csv"])
elif file_type == "JSON":
    uploaded_file = st.sidebar.file_uploader("Faça upload do seu arquivo JSON", type=["json"])
elif file_type == "Excel":
    uploaded_file = st.sidebar.file_uploader("Faça upload do seu arquivo Excel", type=["xls", "xlsx"])

data = load_data(uploaded_file, delimiter=delimiter)

# Etapa 1: Seleção das colunas
if st.session_state.step == 1:
    if data is not None:
        st.write("Dados Carregados:")
        st.write(data.head())

        if not st.session_state.selected_columns:
            st.session_state.selected_columns = data.columns.tolist()

        selected_columns = st.multiselect("Selecione as colunas que deseja incluir:", data.columns.tolist(), default=st.session_state.selected_columns)

        if st.button("Concluir seleção de colunas"):
            st.session_state.selected_columns = selected_columns
            st.session_state.step = 2

# Etapa 2: Especificação do tipo de variável
elif st.session_state.step == 2:
    data_subset = data[st.session_state.selected_columns]
    st.write("Dados Selecionados:")
    st.write(data_subset.head())

    # Mostrar opções para cada coluna selecionada
    for col in st.session_state.selected_columns:
        if col not in st.session_state.variable_types:
            initial_type = "Categórica" if pd.api.types.is_categorical_dtype(data[col]) else "Numérica"
            selected_type = st.radio(f"Selecione o tipo da variável '{col}':", ["Categórica", "Numérica"], index=0 if initial_type == "Categórica" else 1)
            st.session_state.variable_types[col] = selected_type  # Armazenar a escolha do usuário
        else:
            selected_type = st.session_state.variable_types[col]
            new_type = st.radio(f"Selecione o tipo da variável '{col}':", ["Categórica", "Numérica"], index=0 if selected_type == "Categórica" else 1)
            if new_type != selected_type:
                st.session_state.variable_types[col] = new_type

    if st.button("Voltar ao passo anterior"):
        st.session_state.step = 1

    if st.button("Concluir especificação de tipos"):
        st.session_state.step = 3
        
# Etapa 3: Especificação dos tipos numéricos
elif st.session_state.step == 3:
    data_subset = data[st.session_state.selected_columns]
    st.write("Dados Selecionados:")
    st.write(data_subset.head())

    # Mostrar opções para tipos numéricos apenas para variáveis selecionadas como numéricas
    for col in st.session_state.selected_columns:
        if st.session_state.variable_types.get(col) == "Numérica":
            if col not in st.session_state.numeric_types:
                st.session_state.numeric_types[col] = "Int"  # Definir um tipo numérico padrão inicial

            numeric_type = st.selectbox(f"Tipo Numérico para '{col}':", ["Int", "Float", "Complex", "Dec", "Frac", "Bool"], index=0)
            st.session_state.numeric_types[col] = numeric_type  # Armazenar o tipo numérico selecionado

    st.write("Tipos Numéricos Selecionados:")
    st.write(st.session_state.numeric_types)

    if st.button("Voltar ao passo anterior"):
        st.session_state.step = 1
        
    if st.button("Concluir e passar para o próximo passo"):
        st.session_state.step = 4
