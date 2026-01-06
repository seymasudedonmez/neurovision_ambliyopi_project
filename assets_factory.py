import pygame
import os
from PIL import Image, ImageTk, ImageDraw
import random

class AssetManager:
    """Font dosyalarını yönetir."""
    
    @staticmethod
    def get_font(size, bold=False):
        """assets/fonts klasöründen font yükler."""
        font_path = os.path.join("assets", "fonts", "OyunFontu.ttf")
        if os.path.exists(font_path):
            return pygame.font.Font(font_path, size)
        else:
            return pygame.font.SysFont("Arial", size, bold=bold)

class DynamicBackground:
    """Arka plan animasyonları."""
    def __init__(self, canvas, width, height, theme_mode="gece"):
        self.canvas = canvas
        self.w = width
        self.h = height
        self.theme_mode = theme_mode
        self.blobs = []
        self.update_theme(theme_mode)

    def update_theme(self, theme_mode):
        """Tema renklerini güncelle (GÜNCELLENDİ - AKŞAM MODU RENKLERİ)"""
        self.theme_mode = theme_mode
        
        # Tema renkleri - AKŞAM MODU RENKLERİ YENİLENDİ
        if theme_mode == "gece":
            colors = ["#1A2F1A", "#0B1026", "#2F1A2F", "#003333"]
        else:  # aksam modu - daha sıcak renkler
            colors = ["#2C4E5A", "#1F3A5F", "#3D4E6E", "#1A4D5C"]
        
        # Eğer blob'lar varsa renklerini güncelle
        for b in self.blobs:
            b["color"] = random.choice(colors)
        
        # İlk oluşturma
        if not self.blobs:
            for _ in range(15):
                self.blobs.append({
                    "x": random.randint(0, self.w),
                    "y": random.randint(0, self.h),
                    "r": random.randint(80, 200),
                    "vx": random.uniform(-0.4, 0.4),
                    "vy": random.uniform(-0.4, 0.4),
                    "color": random.choice(colors),
                    "id": None
                })

    def update(self):
        for b in self.blobs:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            
            if b["x"] < -100 or b["x"] > self.w + 100: 
                b["vx"] *= -1
            if b["y"] < -100 or b["y"] > self.h + 100: 
                b["vy"] *= -1
            
            if b["id"] is None:
                b["id"] = self.canvas.create_oval(
                    b["x"]-b["r"], b["y"]-b["r"], 
                    b["x"]+b["r"], b["y"]+b["r"], 
                    fill=b["color"], outline=""
                )
                self.canvas.tag_lower(b["id"])
            else:
                self.canvas.coords(b["id"], 
                    b["x"]-b["r"], b["y"]-b["r"], 
                    b["x"]+b["r"], b["y"]+b["r"]
                )