import pygame
import os
import json
from PIL import Image

def imageToSurface(image):
    img = image.convert("RGBA")
    size = img.size
    image_data = img.tobytes()
    return pygame.image.fromstring(image_data, size, 'RGBA')

class Frame:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = None
        self.imgSurface = None
    def pos(self):
        return (self.x, self.y)
    def resize(self, size):
        self.img = self.img.resize(size)
        self.imgSurface = imageToSurface(self.img)
    def load(self, file, Mask=None):
        try:
            self.img = loadImg(file)
            if Mask:
                mask = loadImg(Mask).convert('L')
                self.img = Image.composite(self.img, Image.new('RGBA', self.img.size), mask)
            self.imgSurface = imageToSurface(self.img)
        except Exception as e:
            handleCrash(f'error while loading image:{e}')
        return self
    def render(self):
        try:
            if self.img is not None:
                screen.blit(self.imgSurface, self.pos())
        except Exception as e:
            handleCrash(f'error while rendering image:{e}')
        return self

SAVE_FILE_PATH = "./save.json"

def handleCrash(error_message):
    pygame.display.quit()
    
    pygame.display.init()
    
    screen_info = pygame.display.Info()
    size = screen_info.current_h//5

    new_screen = pygame.display.set_mode((screen_info.current_w, size))
    pygame.display.set_caption("Error")

    new_screen.fill((0, 0, 0))

    font = pygame.font.SysFont(None, 20)
    text_surface = font.render('Something went wrong: '+repr(error_message), True, (255, 0, 0))

    text_rect = text_surface.get_rect(center=new_screen.get_rect().center)

    new_screen.blit(text_surface, text_rect)

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()

def save(data):
    try:
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(data, file)
            return None, True
    except FileExistsError or FileNotFoundError as e:
        return e, False

def load():
    try:
        if os.path.exists(SAVE_FILE_PATH):
            with open(SAVE_FILE_PATH, "r") as file:
                return json.load(file), True
        else:
            return {}, False
    except Exception as e:
        handleCrash(e)

def loadImg(file_path):
    if not os.path.exists(file_path):
        handleCrash(f"no image found in {file_path}")
        return None
    
    try:
        rawImage = Image.open(file_path)
    except pygame.error as e:
        handleCrash(f'Pygame error {e}')
        return None
    
    return rawImage

if not os.path.exists(SAVE_FILE_PATH):
    with open(SAVE_FILE_PATH, 'w') as file:
        file.write('')
    save({
        'coins':0,
        'unlockedLevels':[[1,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    })

data, _ = load()

for name, value in data.items():
    exec(f'{name}={value}', globals())

def handleQuit():
    newData = {}
    for name, _ in data.items():
        newData[name] = eval(name)
    save(newData)

menu = 'menu'
scenes = []

class Scene:
    def __init__(self, menu):
        self.menu = menu
        self.frames = []
        scenes.append(self)
    def build(self, frames):
        self.frames.append(*frames)

gameRunning = True

pygame.init()
pygame.display.set_caption('Plants Vs. Zombies')
info = pygame.display.Info()

screen = pygame.display.set_mode((800, 595))
screens = pygame.display.get_window_size()

clock = pygame.time.Clock()

path = 'C:/Users/kaykv/Videos/Roblox/PVZ/images'

mainMenu = Scene('main')

menuBackground = Frame(78,248)
backgroundTree = Frame(0,-70)
backgroundSun = Frame(0,0)
menuGrave = Frame(70,40)

mainMenu.build([
menuBackground.load(f'{path}/mainBackground.jpg', Mask=f'{path}/mainBackgroundMask.png'),
backgroundTree.load(f'{path}/mainBackgroundTree.jpg', Mask=f'{path}/mainBackgroundTreeMask.png'),
backgroundSun.load(f'{path}/backgroundSun.jpg'),
menuGrave.load(f'{path}/menuGrave.jpg', Mask=f'{path}/menuGraveMask.png')
])

backgroundSun.resize(screens)

while gameRunning:
    screen.fill((120,150,255))
    
    for scene in scenes:
        if menu == scene.menu:
            for frame in scene.frames:
                frame.render()

    pygame.display.flip()
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameRunning = False
            handleQuit()
