"""
FSM.py — Finite State Machine untuk SIPA BOT
=============================================
Mengimplementasikan konsep Teori Bahasa dan Otomata:
- State: representasi kondisi percakapan saat ini
- Transisi: perpindahan state berdasarkan input pengguna
- Alphabet: himpunan kata kunci / pola input yang valid

DIAGRAM STATE (Sederhana):
─────────────────────────────────────────────────────────────
IDLE ──► MENU_UTAMA ──► INFO_KTP
                    ──► AJUKAN_KTP ──► KTP_NAMA ──► KTP_NIK
                                    ──► KTP_ALAMAT ──► KTP_HP
                                    ──► KTP_KONFIRMASI ──► KTP_SELESAI
                    ──► INFO_KK
                    ──► AJUKAN_KK ──► (serupa alur KTP)
                    ──► INFO_AKTA
                    ──► AJUKAN_AKTA ──► (serupa alur KTP)
                    ──► AJUKAN_PINDAH ──► (serupa alur KTP)
                    ──► PENGADUAN ──► PENGADUAN_DETAIL ──► PENGADUAN_SELESAI
                    ──► CEK_STATUS ──► CEK_TIKET
                    ──► FAQ
─────────────────────────────────────────────────────────────
"""

from enum import Enum, auto


class State(Enum):
    """
    Himpunan State (Q) dalam FSM SIPA BOT.
    Setiap state merepresentasikan kondisi percakapan pada satu titik waktu.
    """
    # ── State Awal & Navigasi ──────────────────────────────
    IDLE            = auto()   # q0: State awal sebelum pengguna berinteraksi
    MENU_UTAMA      = auto()   # q1: Pengguna aktif, menunggu pilihan layanan

    # ── State Informasi ────────────────────────────────────
    INFO_KTP        = auto()   # q2: Menampilkan info syarat/prosedur KTP
    INFO_KK         = auto()   # q3: Menampilkan info syarat/prosedur KK
    INFO_AKTA       = auto()   # q4: Menampilkan info syarat/prosedur Akta
    FAQ             = auto()   # q5: Menampilkan FAQ layanan

    # ── State Pengajuan KTP ────────────────────────────────
    AJUKAN_KTP      = auto()   # q6:  Mulai alur pengajuan KTP
    KTP_NAMA        = auto()   # q7:  Menunggu input nama lengkap
    KTP_NIK         = auto()   # q8:  Menunggu input NIK (16 digit)
    KTP_ALAMAT      = auto()   # q9:  Menunggu input alamat
    KTP_HP          = auto()   # q10: Menunggu input nomor HP
    KTP_KONFIRMASI  = auto()   # q11: Menampilkan ringkasan, menunggu konfirmasi
    KTP_SELESAI     = auto()   # q12: Tiket berhasil dibuat, sesi selesai

    # ── State Pengajuan KK ─────────────────────────────────
    AJUKAN_KK       = auto()   # q13: Mulai alur pengajuan KK
    KK_NAMA         = auto()   # q14
    KK_NIK          = auto()   # q15
    KK_ALAMAT       = auto()   # q16
    KK_HP           = auto()   # q17
    KK_KONFIRMASI   = auto()   # q18
    KK_SELESAI      = auto()   # q19

    # ── State Pengajuan Akta Kelahiran ─────────────────────
    AJUKAN_AKTA     = auto()   # q20
    AKTA_NAMA       = auto()   # q21
    AKTA_NIK        = auto()   # q22
    AKTA_ALAMAT     = auto()   # q23
    AKTA_HP         = auto()   # q24
    AKTA_KONFIRMASI = auto()   # q25
    AKTA_SELESAI    = auto()   # q26

    # ── State Pengajuan Surat Pindah ───────────────────────
    AJUKAN_PINDAH       = auto()   # q27
    PINDAH_NAMA         = auto()   # q28
    PINDAH_NIK          = auto()   # q29
    PINDAH_ALAMAT_ASAL  = auto()   # q30
    PINDAH_ALAMAT_TUJUAN = auto()  # q31
    PINDAH_HP           = auto()   # q32
    PINDAH_KONFIRMASI   = auto()   # q33
    PINDAH_SELESAI      = auto()   # q34

    # ── State Pengaduan ────────────────────────────────────
    PENGADUAN        = auto()  # q35: Menunggu jenis pengaduan
    PENGADUAN_DETAIL = auto()  # q36: Menunggu detail/lokasi pengaduan
    PENGADUAN_HP     = auto()  # q37: Menunggu nomor HP pelapor
    PENGADUAN_SELESAI = auto() # q38: Laporan berhasil dibuat

    # ── State Cek Status ───────────────────────────────────
    CEK_STATUS  = auto()  # q39: Menunggu input nomor tiket
    CEK_TIKET   = auto()  # q40: Menampilkan status tiket


