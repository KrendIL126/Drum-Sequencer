import pygame
from pygame import mixer

pygame.init()

# create app window
WIN_WIDTH = 1650
WIN_HEIGHT = 550
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Drum Sequencer")
pygame.display.set_icon(pygame.image.load("assets/Adrum_icon.bmp"))

# color consts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
DARK_RED = (200, 50, 50)
GREEN = (0, 255, 0)
DARK_GREEN = (50, 200, 50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (150, 75, 0)
LIGHT_BROWN = (152, 118, 84)
DARK_BROWN = (90, 61, 48)

# sounds
BASS = mixer.Sound("assets/bass-drum1.wav")
SNARE = mixer.Sound("assets/snare-drum2.wav")
CLOSED_HIHAT = mixer.Sound("assets/closed-hi-hat2.wav")
OPENED_HIHAT = mixer.Sound("assets/open-hi-hat1.wav")
CRASH = mixer.Sound("assets/crash-cymbal3.wav")
RIDE = mixer.Sound("assets/ride-cymbal1.wav")
TOM1 = mixer.Sound("assets/hi-tom3.wav")
TOM2 = mixer.Sound("assets/hi-tom2.wav")
TOM3 = mixer.Sound("assets/floor-tom1.wav")
BASS.set_volume(1)
SNARE.set_volume(1)
CLOSED_HIHAT.set_volume(1)
OPENED_HIHAT.set_volume(1)
CRASH.set_volume(1)
RIDE.set_volume(1)
TOM1.set_volume(1)
TOM2.set_volume(1)
TOM3.set_volume(1)


def check_on_tiles_click(arr):
    """check: did you click on the tile with the mouse"""
    if arr[0].rect.top <= pygame.mouse.get_pos()[1] <= arr[0].rect.bottom:
        for elem in arr:
            if elem.check_tile_on_click(pygame.mouse.get_pos()[0]):
                break


def draw_buttons():
    """Draw buttons"""
    for button in bpm_buttons_list:
        button.blit()
    pause_button.blit()
    to_start_button.blit()


def draw_texts():
    """Draw texts"""
    bass_text.blit()
    snare_text.blit()
    closed_hihat_text.blit()
    opened_hihat_text.blit()
    crash_text.blit()
    ride_text.blit()
    tom1_text.blit()
    tom2_text.blit()
    tom3_text.blit()


def draw_tiles():
    """Draw tiles"""
    for arr in tiles_list:
        for tile in arr:
            win.blit(tile.surf, tile.rect)


def draw_markup(beats=4):
    """
    draw markup, that split up every 4 tiles
    You can optionally specify 1 argument, that mean amount of tiles to be split
    """
    interval = 10
    for x in range(47 + 25 * beats, WIN_WIDTH - 10, 25 * beats):
        for y in range(100, WIN_HEIGHT - 10, interval + 10):
            pygame.draw.aaline(win, BLACK, (x, y), (x, y + 10))


class Tile:
    """
    Tile class.
    With this class, the program implements tiles. When activated, a sound is playing
    """
    def __init__(self, coords, colors, sound, size=(20, 40)):
        self.surf = pygame.Surface(size)
        self.inactive_color = colors[0]
        self.active_color = colors[1]
        self.current_color = self.inactive_color
        self.surf.fill(self.current_color)
        self.rect = self.surf.get_rect(topleft=coords)
        self.sound = sound

    def change_color(self):
        if self.current_color == self.inactive_color:
            self.current_color = self.active_color
        else:
            self.current_color = self.inactive_color
        self.surf.fill(self.current_color)

    def check_tile_on_click(self, mouse_x):
        if self.rect.left < mouse_x < self.rect.right:
            self.change_color()
            pygame.display.update()
            return True
        return False

    def make_sound(self):
        self.sound.play()


class Line:
    """
    Line class.
    With this class, the program implements line. When a line crosses an activated tile, a sound is played
    """
    def __init__(self, coords, color=RED, speed=1):
        self.surf = pygame.Surface((3, WIN_HEIGHT - 100 - 10))
        self.color = color
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(topright=coords)
        self.speed = speed

    def check_tiles(self):
        for arr in tiles_list:
            for tile in arr:
                if self.rect.right == tile.rect.left and tile.current_color == tile.active_color:
                    tile.make_sound()

    def move_line(self):
        if not pause_button.is_active():
            self.check_tiles()
            self.rect.left += self.speed
            if self.rect.right >= WIN_WIDTH:
                self.rect.right = 50


class Text:
    """
    Text class.
    With this class, the program implements texts. Program prints text on the screen
    """
    def __init__(self, text_font, text, colors, coords, size=(40, 40)):
        self.font = text_font
        self.text = text
        self.text_color = colors[0]
        self.background_color = colors[1]
        self.surf = pygame.Surface(size)
        self.surf.fill(self.background_color)
        self.surf_rect = self.surf.get_rect(topleft=coords)
        self.rendered_text = self.font.render(self.text, 1, self.text_color, self.background_color)
        self.text_rect = self.rendered_text.get_rect(center=(self.surf_rect.center[0], self.surf_rect.center[1]))

    def blit(self):
        win.blit(self.surf, self.surf_rect)
        win.blit(self.rendered_text, self.text_rect)


class Button(Text):
    """
    Button class.
    With this class, the program implements buttons. When you click on button, something happens.
    this class implements several types of buttons: bpm buttons, to-start-button and pause-button
    """
    def __init__(self, text_font, text, colors, coords, size=(100, 40), bpm=0):
        super(Button, self).__init__(text_font, text, colors, coords, size)
        self.inactive_color = colors[2]
        self.current_color = self.inactive_color
        self.set_current_color(self.inactive_color)
        self.bpm = bpm

    def is_active(self):
        if self.current_color == self.background_color:
            return True
        return False

    def set_current_color(self, color):
        self.current_color = color
        self.surf.fill(self.current_color)
        self.rendered_text = self.font.render(self.text, 1, self.text_color, self.current_color)

    def change_color(self):
        if self.surf_rect.left <= pygame.mouse.get_pos()[0] <= self.surf_rect.right:
            if self.current_color == self.inactive_color:
                self.set_current_color(self.background_color)
            else:
                self.set_current_color(self.inactive_color)

    def bpm_button_on_click(self, arr):
        global FPS
        if self.surf_rect.left <= pygame.mouse.get_pos()[0] <= self.surf_rect.right:
            for button in arr:
                if button.is_active():
                    button.set_current_color(button.inactive_color)
                self.set_current_color(self.background_color)
                FPS = round(self.bpm * 0.4166666666)
            return True
        return False

    def to_start_button_on_click(self):
        if self.surf_rect.left <= pygame.mouse.get_pos()[0] <= self.surf_rect.right:
            self.set_current_color(self.background_color)
            line.rect.right = 50


# font and texts
font = pygame.font.SysFont("arial", 24, bold=True)
bass_text = Text(font, "BD", (WHITE, BLUE), (0, 100))
snare_text = Text(font, "SD", (WHITE, YELLOW), (0, 150))
closed_hihat_text = Text(font, "CH", (WHITE, GREEN), (0, 200))
opened_hihat_text = Text(font, "OH", (WHITE, DARK_GREEN), (0, 250))
crash_text = Text(font, "CC", (WHITE, RED), (0, 300))
ride_text = Text(font, "RC", (WHITE, DARK_RED), (0, 350))
tom1_text = Text(font, "T1", (WHITE, LIGHT_BROWN), (0, 400))
tom2_text = Text(font, "T2", (WHITE, BROWN), (0, 450))
tom3_text = Text(font, "T3", (WHITE, DARK_BROWN), (0, 500))

# buttons
bpm_buttons_list = [
    Button(font, "60 BPM", (WHITE, GREEN, GRAY), (50, 20), bpm=60),
    Button(font, "80 BPM", (WHITE, GREEN, GRAY), (160, 20), bpm=80),
    Button(font, "120 BPM", (WHITE, GREEN, GRAY), (270, 20), bpm=120),
    Button(font, "150 BPM", (WHITE, GREEN, GRAY), (380, 20), bpm=150),
    Button(font, "180 BPM", (WHITE, GREEN, GRAY), (490, 20), bpm=180),
    Button(font, "200 BPM", (WHITE, GREEN, GRAY), (600, 20), bpm=200),
    Button(font, "240 BPM", (WHITE, GREEN, GRAY), (710, 20), bpm=240),
    Button(font, "300 BPM", (WHITE, GREEN, GRAY), (820, 20), bpm=300),
    Button(font, "360 BPM", (WHITE, GREEN, GRAY), (930, 20), bpm=360),
]
bpm_buttons_list[0].set_current_color(bpm_buttons_list[0].background_color)

to_start_button = Button(font, "To Start", (WHITE, RED, GRAY), (WIN_WIDTH - 220, 20), (100, 40))
pause_button = Button(font, "Pause", (WHITE, RED, GRAY), (WIN_WIDTH - 110, 20), (100, 40))
pause_button.set_current_color(pause_button.background_color)

# create tiles
tiles_list = [
    [Tile((i, 100), (GRAY, BLUE), BASS) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 150), (GRAY, YELLOW), SNARE) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 200), (GRAY, GREEN), CLOSED_HIHAT) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 250), (GRAY, DARK_GREEN), OPENED_HIHAT) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 300), (GRAY, RED), CRASH) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 350), (GRAY, DARK_RED), RIDE) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 400), (GRAY, LIGHT_BROWN), TOM1) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 450), (GRAY, BROWN), TOM2) for i in range(50, WIN_WIDTH, 25)],
    [Tile((i, 500), (GRAY, DARK_BROWN), TOM3) for i in range(50, WIN_WIDTH, 25)]
]

