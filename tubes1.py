import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# ==============================================================================
# KONFIGURASI HALAMAN (AESTHETIC COASTAL / PASTEL SKY HERO UI)
# ==============================================================================
st.set_page_config(
    page_title="CHILIE",
    page_icon="🌶️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CUSTOM CSS (GAYA HERO COASTAL PASTEL + KARTU VERTIKAL + TOP NAV BAR)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    /* Latar belakang lembut bernuansa langit & pasir pantai pastel */
    .stApp {
        background: linear-gradient(155deg, #2B869C 0%, #7CC0CE 24%, #F4E6D8 56%, #E4D7CA 80%, #99BDC6 100%);
        background-attachment: fixed;
        color: #163C4B;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sembunyikan sidebar & header bawaan */
    [data-testid="collapsedControl"], section[data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    /* TOP BAR BRANDING */
    .topbar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.15rem;
        letter-spacing: 1px;
        padding-top: 6px;
    }
    .logo-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 3px solid #FFFFFF;
        background: radial-gradient(circle at 65% 35%, #FFFFFF 35%, transparent 38%);
        display: inline-block;
    }

    /* STYLING RADIO BUTTON MENJADI TOP NAVIGATION BAR SIMPEL */
    div[data-testid="stRadio"] > div {
        flex-direction: row;
        justify-content: flex-end;
        gap: 10px;
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(10px);
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }
    div[data-testid="stRadio"] label {
        background: transparent !important;
        padding: 5px 14px !important;
        border-radius: 999px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.6px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: #1C7C91 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(22, 60, 75, 0.25);
    }
    /* Sembunyikan bulatan radio bawaan */
    div[data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* HERO DISPLAY TYPOGRAPHY (SEPERTI "NEVER STOP EXPLORING THE WORLD.") */
    .kicker-text {
        font-size: 0.85rem;
        font-weight: 700;
        color: #164E63;
        letter-spacing: 0.8px;
        margin-top: 1.6rem;
        margin-bottom: 0.3rem;
    }
    .display-hero {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4.3rem;
        line-height: 0.94;
        color: #124559;
        letter-spacing: 1px;
        margin: 0 0 1rem 0;
        text-shadow: 0 2px 12px rgba(255, 255, 255, 0.45);
    }
    .hero-copy {
        font-size: 0.9rem;
        line-height: 1.6;
        color: #264653;
        max-width: 440px;
        margin-bottom: 1.4rem;
    }
    .pill-cta {
        display: inline-block;
        background: #1C7C91;
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 1px;
        padding: 10px 26px;
        border-radius: 999px;
        box-shadow: 0 8px 18px rgba(28, 124, 145, 0.32);
        text-decoration: none;
    }

    /* 3 KARTU VERTIKAL ROUNDED (ALA KARTU BEACH / NATURE / HOTEL) */
    .story-card {
        border-radius: 22px;
        padding: 1.35rem 1.2rem;
        height: 310px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        color: #FFFFFF;
        box-shadow: 0 16px 32px rgba(18, 69, 89, 0.22);
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease;
    }
    .story-card:hover {
        transform: translateY(-6px);
    }
    .card-coral {
        background: linear-gradient(165deg, #E29578 0%, #C85A32 58%, #7F2D18 100%);
    }
    .card-lagoon {
        background: linear-gradient(165deg, #2A9D8F 0%, #1B6B7A 58%, #0F3D4C 100%);
    }
    .card-reef {
        background: linear-gradient(165deg, #48CAE4 0%, #0077B6 58%, #023E8A 100%);
    }
    .card-tag {
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(6px);
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        align-self: flex-start;
        letter-spacing: 0.5px;
    }
    .card-stat {
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.15;
        margin-top: auto;
        margin-bottom: 0.35rem;
    }
    .card-desc-mini {
        font-size: 0.78rem;
        opacity: 0.92;
        line-height: 1.4;
        margin-bottom: 0.7rem;
    }
    .card-footer-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.85rem;
        letter-spacing: 1px;
        line-height: 1;
        border-top: 1px solid rgba(255, 255, 255, 0.28);
        padding-top: 0.55rem;
    }

    /* PANEL KACA (GLASSMORPHISM) UNTUK AREA GRAFIK & ANALISIS */
    .glass-panel {
        background: rgba(255, 255, 255, 0.76);
        backdrop-filter: blur(14px);
        border-radius: 24px;
        padding: 1.6rem 1.8rem;
        border: 1px solid rgba(255, 255, 255, 0.65);
        box-shadow: 0 12px 30px rgba(18, 69, 89, 0.1);
        margin-top: 1.2rem;
    }
    .section-num {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.6rem;
        color: #FFFFFF;
        text-shadow: 0 2px 10px rgba(18, 69, 89, 0.3);
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# LOAD DATA
# ==============================================================================
@st.cache_data
def load_data():
    return pd.read_csv("dataset_tubes_cabai_2023.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ File `dataset_tubes_cabai_2023.csv` tidak ditemukan di folder yang sama dengan `app.py`.")
    st.stop()

opt_cols = [
    "Virus Kuning", "Lalat Buah", "Antraknose", "Layu Bakteri",
    "Virus Keriting", "Bercak Daun", "Kutu Daun", "Layu Fusarium",
    "Tungau", "Ulat Grayak", "Virus Mozaik"
]

# ==============================================================================
# TOP BAR (LOGO DI KIRI + MENU PILIHAN DI BAR ATAS KANAN)
# ==============================================================================
nav_l, nav_r = st.columns([1, 2.2])
with nav_l:
    st.markdown("""
    <div class="topbar-brand">
        <span class="logo-circle"></span>
        <span>KELOMPOK 11</span>
    </div>
    """, unsafe_allow_html=True)

with nav_r:
    menu = st.radio(
        "Navigasi Utama",
        ["HOME", "REGRESI IKLIM", "KLUSTERING", "DATA & KESIMPULAN"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.write("")

# ==============================================================================
# HALAMAN 1: HOME (PERSIS LAYOUT HERO + 3 KARTU VERTIKAL ROUNDED)
# ==============================================================================
if menu == "HOME":
    col_hero, col_cards = st.columns([1, 1.35], gap="large")

    with col_hero:
        st.markdown("""
        <div class="kicker-text"> Dashboard Statistik Kementan & BMKG</div>
        <h1 class="display-hero">JELAJAHI POLA<br>IKLIM & HAMA<br>CABAI.</h1>
        <p class="hero-copy">
            Analisis interaktif pengaruh curah hujan, suhu, dan kelembapan terhadap 
            serangan 11 organisme pengganggu tumbuhan (OPT) cabai serta pemetaan klaster 
            34 provinsi di Indonesia.
        </p>
        <div class="pill-cta">PILIH MENU DI BAR ATAS ↑</div>
        """, unsafe_allow_html=True)

    with col_cards:
        c1, c2, c3 = st.columns(3, gap="medium")
        top_prov = df.sort_values("Total_LTS_11_OPT_Ha", ascending=False).iloc[0]
        top_opt_name = df[opt_cols].sum().idxmax()
        top_opt_val = df[opt_cols].sum().max()

        with c1:
            st.markdown(f"""
            <div class="story-card card-coral">
                <div class="card-tag"> OPT TERTINGGI</div>
                <div>
                    <div class="card-stat">{top_opt_val:,.0f} Ha</div>
                    <div class="card-desc-mini">Serangan nasional terluas tahun 2023 didominasi oleh jamur penyebab busuk buah.</div>
                    <div class="card-footer-title">{top_opt_name.upper()}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="story-card card-lagoon">
                <div class="card-tag"> RATA-RATA IKLIM</div>
                <div>
                    <div class="card-stat">{df['Curah_Hujan_Total_mm'].mean():,.0f} mm</div>
                    <div class="card-desc-mini">Suhu rata-rata {df['Suhu_Rata2_C'].mean():.1f}°C & kelembapan {df['Kelembapan_Rata2_Persen'].mean():.1f}% dari 157 stasiun BMKG.</div>
                    <div class="card-footer-title">IKLIM 2023</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="story-card card-reef">
                <div class="card-tag">SENTRA RAWAN</div>
                <div>
                    <div class="card-stat">{top_prov['Total_LTS_11_OPT_Ha']:,.0f} Ha</div>
                    <div class="card-desc-mini">Provinsi dengan akumulasi serangan tertinggi dari total {df['Total_LTS_11_OPT_Ha'].sum():,.0f} Ha nasional.</div>
                    <div class="card-footer-title">{top_prov['Provinsi'].upper()}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Indikator halaman & grafik ringkas di bawah
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.5rem;">
        <div style="color:#FFFFFF; font-weight:700; font-size:0.85rem;">● 34 PROVINSI • 11 JENIS OPT • METODE OLS & K-MEANS</div>
        <div class="section-num">01</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    g_l, g_r = st.columns([1.2, 1])
    with g_l:
        top10 = df.sort_values("Total_LTS_11_OPT_Ha", ascending=False).head(10)
        fig_bar = px.bar(
            top10, x="Total_LTS_11_OPT_Ha", y="Provinsi", orientation="h",
            text_auto=",.0f", color="Total_LTS_11_OPT_Ha",
            color_continuous_scale=["#7CC0CE", "#1C7C91", "#124559"],
            title="Top 10 Provinsi dengan Luas Serangan OPT Tertinggi (Ha)"
        )
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(autorange="reversed", title=""), xaxis=dict(title="Luas (Ha)"),
            coloraxis_showscale=False, height=340, margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with g_r:
        opt_sum = df[opt_cols].sum().reset_index()
        opt_sum.columns = ["OPT", "Luas"]
        fig_pie = px.pie(
            opt_sum, names="OPT", values="Luas", hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Proporsi Jenis Serangan Nasional"
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            height=340, margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# HALAMAN 2: REGRESI IKLIM
# ==============================================================================
elif menu == "REGRESI IKLIM":
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div>
            <div class="kicker-text" style="margin-top:0.4rem;"> Pemodelan Regresi Linear Berganda (OLS)</div>
            <h1 class="display-hero" style="font-size:3.2rem; margin-bottom:0;">HUBUNGAN IKLIM & SERANGAN</h1>
        </div>
        <div class="section-num">02</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1.5, 1.1, 0.8])
    with c1:
        target_y = st.selectbox("Target Serangan (Y)", ["Total_LTS_11_OPT_Ha"] + opt_cols)
    with c2:
        pred_x = st.multiselect(
            "Variabel Iklim (X)",
            ["Curah_Hujan_Total_mm", "Suhu_Rata2_C", "Kelembapan_Rata2_Persen"],
            default=["Curah_Hujan_Total_mm", "Suhu_Rata2_C", "Kelembapan_Rata2_Persen"]
        )
    with c3:
        x_plot = st.selectbox("Variabel Sumbu X", pred_x if pred_x else ["Curah_Hujan_Total_mm"])
    with c4:
        st.write("")
        use_log = st.toggle("Log(Y+1)", value=False)

    if len(pred_x) == 0:
        st.warning("Pilih minimal 1 variabel iklim di atas ya!")
    else:
        y = np.log1p(df[target_y]) if use_log else df[target_y]
        X = sm.add_constant(df[pred_x])
        model = sm.OLS(y, X).fit()

        m1, m2, m3 = st.columns(3)
        m1.metric("R-Squared (R²)", f"{model.rsquared:.4f}")
        m2.metric("Adjusted R²", f"{model.rsquared_adj:.4f}")
        m3.metric("P-Value Simultan (F)", f"{model.f_pvalue:.4f}")

        if model.f_pvalue < 0.05:
            st.success(f" **Signifikan (p = {model.f_pvalue:.4f} < 0,05):** Unsur iklim menjelaskan **{model.rsquared*100:.2f}%** variasi `{target_y}`.")
        else:
            st.info(f" **Tidak signifikan secara simultan (p = {model.f_pvalue:.4f}):** Unsur iklim hanya menjelaskan **{model.rsquared*100:.2f}%** variasi `{target_y}` karena luas lahan tanam tiap provinsi berbeda jauh.")

        col_sc, col_tb = st.columns([1.2, 1], gap="large")
        with col_sc:
            df_p = df.copy()
            df_p["Y_Val"] = y
            y_lbl = f"Log({target_y}+1)" if use_log else f"{target_y} (Ha)"
            fig_reg = px.scatter(
                df_p, x=x_plot, y="Y_Val", hover_name="Provinsi", trendline="ols",
                color_discrete_sequence=["#1C7C91"], labels={"Y_Val": y_lbl},
                title=f"Sebaran {x_plot} vs {y_lbl}"
            )
            fig_reg.update_traces(marker=dict(size=10, color="#C85A32", line=dict(width=1.5, color="#FFFFFF")))
            fig_reg.update_layout(plot_bgcolor="rgba(255,255,255,0.5)", paper_bgcolor="rgba(0,0,0,0)", height=360)
            st.plotly_chart(fig_reg, use_container_width=True)

        with col_tb:
            st.markdown("##### Tabel Koefisien & Uji Parsial")
            coef_df = pd.DataFrame({
                "Variabel": model.params.index,
                "Koefisien": model.params.values,
                "t-Stat": model.tvalues.values,
                "P-Value": model.pvalues.values,
                "Status": ["Signifikan" if p < 0.05 else "Tidak" for p in model.pvalues.values]
            })
            st.dataframe(
                coef_df.style.format({"Koefisien": "{:.4f}", "t-Stat": "{:.3f}", "P-Value": "{:.4f}"}),
                use_container_width=True, hide_index=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# HALAMAN 3: KLUSTERING
# ==============================================================================
elif menu == "KLUSTERING":
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div>
            <div class="kicker-text" style="margin-top:0.4rem;"> Pengelompokan Wilayah (K-Means + PCA)</div>
            <h1 class="display-hero" style="font-size:3.2rem; margin-bottom:0;">KLASTER POLA SERANGAN PROVINSI</h1>
        </div>
        <div class="section-num">03</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[opt_cols])

    c_sl, c_mt = st.columns([2, 1])
    with c_sl:
        k_val = st.slider("Pilih Jumlah Klaster Provinsi (k):", 2, 6, 3)

    kmeans = KMeans(n_clusters=k_val, random_state=42, n_init=10)
    raw_lbl = kmeans.fit_predict(X_scaled)
    df_c = df.copy()
    df_c["raw"] = raw_lbl
    order_c = df_c.groupby("raw")["Total_LTS_11_OPT_Ha"].mean().sort_values(ascending=False).index.tolist()
    df_c["Klaster"] = df_c["raw"].map({old: f"Klaster {i+1}" for i, old in enumerate(order_c)})
    sil_val = silhouette_score(X_scaled, df_c["Klaster"])

    with c_mt:
        st.metric("Silhouette Score", f"{sil_val:.4f}", f"k = {k_val} Kelompok")

    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    df_c["PC1"], df_c["PC2"] = coords[:, 0], coords[:, 1]

    fig_pca = px.scatter(
        df_c.sort_values("Klaster"), x="PC1", y="PC2", color="Klaster",
        size="Total_LTS_11_OPT_Ha", size_max=34, text="Provinsi",
        color_discrete_sequence=["#C85A32", "#1C7C91", "#2A9D8F", "#E9C46A", "#6D597A"],
        hover_data=["Total_LTS_11_OPT_Ha", "Antraknose", "Virus Kuning"],
        title=f"Peta Sebaran Klaster 34 Provinsi (Varians Terjelaskan PCA: {pca.explained_variance_ratio_.sum()*100:.1f}%)"
    )
    fig_pca.update_traces(textposition="top center")
    fig_pca.update_layout(plot_bgcolor="rgba(255,255,255,0.5)", paper_bgcolor="rgba(0,0,0,0)", height=430)
    st.plotly_chart(fig_pca, use_container_width=True)

    t1, t2 = st.columns([1, 1.3], gap="large")
    with t1:
        st.markdown("##### Daftar Provinsi per Klaster")
        anggota = (
            df_c.sort_values(["Klaster", "Total_LTS_11_OPT_Ha"], ascending=[True, False])
            .groupby("Klaster")
            .agg(Jml=("Provinsi", "count"), Rata2_Ha=("Total_LTS_11_OPT_Ha", "mean"), Provinsi=("Provinsi", lambda x: ", ".join(x)))
            .reset_index()
        )
        anggota["Rata2_Ha"] = anggota["Rata2_Ha"].round(1)
        st.dataframe(anggota, use_container_width=True, hide_index=True)

    with t2:
        st.markdown("##### Rata-rata Luas Serangan Tiap Klaster (Ha)")
        profil = df_c.groupby("Klaster")[opt_cols + ["Total_LTS_11_OPT_Ha"]].mean().round(1)
        st.dataframe(profil, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# HALAMAN 4: DATA & KESIMPULAN
# ==============================================================================
else:
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
        <div>
            <div class="kicker-text" style="margin-top:0.4rem;">📑 Ringkasan Temuan & Dataset Master</div>
            <h1 class="display-hero" style="font-size:3.2rem; margin-bottom:0;">KESIMPULAN & DATA LENGKAP</h1>
        </div>
        <div class="section-num">04</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    s1, s2 = st.columns(2, gap="large")
    with s1:
        st.markdown("""
        ###  Kesimpulan Regresi Iklim vs OPT
        * **Agregat Nasional:** Curah hujan, suhu, dan kelembapan rata-rata tahunan memiliki korelasi linear yang rendah terhadap total luas serangan lintas provinsi karena perbedaan luas lahan tanam cabai tiap daerah.
        * **Spesifik Patogen:** Penyakit berbasis kelembapan tinggi (*Antraknose* dan *Layu Fusarium*) menunjukkan sensitivitas iklim lebih kuat dibanding hama vektor.
        """)
    with s2:
        st.markdown("""
        ###  Kesimpulan Klustering Provinsi
        * **Klaster 1 (Endemik Tinggi):** Sentra produksi utama seperti Sumatera Utara dan Jawa Tengah dengan serangan dominan pada *Antraknose*, *Virus Keriting*, dan *Virus Kuning*.
        * **Klaster 2 & 3 (Menengah & Rendah):** Kelompok provinsi dengan serangan spesifik (Jawa Barat, Gorontalo, NTB, Jawa Timur) serta kelompok provinsi dengan intensitas serangan rendah.
        """)
    st.divider()
    st.markdown("#####  Dataset Gabungan 34 Provinsi (Tahun 2023)")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)