import re
import random
import string
from datetime import datetime
from FSM import FSMachine, State

REGEX = {
    "nik": re.compile(r"^\d{16}$"),
    "hp": re.compile(r"^(08|628|\+628)\d{8,11}$"),
    "email": re.compile(r"^[\w.+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"),
    "tiket": re.compile(r"^(KTP|KK|AKTA|PINDAH|LPR)-\d{8}-\d{4}$"),
}

KEYWORDS: dict[str, list[str]] = {
    "salam": ["halo", "hai", "hi", "hey", "selamat pagi", "selamat siang", "selamat sore", "selamat malam", "assalamu", "assalamualaikum", "helo", "hola", "pagi", "siang", "sore", "malam"],
    "terima_kasih": ["terima kasih", "makasih", "thanks", "thank you", "tks", "tengkyu", "terimakasih", "trims", "thx"],
    "identitas_bot": ["siapa kamu", "kamu siapa", "bot apa ini", "tentang kamu", "sipa bot", "pembuatmu", "kamu robot"],
    "info_ktp": ["info ktp", "informasi ktp", "syarat ktp", "prosedur ktp", "cara buat ktp", "buat ktp", "ktp", "e-ktp", "e ktp", "kartu tanda penduduk"],
    "ajukan_ktp": ["daftar ktp", "pengajuan ktp", "ajukan ktp", "minta ktp", "buat ktp sekarang", "daftar sekarang ktp", "proses ktp"],
    "info_kk": ["info kk", "informasi kk", "syarat kk", "kartu keluarga", "cara buat kk", "buat kk", "prosedur kk"],
    "ajukan_kk": ["daftar kk", "pengajuan kk", "ajukan kk", "minta kk", "buat kk sekarang", "proses kk"],
    "info_akta": ["info akta", "akta kelahiran", "syarat akta", "cara buat akta", "buat akta", "prosedur akta", "akta lahir"],
    "ajukan_akta": ["daftar akta", "pengajuan akta", "ajukan akta", "buat akta sekarang", "proses akta"],
    "ajukan_pindah": ["pindah", "surat pindah", "domisili baru", "pindah domisili", "mutasi penduduk", "pengajuan pindah", "ajukan pindah"],
    "pengaduan": ["lapor", "pengaduan", "aduan", "complaint", "laporkan", "jalan rusak", "lampu mati", "sampah", "drainase", "banjir", "masalah", "keluhan", "mengadu"],
    "cek_status": ["cek status", "cek tiket", "status pengajuan", "status laporan", "lihat status", "periksa tiket", "nomor tiket", "sudah sampai mana", "lacak", "tracking", "pantau"],
    "faq": ["faq", "pertanyaan", "tanya", "jam buka", "jam pelayanan", "biaya", "gratis", "berapa lama", "syarat umum", "apa saja", "ketentuan", "persyaratan"],
    "konfirmasi_ya": ["ya", "iya", "yes", "benar", "betul", "setuju", "ok", "oke", "lanjut", "submit", "kirim", "konfirmasi", "yep", "yap"],
    "konfirmasi_tidak": ["tidak", "no", "batal", "cancel", "ulang", "salah", "ganti", "koreksi", "nope", "nggak", "enggak"],
    "bantuan": ["help", "bantuan", "bingung", "tidak mengerti", "tidak tau", "apa yang bisa", "menu", "bisa apa", "fitur"],
}

def _contains_keyword(text: str, keywords: list[str]) -> bool:
    t = text.lower()
    return any(kw in t for kw in keywords)

