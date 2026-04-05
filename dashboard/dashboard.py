import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='darkgrid')

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

@st.cache_data
def load_data():
    day_df = pd.read_csv("dashboard/clean_day.csv")
    hour_df = pd.read_csv("dashboard/clean_hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

st.title("Bike Sharing Dashboard")
st.markdown("---")

# Bagian 1: Analisis Harian
st.header("Analisis Peminjaman Harian")

col1, col2 = st.columns(2)

with col1:
    # Visualisasi 1: Pengaruh Musim
    st.subheader("Pengaruh Musim terhadap Peminjaman")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season', y='cnt', data=day_df, ax=ax1, palette='viridis', errorbar=None)
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig1)

with col2:
    # Visualisasi 2: Casual vs Registered
    st.subheader("Pola Pengguna: Casual vs Registered")
    user_pattern = day_df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
    user_pattern_melted = user_pattern.melt(id_vars='workingday', var_name='user_type', value_name='count')
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x='workingday', y='count', hue='user_type', data=user_pattern_melted, palette='Set2', ax=ax2)
    ax2.set_xlabel("Tipe Hari")
    ax2.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig2)

# Visualisasi Analisis Lanjutan (Binning)
st.subheader("Distribusi Kategori Hari")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.countplot(data=day_df, x='rental_category', palette='magma', order=['Sepi', 'Normal', 'Ramai'], ax=ax3)
ax3.set_xlabel("Kategori Penyewaan")
ax3.set_ylabel("Jumlah Hari")
st.pyplot(fig3)

st.markdown("---")

# Bagian 2: Analisis Per Jam
st.header("Analisis Peminjaman Per Jam")
st.subheader("Tren Penyewaan Berdasarkan Jam")

# Visualisasi Tren Jam Sibuk
hourly_trend = hour_df.groupby('hr')['cnt'].mean().reset_index()
fig4, ax4 = plt.subplots(figsize=(12, 5))
sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker='o', ax=ax4, color='b')

ax4.set_xticks(range(0, 24))
ax4.set_xlabel("Jam (0-23)")
ax4.set_ylabel("Rata-rata Peminjaman")
ax4.set_title("Rata-rata Penyewaan Sepeda per Jam")
st.pyplot(fig4)