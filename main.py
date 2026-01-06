# Ana modüller
import customtkinter as ctk
import tkinter as tk
# Özel modüller (modüler yapı)
from data_manager import DataManager
from exercise_engine import GameEngine
from assets_factory import DynamicBackground
from datetime import datetime, timedelta
# Sistem modülleri
import sys
import platform

class AutoClosePopup(ctk.CTkToplevel):
    def __init__(self, parent, title, message, color="#0f0f1f", auto_close_ms=2000):
        super().__init__(parent)
        self.geometry("500x300")
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        parent.update_idletasks()
        p_width = parent.winfo_width()
        p_height = parent.winfo_height()
        p_x = parent.winfo_x()
        p_y = parent.winfo_y()
        
        popup_width = 500
        popup_height = 300
        x = p_x + (p_width - popup_width) // 2
        y = p_y + (p_height - popup_height) // 2
        
        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        self.configure(fg_color="#1a1a2e")
        
        f = ctk.CTkFrame(self, fg_color="#1a1a2e", border_width=2, border_color=color)
        f.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(f, text=title, font=("Impact", 30), text_color="#00FFCC").pack(pady=30)
        ctk.CTkLabel(f, text=message, font=("Arial", 20), wraplength=450, text_color="#ddd").pack(pady=20)
        
        self.after(auto_close_ms, self.destroy)
        self.lift()
        self.focus_force()

