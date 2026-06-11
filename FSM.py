from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    MENU_UTAMA = auto()
    INFO_KTP = auto()
    INFO_KK = auto()
    INFO_AKTA = auto()
    FAQ = auto()
    
    AJUKAN_KTP = auto()
    KTP_NAMA = auto()
    KTP_NIK = auto()
    KTP_ALAMAT = auto()
    KTP_HP = auto()
    KTP_KONFIRMASI = auto()
    KTP_SELESAI = auto()
    
    AJUKAN_KK = auto()
    KK_NAMA = auto()
    KK_NIK = auto()
    KK_ALAMAT = auto()
    KK_HP = auto()
    KK_KONFIRMASI = auto()
    KK_SELESAI = auto()
    
    AJUKAN_AKTA = auto()
    AKTA_NAMA = auto()
    AKTA_NIK = auto()
    AKTA_ALAMAT = auto()
    AKTA_HP = auto()
    AKTA_KONFIRMASI = auto()
    AKTA_SELESAI = auto()
    
    AJUKAN_PINDAH = auto()
    PINDAH_NAMA = auto()
    PINDAH_NIK = auto()
    PINDAH_ALAMAT_ASAL = auto()
    PINDAH_ALAMAT_TUJUAN = auto()
    PINDAH_HP = auto()
    PINDAH_KONFIRMASI = auto()
    PINDAH_SELESAI = auto()
    
    PENGADUAN = auto()
    PENGADUAN_DETAIL = auto()
    PENGADUAN_HP = auto()
    PENGADUAN_SELESAI = auto()
    
    CEK_STATUS = auto()
    CEK_TIKET = auto()

TRANSITION_TABLE = {
    State.IDLE: {"salam": State.MENU_UTAMA, "apa_saja": State.MENU_UTAMA},
    State.MENU_UTAMA: {
        "info_ktp": State.INFO_KTP, "ajukan_ktp": State.AJUKAN_KTP,
        "info_kk": State.INFO_KK, "ajukan_kk": State.AJUKAN_KK,
        "info_akta": State.INFO_AKTA, "ajukan_akta": State.AJUKAN_AKTA,
        "ajukan_pindah": State.AJUKAN_PINDAH, "pengaduan": State.PENGADUAN,
        "cek_status": State.CEK_STATUS, "faq": State.FAQ, "apa_saja": State.MENU_UTAMA
    },
    
    State.INFO_KTP: {"lanjut": State.MENU_UTAMA, "ajukan_ktp": State.AJUKAN_KTP, "apa_saja": State.MENU_UTAMA},
    State.AJUKAN_KTP: {"lanjut": State.KTP_NAMA},
    State.KTP_NAMA: {"input": State.KTP_NIK},
    State.KTP_NIK: {"input": State.KTP_ALAMAT},
    State.KTP_ALAMAT: {"input": State.KTP_HP},
    State.KTP_HP: {"input": State.KTP_KONFIRMASI},
    State.KTP_KONFIRMASI: {"ya": State.KTP_SELESAI, "tidak": State.MENU_UTAMA},
    State.KTP_SELESAI: {"apa_saja": State.MENU_UTAMA},
    
    State.INFO_KK: {"lanjut": State.MENU_UTAMA, "ajukan_kk": State.AJUKAN_KK, "apa_saja": State.MENU_UTAMA},
    State.AJUKAN_KK: {"lanjut": State.KK_NAMA},
    State.KK_NAMA: {"input": State.KK_NIK},
    State.KK_NIK: {"input": State.KK_ALAMAT},
    State.KK_ALAMAT: {"input": State.KK_HP},
    State.KK_HP: {"input": State.KK_KONFIRMASI},
    State.KK_KONFIRMASI: {"ya": State.KK_SELESAI, "tidak": State.MENU_UTAMA},
    State.KK_SELESAI: {"apa_saja": State.MENU_UTAMA},
    
    State.INFO_AKTA: {"lanjut": State.MENU_UTAMA, "ajukan_akta": State.AJUKAN_AKTA, "apa_saja": State.MENU_UTAMA},
    State.AJUKAN_AKTA: {"lanjut": State.AKTA_NAMA},
    State.AKTA_NAMA: {"input": State.AKTA_NIK},
    State.AKTA_NIK: {"input": State.AKTA_ALAMAT},
    State.AKTA_ALAMAT: {"input": State.AKTA_HP},
    State.AKTA_HP: {"input": State.AKTA_KONFIRMASI},
    State.AKTA_KONFIRMASI: {"ya": State.AKTA_SELESAI, "tidak": State.MENU_UTAMA},
    State.AKTA_SELESAI: {"apa_saja": State.MENU_UTAMA},
    
    State.AJUKAN_PINDAH: {"lanjut": State.PINDAH_NAMA},
    State.PINDAH_NAMA: {"input": State.PINDAH_NIK},
    State.PINDAH_NIK: {"input": State.PINDAH_ALAMAT_ASAL},
    State.PINDAH_ALAMAT_ASAL: {"input": State.PINDAH_ALAMAT_TUJUAN},
    State.PINDAH_ALAMAT_TUJUAN: {"input": State.PINDAH_HP},
    State.PINDAH_HP: {"input": State.PINDAH_KONFIRMASI},
    State.PINDAH_KONFIRMASI: {"ya": State.PINDAH_SELESAI, "tidak": State.MENU_UTAMA},
    State.PINDAH_SELESAI: {"apa_saja": State.MENU_UTAMA},
    
    State.PENGADUAN: {"input": State.PENGADUAN_DETAIL},
    State.PENGADUAN_DETAIL: {"input": State.PENGADUAN_HP},
    State.PENGADUAN_HP: {"input": State.PENGADUAN_SELESAI},
    State.PENGADUAN_SELESAI: {"apa_saja": State.MENU_UTAMA},
    
    State.CEK_STATUS: {"input": State.CEK_TIKET},
    State.CEK_TIKET: {"apa_saja": State.MENU_UTAMA},
    
    State.FAQ: {"apa_saja": State.MENU_UTAMA},
}

class FSMachine:
    def __init__(self):
        self.current_state = State.IDLE
        self.previous_state = State.IDLE

    def transition(self, action: str) -> bool:
        transitions = TRANSITION_TABLE.get(self.current_state, {})
        next_state = transitions.get(action) or transitions.get("apa_saja")
        if next_state:
            self.previous_state = self.current_state
            self.current_state = next_state
            return True
        return False

    def force_state(self, state: State):
        self.previous_state = self.current_state
        self.current_state = state

    def reset(self):
        self.current_state = State.IDLE
        self.previous_state = State.IDLE

    def get_state_name(self) -> str:
        return self.current_state.name