def detect_intent(text: str) -> str:
    cleaned = text.strip().upper()
    if REGEX["tiket"].match(cleaned):
        return "nomor_tiket"
    if _contains_keyword(text, KEYWORDS["cek_status"]):
        return "cek_status"
    if _contains_keyword(text, KEYWORDS["pengaduan"]):
        return "pengaduan"
    if _contains_keyword(text, KEYWORDS["ajukan_ktp"]):
        return "ajukan_ktp"
    if _contains_keyword(text, KEYWORDS["ajukan_kk"]):
        return "ajukan_kk"
    if _contains_keyword(text, KEYWORDS["ajukan_akta"]):
        return "ajukan_akta"
    if _contains_keyword(text, KEYWORDS["ajukan_pindah"]):
        return "ajukan_pindah"
    if _contains_keyword(text, KEYWORDS["info_ktp"]):
        return "info_ktp"
    if _contains_keyword(text, KEYWORDS["info_kk"]):
        return "info_kk"
    if _contains_keyword(text, KEYWORDS["info_akta"]):
        return "info_akta"
    if _contains_keyword(text, KEYWORDS["faq"]):
        return "faq"
    if _contains_keyword(text, KEYWORDS["bantuan"]):
        return "bantuan"
    if _contains_keyword(text, KEYWORDS["identitas_bot"]):
        return "identitas_bot"
    if _contains_keyword(text, KEYWORDS["salam"]):
        return "salam"
    if _contains_keyword(text, KEYWORDS["terima_kasih"]):
        return "terima_kasih"
    if _contains_keyword(text, KEYWORDS["konfirmasi_ya"]):
        return "konfirmasi_ya"
    if _contains_keyword(text, KEYWORDS["konfirmasi_tidak"]):
        return "konfirmasi_tidak"
    return "unknown"

def validate_input(field: str, value: str) -> tuple[bool, str]:
    v = value.strip()
    if field == "nik":
        if not REGEX["nik"].match(v):
            return False, "❌ NIK harus tepat **16 digit angka**. Contoh: `3374012501990001`"
        return True, ""
    elif field == "hp":
        if not REGEX["hp"].match(v):
            return False, "❌ Format nomor HP tidak valid. Gunakan format: `08xxxxxxxxxx` atau `628xxxxxxxxxx`"
        return True, ""
    elif field == "email":
        if not REGEX["email"].match(v):
            return False, "❌ Format email tidak valid. Contoh: `nama@email.com`"
        return True, ""
    elif field == "tiket":
        if not REGEX["tiket"].match(v.upper()):
            return False, "❌ Format nomor tiket tidak valid. Contoh: `KTP-20250601-1234`"
        return True, ""
    return True, ""

def generate_ticket(prefix: str) -> str:
    tanggal = datetime.now().strftime("%Y%m%d")
    suffix = "".join(random.choices(string.digits, k=4))
    return f"{prefix}-{tanggal}-{suffix}"

FAKE_TICKET_DB: dict[str, dict] = {}

def query_ticket_status(nomor: str) -> dict | None:
    return FAKE_TICKET_DB.get(nomor.upper())

def register_ticket(nomor: str, jenis: str, nama: str):
    FAKE_TICKET_DB[nomor] = {
        "jenis": jenis,
        "nama": nama,
        "status": "📋 Diterima — Menunggu verifikasi petugas",
        "tanggal": datetime.now().strftime("%d %B %Y, %H:%M"),
    }

def resp_sambutan() -> str:
    return (
        "👋 **Halo! Selamat datang di SIPA BOT**\n\n"
        "Saya siap membantu Anda mengurus berbagai layanan administrasi "
        "kependudukan secara digital. Berikut yang bisa saya bantu:\n\n"
        "📄 **Dokumen Kependudukan**\n"
        "• Informasi & pengajuan **KTP**\n"
        "• Informasi & pengajuan **Kartu Keluarga (KK)**\n"
        "• Informasi & pengajuan **Akta Kelahiran**\n"
        "• Pengajuan **Surat Pindah**\n\n"
        "📣 **Layanan Pengaduan**\n"
        "• Laporkan masalah infrastruktur & pelayanan publik\n\n"
        "🔍 **Lainnya**\n"
        "• Cek status pengajuan/laporan\n"
        "• FAQ layanan publik\n\n"
        "Silakan ceritakan kebutuhan Anda, misalnya:\n"
        "_\"Saya mau buat KTP\"_ atau _\"Mau lapor jalan rusak\"_"
    )

def resp_menu_utama() -> str:
    return (
        "Apakah ada layanan administrasi lain yang Anda butuhkan? 😊\n\n"
        "• **KTP / e-KTP** — info atau pengajuan\n"
        "• **Kartu Keluarga** — info atau pengajuan\n"
        "• **Akta Kelahiran** — info atau pengajuan\n"
        "• **Surat Pindah** — pengajuan\n"
        "• **Pengaduan** — lapor masalah di lingkungan Anda\n"
        "• **Cek Status** — pantau pengajuan atau laporan\n"
        "• **FAQ** — jam layanan, biaya, dan persyaratan\n\n"
        "Ketik apa yang ingin Anda lakukan!"
    )