# create line
line = Line((50, 100))

# start loop
clock = pygame.time.Clock()
FPS = 25  # 25fps ~ 60bpm
run = True
while run:
    # set FPS
    clock.tick(FPS)

    # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if bpm_buttons_list[0].surf_rect.top < pygame.mouse.get_pos()[1] < bpm_buttons_list[0].surf_rect.bottom:
                for btn in bpm_buttons_list:
                    if btn.bpm_button_on_click(bpm_buttons_list):
                        break
                pause_button.change_color()
                to_start_button.to_start_button_on_click()

            check_on_tiles_click(tiles_list[0])
            check_on_tiles_click(tiles_list[1])
            check_on_tiles_click(tiles_list[2])
            check_on_tiles_click(tiles_list[3])
            check_on_tiles_click(tiles_list[4])
            check_on_tiles_click(tiles_list[5])
            check_on_tiles_click(tiles_list[6])
            check_on_tiles_click(tiles_list[7])
            check_on_tiles_click(tiles_list[8])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            to_start_button.set_current_color(to_start_button.inactive_color)

    win.fill(WHITE)

    # draw buttons, texts, tiles, markup
    draw_texts()
    draw_buttons()
    draw_tiles()
    draw_markup()

    # draw line
    win.blit(line.surf, line.rect)
    line.move_line()

    pygame.display.update()
# close app
pygame.quit()
quit()
