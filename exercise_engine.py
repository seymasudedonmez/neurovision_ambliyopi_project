import pygame
import random
import math
import sys
import platform

TETROMINOS = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}
COLORS = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]

class GameEngine:
    def __init__(self, duration_sec=1200, single_mode=None):
        pygame.init()
        
        # İşletim sistemi tespiti
        self.os_name = platform.system()
        
        # Tam ekran için optimize edilmiş başlatma
        self.setup_display()
        
        pygame.display.set_caption("VisionFlow Egzersiz")
        self.clock = pygame.time.Clock()
        self.duration = duration_sec
        self.running = True
        
        self.games = ["tetris", "saccadic", "tracking", "gabor", "eye_roll", "cross"]
        self.single_mode = single_mode
        self.current_mode = single_mode.lower() if single_mode else "tetris"
        
        # OYUN ÖZEL DEĞİŞKENLERİ
        self.sac_timer = 0
        self.sac_pos = (self.width//2, self.height//2)
        
        # TETRIS DEĞİŞKENLERİ
        self.grid_w, self.grid_h = 10, 20
        # Ekranın %80'ini kullan, kenarlarda boşluk bırak
        available_width = self.width * 0.8
        available_height = self.height * 0.8
        self.cell_size = min(int(available_width // (self.grid_w + 2)), 
                            int(available_height // (self.grid_h + 2)))
        
        # Merkezde konumlandır ve ekranın içinde kal
        self.grid_offset_x = (self.width - self.grid_w * self.cell_size) // 2
        self.grid_offset_y = (self.height - self.grid_h * self.cell_size) // 2
        
        # Ekranın içinde kalmayı sağla
        margin = 50
        if self.grid_offset_x < margin:
            self.grid_offset_x = margin
        if self.grid_offset_y < margin:
            self.grid_offset_y = margin
        
        self.grid = [[(0,0,0) for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        self.current_piece = self.new_piece()
        self.tetris_timer = 0
        self.fall_speed = 500
        self.lock_delay = 500
        self.lock_timer = 0
        self.piece_locked = False

    def setup_display(self):
        """İşletim sistemine göre ekran ayarları"""
        if self.os_name == "Windows":
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width = self.screen.get_width()
            self.height = self.screen.get_height()
            
            if self.width < 1024 or self.height < 768:
                info = pygame.display.Info()
                self.width = info.current_w
                self.height = info.current_h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
                
        elif self.os_name == "Darwin":
            info = pygame.display.Info()
            self.width = info.current_w
            self.height = info.current_h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            
        else:
            try:
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.width = self.screen.get_width()
                self.height = self.screen.get_height()
            except:
                info = pygame.display.Info()
                self.width = info.current_w
                self.height = info.current_h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        
        print(f"Ekran çözünürlüğü: {self.width}x{self.height}")

    def run(self):
        start_ticks = pygame.time.get_ticks()
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.running = False
                    return False  # Egzersiz tamamlanmadı
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.running = False
                        return False  # Egzersiz tamamlanmadı
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    if self.current_mode == "tetris":
                        if event.key == pygame.K_LEFT: 
                            self.move_piece(-1, 0)
                        if event.key == pygame.K_RIGHT: 
                            self.move_piece(1, 0)
                        if event.key == pygame.K_DOWN: 
                            if not self.move_piece(0, 1):
                                self.lock_piece()
                        if event.key == pygame.K_UP: 
                            self.rotate_piece()
                        if event.key == pygame.K_SPACE:
                            self.hard_drop()

            elapsed = (current_time - start_ticks) / 1000
            remaining = self.duration - elapsed
            
            if remaining <= 0: 
                break
            
            self.screen.fill((10, 10, 25))
            
            if self.single_mode:
                mode_func = f"play_{self.current_mode}"
                if hasattr(self, mode_func):
                    getattr(self, mode_func)(elapsed)
                else:
                    self.play_tetris(elapsed)
            else:
                current_idx = int(elapsed / 180) % len(self.games)
                self.current_mode = self.games[current_idx]
                getattr(self, f"play_{self.current_mode}")(elapsed)
            
            self.draw_hud(remaining, self.current_mode)
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        return True  # Egzersiz başarıyla tamamlandı

    def toggle_fullscreen(self):
        if self.screen.get_flags() & pygame.FULLSCREEN:
            pygame.display.set_mode((self.width, self.height))
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # TETRIS FONKSİYONLARI
    def new_piece(self):
        shape_name = random.choice(list(TETROMINOS.keys()))
        shape = TETROMINOS[shape_name]
        color = random.choice(COLORS)
        return {"shape": shape, "color": color, "x": self.grid_w // 2 - 1, "y": 0}

    def check_collision(self, dx=0, dy=0, shape=None):
        if shape is None: 
            shape = self.current_piece["shape"]
        for px, py in shape:
            nx, ny = self.current_piece["x"] + px + dx, self.current_piece["y"] + py + dy
            if nx < 0 or nx >= self.grid_w: 
                return True
            if ny >= self.grid_h: 
                return True
            if ny >= 0 and self.grid[ny][nx] != (0,0,0): 
                return True
        return False

    def move_piece(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_piece["x"] += dx
            self.current_piece["y"] += dy
            self.lock_timer = pygame.time.get_ticks()
            self.piece_locked = False
            return True
        else:
            # Çarpışma varsa ve aşağı hareket ediyorsa, kilit zamanını kontrol et
            if dy > 0:
                current_time = pygame.time.get_ticks()
                if current_time - self.lock_timer > self.lock_delay:
                    self.lock_piece()
            return False

    # Tetris parça döndürme algoritması
    def rotate_piece(self):
        new_shape = [(-y, x) for x, y in self.current_piece["shape"]]   # Liste üreteci kullanımı
        if not self.check_collision(shape=new_shape):
            self.current_piece["shape"] = new_shape
            self.lock_timer = pygame.time.get_ticks()
            return True
        return False

    def hard_drop(self):
        """Parçayı en alta kadar hızlı düşür"""
        while self.move_piece(0, 1):
            pass
        self.lock_piece()

    def lock_piece(self):
        """Parçayı kilitler ve oyun alanına yerleştirir"""
        # Parçayı oyun alanına kaydet
        for px, py in self.current_piece["shape"]:
            nx, ny = self.current_piece["x"] + px, self.current_piece["y"] + py
            if 0 <= nx < self.grid_w and 0 <= ny < self.grid_h:
                self.grid[ny][nx] = self.current_piece["color"]
        
        # Tam satırları kontrol et ve temizle
        self.clear_completed_lines()
        
        # Yeni parça başlat
        self.current_piece = self.new_piece()
        self.lock_timer = pygame.time.get_ticks()
        
        # Yeni parça için çarpışma kontrolü (oyun bitti mi?)
        if self.check_collision():
            self.grid = [[(0,0,0) for _ in range(self.grid_w)] for _ in range(self.grid_h)]

    def clear_completed_lines(self):
        """Tamamlanan satırları temizler"""
        lines_to_clear = []
        for y in range(self.grid_h):
            if all(self.grid[y][x] != (0,0,0) for x in range(self.grid_w)):
                lines_to_clear.append(y)
        
        # Satırları temizle ve yukarı kaydır
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [(0,0,0) for _ in range(self.grid_w)])

    def play_tetris(self, t):
        """Tetris oyununu güncelle"""
        current_time = pygame.time.get_ticks()
        
        # Otomatik düşürme
        if current_time - self.tetris_timer > self.fall_speed:
            if not self.move_piece(0, 1):
                # Hareket edemiyorsa, parça kilitlenmiştir
                pass
            self.tetris_timer = current_time
        
        start_x = self.grid_offset_x
        start_y = self.grid_offset_y
        
        # Oyun alanı arka planı - EKRAN İÇİNDE
        pygame.draw.rect(self.screen, (30, 30, 40), 
                        (start_x-10, start_y-10, 
                         self.grid_w*self.cell_size+20, 
                         self.grid_h*self.cell_size+20))
        
        # Oyun alanı çerçevesi - ALT SINIR GÖRÜNÜR
        pygame.draw.rect(self.screen, (80, 80, 100), 
                        (start_x-5, start_y-5, 
                         self.grid_w*self.cell_size+10, 
                         self.grid_h*self.cell_size+10), 3)
        
        # ALT SINIR ÇİZGİSİ - BELİRGİN
        bottom_y = start_y + self.grid_h*self.cell_size
        pygame.draw.line(self.screen, (255, 255, 255),
                        (start_x, bottom_y),
                        (start_x + self.grid_w*self.cell_size, bottom_y), 2)
        
        # Sabit blokları çiz
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                if self.grid[y][x] != (0,0,0):
                    rect_x = start_x + x*self.cell_size
                    rect_y = start_y + y*self.cell_size
                    
                    # Ana blok
                    pygame.draw.rect(self.screen, self.grid[y][x], 
                                    (rect_x, rect_y, 
                                     self.cell_size-1, self.cell_size-1))
                    
                    # 3D efekti (üst aydınlık)
                    pygame.draw.rect(self.screen, 
                                    tuple(min(255, c+30) for c in self.grid[y][x]), 
                                    (rect_x, rect_y, 
                                     self.cell_size-1, 3))
        
        # Hareketli parçayı çiz
        for px, py in self.current_piece["shape"]:
            dx, dy = self.current_piece["x"] + px, self.current_piece["y"] + py
            if 0 <= dy < self.grid_h:
                rect_x = start_x + dx*self.cell_size
                rect_y = start_y + dy*self.cell_size
                
                # Ana blok
                pygame.draw.rect(self.screen, self.current_piece["color"], 
                                (rect_x, rect_y, 
                                 self.cell_size-1, self.cell_size-1))
                
                # 3D efekti
                pygame.draw.rect(self.screen, 
                                tuple(min(255, c+40) for c in self.current_piece["color"]), 
                                (rect_x, rect_y, 
                                 self.cell_size-1, 4))

    # DİĞER OYUNLAR ( Saccadic, Tracking, Gabor, Eye Roll, Cross)
    def play_saccadic(self, t):
        if pygame.time.get_ticks() - self.sac_timer > 1000:
            margin = 100
            self.sac_pos = (random.randint(margin, self.width-margin), 
                           random.randint(margin, self.height-margin))
            self.sac_timer = pygame.time.get_ticks()
        
        pygame.draw.circle(self.screen, (255, 50, 50), self.sac_pos, 30)
        pygame.draw.circle(self.screen, (255, 255, 255), self.sac_pos, 10)
        
        center_x, center_y = self.width//2, self.height//2
        pygame.draw.line(self.screen, (255, 255, 255, 128), 
                        (center_x, center_y), self.sac_pos, 2)

    def play_tracking(self, t):
        x = self.width//2 + math.cos(t*0.5)*(self.width/3)
        y = self.height//2 + math.sin(t)*(self.height/4)
        
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        for i in range(20, 0, -2):
            alpha = 100 - i*4
            pygame.draw.circle(surf, (0, 255, 255, alpha), (50, 50), i + 20)
        pygame.draw.circle(surf, (255, 255, 255), (50, 50), 15)
        
        glow = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(glow, (0, 255, 255, 50), (60, 60), 60)
        self.screen.blit(glow, (int(x)-60, int(y)-60))
        
        self.screen.blit(surf, (int(x)-50, int(y)-50))

    def play_gabor(self, t):
        cx, cy = self.width//2, self.height//2
        
        for i in range(-100, 100, 20):
            off = math.sin(t*2 + i*0.1) * 20
            pygame.draw.line(self.screen, (0, 255, 100), 
                            (cx+i, cy-100+off), (cx+i, cy+100+off), 4)
            pygame.draw.line(self.screen, (0, 200, 80, 100), 
                            (cx+i+2, cy-100+off), (cx+i+2, cy+100+off), 2)

    def play_eye_roll(self, t):
        r = 300
        x = self.width//2 + math.cos(t)*r
        y = self.height//2 + math.sin(t)*r
        
        pygame.draw.circle(self.screen, (255, 255, 255), 
                          (self.width//2, self.height//2), 20)
        
        pygame.draw.circle(self.screen, (100, 200, 255), (int(x), int(y)), 40)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), 15)
        
        pygame.draw.line(self.screen, (50, 50, 50, 150), 
                        (self.width//2, self.height//2), (x, y), 3)

    def play_cross(self, t):
        cycle = t % 8
        
        if cycle < 4: 
            start, end = (100, 100), (self.width-100, self.height-100)
            p = cycle/4
        else: 
            start, end = (self.width-100, 100), (100, self.height-100)
            p = (cycle-4)/4
        
        cur_x = start[0] + (end[0]-start[0])*p
        cur_y = start[1] + (end[1]-start[1])*p
        
        pygame.draw.line(self.screen, (255, 255, 255, 100), 
                        (100, 100), (self.width-100, self.height-100), 2)
        pygame.draw.line(self.screen, (255, 255, 255, 100), 
                        (self.width-100, 100), (100, self.height-100), 2)
        
        pygame.draw.circle(self.screen, (255, 0, 255), (int(cur_x), int(cur_y)), 35)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(cur_x), int(cur_y)), 15)

    def draw_hud(self, rem, mode):
        font = pygame.font.SysFont("Arial", 40, bold=True)
        small_font = pygame.font.SysFont("Arial", 25)
        
        time_text = font.render(f"{int(rem//60)}:{int(rem%60):02d}", True, (255,255,255))
        self.screen.blit(time_text, (50, 50))
        
        mode_text = font.render(f"MOD: {mode.upper()}", True, (0,255,200))
        self.screen.blit(mode_text, (self.width - 400, 50))
        
        exit_text = small_font.render("ÇIKMAK İÇİN ESC TUŞUNA BASIN", True, (200,200,200))
        self.screen.blit(exit_text, (self.width//2 - 150, self.height - 50))