def resp_identitas() -> str:
    return (
        "🤖 **Saya adalah SIPA BOT!**\n\n"
        "Asisten digital resmi untuk membantu masyarakat mengurus pelayanan administrasi "
        "secara cepat dan praktis di **Kantor Pusat - Pati**.\n\n"
        "Karena saya adalah sistem otomatis, saya difokuskan khusus untuk membantu permohonan "
        "dokumen kependudukan (KTP, KK, Akta, Surat Pindah) dan pelaporan pengaduan masyarakat.\n\n"
        "Ada layanan yang ingin Anda urus hari ini?"
    )

def resp_info_ktp() -> str:
    return (
        "📄 **Informasi Pembuatan KTP / e-KTP**\n\n"
        "**Syarat Dokumen:**\n"
        "• Surat pengantar dari RT/RW\n"
        "• Fotokopi Kartu Keluarga (KK)\n"
        "• Pas foto terbaru 3×4 (2 lembar)\n"
        "• Mengisi formulir F1.01\n\n"
        "**Prosedur:**\n"
        "1. Ambil surat pengantar dari RT/RW\n"
        "2. Datang ke Kantor Kelurahan\n"
        "3. Serahkan berkas ke petugas\n"
        "4. Lakukan perekaman biometrik (sidik jari, retina, tanda tangan)\n"
        "5. Tunggu proses cetak (1–14 hari kerja)\n\n"
        "**Biaya:** ✅ **GRATIS** (tidak dipungut biaya)\n"
        "**Jam Layanan:** Senin–Jumat, 08.00–15.00 WIB\n\n"
        "Mau langsung mengajukan KTP secara online? Ketik _\"daftar KTP\"_"
    )

def resp_info_kk() -> str:
    return (
        "📋 **Informasi Pembuatan Kartu Keluarga (KK)**\n\n"
        "**Syarat Dokumen:**\n"
        "• Surat pengantar dari RT/RW\n"
        "• KK lama (jika ada perubahan data)\n"
        "• Akta nikah/cerai (jika ada)\n"
        "• Akta kelahiran anak\n"
        "• Surat keterangan pindah (jika pindah dari luar daerah)\n\n"
        "**Prosedur:**\n"
        "1. Siapkan dokumen persyaratan\n"
        "2. Datang ke Kantor Kelurahan\n"
        "3. Isi formulir permohonan\n"
        "4. Proses di Dinas Kependudukan & Catatan Sipil\n"
        "5. KK baru selesai dalam 3–7 hari kerja\n\n"
        "**Biaya:** ✅ **GRATIS**\n"
        "**Jam Layanan:** Senin–Jumat, 08.00–15.00 WIB\n\n"
        "Mau ajukan KK? Ketik _\"daftar KK\"_"
    )

def resp_info_akta() -> str:
    return (
        "📜 **Informasi Pembuatan Akta Kelahiran**\n\n"
        "**Syarat Dokumen:**\n"
        "• Surat keterangan lahir dari rumah sakit/bidan/puskesmas\n"
        "• KTP kedua orang tua\n"
        "• Kartu Keluarga\n"
        "• Buku nikah/akta perkawinan orang tua\n"
        "• Formulir permohonan yang telah diisi\n\n"
        "**Prosedur:**\n"
        "1. Siapkan seluruh dokumen\n"
        "2. Datang ke Dinas Dukcapil setempat\n"
        "3. Serahkan berkas ke loket pelayanan\n"
        "4. Tunggu verifikasi (1–3 hari kerja)\n"
        "5. Ambil akta yang telah diterbitkan\n\n"
        "**Biaya:** ✅ **GRATIS**\n"
        "**Catatan:** Pengurusan anak usia < 60 hari tidak dikenakan denda\n\n"
        "Mau ajukan akta? Ketik _\"daftar akta\"_"
    )

def resp_faq() -> str:
    return (
        "❓ **FAQ — Pertanyaan Umum Layanan Publik**\n\n"
        "**🕐 Jam Pelayanan**\n"
        "Senin–Kamis : 08.00 – 15.00 WIB\n"
        "Jumat : 08.00 – 11.00 WIB\n"
        "Sabtu–Minggu : Tutup\n\n"
        "**💰 Biaya Layanan**\n"
        "Seluruh layanan administrasi kependudukan **GRATIS**\n"
        "Jika dimintai biaya, segera laporkan ke pengawas pelayanan!\n\n"
        "**⏱ Estimasi Waktu Proses**\n"
        "• KTP : 1–14 hari kerja\n"
        "• Kartu Keluarga : 3–7 hari kerja\n"
        "• Akta Kelahiran : 1–3 hari kerja\n"
        "• Surat Pindah : 1–3 hari kerja\n\n"
        "**📍 Lokasi Pelayanan**\n"
        "Kantor Kelurahan/Kecamatan setempat atau\n"
        "Dinas Kependudukan dan Catatan Sipil\n\n"
        "Ada pertanyaan lain? Silakan tanya saya 😊"
    )

