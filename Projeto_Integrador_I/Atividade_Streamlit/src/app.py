import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Configuração da página
st.set_page_config(page_title="Dashboard de Sinalização Ferroviária", layout="wide")

# Título
st.title("🚆 Dashboard de Sinalização Ferroviária")
st.markdown("Análise de velocidade permitida e ocupação de circuitos por tipo de sinalização")

# Definição da base de dados
#csv_data = st.file_uploader("Carregue a base CSV", type="csv")

# Carregar dados
#df = pd.read_csv(StringIO(csv_data))
df = pd.read_csv("C:/Users/dougm/OneDrive/Documentos/Projetos_Python/Projetos_FATEC_CD_2026_2028_Public/Projeto_Integrador_I/Atividade_Streamlit/data/dataset_sinalizacao_ferroviaria_amostra.csv")

# Criar abas para os gráficos
tab1, tab2 = st.tabs(["📈 Velocidade vs Tempo de Ocupação", "📊 Aspecto do Sinal por Tipo"])

## Gráfico 1: Dispersão (velocidade_permitida_kmh por tempo_ocupacao_circuito_seg)
with tab1:
    st.subheader("Relação entre Velocidade Permitida e Tempo de Ocupação do Circuito")
    
    # Criar gráfico de dispersão com Plotly
    fig_scatter = px.scatter(
        df,
        x='tempo_ocupacao_circuito_seg',
        y='velocidade_permitida_kmh',
        color='tipo_sinalizacao',
        hover_data=['id_trem', 'linha', 'id_bloco', 'aspecto_sinal'],
        title='Velocidade Permitida (km/h) vs Tempo de Ocupação (s)',
        labels={
            'tempo_ocupacao_circuito_seg': 'Tempo de Ocupação do Circuito (segundos)',
            'velocidade_permitida_kmh': 'Velocidade Permitida (km/h)',
            'tipo_sinalizacao': 'Tipo de Sinalização'
        },
        size_max=15,
        opacity=0.7
    )
    
    # Personalizar layout
    fig_scatter.update_layout(
        hovermode='closest',
        showlegend=True,
        height=600
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Estatísticas descritivas
    st.markdown("### 📊 Estatísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Velocidade Média", f"{df['velocidade_permitida_kmh'].mean():.1f} km/h")
    with col2:
        st.metric("Tempo Médio de Ocupação", f"{df['tempo_ocupacao_circuito_seg'].mean():.1f} s")

## Gráfico 2: Barras verticais (aspecto_sinal no X, tipo_sinalizacao no Y)
with tab2:
    st.subheader("Distribuição de Aspectos de Sinal por Tipo de Sinalização")
    
    # Agrupar dados por aspecto_sinal e tipo_sinalizacao
    df_grouped = df.groupby(['aspecto_sinal', 'tipo_sinalizacao']).size().reset_index(name='count')
    
    # Criar gráfico de barras com Plotly
    fig_bar = px.bar(
        df_grouped,
        x='aspecto_sinal',
        y='tipo_sinalizacao',
        color='aspecto_sinal',
        text='count',
        title='Contagem de Aspectos de Sinal por Tipo de Sinalização',
        labels={
            'aspecto_sinal': 'Aspecto do Sinal',
            'tipo_sinalizacao': 'Tipo de Sinalização',
            'count': 'Quantidade'
        },
        orientation='v',
        height=500
    )
    
    # Personalizar layout
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        showlegend=False,
        yaxis={'categoryorder': 'total descending'}
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tabela resumo
    st.markdown("### 📋 Tabela Resumo")
    st.dataframe(df_grouped, use_container_width=True)

# Sidebar com informações
with st.sidebar:
    st.header("ℹ️ Informações")
    st.markdown(f"""
    - **Total de registros:** {len(df)}
    - **Trens únicos:** {df['id_trem'].nunique()}
    - **Tipos de sinalização:** {df['tipo_sinalizacao'].nunique()}
    - **Aspectos de sinal:** {df['aspecto_sinal'].nunique()}
    """)
    
    st.markdown("---")
    st.markdown("**Legenda das cores:**")
    st.markdown("- 🟡 **Amarelo**: Atenção/redução de velocidade")
    st.markdown("- 🟢 **Verde**: Via livre")
    st.markdown("- 🔴 **Vermelho**: Parada obrigatória")