# ─────────────────────────────────────────────────────────────────────────────
# Tabel Transisi (δ: Q × Σ → Q)
# Mendefinisikan perpindahan state berdasarkan aksi input
# ─────────────────────────────────────────────────────────────────────────────
TRANSITION_TABLE: dict[State, dict[str, State]] = {
    State.IDLE: {
        "salam":    State.MENU_UTAMA,
        "apa_saja": State.MENU_UTAMA,
    },
    State.MENU_UTAMA: {
        "info_ktp":     State.INFO_KTP,
        "ajukan_ktp":   State.AJUKAN_KTP,
        "info_kk":      State.INFO_KK,
        "ajukan_kk":    State.AJUKAN_KK,
        "info_akta":    State.INFO_AKTA,
        "ajukan_akta":  State.AJUKAN_AKTA,
        "ajukan_pindah":State.AJUKAN_PINDAH,
        "pengaduan":    State.PENGADUAN,
        "cek_status":   State.CEK_STATUS,
        "faq":          State.FAQ,
        "apa_saja":     State.MENU_UTAMA,
    },
    # KTP flow
    State.INFO_KTP:       {"lanjut": State.MENU_UTAMA, "ajukan_ktp": State.AJUKAN_KTP, "apa_saja": State.MENU_UTAMA},
    State.AJUKAN_KTP:     {"lanjut": State.KTP_NAMA},
    State.KTP_NAMA:       {"input":  State.KTP_NIK},
    State.KTP_NIK:        {"input":  State.KTP_ALAMAT},
    State.KTP_ALAMAT:     {"input":  State.KTP_HP},
    State.KTP_HP:         {"input":  State.KTP_KONFIRMASI},
    State.KTP_KONFIRMASI: {"ya": State.KTP_SELESAI, "tidak": State.MENU_UTAMA},
    State.KTP_SELESAI:    {"apa_saja": State.MENU_UTAMA},
    # KK flow
    State.INFO_KK:        {"lanjut": State.MENU_UTAMA, "ajukan_kk": State.AJUKAN_KK, "apa_saja": State.MENU_UTAMA},
    State.AJUKAN_KK:      {"lanjut": State.KK_NAMA},
    State.KK_NAMA:        {"input":  State.KK_NIK},
    State.KK_NIK:         {"input":  State.KK_ALAMAT},
    State.KK_ALAMAT:      {"input":  State.KK_HP},
    State.KK_HP:          {"input":  State.KK_KONFIRMASI},
    State.KK_KONFIRMASI:  {"ya": State.KK_SELESAI, "tidak": State.MENU_UTAMA},
    State.KK_SELESAI:     {"apa_saja": State.MENU_UTAMA},
    # Akta flow
    State.INFO_AKTA:        {"lanjut": State.MENU_UTAMA, "ajukan_akta": State.AJUKAN_AKTA, "apa_saja": State.MENU_UTAMA},
    State.AJUKAN_AKTA:      {"lanjut": State.AKTA_NAMA},
    State.AKTA_NAMA:        {"input":  State.AKTA_NIK},
    State.AKTA_NIK:         {"input":  State.AKTA_ALAMAT},
    State.AKTA_ALAMAT:      {"input":  State.AKTA_HP},
    State.AKTA_HP:          {"input":  State.AKTA_KONFIRMASI},
    State.AKTA_KONFIRMASI:  {"ya": State.AKTA_SELESAI, "tidak": State.MENU_UTAMA},
    State.AKTA_SELESAI:     {"apa_saja": State.MENU_UTAMA},
    # Pindah flow
    State.AJUKAN_PINDAH:        {"lanjut": State.PINDAH_NAMA},
    State.PINDAH_NAMA:          {"input":  State.PINDAH_NIK},
    State.PINDAH_NIK:           {"input":  State.PINDAH_ALAMAT_ASAL},
    State.PINDAH_ALAMAT_ASAL:   {"input":  State.PINDAH_ALAMAT_TUJUAN},
    State.PINDAH_ALAMAT_TUJUAN: {"input":  State.PINDAH_HP},
    State.PINDAH_HP:            {"input":  State.PINDAH_KONFIRMASI},
    State.PINDAH_KONFIRMASI:    {"ya": State.PINDAH_SELESAI, "tidak": State.MENU_UTAMA},
    State.PINDAH_SELESAI:       {"apa_saja": State.MENU_UTAMA},
    # Pengaduan flow
    State.PENGADUAN:         {"input":  State.PENGADUAN_DETAIL},
    State.PENGADUAN_DETAIL:  {"input":  State.PENGADUAN_HP},
    State.PENGADUAN_HP:      {"input":  State.PENGADUAN_SELESAI},
    State.PENGADUAN_SELESAI: {"apa_saja": State.MENU_UTAMA},
    # Cek status
    State.CEK_STATUS: {"input": State.CEK_TIKET},
    State.CEK_TIKET:  {"apa_saja": State.MENU_UTAMA},
    # FAQ
    State.FAQ: {"apa_saja": State.MENU_UTAMA},
}


class FSMachine:
    """
    Mesin Finite State Machine (FSM) untuk SIPA BOT.

    Implementasi formal:
        M = (Q, Σ, δ, q0, F)
        Q = himpunan state (State enum)
        Σ = himpunan aksi/simbol transisi (string)
        δ = fungsi transisi (TRANSITION_TABLE)
        q0 = State.IDLE (state awal)
        F = {} (tidak ada state akhir tetap; percakapan bisa berlanjut)
    """

    def __init__(self):
        self.current_state: State = State.IDLE
        self.previous_state: State = State.IDLE

    def transition(self, action: str) -> bool:
        """
        Fungsi transisi δ(q, a) → q'.
        Berpindah dari state saat ini ke state baru berdasarkan aksi.

        Parameter:
            action (str): simbol dari alphabet Σ

        Return:
            bool: True jika transisi berhasil, False jika tidak ada transisi
        """
        transitions = TRANSITION_TABLE.get(self.current_state, {})
        next_state = transitions.get(action) or transitions.get("apa_saja")

        if next_state:
            self.previous_state = self.current_state
            self.current_state = next_state
            return True
        return False

    def force_state(self, state: State):
        """Paksa perpindahan ke state tertentu (digunakan untuk reset)."""
        self.previous_state = self.current_state
        self.current_state = state

    def reset(self):
        """Reset ke state awal q0 = IDLE."""
        self.current_state = State.IDLE
        self.previous_state = State.IDLE

    def get_state_name(self) -> str:
        return self.current_state.name