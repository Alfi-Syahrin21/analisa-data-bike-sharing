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

st.title("🚲 Bike Sharing Dashboard")

st.subheader("Informasi Umum")
col1, col2, col3 = st.columns(3)

with col1:
    total_peminjaman = day_df['cnt'].sum()
    st.metric("Total Peminjaman", value=f"{total_peminjaman:}")
with col2:
    total_registered = day_df['registered'].sum()
    st.metric("Total Pengguna Registered", value=f"{total_registered:}")
with col3:
    total_casual = day_df['casual'].sum()
    st.metric("Total Pengguna Casual", value=f"{total_casual:}")

st.markdown("---")



st.header("Analisis Peminjaman Harian")

st.markdown("**Filter Data Harian:**")
col_filter_day1, col_filter_day2, col_filter_day3 = st.columns(3)

with col_filter_day1:
    year_filter_day = st.multiselect("Pilih Tahun:", options=day_df['yr'].unique(), default=day_df['yr'].unique())
with col_filter_day2:
    season_filter = st.multiselect("Pilih Musim:", options=day_df['season'].unique(), default=day_df['season'].unique())
with col_filter_day3:
    workingday_filter = st.multiselect("Pilih Tipe Hari:", options=day_df['workingday'].unique(), default=day_df['workingday'].unique())

filtered_day_df = day_df[
    (day_df['season'].isin(season_filter)) & 
    (day_df['workingday'].isin(workingday_filter)) &
    (day_df['yr'].isin(year_filter_day))
]

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Pengaruh Musim")
    if not filtered_day_df.empty:

        st.info("Insight: Musim gugur secara konsisten menjadi musim dengan penyewaan tertinggi.")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='season', y='cnt', hue='yr', data=filtered_day_df, ax=ax1, palette='viridis', errorbar=None)
        ax1.set_xlabel("Musim")
        ax1.set_ylabel("Rata-rata Peminjaman")
        st.pyplot(fig1)
    else:
        st.warning("Data kosong. Silakan sesuaikan filter Anda.")

with col_chart2:
    st.subheader("Pola Pengguna Casual vs Registered")
    if not filtered_day_df.empty:
        user_pattern = filtered_day_df.groupby(['yr', 'workingday'])[['casual', 'registered']].mean().reset_index()
        user_pattern_melted = user_pattern.melt(id_vars=['yr', 'workingday'], var_name='user_type', value_name='count')
        user_pattern_melted['day_user'] = user_pattern_melted['workingday'] + " - " + user_pattern_melted['user_type'].str.capitalize()
        
        st.info("Insight: Pengguna Registered mendominasi di hari kerja, sedangkan Casual lebih aktif saat hari libur.")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(x='day_user', y='count', hue='yr', data=user_pattern_melted, palette='Set2', ax=ax2)
        ax2.set_xlabel("Kondisi Hari & Tipe Pengguna")
        ax2.set_ylabel("Rata-rata Peminjaman")
        plt.xticks(rotation=15)
        st.pyplot(fig2)
    else:
        st.warning("Data kosong. Silakan sesuaikan filter Anda.")

st.markdown("---")

st.header("Analisis Peminjaman Per Jam")

st.markdown("**Filter Data Per Jam:**")
col_filter_hour1, col_filter_hour2 = st.columns(2)

with col_filter_hour1:
    year_filter_hour = st.multiselect("Pilih Tahun :", options=hour_df['yr'].unique(), default=hour_df['yr'].unique())
with col_filter_hour2:
    hour_filter = st.slider("Pilih Rentang Jam:", min_value=0, max_value=23, value=(0, 23))

# Menerapkan Filter Per Jam
filtered_hour_df = hour_df[
    (hour_df['hr'] >= hour_filter[0]) & 
    (hour_df['hr'] <= hour_filter[1]) &
    (hour_df['yr'].isin(year_filter_hour))
]

if not filtered_hour_df.empty:
    hourly_trend = filtered_hour_df.groupby('hr')['cnt'].mean().reset_index()

    st.info(f"Insight: Menampilkan rata-rata penyewaan pada rentang jam {hour_filter[0]}:00 - {hour_filter[1]}:00. Puncak penyewaan terjadi di jam masuk kerja dan pulang kerja.")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker='o', ax=ax3, color='b')
    ax3.set_xticks(range(hour_filter[0], hour_filter[1] + 1))
    ax3.set_xlabel("Jam")
    ax3.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig3)
else:
    st.warning("Data kosong. Silakan sesuaikan filter Anda.")