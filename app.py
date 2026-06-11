import streamlit as st
from datetime import datetime
from engine import SIPABotEngine

st.set_page_config(
    page_title="SIPA BOT",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a1628;
    color: #e8edf5;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stHeaderActionElements"] { display: none !important; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a1628; }
::-webkit-scrollbar-thumb { background: #c9aa71; border-radius: 3px; }

.hero-section {
    background: linear-gradient(135deg, #0a1628 0%, #0f2347 40%, #1a3a6b 100%);
    border-radius: 24px;
    padding: 5rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(201,170,113,0.2);
    margin-bottom: 2rem;
}
.hero-section::before {
    content: '';
    position: absolute;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(201,170,113,0.08) 0%, transparent 70%);
    top: -200px; left: 50%; transform: translateX(-50%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(201,170,113,0.15);
    border: 1px solid rgba(201,170,113,0.4);
    color: #c9aa71;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.4rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.5rem;
}
.hero-logo { font-size: 4rem; margin-bottom: 1rem; display: block; }
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #c9aa71; }
.hero-subtitle-tag {
    font-size: 0.9rem;
    color: #c9aa71;
    font-weight: 500;
    letter-spacing: 0.05em;
    margin-bottom: 1.2rem;
}
.hero-desc {
    font-size: 1.1rem;
    line-height: 1.7;
    color: #a0b0cc;
    max-width: 600px;
    margin: 0 auto 2.5rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
    margin: 2rem 0;
}
.stat-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(201,170,113,0.15);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
}
.stat-card:hover { transform: translateY(-3px); border-color: rgba(201,170,113,0.4); }
.stat-number { font-size: 2rem; font-weight: 800; color: #c9aa71; line-height: 1; margin-bottom: 0.4rem; }
.stat-label { font-size: 0.78rem; color: #7a90b0; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; }

.section-title { font-family: 'Playfair Display', serif; font-size: 2rem; color: #ffffff; text-align: center; margin-bottom: 0.5rem; }
.section-title span { color: #c9aa71; }
.section-sub { text-align: center; color: #7a90b0; font-size: 0.95rem; margin-bottom: 2rem; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 2rem; }
.feature-card {
    background: linear-gradient(135deg, rgba(15,35,71,0.8) 0%, rgba(10,22,40,0.9) 100%);
    border: 1px solid rgba(201,170,113,0.12);
    border-radius: 16px; padding: 1.75rem 1.5rem;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
}
.feature-card:hover { transform: translateY(-4px); border-color: rgba(201,170,113,0.35); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
.feature-icon { font-size: 2rem; margin-bottom: 0.75rem; display: block; }
.feature-title { font-size: 1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.85rem; color: #7a90b0; line-height: 1.5; }

.tbo-section {
    background: linear-gradient(135deg, rgba(201,170,113,0.08) 0%, rgba(201,170,113,0.03) 100%);
    border: 1px solid rgba(201,170,113,0.2);
    border-radius: 16px; padding: 2rem; margin: 1.5rem 0;
}
.tbo-title { font-size: 1.1rem; font-weight: 700; color: #c9aa71; margin-bottom: 1rem; }
.tbo-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.tbo-item { background: rgba(255,255,255,0.03); border-radius: 10px; padding: 1rem; }
.tbo-item-title { font-size: 0.8rem; font-weight: 700; color: #c9aa71; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.tbo-item-desc { font-size: 0.8rem; color: #7a90b0; line-height: 1.5; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f3c 0%, #0a1628 100%);
    border-right: 1px solid rgba(201,170,113,0.15);
}
.sidebar-logo { text-align: center; padding: 1rem 0 0.5rem; }
.sidebar-logo span { font-size: 3rem; }
.sidebar-logo h2 { font-family: 'Playfair Display', serif; color: #c9aa71; font-size: 1.4rem; margin-top: 0.3rem; }
.sidebar-logo p { color: #7a90b0; font-size: 0.8rem; }
.sidebar-divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(201,170,113,0.3), transparent); margin: 1rem 0; }
.sidebar-section-title { font-size: 0.7rem; font-weight: 700; color: #c9aa71; text-transform: uppercase; letter-spacing: 0.1em; margin: 1rem 0 0.5rem; padding: 0 0.5rem; }
.sidebar-item { background: rgba(255,255,255,0.03); border: 1px solid rgba(201,170,113,0.08); border-radius: 10px; padding: 0.6rem 0.8rem; margin-bottom: 0.4rem; font-size: 0.8rem; color: #a0b0cc; }
.sidebar-item strong { color: #c9aa71; }
.state-badge { display: inline-block; background: rgba(201,170,113,0.15); border: 1px solid rgba(201,170,113,0.3); color: #c9aa71; font-size: 0.7rem; font-weight: 600; padding: 0.15rem 0.5rem; border-radius: 6px; font-family: monospace; margin-top: 0.2rem; }

.stChatMessage { max-width: 850px; margin: auto; }
.block-container { max-width: 1000px !important; padding-top: 2rem; padding-bottom: 140px; }

[data-testid="stChatInput"] { max-width: 850px !important; margin: 0 auto !important; padding-bottom: 2px !important; }
[data-testid="stChatInput"] > div { border-radius: 18px !important; border: 1px solid rgba(201,170,113,0.3) !important; background: #0f172a !important; box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important; }
[data-testid="stChatInput"] textarea { color: white !important; }
[data-testid="stChatInput"]::after { content: "SIPA BOT memproses bahasa menggunakan FSM & Regex. Harap periksa kembali keakuratan informasi."; display: block; text-align: center; color: #4a6080; font-size: 0.72rem; margin-top: 8px; margin-bottom: 4px; font-weight: 500; letter-spacing: 0.02em; }
div[data-testid="stChatInputContainer"] { background: transparent !important; }

.stButton > button { background: linear-gradient(135deg, #c9aa71, #b8944f) !important; color: #0a1628 !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 0.85rem !important; padding: 0.55rem 1.4rem !important; transition: all 0.2s !important; font-family: 'Inter', sans-serif !important; }
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(201,170,113,0.35) !important; }
</style>
""", unsafe_allow_html=True)


def init_session():
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "bot" not in st.session_state:
        st.session_state.bot = SIPABotEngine()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now().strftime("%d %b %Y, %H:%M")


init_session()

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span>🏛️</span>
        <h2>SIPA BOT</h2>
        <p>Sistem Informasi Pelayanan Administrasi</p>
    </div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    if st.session_state.page == "chat":
        state_name = st.session_state.bot.fsm.get_state_name()
        st.markdown(f"""
        <div class="sidebar-section-title">Status FSM</div>
        <div class="sidebar-item">State Aktif<br><span class="state-badge">{state_name}</span></div>
        """, unsafe_allow_html=True)

        total_msg = len(st.session_state.messages)
        user_msg = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.markdown(f"""
        <div class="sidebar-section-title">Sesi Ini</div>
        <div class="sidebar-item">Mulai: <strong>{st.session_state.session_start}</strong></div>
        <div class="sidebar-item">Total pesan: <strong>{total_msg}</strong></div>
        <div class="sidebar-item">Pesan Anda: <strong>{user_msg}</strong></div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-section-title">Layanan Tersedia</div>
    <div class="sidebar-item">KTP / e-KTP</div>
    <div class="sidebar-item">Kartu Keluarga (KK)</div>
    <div class="sidebar-item">Akta Kelahiran</div>
    <div class="sidebar-item">Surat Pindah</div>
    <div class="sidebar-item">Pengaduan Masyarakat</div>
    <div class="sidebar-item">Cek Status Layanan</div>
    <div class="sidebar-item">FAQ & Informasi</div>
    <div class="sidebar-divider"></div>
    <div class="sidebar-section-title">Teknologi TBO</div>
    <div class="sidebar-item"><strong>FSM</strong> — 40 State</div>
    <div class="sidebar-item"><strong>Regex</strong> — NIK, HP, Tiket</div>
    <div class="sidebar-item"><strong>Keyword Matching</strong></div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    if st.session_state.page == "chat":
        if st.button("Kembali ke Beranda", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
        if st.button("Reset Percakapan", use_container_width=True):
            st.session_state.bot = SIPABotEngine()
            st.session_state.messages = []
            st.session_state.session_start = datetime.now().strftime("%d %b %Y, %H:%M")
            st.rerun()
    else:
        if st.button("Mulai Chat Sekarang", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; margin-top:2rem; color:#4a6080; font-size:0.72rem;">
        SIPA BOT v1.0<br>Powered by FSM + Regex
    </div>
    """, unsafe_allow_html=True)


def render_landing():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">Layanan Publik Digital</div>
        <span class="hero-logo">🤖</span>
        <h1 class="hero-title">SIPA <span>BOT</span></h1>
        <p class="hero-subtitle-tag">Sistem Informasi Pelayanan Administrasi</p>
        <p class="hero-desc">
            Asisten digital cerdas untuk membantu masyarakat mengurus dokumen kependudukan, mengajukan layanan administrasi, menyampaikan pengaduan, dan memantau status layanan — kapan saja, di mana saja.
        </p>
        <div class="stats-grid">
            <div class="stat-card"><div class="stat-number">7+</div><div class="stat-label">Jenis Layanan</div></div>
            <div class="stat-card"><div class="stat-number">40</div><div class="stat-label">State FSM</div></div>
            <div class="stat-card"><div class="stat-number">4</div><div class="stat-label">Pola Regex</div></div>
            <div class="stat-card"><div class="stat-number">24/7</div><div class="stat-label">Siap Melayani</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([2, 1.5, 2])
    with col_c:
        if st.button("Mulai Percakapan", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h2 class="section-title">Fitur <span>Layanan</span></h2>
    <p class="section-sub">Semua kebutuhan administrasi kependudukan dalam satu platform</p>
    <div class="features-grid">
        <div class="feature-card"><span class="feature-icon">📄</span><div class="feature-title">Informasi & Pengajuan KTP</div><div class="feature-desc">Dapatkan info syarat, prosedur, dan ajukan permohonan KTP/e-KTP secara digital.</div></div>
        <div class="feature-card"><span class="feature-icon">📋</span><div class="feature-title">Kartu Keluarga (KK)</div><div class="feature-desc">Informasi lengkap dan simulasi pengajuan Kartu Keluarga baru atau perubahan data.</div></div>
        <div class="feature-card"><span class="feature-icon">📜</span><div class="feature-title">Akta Kelahiran</div><div class="feature-desc">Panduan dan pengajuan akta kelahiran untuk anak baru lahir hingga dewasa.</div></div>
        <div class="feature-card"><span class="feature-icon">📦</span><div class="feature-title">Surat Pindah Domisili</div><div class="feature-desc">Proses pengajuan surat pindah antar kelurahan, kecamatan, atau kota/kabupaten.</div></div>
        <div class="feature-card"><span class="feature-icon">📣</span><div class="feature-title">Pengaduan Masyarakat</div><div class="feature-desc">Laporkan jalan rusak, lampu mati, sampah menumpuk, drainase, atau masalah pelayanan.</div></div>
        <div class="feature-card"><span class="feature-icon">🔍</span><div class="feature-title">Pantau Status Layanan</div><div class="feature-desc">Cek status pengajuan dan laporan pengaduan secara real-time dengan nomor tiket.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tbo-section">
        <div class="tbo-title">Implementasi Teori Bahasa & Otomata (TBO)</div>
        <div class="tbo-grid">
            <div class="tbo-item"><div class="tbo-item-title">Finite State Machine</div><div class="tbo-item-desc">M = (Q, Σ, δ, q0, F)<br>40 state aktif yang mengatur seluruh alur percakapan. Setiap layanan memiliki state dan transisi yang terdefinisi jelas.</div></div>
            <div class="tbo-item"><div class="tbo-item-title">Regular Expression</div><div class="tbo-item-desc">Validasi input menggunakan pola regex:<br>NIK: ^\d{16}$<br>HP: ^(08|628|\+628)\d{8,11}$<br>Tiket: PREFIX-YYYYMMDD-XXXX</div></div>
            <div class="tbo-item"><div class="tbo-item-title">Keyword Matching</div><div class="tbo-item-desc">Pencocokan kata kunci (Alphabet Σ) untuk mendeteksi intent pengguna secara natural.</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def add_message(role: str, content: str):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "time": datetime.now().strftime("%H:%M"),
    })


def render_chat():
    if not st.session_state.messages:
        welcome = st.session_state.bot.process("halo")
        add_message("bot", welcome)

    for msg in st.session_state.messages:
        role = "assistant" if msg["role"] == "bot" else "user"
        with st.chat_message(role):
            st.markdown(msg["content"])

    quick_prompt = None
    if len(st.session_state.messages) == 1:
        _, col_center, _ = st.columns([1, 8, 1]) 
        
        with col_center:
            st.markdown("<div style='text-align: center; color: #7a90b0; font-size: 0.95rem; margin: 3rem 0 1.5rem;'><strong>Saran Topik Pembicaraan</strong></div>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            if c1.button("Syarat KTP Baru", use_container_width=True):
                quick_prompt = "Apa saja syarat membuat KTP baru?"
            if c2.button("Akta Kelahiran", use_container_width=True):
                quick_prompt = "Syarat membuat akta kelahiran"
            if c3.button("Buat Pengaduan", use_container_width=True):
                quick_prompt = "Saya ingin mengajukan pengaduan"

    prompt = st.chat_input("Ketik pesan Anda...")
    final_prompt = prompt or quick_prompt

    if final_prompt:
        add_message("user", final_prompt)
        response = st.session_state.bot.process(final_prompt)
        add_message("bot", response)
        st.rerun()


if st.session_state.page == "landing":
    render_landing()
else:
    render_chat()