def resp_bantuan() -> str:
    return (
        "🤔 Sepertinya Anda butuh panduan. Berikut yang bisa saya bantu:\n\n"
        "Cukup ketik secara natural, misalnya:\n"
        "• _\"Mau buat KTP\"_ → info & pengajuan KTP\n"
        "• _\"Daftar KK\"_ → pengajuan Kartu Keluarga\n"
        "• _\"Lapor jalan rusak\"_ → kirim pengaduan\n"
        "• _\"Cek tiket KTP-20250601-1234\"_ → pantau status\n"
        "• _\"FAQ\"_ → jam buka, biaya, dll\n\n"
        "Tidak perlu pilih nomor menu — cukup ceritakan kebutuhan administrasi Anda!"
    )

def resp_terima_kasih() -> str:
    pilihan = [
        "Sama-sama! Senang bisa membantu Anda 😊 Ada dokumen administrasi lain yang perlu diurus?",
        "Terima kasih kembali sudah menggunakan SIPA BOT! Ada lagi layanan publik yang ingin ditanyakan? 🙏",
        "Dengan senang hati! SIPA BOT siap membantu administrasi Anda kapan saja 😊",
    ]
    return random.choice(pilihan)

def resp_tidak_mengerti() -> str:
    return (
        "Mohon maaf, saya adalah bot pelayanan administrasi sehingga kurang mengerti pertanyaan atau topik tersebut. 😅\n\n"
        "Namun, saya **sangat ahli** dalam membantu Anda mengurus dokumen berikut:\n"
        "🔹 **KTP, Kartu Keluarga, Akta Kelahiran, dan Surat Pindah**\n"
        "🔹 **Laporan Pengaduan Masyarakat** (Jalan rusak, fasilitas umum, dll)\n\n"
        "Ketik **\"Menu\"** untuk melihat daftar layanan, atau beritahu saya dokumen apa yang ingin Anda urus hari ini!"
    )

