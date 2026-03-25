# arquivo: frontend/app/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
import time

# Configuração da Página
st.set_page_config(page_title="Inteligência de Frotas & SST", page_icon="🚚", layout="wide")

# Conexão com o Banco de Dados
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "admin_password")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "frotas_db")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

@st.cache_data(ttl=5) # Cache de 5 segundos para não derrubar o banco com muitas queries
def carregar_dados():
    try:
        engine = create_engine(DATABASE_URL)
        # Lendo diretamente da tabela que nosso Worker está alimentando
        query = "SELECT * FROM telemetria_frota ORDER BY timestamp DESC"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no banco de dados: {e}")
        return pd.DataFrame()

# --- Interface do Dashboard ---
st.title("📊 Centro de Controle Operacional: Frotas & SST")
st.markdown("Monitoramento em tempo real de telemetria, gestão de pneus e alertas de segurança.")

# Botão de atualização manual
if st.button("🔄 Atualizar Dados Agora"):
    st.cache_data.clear()

df = carregar_dados()

if df.empty:
    st.warning("Aguardando dados da telemetria... Vá no Swagger da API e envie algumas requisições!")
else:
    # --- KPIs Principais ---
    st.markdown("### 🎯 KPIs Globais")
    col1, col2, col3, col4 = st.columns(4)
    
    total_veiculos = df['veiculo_id'].nunique()
    alertas_fadiga = df[df['alerta_fadiga'] == True].shape[0]
    vel_maxima = df['velocidade_kmh'].max()
    cargas_perigosas = df[df['carga_perigosa_status'] != "NORMAL"].shape[0]

    col1.metric("Veículos Ativos", total_veiculos)
    col2.metric("🚨 Alertas de Fadiga (SST)", alertas_fadiga, delta_color="inverse")
    col3.metric("Velocidade Máxima Registrada", f"{vel_maxima} km/h")
    col4.metric("Atenção: Cargas Perigosas", cargas_perigosas)

    st.divider()

    # --- Análises Gráficas ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### 🌡️ Temperatura Atual do Motor por Veículo")
        
        # O Toque de Mestre: Agrupamos pelo veículo pegando apenas a última temperatura registrada (a mais recente)
        df_temp_atual = df.groupby('veiculo_id')['temperatura_motor_celsius'].first().reset_index()
        
        fig_temp = px.bar(df_temp_atual, x='veiculo_id', y='temperatura_motor_celsius', color='veiculo_id')
        st.plotly_chart(fig_temp, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### 🛞 Anomalias na Pressão dos Pneus")
        st.info("A extração de dados JSON do PostgreSQL permite análises profundas de componentes isolados.")
        # Mostrando a tabela bruta para os pneus (como o campo é JSON, o Pandas já o trata como dicionário)
        df_pneus = df[['veiculo_id', 'pressao_pneus_psi', 'timestamp']].head(5)
        st.dataframe(df_pneus, use_container_width=True)

    st.divider()
    
    st.markdown("#### 📋 Últimos Registros Brutos (Auditoria)")
    st.dataframe(df.drop(columns=['id']).head(10), use_container_width=True)