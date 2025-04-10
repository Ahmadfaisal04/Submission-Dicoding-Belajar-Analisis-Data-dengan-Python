import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide", initial_sidebar_state="expanded")

# Tema terang untuk seaborn/matplotlib
sns.set_theme(style="whitegrid")

# Judul utama
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Menampilkan analisis data penyewaan sepeda berdasarkan data harian dan per jam.")

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("data/day.csv")
    hour_df = pd.read_csv("data/hour.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar untuk filter
st.sidebar.header("🔍 Filter Data")
years = day_df["yr"].map({0: "2011", 1: "2012"}).unique().tolist()
selected_years = st.sidebar.multiselect("Pilih Tahun:", years, default=years)

seasons = day_df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}).unique().tolist()
selected_seasons = st.sidebar.multiselect("Pilih Musim:", seasons, default=seasons)

# Terapkan filter ke data
filtered_day_df = day_df[
    (day_df["yr"].map({0: "2011", 1: "2012"}).isin(selected_years)) &
    (day_df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}).isin(selected_seasons))
]

# ----------------------#
# Layout 1: Ringkasan #
# ----------------------#
st.subheader("📊 Ringkasan Penyewaan Sepeda")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Harian", f"{filtered_day_df['cnt'].mean():,.2f}")
with col3:
    st.metric("Penyewaan Maksimum", f"{filtered_day_df['cnt'].max():,}")

# ------------------------------#
# Grafik 1: Pola Penyewaan Harian
# ------------------------------#
st.subheader("📅 Pola Penyewaan Sepeda per Hari")

fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(pd.to_datetime(filtered_day_df["dteday"]), filtered_day_df["cnt"], color="tab:blue", linewidth=2)
ax1.set_xlabel("Tanggal")
ax1.set_ylabel("Jumlah Penyewaan")
ax1.set_title("Tren Penyewaan Sepeda Harian")
st.pyplot(fig1)

# ------------------------------#
# Grafik 2: Pola Penyewaan per Jam
# ------------------------------#
st.subheader("⏰ Pola Penyewaan Sepeda per Jam (Rata-rata)")

avg_hourly = hour_df.groupby("hr")["cnt"].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 4))
sns.lineplot(data=avg_hourly, x="hr", y="cnt", ax=ax2, color="tab:green")
ax2.set_title("Rata-rata Penyewaan per Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig2)

# ------------------------------#
# Grafik 3: Penyewaan Berdasarkan Musim
# ------------------------------#
st.subheader("🌤️ Penyewaan Berdasarkan Musim")

season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_df = filtered_day_df.copy()
season_df["season_label"] = season_df["season"].map(season_map)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.boxplot(data=season_df, x="season_label", y="cnt", palette="Set2", ax=ax3)
ax3.set_title("Distribusi Penyewaan Sepeda per Musim")
ax3.set_xlabel("Musim")
ax3.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig3)

# ------------------------------#
# Grafik 4: Penyewaan vs. Cuaca
# ------------------------------#
st.subheader("🌦️ Penyewaan Berdasarkan Kondisi Cuaca")

weather_map = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan ringan",
    4: "Hujan lebat"
}
weather_df = filtered_day_df.copy()
weather_df["weather_label"] = weather_df["weathersit"].map(weather_map)

fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.barplot(data=weather_df, x="weather_label", y="cnt", palette="pastel", ax=ax4)
ax4.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax4.set_xlabel("Cuaca")
ax4.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig4)

# ------------------------------#
# Tabel data akhir
# ------------------------------#
st.subheader("📄 Tabel Data Harian (Setelah Filter)")
st.dataframe(filtered_day_df.head(20))