class UltimateVisionApp(ctk.CTk):     # Kalıtım
    def __init__(self):
        super().__init__()
        self.db = DataManager()       # Kompozisyon (başka bir sınıfın örneğini kullanma)
        
        self.os_name = platform.system()
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        
        self.setup_fullscreen()
        
        self.current_theme = self.db.get_setting("theme_mode")
        
        self.main_canvas = tk.Canvas(self, bg="#050510", highlightthickness=0)
        self.main_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_engine = DynamicBackground(self.main_canvas, self.screen_w, self.screen_h, self.current_theme)
        self.animate_bg()
        self.setup_ui()

    def setup_fullscreen(self):
        self.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
        
        if self.os_name == "Windows":
            self.state('zoomed')
            self.attributes('-fullscreen', True)
            self.update()
            
            if self.winfo_width() != self.screen_w:
                self.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
                self.overrideredirect(True)
                self.update()
                self.after(100, lambda: self.overrideredirect(False))
                
        elif self.os_name == "Darwin":
            self.attributes('-fullscreen', True)
            self.update_idletasks()
        else:
            self.attributes('-fullscreen', True)
            self.update()
            self.bind("<Configure>", self.on_resize)
            
        self.after(200, self.verify_fullscreen)

    def on_resize(self, event):
        if self.winfo_width() != self.screen_w or self.winfo_height() != self.screen_h:
            self.geometry(f"{self.screen_w}x{self.screen_h}+0+0")

    def verify_fullscreen(self):
        current_w = self.winfo_width()
        current_h = self.winfo_height()
        
        if current_w != self.screen_w or current_h != self.screen_h:
            self.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
            
            if self.os_name == "Windows":
                self.overrideredirect(True)
                self.update()
                self.after(100, lambda: self.overrideredirect(False))

    def restore_main_window(self):
        self.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
        
        if self.os_name == "Windows":
            self.state('zoomed')
            self.attributes('-fullscreen', True)
            self.update()
            self.update_idletasks()
        else:
            self.attributes('-fullscreen', True)
            self.update_idletasks()
        
        self.setup_ui()
        self.animate_bg()

    def animate_bg(self):
        self.bg_engine.update()
        self.after(30, self.animate_bg)

    def get_theme_colors(self):
        if self.current_theme == "gece":
            return {
                "bg_main": "#0f0f1f", 
                "bg_secondary": "#161625", 
                "canvas_bg": "#050510", 
                "text_bg": "#0a0a1a",
                "text_color": "#ffffff",
                "reading_bg": "#0f0f1f",
                "reading_text": "#ffffff"
            }
        else:
            return {
                "bg_main": "#2c3e50", 
                "bg_secondary": "#34495e", 
                "canvas_bg": "#1a252f", 
                "text_bg": "#fef9e7",
                "text_color": "#000000",
                "reading_bg": "#fef9e7",
                "reading_text": "#000000"
            }

    def setup_ui(self):      # Kapsüllenmiş metod
        colors = self.get_theme_colors()
        for w in self.winfo_children():
            if not isinstance(w, tk.Canvas): 
                w.destroy()
        
        ctk.CTkButton(
            self,
            text="✕ ÇIKIŞ",
            command=self.destroy,
            fg_color="#c0392b",
            hover_color="#a93226",
            font=("Arial", 14, "bold"),
            width=100,
            height=40,
            corner_radius=10
        ).place(relx=0.95, rely=0.02, anchor="ne")
        
        self.dash = ctk.CTkFrame(self, fg_color=colors["bg_main"], corner_radius=30, border_width=2, border_color="#333")
        self.dash.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.85)

        self.map_panel = ctk.CTkFrame(self.dash, fg_color="transparent")
        self.map_panel.place(relx=0.02, rely=0.05, relwidth=0.68, relheight=0.9)
        
        self.side_panel = ctk.CTkFrame(self.dash, fg_color=colors["bg_secondary"], corner_radius=20)
        self.side_panel.place(relx=0.72, rely=0.05, relwidth=0.26, relheight=0.9)

        self.draw_session_map()
        self.setup_side_panel()

    def draw_session_map(self):
        colors = self.get_theme_colors()
        ctk.CTkLabel(self.map_panel, text="🗺️ YOLCULUK HARİTAM", 
                    font=("Impact", 28, "bold"), text_color="#00FFCC").pack(pady=10)
        
        # Canvas oluşturma
        canvas_frame = ctk.CTkFrame(self.map_panel, fg_color=colors["bg_main"])
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        c = tk.Canvas(canvas_frame, bg=colors["bg_main"], highlightthickness=0)
        c.pack(fill="both", expand=True)
        
        last_successful = self.db.data["last_successful_session"]
        current_session = self.db.get_current_session_number()
        session_status = self.db.get_current_session_status()
        
        # Canvas boyut hesaplamaları
        canvas_width = self.screen_w * 0.6
        canvas_height = self.screen_h * 0.6
        cw, ch = canvas_width / 6, canvas_height / 3
        
        for i in range(18):
            x = 100 + (i % 6) * cw
            y = 80 + (i // 6) * ch
            
            session_number = i + 1
            
            if session_number <= last_successful:
                fill = "#FFCC00"        # Tamamlanmış - Sarı
                outline_color = "#FFCC00"
                text_color = "black"
            elif session_number == current_session:
                if session_status == "active":
                    fill = "#00FF88"      # Aktif - Yeşil
                    outline_color = "white"
                    text_color = "black"
                elif session_status == "failed":
                    fill = "#FF5555"
                    outline_color = "#FF0000"     # Başarısız - Kırmızı
                    text_color = "white"
                else:
                    fill = "#00FF88"
                    outline_color = "white"
                    text_color = "black"
            else:
                # Mevcut ve başarısız seanslar hariç kilit kontrolü
                if self.db.is_session_locked(session_number):
                    fill = "#666"
                    outline_color = "#999"
                    text_color = "white"
                else:
                    fill = "#444"
                    outline_color = "#777"
                    text_color = "white"
                
            tag = f"s_{session_number}"
            radius = 35
            
            c.create_oval(x-radius, y-radius, x+radius, y+radius, 
                         fill=fill, outline=outline_color, 
                         width=3 if session_number == current_session else 1, tags=tag)
            
            c.create_text(x, y, text=str(session_number), 
                         fill=text_color, font=("Arial", 16, "bold"), tags=tag)
            
            c.create_text(x, y + radius + 20, text=f"Seans {session_number}", 
                         fill="white", font=("Arial", 10, "bold"), tags=tag)
            
            c.tag_bind(tag, "<Button-1>", lambda e, s=session_number: self.show_session_info(s))

    def show_session_info(self, s):
        last_successful = self.db.data["last_successful_session"]
        current_session = self.db.get_current_session_number()
        session_status = self.db.get_current_session_status()
        
        if s <= last_successful:
            status = "TAMAMLANDI"
            message = f"Seans {s} başarıyla tamamlandı!"
        elif s == current_session:
            if session_status == "active":
                status = "AKTİF"
                message = f"Seans {s} aktif - egzersiz bekleniyor"
            elif session_status == "failed":
                # Başarısız seans için özel popup
                self.show_failed_session_popup(s)
                return
            else:
                status = "AKTİF"
                message = f"Seans {s} aktif"
        else:
            # Sadece gelecekteki seanslar için kilit kontrolü
            if s > current_session and self.db.is_session_locked(s):
                remaining = self.db.get_remaining_lock_time(s)
                status = f"KİLİTLİ - {remaining}"
                message = f"Seans {s} 36 saat kilitli"
            else:
                status = "HENÜZ BAŞLANMADI"
                message = f"Seans {s} henüz başlamadı"
        
        popup = AutoClosePopup(self, f"Seans {s}", 
               f"Durum: {status}\n{message}",
               color="#2980b9", auto_close_ms=3000)

    def show_failed_session_popup(self, session_number):
        """Başarısız seans için özel popup - EGZERSİZİ YENİDEN BAŞLATMA SEÇENEĞİ"""
        win = ctk.CTkToplevel(self)
        win.geometry("600x400")
        win.title(f"Seans {session_number} Başarısız")
        win.transient(self)
        win.grab_set()
        
        # Ana pencere pozisyonunu al
        self.update_idletasks()
        p_width = self.winfo_width()
        p_height = self.winfo_height()
        p_x = self.winfo_x()
        p_y = self.winfo_y()
        
        # Popup'ı ortala
        popup_width = 600
        popup_height = 400
        x = p_x + (p_width - popup_width) // 2
        y = p_y + (p_height - popup_height) // 2
        
        win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        win.configure(fg_color="#1a1a2e")
        
        f = ctk.CTkFrame(win, fg_color="#1a1a2e", border_width=2, border_color="#f39c12")
        f.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(f, text=f"⚠️ SEANS {session_number} BAŞARISIZ", 
                    font=("Impact", 30), text_color="#FFCC00").pack(pady=30)
        
        # Mesaj
        message = ("Egzersizi tamamlamadınız. Aynı seansta kalmaya devam edebilirsiniz:\n\n"
                  "1. 📖 Kütüphaneden mevcut metinlere erişebilirsiniz\n"
                  "2. 🎮 2 metin tamamladıktan sonra egzersizi yeniden deneyebilirsiniz\n"
                  "3. ✅ Egzersizi başarıyla tamamlayana kadar bu seans devam edecek")
        
        ctk.CTkLabel(f, text=message, font=("Arial", 16), 
                    wraplength=550, text_color="#ddd", justify="left").pack(pady=20)
        
        btn_frame = ctk.CTkFrame(f, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        # Egzersizi yeniden başlat butonu
        ctk.CTkButton(
            btn_frame, 
            text="🎮 EGZERSİZİ YENİDEN BAŞLAT", 
            command=lambda: [win.destroy(), self.start_training()],
            fg_color="#f39c12",
            hover_color="#d35400",
            font=("Arial", 16, "bold"),
            width=250,
            height=45
        ).pack(side="left", padx=10)
        
        # Kütüphaneye git butonu
        ctk.CTkButton(
            btn_frame, 
            text="📖 KÜTÜPHANEYE GİT", 
            command=lambda: [win.destroy(), self.open_library()],
            fg_color="#3498db",
            hover_color="#2980b9",
            font=("Arial", 16, "bold"),
            width=200,
            height=45
        ).pack(side="left", padx=10)
        
        win.lift()
        win.focus_force()

    def setup_side_panel(self):
        ctk.CTkLabel(self.side_panel, text="KONTROL MERKEZİ", 
                    font=("Impact", 24)).pack(pady=20)
        
        menu = [
            ("📖 KÜTÜPHANE", self.open_library, "#2980b9"),
            ("🎮 EGZERSİZLER", self.open_exercises_menu, "#8e44ad"),
            ("📊 İLERLEME", self.open_progress, "#27ae60"),
            ("💡 İPUÇLARI", self.open_reminders, "#f39c12"),
            ("📢 BİLDİRİMLER", self.open_notifications, "#b81119"),
            ("⚙️ AYARLAR", self.open_settings, "#34495e")
        ]
        
        for text, command, color in menu:
            btn = ctk.CTkButton(
                self.side_panel, 
                text=text, 
                fg_color=color,
                hover_color=self.adjust_color(color, -20),
                height=50,
                command=command,
                font=("Arial", 16, "bold")
            )
            btn.pack(pady=8, padx=20, fill="x")

    def adjust_color(self, hex_color, adjust):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, min(255, r + adjust))
        g = max(0, min(255, g + adjust))
        b = max(0, min(255, b + adjust))
        
        return f"#{r:02x}{g:02x}{b:02x}"

    def open_child_window(self, title):
        # Alt pencere oluşturma - tüm pencereler için ortak
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry(f"{self.screen_w}x{self.screen_h}+0+0")
        
        if self.os_name == "Windows":
            win.state('zoomed')
            win.attributes('-fullscreen', True)
        else:
            win.attributes('-fullscreen', True)
        
        colors = self.get_theme_colors()
        win.configure(fg_color=colors["canvas_bg"])
        
        # Ana sayfaya dön butonu
        ctk.CTkButton(
            win, 
            text="← ANA SAYFAYA DÖN", 
            command=win.destroy,
            fg_color="#3498db",
            hover_color="#2980b9",
            font=("Arial", 16, "bold"),
            width=180,
            height=40,
            corner_radius=10
        ).place(relx=0.02, rely=0.02, anchor="nw")
        
        win.transient(self)
        win.grab_set()
        win.lift()
        win.focus_force()
        
        return win

    def open_settings(self):
        win = self.open_child_window("Ayarlar")
        ctk.CTkLabel(win, text="⚙️ AYARLAR", font=("Impact", 40)).pack(pady=20)
        
        f = ctk.CTkFrame(win, fg_color=self.get_theme_colors()["bg_secondary"], corner_radius=20)
        f.pack(padx=100, fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(f, text="Yazı Boyutu", font=("Arial", 18)).pack(pady=(20,0))
        s = ctk.CTkSlider(
            f, 
            from_=16, 
            to=40, 
            command=lambda v: self.db.set_setting("font_size", int(v)),
            progress_color="#2980b9",
            button_color="#3498db",
            button_hover_color="#2980b9"
        )
        s.set(self.db.get_setting("font_size"))
        s.pack(pady=10, padx=100, fill="x")
        
        theme_frame = ctk.CTkFrame(f, fg_color="transparent")
        theme_frame.pack(pady=10)
        
        ctk.CTkLabel(theme_frame, text="Tema Modu:", font=("Arial", 16)).pack(side="left", padx=(0, 10))
        
        def change_theme(theme):
            self.current_theme = theme
            self.db.set_setting("theme_mode", theme)
            self.bg_engine.update_theme(theme)
            self.after(100, self.setup_ui)
        
        gece_btn = ctk.CTkButton(
            theme_frame,
            text="🌙 Gece",
            command=lambda: change_theme("gece"),
            fg_color="#2980b9" if self.current_theme == "gece" else "#34495e",
            hover_color="#21618c" if self.current_theme == "gece" else "#2c3e50",
            width=100,
            height=35
        )
        gece_btn.pack(side="left", padx=5)
        
        aksam_btn = ctk.CTkButton(
            theme_frame,
            text="🌅 Akşam",
            command=lambda: change_theme("aksam"),
            fg_color="#2980b9" if self.current_theme == "aksam" else "#34495e",
            hover_color="#21618c" if self.current_theme == "aksam" else "#2c3e50",
            width=100,
            height=35
        )
        aksam_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(
            f, 
            text="🔁 İLERLEMEYİ SIFIRLA", 
            fg_color="#c0392b", 
            hover_color="#a93226",
            font=("Arial", 16, "bold"),
            command=lambda: self.reset_confirm(win),
            width=250,
            height=45
        ).pack(pady=20)

    def reset_confirm(self, win):
        confirm_win = ctk.CTkToplevel(win)
        confirm_win.title("Onay")
        confirm_win.geometry("500x350")
        confirm_win.configure(fg_color="#1a1a2e")
        
        confirm_win.transient(win)
        confirm_win.grab_set()
        confirm_win.lift()
        confirm_win.focus_force()
        
        # Ana pencere pozisyonunu al
        win.update_idletasks()
        w_width = win.winfo_width()
        w_height = win.winfo_height()
        w_x = win.winfo_x()
        w_y = win.winfo_y()
        
        # Popup'ı ortala
        popup_width = 500
        popup_height = 350
        x = w_x + (w_width - popup_width) // 2
        y = w_y + (w_height - popup_height) // 2
        confirm_win.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        ctk.CTkLabel(confirm_win, text="⚠️ DİKKAT", 
                    font=("Impact", 30), text_color="#FFCC00").pack(pady=30)
        
        ctk.CTkLabel(confirm_win, 
                    text="Tüm ilerlemeniz sıfırlanacak:\n• Okuma metinleri\n• Egzersiz skorları\n• 36 saatlik kilitler\n• Haftalık takip\n\nBu işlem geri alınamaz!",
                    font=("Arial", 16), 
                    text_color="#ddd").pack(pady=20)
        
        btn_frame = ctk.CTkFrame(confirm_win, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="VAZGEÇ", fg_color="#34495e", 
                     hover_color="#2c3e50",
                     command=confirm_win.destroy,
                     width=150,
                     height=40).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="SIFIRLA", fg_color="#c0392b",
                     hover_color="#a93226",
                     command=lambda: self.perform_reset(confirm_win, win),
                     width=150,
                     height=40).pack(side="left", padx=10)

    def perform_reset(self, confirm_win, settings_win):
        self.db.reset_progress()
        self.db.reset_lock()
        
        confirm_win.destroy()
        settings_win.destroy()
        
        AutoClosePopup(self, "BAŞARILI", 
                      "Tüm ilerleme ve kilitler sıfırlandı.\nUygulama yeniden başlatılıyor...",
                      color="#27ae60", auto_close_ms=1500)
        
        self.after(1500, self.setup_ui)

    def open_library(self):
        """72 METİNLİK OKUMA EKRANI"""
        win = self.open_child_window("72 Metinlik Okuma Kütüphanesi")
        
        current_session = self.db.get_current_session_number()
        last_successful = self.db.data["last_successful_session"]
        session_status = self.db.get_current_session_status()
        
        # Başlık
        title_frame = ctk.CTkFrame(win, fg_color="#34495e", corner_radius=10)
        title_frame.pack(pady=20, padx=100, fill="x")
        
        ctk.CTkLabel(title_frame, text="📖 72 METİNLİK OKUMA KÜTÜPHANESİ", 
                     font=("Impact", 28), text_color="#00FFCC").pack(pady=15)
        
        # Kilit uyarısı - Sadece gelecekteki kilitli seanslar için
        next_locked_session = self.db.get_next_locked_session()
        
        if next_locked_session and next_locked_session > current_session:
            remaining = self.db.get_remaining_lock_time(next_locked_session)
            
            warning_frame = ctk.CTkFrame(win, fg_color="#2c3e50", corner_radius=10)
            warning_frame.pack(pady=10, padx=100, fill="x")
            ctk.CTkLabel(warning_frame, text=f"⏳ {next_locked_session}. seans için bekleyin: {remaining}", 
                         text_color="#FFCC00", font=("Arial", 18)).pack(pady=10, padx=20)
        
        # Mevcut seans durumu bilgisi
        status_frame = ctk.CTkFrame(win, fg_color="#34495e", corner_radius=10)
        status_frame.pack(pady=10, padx=100, fill="x")
        
        if session_status == "failed":
            status_text = f"⚠️ Seans {current_session} BAŞARISIZ - Egzersizi tamamlayın!"
            status_color = "#e74c3c"
            
            # Başarısız seans durumunda egzersiz butonu
            exercise_btn_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
            exercise_btn_frame.pack(pady=10)
            
            ctk.CTkButton(
                exercise_btn_frame,
                text="🎮 EGZERSİZİ YENİDEN BAŞLAT",
                command=lambda: [win.destroy(), self.start_training()],
                fg_color="#f39c12",
                hover_color="#d35400",
                font=("Arial", 14, "bold"),
                width=250,
                height=40
            ).pack(pady=5)
            
        elif session_status == "active":
            status_text = f"🎯 Seans {current_session} AKTİF - Egzersiz bekleniyor"
            status_color = "#f39c12"
        elif session_status == "completed":
            status_text = f"✅ Seans {current_session} TAMAMLANDI"
            status_color = "#27ae60"
        else:
            status_text = f"📖 Seans {current_session} hazır"
            status_color = "#3498db"
        
        ctk.CTkLabel(status_frame, text=status_text, 
                     text_color=status_color, font=("Arial", 16, "bold")).pack(pady=10)
        
        # Metin grid'i
        scr = ctk.CTkScrollableFrame(win, width=self.screen_w-100, 
                                    fg_color=self.get_theme_colors()["bg_secondary"])
        scr.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Her seans için 2 metin
        for session_num in range(1, 37):  # 36 seans
            first_text, last_text = self.db.get_session_text_range(session_num)
            
            # Seans başlığı
            session_frame = ctk.CTkFrame(scr, fg_color="#2c3e50", corner_radius=10)
            session_frame.pack(pady=10, padx=10, fill="x")
            
            session_status_text = ""
            if session_num <= last_successful:
                session_status_text = "✅ TAMAMLANDI"
                session_color = "#27ae60"
            elif session_num == current_session:
                if session_status == "failed":
                    session_status_text = "⚠️ BAŞARISIZ"
                    session_color = "#e74c3c"
                elif session_status == "active":
                    session_status_text = "🎯 AKTİF"
                    session_color = "#f39c12"
                else:
                    session_status_text = "📖 DEVAM EDİYOR"
                    session_color = "#3498db"
            else:
                # Sadece gelecekteki ve kilitli seanslar için
                if session_num > current_session and self.db.is_session_locked(session_num):
                    remaining = self.db.get_remaining_lock_time(session_num)
                    session_status_text = f"🔒 KİLİTLİ - {remaining}"
                    session_color = "#7f8c8d"
                else:
                    session_status_text = "⏳ BEKLİYOR"
                    session_color = "#95a5a6"
            
            ctk.CTkLabel(session_frame, text=f"Seans {session_num}: {session_status_text}", 
                        font=("Arial", 16, "bold"), text_color=session_color).pack(pady=5)
            
            # Metin butonları
            button_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
            button_frame.pack(pady=5)
            
            for text_id in range(first_text, last_text + 1):
                can_access = self.db.can_access_text(text_id)
                
                # Buton metni belirleme

                # DURUM 1: Şu anki sıradaki metin (özel vurgu)
                if text_id == self.db.data["unlocked_text_index"]:
                    btn_text = f"⏩\nMetin {text_id}"
                    fg_color = "#00FFCC"      # Özel yeşil-mavi
                # DURUM 2: Tamamlanmış metin
                elif text_id < self.db.data["unlocked_text_index"]:
                    btn_text = f"✅\nMetin {text_id}"
                    fg_color = "#27ae60"      # Yeşil
                # DURUM 3: Erişilebilir metin (okunabilir)
                elif can_access:
                    btn_text = f"📖\nMetin {text_id}"
                    fg_color = "#3498db"      # Mavi
                # DURUM 4: Erişilemez metinler (çeşitli durumlar)
                else:
                    text_session = (text_id + 1) // 2
                    # 4a: Mevcut seanstaki kilitli metin
                    if text_session == current_session:
                        btn_text = f"🔒\nMetin {text_id}"
                        fg_color = "#34495e"     # Koyu gri-mavi
                    # 4b: Gelecekteki kilitli seanstaki metin
                    elif text_session > current_session:
                        if self.db.is_session_locked(text_session):
                            btn_text = f"🔒\nMetin {text_id}"
                            fg_color = "#34495e" # Koyu gri-mavi
                        else:
                            btn_text = f"🔒\nMetin {text_id}"
                            fg_color = "#34495e" # Koyu gri-mavi
                    # 4c: Diğer durumlar
                    else:
                        btn_text = f"🔒\nMetin {text_id}"
                        fg_color = "#34495e"     # Koyu gri-mavi
                
                # Buton oluşturma
                btn = ctk.CTkButton(
                    button_frame, 
                    text=btn_text, 
                    state="disabled" if not can_access else "normal",
                    fg_color=fg_color,
                    hover_color=self.adjust_color(fg_color, -20),
                    command=lambda x=text_id: self.read_text(x, win),
                    font=("Arial", 12, "bold"),
                    width=80,
                    height=80,
                    corner_radius=10
                )
                btn.pack(side="left", padx=5, pady=5)

    def read_text(self, idx, lib_win):
        """Metin okuma penceresi"""
        if not self.db.can_access_text(idx):
            current_session = self.db.get_current_session_number()
            text_session = (idx + 1) // 2
            
            # DURUM 1: Sırayla ilerlenmediğinde uyarı
            if text_session == current_session:
                AutoClosePopup(self, "⛔ SIRAYLA İLERLEYİN", 
                              f"Lütfen sırayla ilerleyin!\nSıradaki metin: {self.db.data['unlocked_text_index']}", 
                              color="#f39c12", auto_close_ms=3000)
                
            # DURUM 2: Seans kilitliyse kalan süre bilgisi
            elif self.db.is_session_locked(text_session):
                remaining = self.db.get_remaining_lock_time(text_session)
                AutoClosePopup(self, "⛔ SEANS KİLİTLİ", 
                              f"Metin {idx} {text_session}. seansa ait!\n"
                              f"Bu seans 36 saat kilitli.\nKalan süre: {remaining}",
                              color="#e74c3c", auto_close_ms=4000)
            
            # DURUM 3: Genel olarak erişilemezse basit kilit mesajı
            else:
                AutoClosePopup(self, "⛔ ULAŞILAMAZ", 
                              f"Metin {idx} henüz kilitli!", 
                              color="#e74c3c", auto_close_ms=3000)
            return
        
        # DURUM 4: Sıradaki metin değilse uyarı
        if idx != self.db.data["unlocked_text_index"]:
            AutoClosePopup(self, "⛔ UYARI", 
                          f"Lütfen sırayla ilerleyin!\nSıradaki metin: {self.db.data['unlocked_text_index']}", 
                          color="#e74c3c", auto_close_ms=3000)
            return
        
        win = self.open_child_window(f"Metin {idx}")
        
        colors = self.get_theme_colors()
        
        title_frame = ctk.CTkFrame(win, fg_color=colors["bg_main"], corner_radius=10)
        title_frame.pack(pady=10, padx=100, fill="x")
        
        text_data = self.db.get_text(idx)
        current_session = (idx + 1) // 2
        ctk.CTkLabel(title_frame, text=f"Seans {current_session} - {text_data['title']}", 
                    font=("Arial", 24, "bold"), text_color="#00FFCC").pack(pady=10)
        
        text_frame = ctk.CTkFrame(win, fg_color=colors["bg_secondary"], corner_radius=15)
        text_frame.pack(pady=10, padx=100, fill="both", expand=True)
        
        box = ctk.CTkTextbox(
            text_frame, 
            font=("Arial", self.db.get_setting("font_size")), 
            wrap="word",
            fg_color=colors["reading_bg"],
            text_color=colors["reading_text"],
            border_width=2,
            border_color="#444" if self.current_theme == "gece" else "#ddd"
        )
        box.pack(fill="both", expand=True, padx=20, pady=20)
        box.insert("0.0", text_data["content"])
        box.configure(state="disabled")
        
        def finish():
            # Metni tamamla
            self.db.complete_text(idx)
            
            win.destroy()
            
            completed_texts = self.db.data["completed_texts_total"]
            current_session = self.db.get_current_session_number()
            session_status = self.db.get_current_session_status()
            
            # 2 metin tamamlandığında otomatik egzersize geçiş
            if completed_texts % 2 == 0:
                # Seansı başlat
                self.db.start_session()
                
                # OTOMATİK EGZERSİZE GEÇ
                AutoClosePopup(self, "🎮 Egzersize Geçiliyor", 
                             f"Seans {current_session} için 2 metin tamamlandı!\n"
                             f"20 dakikalık egzersiz başlatılıyor...",
                             color="#8e44ad", auto_close_ms=2000)
                
                self.after(2200, lambda: [lib_win.destroy(), self.start_training()])
            else:
                # Sadece 1 metin tamamlandı
                AutoClosePopup(self, "📖 Sonraki Metin", 
                             f"Metin {idx} tamamlandı!\n"
                             f"Sıradaki metni kütüphaneden seçebilirsiniz.",
                             color="#3498db", auto_close_ms=1500)
        
        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=20, padx=100, fill="x")
        
        ctk.CTkButton(
            btn_frame, 
            text="✅ TAMAMLADIM", 
            command=finish, 
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=("Arial", 18, "bold"),
            height=60,
            corner_radius=10
        ).pack(fill="x")

    def start_training(self):
        """Egzersiz başlatma"""
        current_session = self.db.get_current_session_number()
        session_status = self.db.get_current_session_status()
        
        # Başarısız seans durumunda da egzersiz başlatılabilir
        if session_status == "failed":
            # Başarısız seans için kontrol: 2 metin tamamlanmış mı?
            session_key = str(current_session)
            texts_completed = len(self.db.data["session_texts"].get(session_key, []))
            
            if texts_completed < 2:
                AutoClosePopup(self, "⚠️ UYARI", 
                              f"Egzersiz için önce 2 metin tamamlamalısınız!\n"
                              f"Tamamlanan metinler: {texts_completed}/2",
                              color="#f39c12", auto_close_ms=3000)
                return
        elif self.db.data["completed_texts_total"] % 2 != 0:
            # Normal durum: 2 metin tamamlanmış mı?
            AutoClosePopup(self, "⚠️ UYARI", 
                          "Egzersiz için önce 2 metin tamamlamalısınız!", 
                          color="#f39c12", auto_close_ms=3000)
            return

        self.withdraw()
        
        try:
            engine = GameEngine(duration_sec=1200)
            success = engine.run()
        except Exception as e:
            print(f"Egzersiz hatası: {e}")
            self.restore_main_window()
            AutoClosePopup(self, "HATA", "Egzersiz başlatılamadı. Lütfen tekrar deneyin.", 
                          color="#c0392b", auto_close_ms=3000)
            return
        
        self.restore_main_window()
        
        # EGZERSİZ SONUCU
        current_session = self.db.get_current_session_number()
        
        if not success:
            # BAŞARISIZ - ESC ile çıkıldı
            self.db.complete_session(False)
            
            AutoClosePopup(self, "⚠️ Egzersiz Tamamlanmadı", 
                          f"Egzersizi tamamlamadınız. Seans {current_session} başarısız sayıldı.\n\n"
                          f"⚠️ DİKKAT: AYNI SEANSTA KALMAYA DEVAM EDİYORSUNUZ!\n"
                          f"1. 📖 Kütüphaneden mevcut metinlere erişebilirsiniz\n"
                          f"2. 🎮 2 metin tamamladıktan sonra egzersizi yeniden deneyebilirsiniz",
                          color="#f39c12", auto_close_ms=5000)
            
        else:
            # BAŞARILI - egzersiz tamamlandı
            self.db.complete_session(True)
            next_session = current_session + 1
            
            AutoClosePopup(self, "🎉 SEANS TAMAMLANDI!", 
                          f"Seans {current_session} başarıyla tamamlandı!\n\n"
                          f"✓ 2 okuma metni tamamlandı\n"
                          f"✓ 20 dakika egzersiz yapıldı\n"
                          f"✓ Yolculuk haritan güncellendi\n\n"
                          f"⚠️ {next_session}. seans 36 saat sonra açılacak!",
                          color="#27ae60", auto_close_ms=4000)
        
        self.after(1000, self.setup_ui)

    def open_exercises_menu(self):
        win = self.open_child_window("Egzersizler")
        ctk.CTkLabel(win, text="🎮 EĞİTİCİ EGZERSİZLER", 
                    font=("Impact", 40)).pack(pady=30)
        
        f = ctk.CTkFrame(win, fg_color=self.get_theme_colors()["bg_secondary"], corner_radius=20)
        f.pack(padx=100, fill="both", expand=True, pady=20)
        
        exercises = [
            ("👁️ SAKKADİK", "saccadic", "Göz atışları geliştirir"),
            ("🎯 TOP TAKİP", "tracking", "Takip yeteneğini artırır"),
            ("🧩 TETRİS", "tetris", "Görsel dikkat ve şekil tanıma"),
            ("🌀 GABOR", "gabor", "Kontrast duyarlılığı"),
            ("🔄 GÖZ HAREKETİ", "eye_roll", "Göz kaslarını çalıştırır"),
            ("✖️ ÇAPRAZ TAKİP", "cross", "Koordinasyon geliştirme")
        ]
        
        for i, (name, mode, desc) in enumerate(exercises):
            btn_frame = ctk.CTkFrame(f, fg_color="transparent")
            btn_frame.grid(row=i//2, column=i%2, padx=20, pady=15, sticky="nsew")
            
            ctk.CTkButton(
                btn_frame, 
                text=name, 
                fg_color="#8e44ad", 
                hover_color="#732d91",
                font=("Arial", 18, "bold"), 
                height=80,
                command=lambda m=mode: self.start_single_exercise(m, win)
            ).pack(fill="both", expand=True)
            
            ctk.CTkLabel(
                btn_frame, 
                text=desc, 
                font=("Arial", 12), 
                text_color="#aaa"
            ).pack()
            
            f.grid_columnconfigure(i%2, weight=1)
            f.grid_rowconfigure(i//2, weight=1)

    def start_single_exercise(self, mode, parent_win):
        parent_win.destroy()
        self.withdraw()
        
        try:
            engine = GameEngine(duration_sec=180, single_mode=mode)
            engine.run()
        except Exception as e:
            print(f"Tekli egzersiz hatası: {e}")
        
        self.restore_main_window()

    def open_progress(self):
        win = self.open_child_window("İlerleme")
        ctk.CTkLabel(win, text="📊 İLERLEME DURUMU", 
                    font=("Impact", 40)).pack(pady=20)
        
        stats_frame = ctk.CTkFrame(win, fg_color=self.get_theme_colors()["bg_secondary"], corner_radius=20)
        stats_frame.pack(pady=20, padx=100, fill="x")
        
        # Detaylı istatistikler
        completed_texts = self.db.data["completed_texts_total"]
        completed_sessions = self.db.data["last_successful_session"]
        current_session = self.db.get_current_session_number()
        session_status = self.db.get_current_session_status()
        
        next_locked_session = self.db.get_next_locked_session()
        lock_time = "Yok" if not next_locked_session else self.db.get_remaining_lock_time(next_locked_session)
        
        # 5 farklı istatistik
        stats = [
            ("📅 Tamamlanan Seans", str(completed_sessions)),
            ("📖 Okunan Metin", str(completed_texts)),
            ("🎯 Mevcut Seans", str(current_session)),
            ("⏱️ Sonraki Kilit", lock_time),
            ("📊 Seans Durumu", session_status.upper())
        ]
        
        # İstatistikleri grid yapısında göster
        for i, (label, value) in enumerate(stats):
            stat_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_frame.grid(row=i//3, column=i%3, padx=30, pady=20, sticky="nsew")
            ctk.CTkLabel(stat_frame, text=label, 
                        font=("Arial", 16), text_color="#aaa").pack()
            ctk.CTkLabel(stat_frame, text=value, 
                        font=("Arial", 24, "bold"), text_color="#00FFCC").pack()
        
        # Haftalık hedef takibi
        weekly_frame = ctk.CTkFrame(win, fg_color=self.get_theme_colors()["bg_secondary"], corner_radius=15)
        weekly_frame.pack(pady=20, padx=100, fill="x")
        
        weekly_stats = self.db.get_weekly_stats()
        ctk.CTkLabel(weekly_frame, text="📅 HAFTALIK HEDEF", 
                    font=("Arial", 20, "bold"), text_color="#FFCC00").pack(pady=10)
        
        weekly_text = f"Bu Hafta: {weekly_stats['completed']}/3 seans"
        ctk.CTkLabel(weekly_frame, text=weekly_text, 
                    font=("Arial", 16), text_color="#ddd").pack(pady=5)
        
        ctk.CTkLabel(weekly_frame, text=f"Haftanın {weekly_stats['day']}. günü", 
                    font=("Arial", 14), text_color="#aaa").pack(pady=5)
        
        # Görsel grafik ekleme
        graph_frame = ctk.CTkFrame(win, fg_color=self.get_theme_colors()["bg_secondary"], corner_radius=15)
        graph_frame.pack(pady=40, padx=100, fill="both", expand=True)
        
        c = tk.Canvas(graph_frame, bg=self.get_theme_colors()["bg_main"], highlightthickness=0)
        c.pack(fill="both", expand=True, padx=20, pady=20)
        
        data = [completed_texts, completed_sessions * 2]
        labels = ["Okunan Metinler", "Hedeflenen"]
        
        canvas_width = 800
        canvas_height = 300
        
        # Çubuk grafik oluşturma
        for i, val in enumerate(data):
            bar_width = 200
            max_height = 250
            h = min((val / 72) * max_height, max_height)
            x1 = 150 + i*(bar_width + 100)
            y1 = 250 - h
            x2 = x1 + bar_width
            y2 = 250
            
            c.create_rectangle(x1, y1, x2, y2, fill="#00FFCC", outline="white", width=2)
            c.create_text(x1 + bar_width//2, y1 - 20, text=str(val), 
                         fill="white", font=("Arial", 18, "bold"))
            c.create_text(x1 + bar_width//2, y2 + 30, text=labels[i], 
                         fill="white", font=("Arial", 14))
            
    def open_reminders(self):
        win = self.open_child_window("İpuçları")
        ctk.CTkLabel(win, text="💡 GÖZ SAĞLIĞI İPUÇLARI", 
                    font=("Impact", 35)).pack(pady=30)
        
        # İpucu listesi: her öğe (başlık, açıklama) formatında
        tips = [
            ("20 Dakika Kuralı", "Her 20 dakikada bir, en az 20 saniye uzağa bak."),
            ("Göz Kırpma", "Ekrana bakarken gözlerini sık sık kırpmayı unutma."),
            ("Parlaklık Ayarı", "Ekran parlaklığını oda ışığına göre ayarla."),
            ("Uygun Mesafe", "Ekranla gözlerin arasında en az 50 cm mesafe olmalı."),
            ("Dinlenme Molası", "Her saat başı 5 dakika gözlerini dinlendir."),
            ("Aydınlatma", "Odanı iyi aydınlat, ekrana doğrudan ışık gelmesin."),
            ("Düzenli Kontrol", "Göz sağlığın için düzenli doktor kontrolü yaptırmayı unutma.")
        ]
        
        # Her ipucu için bir kart oluştur
        for title, desc in tips:
            tip_frame = ctk.CTkFrame(win, fg_color=self.get_theme_colors()["bg_main"], corner_radius=15)
            tip_frame.pack(pady=10, padx=100, fill="x")
            ctk.CTkLabel(tip_frame, text=f"⭐ {title}", 
                        font=("Arial", 18, "bold"), text_color="#FFCC00").pack(anchor="w", padx=20, pady=(10, 0))
            ctk.CTkLabel(tip_frame, text=desc, 
                        font=("Arial", 16), text_color="#ddd").pack(anchor="w", padx=20, pady=(0, 10))

    def open_notifications(self):
        """
    Kullanıcıya özel bildirimleri gösteren pencereyi açar.
    Çeşitli durumlara göre dinamik olarak bildirimler oluşturur.
    """
        win = self.open_child_window("Bildirimler")
        ctk.CTkLabel(win, text="📢 BİLDİRİM MERKEZİ", 
                    font=("Impact", 35)).pack(pady=30)
        
        # Kaydırılabilir bildirim çerçevesi oluşturma
        notifications_frame = ctk.CTkScrollableFrame(win, fg_color=self.get_theme_colors()["bg_secondary"], corner_radius=15)
        notifications_frame.pack(pady=20, padx=100, fill="both", expand=True)
        
        notifications = []

        if self.db.data["completed_texts_total"] > 0:
            notifications.append(("🎯 Başarı!", f"Tebrikler! {self.db.data['completed_texts_total']} metin tamamladınız.", "#27ae60"))
        
        notifications.append(("⏰ Hatırlatma", "Düzenli egzersiz yapmak göz sağlığınız için önemli.", "#f39c12"))
        
        last_successful = self.db.data["last_successful_session"]
        if last_successful > 0:
            notifications.append(("📈 İlerleme", f"{last_successful}. seansı başarıyla tamamladınız.", "#3498db"))
        
        notifications.append(("💡 İpucu", "Bugün göz egzersizlerinizi yapmayı unutmayın!", "#9b59b6"))
        
        next_locked_session = self.db.get_next_locked_session()
        if next_locked_session:
            remaining = self.db.get_remaining_lock_time(next_locked_session)
            notifications.append(("⏳ 36 Saatlik Kilit", 
                                f"{next_locked_session}. seans için {remaining} beklemelisiniz.", 
                                "#f39c12"))
        # Mevcut seans durumu kontrolü
        current_session = self.db.get_current_session_number()
        session_status = self.db.get_current_session_status()
        
        # Başarısız seans durumu bildirimi
        if session_status == "failed":
            session_key = str(current_session)
            texts_completed = len(self.db.data["session_texts"].get(session_key, []))
            
            if texts_completed >= 2:
                notifications.append(("⚠️ EGZERSİZ GEREKLİ", 
                                    f"Seans {current_session} başarısız oldu! 2 metin tamamladınız, egzersizi yeniden deneyin.\n"
                                    f"Egzersiz başarılı olana kadar aynı seansta kalacaksınız.",
                                    "#e74c3c"))
            else:
                notifications.append(("⚠️ SEANS BAŞARISIZ", 
                                    f"Seans {current_session} başarısız oldu! Kalan {2-texts_completed} metni tamamlayıp egzersizi yeniden deneyin.",
                                    "#f39c12"))
        elif session_status == "active":
            notifications.append(("⚠️ EGZERSİZ GEREKLİ", 
                                f"2 metin okudunuz! 20 dakikalık egzersizi tamamlayarak seansı bitirin.",
                                "#e74c3c"))
        
        for session_number in list(self.db.lock_data.get("locks", {}).keys()):
            if not self.db.is_session_locked(int(session_number)):
                notifications.append(("🎉 Yeni Seans Açıldı!", 
                                    f"{session_number}. seans artık erişilebilir!", 
                                    "#27ae60"))
        
        # Doktor kontrolü bildirimleri (6, 12, 18. seanslarda)
        if last_successful >= 6 and last_successful < 12:
            notifications.append(("🏥 DOKTOR KONTROLÜ", 
                                "6. seansı tamamladınız! Göz sağlığınız için doktor kontrolü önerilir.", 
                                "#e74c3c"))
        
        if last_successful >= 12 and last_successful < 18:
            notifications.append(("🏥 DOKTOR KONTROLÜ", 
                                "12. seansı tamamladınız! Lütfen göz doktorunuza başvurun.", 
                                "#e74c3c"))
        
        if last_successful >= 18:
            notifications.append(("🏥 DOKTOR KONTROLÜ", 
                                "18. seansı tamamladınız! Göz sağlığınız için doktor kontrolü gereklidir.", 
                                "#c0392b"))
        
        # Bildirimleri ekranda göster
        if notifications:
            for title, message, color in notifications:
                notif_frame = ctk.CTkFrame(
                    notifications_frame, 
                    fg_color=color, 
                    corner_radius=15,
                    border_width=2,
                    border_color=self.adjust_color(color, -30)
                )
                notif_frame.pack(pady=8, padx=10, fill="x")
                
                ctk.CTkLabel(
                    notif_frame, 
                    text=title, 
                    font=("Arial", 16, "bold"), 
                    text_color="white"
                ).pack(anchor="w", padx=20, pady=(10, 0))
                
                ctk.CTkLabel(
                    notif_frame, 
                    text=message, 
                    font=("Arial", 14), 
                    text_color="white",
                    wraplength=600
                ).pack(anchor="w", padx=20, pady=(0, 10))
        else:
            empty_frame = ctk.CTkFrame(notifications_frame, fg_color="#2c3e50", corner_radius=15)
            empty_frame.pack(pady=50, padx=50, fill="x")
            
            ctk.CTkLabel(
                empty_frame, 
                text="📭 Henüz yeni bir bildirim yok.", 
                font=("Arial", 20), 
                text_color="#95a5a6"
            ).pack(pady=30)

# Uygulama başlangıç noktası
if __name__ == "__main__":
    # CustomTkinter temasını ayarla
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

     # Ana uygulama nesnesi oluştur
    app = UltimateVisionApp()
    
    # Pencere kapatma olayını yönet
    app.protocol("WM_DELETE_WINDOW", app.destroy)

     # Uygulamayı çalıştır
    app.mainloop()