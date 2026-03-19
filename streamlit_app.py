import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Konfigurasi Halaman & Tema Custom
st.set_page_config(page_title="Research DPL", layout="wide", page_icon="🎓")

# Menambahkan CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #1f4e79;
        color: white;
    }
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Nama database
CHAT_FILE = "chat_gita_dpl.csv"
LINK_FILE = "links_gita_dpl.csv"

def load_data(file, cols):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=cols)

def save_data(file, data_dict):
    df = pd.DataFrame([data_dict])
    df.to_csv(file, mode='a', index=False, header=not os.path.exists(file))

# --- SIDEBAR: PROGRESS & INFO ---
with st.sidebar:
    st.image("https://id.images.search.yahoo.com/search/images;_ylt=Awr1QU0ZsrppXAIAWu7LQwx.;_ylu=Y29sbwNzZzMEcG9zAzEEdnRpZAMEc2VjA3Nj?type=E211ID885G0&p=logo+unimed&fr=mcafee&th=355&tw=474&imgurl=https%3A%2F%2Fcdn.kibrispdr.org%2Fdata%2F432%2Fgambar-logo-unimed-1.png&rurl=https%3A%2F%2Fwww.kibrispdr.org%2Fgambar-logo-unimed.html&size=282KB&name=Gambar+Logo+Unimed+-+57%2B+Koleksi+Gambar&oid=1&h=1200&w=1600&turl=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.tf36WEYtOZjkOoybFCVZ-QHaFj%3Fpid%3DApi&tt=Gambar+Logo+Unimed+-+57%2B+Koleksi+Gambar&sigr=T6hN6_8yrZH_&sigit=BxYLUGdMGKpw&sigi=8n9KEjyNlpvm&sign=8CP0aHgbGVXR&sigt=8CP0aHgbGVXR.png", width=100)
    st.title("🎓 Profil Peneliti")
    st.markdown("**Gita - PPKn Unimed**")
    st.divider()
    
    st.subheader("📈 Progres Penelitian")
    steps = ["Penyusunan Judul", "Observasi PLP", "Instrumen", "Analisis Data", "Laporan Akhir"]
    if "done_steps" not in st.session_state: st.session_state.done_steps = steps[:1]
    
    sel_steps = st.multiselect("Capaian:", steps, default=st.session_state.done_steps)
    st.session_state.done_steps = sel_steps
    
    prog = len(sel_steps) * 20
    st.write(f"Capaian: {prog}%")
    st.progress(prog)
    
    st.divider()
    if st.button("🗑️ Reset Room"):
        for f in [CHAT_FILE, LINK_FILE]:
            if os.path.exists(f): os.remove(f)
        st.rerun()

# --- MAIN AREA ---
# Ucapan Selamat Datang yang Estetik
st.markdown(f"""
    <div style="background-color:#1f4e79; padding:25px; border-radius:15px; text-align:center; color:white; margin-bottom:25px;">
        <h1 style="margin:0;">Selamat Datang di Room DPLResearch, Ibu DPL! 👋</h1>
        <p style="font-size:1.1rem; opacity:0.9;">Saya Harap ini dapat Monitoring Penelitian Kita Ibu</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["💬 Ruang Diskusi", "📁 Berkas & Referensi"])

with tab1:
    st.subheader("🗨️ Log Bimbingan")
    
    # Pilih Role (Biar Ibu DPL gampang pilih)
    role = st.toggle("Gunakan mode Ibu DPL", value=False)
    current_user = "Ibu DPL" if role else "Gita (Mahasiswa)"
    
    # Tampilkan Riwayat
    history = load_data(CHAT_FILE, ["Waktu", "User", "Pesan"])
    for _, row in history.iterrows():
        is_dpl = row['User'] == "Ibu DPL"
        with st.chat_message("assistant" if is_dpl else "user", avatar="👩‍🏫" if is_dpl else "🎓"):
            st.write(f"**{row['User']}** • <small>{row['Waktu']}</small>", unsafe_allow_html=True)
            st.write(row['Pesan'])

    # Chat Input
    if prompt := st.chat_input("Tulis pesan atau arahan di sini..."):
        save_data(CHAT_FILE, {
            "Waktu": datetime.now().strftime("%H:%M"),
            "User": current_user,
            "Pesan": prompt
        })
        st.rerun()

with tab2:
    st.subheader("📂 Folder Penelitian")
    col_a, col_b = st.columns(2)
    
    with col_a:
        with st.form("link_form", clear_on_submit=True):
            st.write("**Tambah Berkas Baru**")
            n = st.text_input("Nama Dokumen (misal: Draft Bab II)")
            u = st.text_input("Link Google Drive")
            if st.form_submit_button("Simpan Berkas"):
                if n and u:
                    save_data(LINK_FILE, {"Nama": n, "URL": u})
                    st.toast("Berkas tersimpan!", icon="💾")
                    st.rerun()

    with col_b:
        st.write("**Daftar Berkas Terunggah:**")
        links = load_data(LINK_FILE, ["Nama", "URL"])
        for _, r in links.iterrows():
            st.markdown(f"🔗 [{r['Nama']}]({r['URL']})")