class SIPABotEngine:
    def __init__(self):
        self.fsm = FSMachine()
        self.context: dict = {}
        self.pengaduan_type: str = ""

    def _reset_context(self):
        self.context = {}
        self.pengaduan_type = ""

    def _infer_pengaduan_type(self, text: str) -> str:
        t = text.lower()
        if any(k in t for k in ["jalan", "aspal", "lubang"]):
            return "Jalan Rusak"
        if any(k in t for k in ["lampu", "penerangan", "gelap"]):
            return "Lampu Jalan Mati"
        if any(k in t for k in ["sampah", "tumpukan", "bau"]):
            return "Sampah Menumpuk"
        if any(k in t for k in ["drainase", "selokan", "tersumbat", "banjir"]):
            return "Drainase Tersumbat"
        if any(k in t for k in ["pelayanan", "petugas", "lambat", "tidak ramah"]):
            return "Pelayanan Publik Buruk"
        return "Pengaduan Umum"

    def process(self, user_input: str) -> str:
        raw = user_input.strip()
        if not raw:
            return "Silakan ketik pesan Anda 😊"

        state = self.fsm.current_state
        intent = detect_intent(raw)

        if state == State.IDLE:
            self.fsm.transition("salam")
            return resp_sambutan()

        # Intersepsi Global (Bisa dipanggil dari mana saja)
        if intent == "terima_kasih":
            return resp_terima_kasih()
        if intent == "bantuan":
            return resp_bantuan()
        if intent == "identitas_bot":
            return resp_identitas()
        if intent == "salam" and state == State.MENU_UTAMA:
            return "Halo lagi! 😊 " + resp_menu_utama()

        if state == State.MENU_UTAMA:
            if intent == "info_ktp":
                self.fsm.transition("info_ktp")
                return resp_info_ktp()
            if intent == "ajukan_ktp":
                self._reset_context()
                self.fsm.force_state(State.KTP_NAMA)
                return "✍️ **Pengajuan KTP Baru**\n\nBaik! Mari kita mulai proses pengajuan KTP Anda.\n\nMohon masukkan **nama lengkap** sesuai akta kelahiran:"
            if intent == "info_kk":
                self.fsm.transition("info_kk")
                return resp_info_kk()
            if intent == "ajukan_kk":
                self._reset_context()
                self.fsm.force_state(State.KK_NAMA)
                return "✍️ **Pengajuan Kartu Keluarga**\n\nBaik! Saya akan memandu proses pengajuan KK.\n\nMohon masukkan **nama kepala keluarga**:"
            if intent == "info_akta":
                self.fsm.transition("info_akta")
                return resp_info_akta()
            if intent == "ajukan_akta":
                self._reset_context()
                self.fsm.force_state(State.AKTA_NAMA)
                return "✍️ **Pengajuan Akta Kelahiran**\n\nBaik! Mari lengkapi data untuk pengajuan akta.\n\nMohon masukkan **nama anak** (sesuai yang akan tertera di akta):"
            if intent == "ajukan_pindah":
                self._reset_context()
                self.fsm.force_state(State.PINDAH_NAMA)
                return "✍️ **Pengajuan Surat Pindah**\n\nBaik! Saya akan membantu proses surat pindah Anda.\n\nMohon masukkan **nama lengkap** pemohon:"
            if intent == "pengaduan":
                self._reset_context()
                self.fsm.transition("pengaduan")
                return (
                    "📣 **Layanan Pengaduan Masyarakat**\n\n"
                    "Kami siap menerima laporan Anda. Apa yang ingin dilaporkan?\n\n"
                    "• Jalan rusak\n• Lampu jalan mati\n• Sampah menumpuk\n"
                    "• Drainase tersumbat\n• Pelayanan publik buruk\n\n"
                    "Silakan ceritakan masalahnya:"
                )
            if intent == "cek_status":
                self.fsm.transition("cek_status")
                return (
                    "🔍 **Cek Status Pengajuan / Pengaduan**\n\n"
                    "Masukkan **nomor tiket** Anda:\n"
                    "_(Contoh: `KTP-20250601-1234`)_"
                )
            if intent == "faq":
                self.fsm.transition("faq")
                return resp_faq()
            
            # Jika state Menu Utama tapi input random
            return resp_tidak_mengerti()

        if state == State.INFO_KTP:
            if intent == "ajukan_ktp":
                self._reset_context()
                self.fsm.force_state(State.KTP_NAMA)
                return "✍️ **Pengajuan KTP**\n\nMohon masukkan **nama lengkap** sesuai akta kelahiran:"
            self.fsm.force_state(State.MENU_UTAMA)
            return resp_menu_utama()

        if state == State.INFO_KK:
            if intent == "ajukan_kk":
                self._reset_context()
                self.fsm.force_state(State.KK_NAMA)
                return "✍️ **Pengajuan KK**\n\nMohon masukkan **nama kepala keluarga**:"
            self.fsm.force_state(State.MENU_UTAMA)
            return resp_menu_utama()

        if state == State.INFO_AKTA:
            if intent == "ajukan_akta":
                self._reset_context()
                self.fsm.force_state(State.AKTA_NAMA)
                return "✍️ **Pengajuan Akta Kelahiran**\n\nMohon masukkan **nama anak**:"
            self.fsm.force_state(State.MENU_UTAMA)
            return resp_menu_utama()

        if state == State.FAQ:
            self.fsm.force_state(State.MENU_UTAMA)
            return resp_menu_utama()

        if state == State.KTP_NAMA:
            self.context["nama"] = raw.title()
            self.fsm.force_state(State.KTP_NIK)
            return f"✅ Nama tercatat: **{self.context['nama']}**\n\nSekarang masukkan **NIK** (16 digit angka):"

        if state == State.KTP_NIK:
            valid, pesan = validate_input("nik", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan NIK yang benar:"
            self.context["nik"] = raw.strip()
            self.fsm.force_state(State.KTP_ALAMAT)
            return f"✅ NIK tercatat: **{self.context['nik']}**\n\nMasukkan **alamat lengkap** (termasuk RT/RW, Kelurahan, Kecamatan):"

        if state == State.KTP_ALAMAT:
            self.context["alamat"] = raw
            self.fsm.force_state(State.KTP_HP)
            return f"✅ Alamat tercatat.\n\nMasukkan **nomor HP aktif** (contoh: `081234567890`):"

        if state == State.KTP_HP:
            valid, pesan = validate_input("hp", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan nomor HP yang benar:"
            self.context["hp"] = raw.strip()
            self.fsm.force_state(State.KTP_KONFIRMASI)
            return self._ringkasan_konfirmasi("KTP")

        if state == State.KTP_KONFIRMASI:
            if intent == "konfirmasi_ya":
                tiket = generate_ticket("KTP")
                register_ticket(tiket, "KTP", self.context.get("nama", "-"))
                self.fsm.force_state(State.MENU_UTAMA)
                return self._resp_selesai("KTP", tiket)
            else:
                self._reset_context()
                self.fsm.force_state(State.MENU_UTAMA)
                return "❌ Pengajuan dibatalkan.\n\n" + resp_menu_utama()

        if state == State.KK_NAMA:
            self.context["nama"] = raw.title()
            self.fsm.force_state(State.KK_NIK)
            return f"✅ Nama kepala keluarga: **{self.context['nama']}**\n\nMasukkan **NIK** kepala keluarga (16 digit):"

        if state == State.KK_NIK:
            valid, pesan = validate_input("nik", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan NIK yang benar:"
            self.context["nik"] = raw.strip()
            self.fsm.force_state(State.KK_ALAMAT)
            return f"✅ NIK tercatat.\n\nMasukkan **alamat lengkap** keluarga:"

        if state == State.KK_ALAMAT:
            self.context["alamat"] = raw
            self.fsm.force_state(State.KK_HP)
            return "✅ Alamat tercatat.\n\nMasukkan **nomor HP** yang bisa dihubungi:"

        if state == State.KK_HP:
            valid, pesan = validate_input("hp", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan nomor HP yang benar:"
            self.context["hp"] = raw.strip()
            self.fsm.force_state(State.KK_KONFIRMASI)
            return self._ringkasan_konfirmasi("KK")

        if state == State.KK_KONFIRMASI:
            if intent == "konfirmasi_ya":
                tiket = generate_ticket("KK")
                register_ticket(tiket, "KK", self.context.get("nama", "-"))
                self.fsm.force_state(State.MENU_UTAMA)
                return self._resp_selesai("KK", tiket)
            else:
                self._reset_context()
                self.fsm.force_state(State.MENU_UTAMA)
                return "❌ Pengajuan dibatalkan.\n\n" + resp_menu_utama()

        if state == State.AKTA_NAMA:
            self.context["nama"] = raw.title()
            self.fsm.force_state(State.AKTA_NIK)
            return f"✅ Nama anak: **{self.context['nama']}**\n\nMasukkan **NIK ayah** (16 digit):"

        if state == State.AKTA_NIK:
            valid, pesan = validate_input("nik", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan NIK yang benar:"
            self.context["nik"] = raw.strip()
            self.fsm.force_state(State.AKTA_ALAMAT)
            return "✅ NIK tercatat.\n\nMasukkan **alamat lengkap** orang tua:"

        if state == State.AKTA_ALAMAT:
            self.context["alamat"] = raw
            self.fsm.force_state(State.AKTA_HP)
            return "✅ Alamat tercatat.\n\nMasukkan **nomor HP** orang tua:"

        if state == State.AKTA_HP:
            valid, pesan = validate_input("hp", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan nomor HP yang benar:"
            self.context["hp"] = raw.strip()
            self.fsm.force_state(State.AKTA_KONFIRMASI)
            return self._ringkasan_konfirmasi("Akta Kelahiran")

        if state == State.AKTA_KONFIRMASI:
            if intent == "konfirmasi_ya":
                tiket = generate_ticket("AKTA")
                register_ticket(tiket, "Akta Kelahiran", self.context.get("nama", "-"))
                self.fsm.force_state(State.MENU_UTAMA)
                return self._resp_selesai("Akta Kelahiran", tiket)
            else:
                self._reset_context()
                self.fsm.force_state(State.MENU_UTAMA)
                return "❌ Pengajuan dibatalkan.\n\n" + resp_menu_utama()

        if state == State.PINDAH_NAMA:
            self.context["nama"] = raw.title()
            self.fsm.force_state(State.PINDAH_NIK)
            return f"✅ Nama: **{self.context['nama']}**\n\nMasukkan **NIK** (16 digit):"

        if state == State.PINDAH_NIK:
            valid, pesan = validate_input("nik", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan NIK yang benar:"
            self.context["nik"] = raw.strip()
            self.fsm.force_state(State.PINDAH_ALAMAT_ASAL)
            return "✅ NIK tercatat.\n\nMasukkan **alamat asal** (domisili saat ini):"

        if state == State.PINDAH_ALAMAT_ASAL:
            self.context["alamat_asal"] = raw
            self.fsm.force_state(State.PINDAH_ALAMAT_TUJUAN)
            return "✅ Alamat asal tercatat.\n\nMasukkan **alamat tujuan** (domisili baru):"

        if state == State.PINDAH_ALAMAT_TUJUAN:
            self.context["alamat_tujuan"] = raw
            self.fsm.force_state(State.PINDAH_HP)
            return "✅ Alamat tujuan tercatat.\n\nMasukkan **nomor HP** yang bisa dihubungi:"

        if state == State.PINDAH_HP:
            valid, pesan = validate_input("hp", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan nomor HP yang benar:"
            self.context["hp"] = raw.strip()
            self.fsm.force_state(State.PINDAH_KONFIRMASI)
            return self._ringkasan_pindah()

        if state == State.PINDAH_KONFIRMASI:
            if intent == "konfirmasi_ya":
                tiket = generate_ticket("PINDAH")
                register_ticket(tiket, "Surat Pindah", self.context.get("nama", "-"))
                self.fsm.force_state(State.MENU_UTAMA)
                return self._resp_selesai("Surat Pindah", tiket)
            else:
                self._reset_context()
                self.fsm.force_state(State.MENU_UTAMA)
                return "❌ Pengajuan dibatalkan.\n\n" + resp_menu_utama()

        if state == State.PENGADUAN:
            self.pengaduan_type = self._infer_pengaduan_type(raw)
            self.context["jenis"] = self.pengaduan_type
            self.context["deskripsi"] = raw
            self.fsm.force_state(State.PENGADUAN_DETAIL)
            return (
                f"📍 Jenis pengaduan terdeteksi: **{self.pengaduan_type}**\n\n"
                "Berikan informasi lebih lengkap:\n"
                "• Lokasi kejadian (nama jalan/kelurahan/kecamatan)\n"
                "• Kapan kejadian terjadi\n"
                "• Kondisi saat ini"
            )

        if state == State.PENGADUAN_DETAIL:
            self.context["detail"] = raw
            self.fsm.force_state(State.PENGADUAN_HP)
            return "✅ Detail laporan tercatat.\n\nMasukkan **nomor HP** Anda agar petugas dapat menghubungi:"

        if state == State.PENGADUAN_HP:
            valid, pesan = validate_input("hp", raw)
            if not valid:
                return pesan + "\n\nSilakan masukkan nomor HP yang benar:"
            self.context["hp"] = raw.strip()
            tiket = generate_ticket("LPR")
            register_ticket(tiket, self.context.get("jenis", "Pengaduan"), "Anonim")
            self.fsm.force_state(State.MENU_UTAMA)
            return (
                f"✅ **Laporan Berhasil Dikirim!**\n\n"
                f"📋 **Jenis:** {self.context.get('jenis', '-')}\n"
                f"🎫 **Nomor Laporan:** `{tiket}`\n\n"
                "Laporan Anda telah diterima dan akan ditindaklanjuti oleh petugas "
                "dalam **1×24 jam kerja**. Simpan nomor laporan untuk pengecekan status.\n\n"
                "Terima kasih telah membantu menjaga lingkungan kita! 🙏\n\n"
                + resp_menu_utama()
            )

        if state == State.CEK_STATUS:
            words = raw.upper().split()
            tiket_found = None
            for w in words:
                if REGEX["tiket"].match(w):
                    tiket_found = w
                    break
            if not tiket_found:
                if REGEX["tiket"].match(raw.upper().strip()):
                    tiket_found = raw.upper().strip()

            if not tiket_found:
                return (
                    "❌ Nomor tiket tidak ditemukan dalam pesan Anda.\n\n"
                    "Format tiket yang valid:\n"
                    "`KTP-YYYYMMDD-XXXX`\n`KK-YYYYMMDD-XXXX`\n"
                    "`AKTA-YYYYMMDD-XXXX`\n`PINDAH-YYYYMMDD-XXXX`\n`LPR-YYYYMMDD-XXXX`\n\n"
                    "Silakan masukkan nomor tiket yang benar:"
                )

            data = query_ticket_status(tiket_found)
            self.fsm.force_state(State.MENU_UTAMA)
            if data:
                return (
                    f"🔍 **Informasi Tiket `{tiket_found}`**\n\n"
                    f"📄 **Layanan:** {data['jenis']}\n"
                    f"👤 **Nama:** {data['nama']}\n"
                    f"📅 **Tanggal Pengajuan:** {data['tanggal']}\n"
                    f"📊 **Status:** {data['status']}\n\n"
                    "Ada yang bisa saya bantu lagi?\n" + resp_menu_utama()
                )
            else:
                return (
                    f"⚠️ Nomor tiket **`{tiket_found}`** tidak ditemukan.\n\n"
                    "Kemungkinan penyebab:\n"
                    "• Tiket dibuat di luar sesi ini\n"
                    "• Nomor tiket salah ketik\n\n"
                    "Coba periksa kembali atau hubungi kantor pelayanan setempat.\n\n"
                    + resp_menu_utama()
                )

        # Fallback Terakhir jika intent dikenali tapi salah tempat
        if intent == "info_ktp":
            self.fsm.force_state(State.INFO_KTP)
            return resp_info_ktp()
        if intent == "ajukan_ktp":
            self._reset_context()
            self.fsm.force_state(State.KTP_NAMA)
            return "✍️ **Pengajuan KTP**\n\nMohon masukkan **nama lengkap** sesuai akta:"
        if intent == "info_kk":
            self.fsm.force_state(State.INFO_KK)
            return resp_info_kk()
        if intent == "info_akta":
            self.fsm.force_state(State.INFO_AKTA)
            return resp_info_akta()
        if intent == "faq":
            self.fsm.force_state(State.FAQ)
            return resp_faq()
        if intent == "cek_status":
            self.fsm.force_state(State.CEK_STATUS)
            return "🔍 Masukkan **nomor tiket** Anda:"
        if intent == "pengaduan":
            self.fsm.force_state(State.PENGADUAN)
            return "📣 Ceritakan masalah yang ingin Anda laporkan:"

        return resp_tidak_mengerti()

    def _ringkasan_konfirmasi(self, jenis: str) -> str:
        return (
            f"📋 **Ringkasan Pengajuan {jenis}**\n\n"
            f"👤 **Nama:** {self.context.get('nama', '-')}\n"
            f"🪪 **NIK:** {self.context.get('nik', '-')}\n"
            f"🏠 **Alamat:** {self.context.get('alamat', '-')}\n"
            f"📱 **HP:** {self.context.get('hp', '-')}\n\n"
            "Apakah data di atas sudah benar?\n"
            "Ketik **\"ya\"** untuk konfirmasi atau **\"tidak\"** untuk membatalkan."
        )

    def _ringkasan_pindah(self) -> str:
        return (
            "📋 **Ringkasan Pengajuan Surat Pindah**\n\n"
            f"👤 **Nama:** {self.context.get('nama', '-')}\n"
            f"🪪 **NIK:** {self.context.get('nik', '-')}\n"
            f"🏠 **Alamat Asal:** {self.context.get('alamat_asal', '-')}\n"
            f"🏡 **Alamat Tujuan:** {self.context.get('alamat_tujuan', '-')}\n"
            f"📱 **HP:** {self.context.get('hp', '-')}\n\n"
            "Apakah data di atas sudah benar?\n"
            "Ketik **\"ya\"** untuk konfirmasi atau **\"tidak\"** untuk membatalkan."
        )

    def _resp_selesai(self, jenis: str, tiket: str) -> str:
        return (
            f"🎉 **Pengajuan {jenis} Berhasil Dikirim!**\n\n"
            f"🎫 **Nomor Tiket Anda:** `{tiket}`\n\n"
            "📌 **Langkah Selanjutnya:**\n"
            "1. Simpan nomor tiket untuk pengecekan status\n"
            "2. Siapkan dokumen fisik persyaratan\n"
            "3. Datang ke kantor pelayanan sesuai jadwal\n"
            "4. Proses akan diselesaikan dalam waktu kerja\n\n"
            "Anda bisa cek status kapan saja dengan ketik:\n"
            f"_\"cek tiket {tiket}\"_\n\n"
            "Terima kasih telah menggunakan layanan SIPA BOT! 🙏\n\n"
            + resp_menu_utama()
        )
