import pygame
import os
import random
import webbrowser
import torch
import torch.nn as nn
import numpy as np
from collections import defaultdict
# --- Constants ---
TILE_SIZE = 16
SCREEN_WIDTH = 50 * TILE_SIZE  # 800
SCREEN_HEIGHT = 38 * TILE_SIZE # 608
BG_COLOR = (40, 42, 88)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GOLD = (255, 215, 0)
ORANGE_GOLD = (235,140,30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PLAYER_SCALE = 0.85
ANIMATION_SPEED = 100 # milliseconds per frame

################################################################## ASSETS ##################################################################
TILE_ASSET_PATH = os.path.join('assets', 'environment', 'PNG', 'Tiles')
OBJECT_ASSET_PATH = os.path.join('assets', 'environment', 'PNG', 'Objects')
PLAYER_ASSET_PATH = os.path.join('assets', 'Players') # Corrected folder name
# Load all the google fonts 
START_SCREEN_FONT_PATH =  os.path.join('assets', 'fonts', 'CinzelDecorative-Bold.ttf')
IN_GAME_FONT_PATH =  os.path.join('assets', 'fonts', 'MedievalSharp-Regular.ttf')
CREDITS_FONT_PATH =  os.path.join('assets', 'fonts', 'IMFellEnglishSC-Regular.ttf')
# start_screen font -> CinzelDecorative-Black.ttf
# In-game font -> MedievalSharp-Regular.ttf
# Credits Font -> IMFellEnglishSC-Regular.ttf
ALMANAC = {
    "Fighter": {
        "description": "The Fighter is a versatile and resilient character, excelling in close combat with a balanced mix of offense and defense. With a wide array of attacks and the ability to block incoming damage, the Fighter is a formidable opponent on the battlefield. Their animations include powerful strikes, agile dodges, and a sturdy shield stance, making them a well-rounded choice for players who enjoy a tactical approach to combat.",
        "Attack_1": {"damage": 5},
        "Attack_2": {"damage": 8},
        "Attack_3": {"damage": 12},
        "Shield": {"block_percentage": 20},
    },

    "Samurai": {
        "description": "The Samurai is a swift and precise character, specializing in quick strikes and evasive maneuvers. With a focus on speed and agility, the Samurai can unleash a flurry of attacks that can overwhelm opponents. Their animations feature rapid slashes, graceful jumps, and a unique parry move that allows them to counter enemy attacks. The Samurai is ideal for players who prefer a hit-and-run playstyle and enjoy mastering timing and precision in combat.",
        "Attack_1": {"damage": 4},
        "Attack_2": {"damage": 7},
        "Attack_3": {"damage": 15},
        "Shield": {"block_percentage": 25},
    },
    "Shinobi": {
        "description" : "The Shinobi is a stealthy and agile character, adept at using a variety of weapons and tools to outmaneuver opponents. With a focus on versatility and surprise attacks, the Shinobi can adapt to different combat situations with ease. Their animations include swift strikes with a katana, throwing shurikens, and a unique smoke bomb move that allows them to disappear and reappear in different locations. The Shinobi is perfect for players who enjoy a strategic and unpredictable playstyle, utilizing both offense and evasion to gain the upper hand in battle.",
        "Attack_1": {"damage": 6},
        "Attack_2": {"damage": 9},
        "Attack_3": {"damage": 14},
        "Shield": {"block_percentage": 30},
    }
}
################################################################## LEVEL DATA ##############################################################
LEVEL_MAP = [
    [0, 0, 0, 0, 106, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 106, 101, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 93, 101, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 118, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 118, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 118, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 118, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [53, 54, 54, 55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 54, 54, 54, 54, 57, 0, 0, 0, 0, 0, 0, 0, 0],
    [65, 66, 66, 67, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 68, 66, 66, 66, 66, 69, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [18, 19, 19, 19, 19, 19, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [30, 31, 31, 31, 31, 31, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5, 4, 4, 4, 4, 4, 4, 4, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 43, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 43, 43, 43, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 42, 43, 43, 43, 43, 43, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [88, 89, 89, 89, 89, 89, 90, 43, 43, 43, 43, 43, 43, 43, 44, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [93, 93, 93, 93, 93, 93, 94, 95, 95, 95, 95, 95, 95, 95, 96, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [127, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 129],
    [130, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 132],
]
OBJECT_LIST = [
    ('chain1', 7, 3), ('walls1', 24, 6), ('chest_closed', 36, 6), ('torch', 43, 6),
    ('walls1', 2, 7), ('lever1', 4, 11), ('barrel', 17, 11), ('door2', 3, 24),
    ('vase', 16, 28), ('shield', 22, 17), ('stairs_part4', 33, 16), ('stairs_part3', 33, 17),
    ('stairs_part2', 33, 18), ('stairs_part1', 33, 19), ('stairs_part4', 33, 20),
    ('stairs_part3', 33, 21), ('stairs_part2', 33, 22), ('stairs_part1', 33, 23),
    ('stairs_part4', 33, 24), ('stairs_part3', 33, 25), ('stairs_part2', 33, 26),
    ('stairs_part1', 33, 27),
]

################################################################## SELECTED PLAYER #########################################################
selected_player = 'Fighter'
players = ["Fighter", "Samurai", "Shinobi"]
selected_player_index = players.index(selected_player)
############################################################### HELPER FUNCTIONS ###########################################################
def safe_load_font(font_path, size):
    try:
        return pygame.font.Font(font_path, size)
    except:
        return pygame.font.SysFont("arial", size, bold=True)
def load_animations(character_type, scale):
    """Loads all animation sequences for a given character."""
    animations = {}
    char_path = os.path.join(PLAYER_ASSET_PATH, character_type)
    if not os.path.isdir(char_path):
        return animations

    animation_names = ['Idle', 'Run', 'Attack_1', 'Attack_2', 'Attack_3', 'Dead', 'Hurt', 'Jump', 'Shield', 'Walk']
    for anim_name in animation_names:
        # Case-insensitive filename matching
        found_file = None
        for f in os.listdir(char_path):
            if f.lower() == f"{anim_name.lower()}.png":
                found_file = f
                break
        
        if found_file:
            filepath = os.path.join(char_path, found_file)
            sprite_sheet = pygame.image.load(filepath).convert_alpha()
            frame_width = sprite_sheet.get_height() # Assuming square frames
            frame_height = sprite_sheet.get_height()
            
            # Handle sprite sheets that might not have a perfect width
            if frame_width == 0: continue
            num_frames = sprite_sheet.get_width() // frame_width
            
            frames = []
            for i in range(num_frames):
                frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame_surface.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
                scaled_frame = pygame.transform.scale(frame_surface, (int(frame_width * scale), int(frame_height * scale)))
                frames.append(scaled_frame)
            animations[anim_name] = frames
    return animations
def draw_health_bar(surface, x, y, current_health, animated_health,max_health):
    """Draws a health bar on the given surface."""
    bar_width = 200
    bar_height = 20
    health_ratio = current_health / max_health
    animated_health_ratio = animated_health / max_health
    # Draw background
    pygame.draw.rect(surface, RED, (x,y, bar_width, bar_height))
    # Draw the animated trail
    pygame.draw.rect(surface, YELLOW, (x, y, bar_width * animated_health_ratio, bar_height))
    # Draw the current health
    pygame.draw.rect(surface, GREEN, (x, y, bar_width * health_ratio, bar_height))
    # Draw border
    pygame.draw.rect(surface, WHITE, (x,y, bar_width, bar_height), 2)
def draw_outline(surface, rect, color, width =2):
    "Draws an outline around the non-transparent pixels of a surface."
    mask = pygame.mask.from_surface(surface)
    outline_points = mask.outline()
    translated_points = [(p[0] + rect.x, p[1] + rect.y) for p in outline_points]
    if len(translated_points) > 1:
        pygame.draw.lines(pygame.display.get_surface(), color, False, translated_points, width)
def play_sound(path):
    """Plays the sound according to the path."""
    try:
        pygame.mixer.Sound(path).play()
    except:
        print("warning: The sound is not found at: {}".format(path))
def draw_game_world(screen, background_cache, assets):
    """Draws the game world, including the background and platforms."""
    screen.blit(background_cache, (0, 0))

    for platform in assets['platforms']:
        platform.update()
        screen.blit(platform.image, platform.rect)

class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class FloatingDamageText:
    def __init__(self, x, y, text, color):
        # Center the text slightly above the player's head coordinate
        self.x = x - 10 
        self.y = y - 20
        self.text = f"-{text}" if str(text).isdigit() else text
        self.color = color
        self.alpha = 255
        self.font = safe_load_font(None, 24) # Made font larger and crisp

        # Exploding arc fountain physics
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-7.0, -4.0) # Shoots up forcefully
        self.gravity = 0.35                  # Pulls down over time

    def update(self):
        # FIX: Gravity now correctly pulls down on the Y axis, not the X axis
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        # Smooth fade control
        self.alpha -= 5
        return self.alpha > 0

    def draw(self, screen):
        if self.alpha <= 0: return
        text_surf = self.font.render(self.text, True, self.color)
        
        # Proper alpha handling surface container
        alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        alpha_surf.fill((255, 255, 255, self.alpha))
        text_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(text_surf, (int(self.x), int(self.y)))

class MovingPlatform:
    """A class for the moving brick platforms in the background."""
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.start_x = x
        self.speed = random.choice([-1, 1]) * random.uniform(0.5, 1.5)

    def update(self):
        """Moves the platform and wraps it around the screen."""
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
            
    def draw(self, screen):
        """Draws the platform."""
        screen.blit(self.image, self.rect)

class Button:
    """A simple button class."""
    def __init__(self, x, y, width, height, text, font, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.is_hovered = False
        self.glow = 0

    def handle_event(self, event):
        """Handles mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                self.callback()

    def draw(self, screen):
        """Draws the button."""
        self.glow = min(255, self.glow + 20) if self.is_hovered else max(0, self.glow - 15)
        base_color = (60, 40, 30) if not self.is_hovered else (110, 70, 45)
        pygame.draw.rect(screen, base_color, self.rect, border_radius=8)
        boder_color  = GOLD if self.is_hovered else (181, 136, 99)
        pygame.draw.rect(screen, boder_color, self.rect, 2, border_radius=8)

        if self.glow > 0:
            g_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            g_surf.fill((255, 215, 0, int(self.glow * 0.15)))
            screen.blit(g_surf, self.rect.topleft)

        text_surf = self.font.render(self.text, True, WHITE)
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

class TextLink:
    """A class for creating clickable text links."""
    def __init__(self, x, y, text, font, url, color = GREY, hover_link_color = WHITE):
        self.text = text
        self.font = font
        self.url  = url
        self.color = color
        self.hover_color  = hover_link_color
        self.is_hovered = False
        self.text_surf = self.font.render(self.text, True, self.color)
        self.rect = self.text_surf.get_rect(topleft=(x,y))
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered and event.button == 1:
            if self.url:
                webbrowser.open(self.url)
    def draw(self, screen):
        color = self.hover_color
        text_surf = self.font.render(self.text, True, color)
        self.rect = text_surf.get_rect(topleft = self.rect.topleft)
        screen.blit(text_surf, self.rect)

class Player:
    def __init__(self, x, y, character_type, scale=PLAYER_SCALE):
        self.animations = load_animations(character_type, scale)
        self.character_type = character_type
        self.action = 'Idle'
        self.frame_index = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_force = -13.5
        self.gravity = 0.6
        self.on_ground = True
        self.facing_right = True
        self.health = 100.0
        self.max_health = 100.0
        self.animated_health = 100.0
        self.has_damaged = False
        self.knockback_vx = 0.0
        
        # Combat Timer Guard to prevent single-frame damage repetition spam
        self.hurt_timer = 0 

        if self.animations and self.action in self.animations:
            self.image = self.animations[self.action][self.frame_index]
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            self.image = pygame.Surface((int(32*scale), int(32*scale)), pygame.SRCALPHA)
            self.rect = self.image.get_rect(midbottom=(x, y))

        self.update_time = pygame.time.get_ticks()

    def move(self, keys):
        current_time = pygame.time.get_ticks()
        dx = 0

        # Only accept directional input if not actively reeling back from a hit
        if current_time > self.hurt_timer:
            if keys[pygame.K_a]:
                dx -= self.speed
                self.facing_right = False
                if self.on_ground and not self.action.startswith("Attack"): self.action = "Walk"
            elif keys[pygame.K_d]:
                dx += self.speed
                self.facing_right = True
                if self.on_ground and not self.action.startswith("Attack"): self.action = "Walk"
            elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if self.on_ground and not self.action.startswith("Attack"):
                    dx += self.speed * (1 if self.facing_right else -1)
                    self.action = "Run"
            else:
                if self.on_ground and not self.action.startswith("Attack") and self.action != "Shield":
                    self.action = "Idle"
                    
        # physics friction to our horizontal knockback decay loop
        dx += self.knockback_vx
        if self.action=="Hurt":
            self.knockback_vx*= 0.85
        else:
            self.knockback_vx*=0.70
        if abs(self.knockback_vx) < 0.1:
            self.knockback_vx = 0.0

        # Jump execution mechanics
        if keys[pygame.K_SPACE] and self.on_ground and current_time > self.hurt_timer:
            self.vel_y = self.jump_force
            self.on_ground = False
            self.action = "Jump"

        # Apply gravity processing down onto Y-axis map coordinates
        self.vel_y += self.gravity
        dy = self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Keep characters bounded comfortably inside visible display viewport margins
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        # Floor collision resolution loop 
        ground_y = SCREEN_HEIGHT - 30
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True
            if self.action == "Jump": self.action = "Idle"

    def choose_action(self, keys):
        if self.health <= 0 or pygame.time.get_ticks() < self.hurt_timer: return
        
        # Guard clause: Allow attack animations to finish completely without interrupting intermediate frames
        if self.action.startswith("Attack") and self.frame_index < len(self.animations[self.action]) - 1:
            return

        if keys[pygame.K_j]:
            self.action = "Attack_1"
            self.has_damaged = False
            self.frame_index = 0
        elif keys[pygame.K_k]:
            self.action = "Attack_2"
            self.has_damaged = False
            self.frame_index = 0
        elif keys[pygame.K_l]:
            self.action = "Attack_3"
            self.has_damaged = False
            self.frame_index = 0
        elif keys[pygame.K_s]:
            self.action = "Shield"

    def update_status(self):
        if self.health <= 0:
            self.health = 0
            self.action = "Dead"
            return
            
        # FIX: Removed the buggy frame-locking condition that overwrote manual state handling!
        if self.action == "Hurt" and pygame.time.get_ticks() > self.hurt_timer:
            self.action = "Idle"
            
        # Passively scale regeneration safely up towards max threshold bounds
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + 0.02)

    def fight_with_enemy(self, enemy, floating_texts):
        player_hitbox = self.get_hitbox()
        enemy_hitbox = enemy.get_hitbox()

        if not player_hitbox.colliderect(enemy_hitbox) or enemy.health <= 0:
            return

        if self.action.startswith("Attack") and not self.has_damaged:
            base_damage = ALMANAC[self.character_type][self.action]["damage"]
            
            # Shifting impulse tracking calculation vectors based on facing path direction 
            attack_direction = 1 if self.facing_right else -1
            victim_knockback_force = 14.0 
            attacker_recoil_force = 4.0
            
            # Lock out target's active inputs during hit-stun window (350 milliseconds)
            enemy.hurt_timer = pygame.time.get_ticks() + 300
            enemy.action = "Hurt"
            enemy.frame_index = 0

            if enemy.action == "Shield":
                block_pct = ALMANAC[enemy.character_type]["Shield"]["block_percentage"]
                final_dmg = max(0, base_damage * (1 - block_pct / 100.0))
                enemy.health -= final_dmg
                enemy.knockback_vx = attack_direction * (victim_knockback_force * 0.5)
                self.knockback_vx = -attack_direction * (attacker_recoil_force * 1.5)
                
                # Shield Block: Clean Yellow Font indicator
                floating_texts.append(FloatingDamageText(enemy.rect.centerx, enemy.rect.top, str(int(final_dmg)), YELLOW))
            else:
                enemy.health -= base_damage
                enemy.knockback_vx = attack_direction * (victim_knockback_force)
                self.knockback_vx = -attack_direction * (attacker_recoil_force)
                
                # Normal Hit: Clean Grey indicator as requested
                floating_texts.append(FloatingDamageText(enemy.rect.centerx, enemy.rect.top, str(int(base_damage)), RED))
            
            enemy.animated_health = max(0, enemy.health)
            self.has_damaged = True 

    def update(self):
        if not self.animations or self.action not in self.animations or not self.animations[self.action]:
            return
            
        if pygame.time.get_ticks() - self.update_time > ANIMATION_SPEED:
            self.update_time = pygame.time.get_ticks()
            old_midbottom = self.rect.midbottom

            if self.action == "Dead":
                # Lock the last frame of the death animation to prevent looping
                if self.frame_index < len(self.animations[self.action]) - 1:
                    self.frame_index += 1
            else:
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.action])
            self.image = self.animations[self.action][self.frame_index]

            # Loop check to cleanly switch out of finished attack sequences
            if self.action.startswith("Attack") and self.frame_index == 0:
                self.action = "Idle"

            new_rect = self.image.get_rect()
            new_rect.midbottom = old_midbottom
            self.rect = new_rect

    def draw(self, screen):
        image = self.image
        if not self.facing_right:
            image = pygame.transform.flip(self.image, True, False)
        screen.blit(image, self.rect)

    def draw_overhead_hp(self, screen, animated_hp):
        if self.health <= 0: return
        bar_w = 60
        bar_h = 6
        bar_x = self.rect.centerx - bar_w // 2
        bar_y = self.rect.top - 15

        ratio  = max(0.0, min(1.0, self.health / self.max_health))
        anim_ratio = max(0.0, min(1.0, animated_hp / self.max_health))

        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, bar_w * anim_ratio, bar_h))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_w * ratio, bar_h))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_w, bar_h), 1)

    def get_hitbox(self):
        return self.rect.inflate(-int(self.rect.width* 0.4), 0)
################################################ GAME STATE FUNCTIONS ##########################################################

def start_screen(screen, clock, background_cache, assets):

    global game_state

    # Fonts
    title_font = pygame.font.Font(START_SCREEN_FONT_PATH, 44)
    button_font = pygame.font.Font(START_SCREEN_FONT_PATH, 24)
    # Panel
    panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 160, 400, 360)
    # Buttons
    buttons = [
        Button(SCREEN_WIDTH // 2 - 160, 220, 320, 50, "BATTLE START", button_font, lambda: set_state("PLAY MODE")),
        Button(SCREEN_WIDTH // 2 - 160, 290, 320, 50, "ROSTER SELECT", button_font, lambda: set_state("CUSTOMIZE PLAYER")),
        Button(SCREEN_WIDTH // 2 - 160, 360, 320, 50, "COMBAT INPUTS", button_font, lambda: set_state("CONTROLS")),
        Button(SCREEN_WIDTH // 2 - 160, 430, 320, 50, "STAGE CREDITS", button_font, lambda: set_state("CREDITS")),
    ]
    # Selected Player Index
    def set_state(state):
        global game_state
        game_state = state
    while game_state == "START":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_state = "QUIT"
            for btn in buttons: btn.handle_event(event)
        draw_game_world(screen, background_cache, assets)

        pod_char = assets["players"][selected_player_index]
        pod_char.rect.midbottom = (90, SCREEN_HEIGHT - 30)
        pod_char.update()
        pod_char.draw(screen)

        # PANEL BACKPLATE 
        glass = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        glass.fill((20,20,35,215))
        screen.blit(glass, panel_rect.topleft)
        pygame.draw.rect(screen, GOLD, panel_rect, 2, border_radius=18)
        # Title Text
        title_text = title_font.render("FIGHTER COMBAT", True, WHITE)
        title_x = SCREEN_WIDTH // 2 
        title_y = panel_rect.y - 75
        screen.blit(title_text, title_text.get_rect(center=(title_x, title_y)))
        # Draw buttons
        for btn in buttons: btn.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def play_mode_screen(screen,clock, background_cache):
    """Display the play screen"""
    global game_state
    global selected_player_index
    button_font = pygame.font.Font(IN_GAME_FONT_PATH, 28)
    glass_surface  = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    glass_surface.fill((0,0,0, 150))

    def play_ai_cb():
        global game_state
        game_state = "GAME"
    buttons = [
        Button(SCREEN_WIDTH // 2 - 150, 330, 300, 60, "Play with AI", button_font, play_ai_cb),
    ]
    while game_state == "PLAY MODE":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_state = "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: game_state = "START"
            for button in buttons: button.handle_event(event)
        if game_state != "PLAY MODE": break
        screen.blit(background_cache, (0,0))
        screen.blit(glass_surface, (0,0))
        for button in buttons: button.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def game_loop(screen, clock, background_cache, assets):
    """The main game loop where the action happens."""
    global game_state 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ai_brain = QNetwork(state_dim=9, action_dim=8).to(device)
    try:
        model_path = os.path.join(os.getcwd(), "custom_pytorch_dqn_fighter.pth")
        ai_brain.load_state_dict(torch.load(model_path, map_location=device))
        ai_brain.eval()
    except Exception as e:
        print(f"Warning: Model file not found, AI target falls back to default layout. Error: {e}")
    main_player = Player(100,578, selected_player, scale=PLAYER_SCALE)
    available_chars = ["Shinobi", "Samurai", "Fighter"]
    chosen_ai_char = random.choice(available_chars)
    ai_player = Player(650, 578, chosen_ai_char, scale=PLAYER_SCALE)
    combat_active = True


    floating_texts = []
    name_font = pygame.font.Font(IN_GAME_FONT_PATH, 20)
    countdown_font = pygame.font.Font(IN_GAME_FONT_PATH, 55)
    animation_speed = 0.5

    # Countdown setup
    countdown_items = ["3", "2", "1", "FIGHT NOW!"]
    countdown_index = 0
    last_countdown_tick = pygame.time.get_ticks()
    in_countdown = True
    # empty_kiys to prevent the moment
    empty_keys = defaultdict(bool)

    ai_decision_timer = 0
    current_ai_action = 0
    cached_ai_keys = defaultdict(bool)
    ai_attack_recovery_until = 0

    ai_turn_target_right = False
    ai_turn_timer = 0
    human_turn_target_right = True
    human_turn_timer = 0

    hitstop_frames = 0
    screen_shake_intensity = 0

    ai_personality_aggression = random.uniform(0.4,1.0)

    # ZOOM PLAYER CINEMATICS
    intro_state = "PLAYER_ZOOM"
    intro_timer_start = pygame.time.get_ticks()
    current_zoom_level = 1.0
    target_zoom_level = 1.5
    camera_x,camera_y = SCREEN_WIDTH//2, SCREEN_HEIGHT//2


    while game_state == "GAME":
        current_time = pygame.time.get_ticks()
        intro_elapsed = current_time - intro_timer_start

        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_state = "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:game_state = "START"

        if game_state != "GAME": # Exit loop if state changed
            break

        if hitstop_frames > 0:
            hitstop_frames -= 1
            pygame.display.flip()
            clock.tick(60)
            continue

        if in_countdown:
            if intro_state == "PLAYER_ZOOM":
                target_zoom_level = 1.6
                camera_x = main_player.rect.centerx
                camera_y = main_player.rect.centery- 50
                if intro_elapsed > 1500:
                    intro_state = "AI_ZOOM"
            elif intro_state == "AI_ZOOM":
                target_zoom_level = 1.6
                camera_x = ai_player.rect.centerx
                camera_y = ai_player.rect.centery - 50
                if intro_elapsed > 3000:
                    intro_state = "READY_COUNTDOWN"
            elif intro_state=="READY_COUNTDOWN":
                target_zoom_level = 1.0
                camera_x = SCREEN_WIDTH//2
                camera_y = SCREEN_HEIGHT//2


        if not in_countdown:
            keys = pygame.key.get_pressed()
            should_human_face_right = main_player.rect.x < ai_player.rect.x
            if should_human_face_right != human_turn_target_right:
                human_turn_target_right = should_human_face_right
                human_turn_timer = current_time + 120
            if current_time > human_turn_timer:
                main_player.facing_right = human_turn_target_right

            if main_player.health > 0:
                main_player.move(keys)
                main_player.choose_action(keys)
            else:
                main_player.move(empty_keys)
                main_player.update_status()  
                      
            if ai_player.health > 0:
                should_ai_face_right = ai_player.rect.x < main_player.rect.x

                if should_ai_face_right != ai_turn_target_right:
                    ai_turn_target_right = should_ai_face_right
                    ai_turn_timer = current_time + 120
                
                if current_time >= ai_turn_timer:
                    ai_player.facing_right = ai_turn_target_right

                ai_is_attacking = ai_player.action.startswith("Attack")
                if current_time - ai_decision_timer  > 120 and not ai_is_attacking:
                    ai_decision_timer = current_time
                    relative_x = float(main_player.rect.x - ai_player.rect.x)
                    distance = float(abs(relative_x))
                    health_diff = float(main_player.health - ai_player.health)
                    
                    ai_attacking = 1.0 if ai_player.action.startswith("Attack") else 0.0
                    enemy_attacking = 1.0 if main_player.action.startswith("Attack") else 0.0

                    ai_grounded = 1.0 if ai_player.on_ground else 0.0
                    enemy_grounded = 1.0 if main_player.on_ground else 0.0
                    current_obs_state = np.array([
                        relative_x,
                        distance,
                        ai_player.health,
                        main_player.health,
                        health_diff,
                        ai_attacking,
                        enemy_attacking,
                        ai_grounded,
                        enemy_grounded
                    ], dtype=np.float32)

                    state_tensor = torch.FloatTensor(current_obs_state).to(device)
                    with torch.no_grad():
                        ai_action  = ai_brain(state_tensor).argmax().item()
                    # Map the AI's chosen action to the corresponding key presses
                    # AI PERSONALITY AGGRESSION CHECKS
                    if distance < 90 and ai_personality_aggression > 0.82 :
                        if current_ai_action in [0,1,2]: current_ai_action = random.choice([4,5,6])
                    elif distance < 110 and ai_personality_aggression < 0.50:
                        if current_ai_action in [4,5,6] and random.random() < 0.6: current_ai_action = 7 if random.random() < 0.5 else 1

                    if current_time >= ai_attack_recovery_until or current_ai_action not in [4,5,6]:
                        if ai_action == 1:cached_ai_keys[pygame.K_a] = True       # Move Left
                        elif ai_action == 2: cached_ai_keys[pygame.K_d] = True     # Move Right
                        elif ai_action == 3: cached_ai_keys[pygame.K_SPACE] = True # Jump
                        elif ai_action == 4: cached_ai_keys[pygame.K_j] = True     # Attack 1
                        elif ai_action == 5: cached_ai_keys[pygame.K_k] = True     # Attack 2
                        elif ai_action == 6: cached_ai_keys[pygame.K_l] = True     # Attack 3
                        elif ai_action == 7: cached_ai_keys[pygame.K_LCTRL] = True # Run
                        elif ai_action == 8: cached_ai_keys[pygame.K_RCTRL] = True # RUN
                ai_player.move(cached_ai_keys)
                ai_player.choose_action(cached_ai_keys)
                if ai_is_attacking and ai_player.frame_index == len(ai_player.animations[ai_player.action])-1:
                    ai_attack_recovery_until = current_time + 250

            else:
                ai_player.move(empty_keys)
                ai_player.update_status()

            if combat_active:
                prev_human_hp = main_player.health
                prev_ai_hp = ai_player.health

                main_player.fight_with_enemy(ai_player, floating_texts)
                ai_player.fight_with_enemy(main_player, floating_texts)

                if main_player.health < prev_human_hp or ai_player.health < prev_ai_hp:
                    hitstop_frames = 4
                    if main_player.action == "Attack_3" or ai_player.action == "Attack_3":
                        screen_shake_intensity = 8


        else:
            # stops ai and player from moving during countdown
            main_player.move(empty_keys)
            ai_player.move(empty_keys)

            main_player.choose_action(empty_keys)
            ai_player.choose_action(empty_keys)
            


        ## Health bound check
        
        if main_player.health <= 0:
            main_player.health = 0
            main_player.action = "Dead"
            combat_active = False
            target_zoom_level = 1.8
            camera_x = main_player.rect.centerx
            camera_y = main_player.rect.centery-30
            main_player.move(empty_keys)
            main_player.update_status()
        if ai_player.health <= 0:
            ai_player.health = 0
            ai_player.action = "Dead"
            combat_active = False
            ai_player.move(empty_keys)
            ai_player.update_status()



        main_player.update()
        ai_player.update()
        main_player.update_status()
        ai_player.update_status()

        offset_x = 0 
        offset_y = 0
        if screen_shake_intensity > 0:
            offset_x = random.randint(-screen_shake_intensity, screen_shake_intensity)
            offset_y = random.randint(-screen_shake_intensity, screen_shake_intensity)
            screen_shake_intensity -= 1
        screen.fill(BG_COLOR)

        shake_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        draw_game_world(shake_surface, background_cache, assets)
        main_player.draw(shake_surface)
        ai_player.draw(shake_surface)

        if main_player.animated_health > main_player.health: main_player.animated_health -= animation_speed
        if ai_player.animated_health > ai_player.health: ai_player.animated_health -= animation_speed
        
        main_player.draw_overhead_hp(shake_surface, main_player.animated_health)
        ai_player.draw_overhead_hp(shake_surface, ai_player.animated_health)
        
        for text in floating_texts[:]:
            if not text.update():
                floating_texts.remove(text)
            else:
                text.draw(shake_surface)

        # STATS BOX
        stats_box = pygame.Surface((260, 90), pygame.SRCALPHA)
        stats_box.fill((15,10,5,140))
        pygame.draw.rect(stats_box, ORANGE_GOLD, (0,0,260,90), 2, border_radius=6)
        txt_usr_stat = name_font.render(f"Player State: {main_player.action}", True, WHITE)
        txt_ai_stat = name_font.render(f"AI Target State: {ai_player.action}", True, GOLD)
        stats_box.blit(txt_usr_stat, (15, 15))
        stats_box.blit(txt_ai_stat, (15, 50))
        shake_surface.blit(stats_box, (SCREEN_WIDTH - 260, SCREEN_HEIGHT // 2 - 100))

        current_zoom_level += (target_zoom_level - current_zoom_level) * 0.08
        if current_zoom_level > 1.01:
            scaled_w = int(SCREEN_WIDTH / current_zoom_level)
            scaled_h =  int(SCREEN_HEIGHT / current_zoom_level)

            crop_x = max(0, min(camera_x - scaled_w  // 2, SCREEN_WIDTH - scaled_w))
            crop_y = max(0,  min(camera_y - scaled_h // 2, SCREEN_HEIGHT - scaled_h))
        screen.blit(shake_surface, (offset_x, offset_y))
        
        if in_countdown:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,150))

            screen.blit(overlay, (0,0))
            current_text = countdown_items[countdown_index]
            text_surf = countdown_font.render(current_text, True, WHITE)
            screen.blit(text_surf, text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

            if current_time - last_countdown_tick > 800:
                last_countdown_tick = current_time
                countdown_index += 1
                if countdown_index >= len(countdown_items):
                    in_countdown = False
        if not combat_active:
            end_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            end_overlay.fill((10, 8, 12,180))
            screen.blit(end_overlay,(0,0))

            if main_player.health <= 0:
                result_text = "You are Defeated"
                text_color = RED
            else:
                result_text = "You Won"
                text_color = GREEN


        pygame.display.flip()
        clock.tick(60)

def customize_player_screen(screen, clock, background_cache, assets):
    """Displays the players onto screen for customization."""
    global game_state
    global selected_player
    
    title_font = pygame.font.Font(IN_GAME_FONT_PATH, 50)
    char_font = pygame.font.Font(IN_GAME_FONT_PATH, 28)

    fighter_display = Player(SCREEN_WIDTH * 0.25,300, "Fighter", scale= PLAYER_SCALE)
    samurai_display = Player(SCREEN_WIDTH * 0.50,300, "Samurai", scale= PLAYER_SCALE)
    shinobi_display = Player(SCREEN_WIDTH * 0.75,300, "Shinobi", scale= PLAYER_SCALE)
    player_options = [fighter_display, samurai_display, shinobi_display]
    def back_to_menu_cb():
        global game_state
        game_state = "START"
    
    back_button = Button(SCREEN_WIDTH // 2 -75, SCREEN_HEIGHT - 100, 150, 50, "Back", char_font,back_to_menu_cb )

    while game_state == "CUSTOMIZE PLAYER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click on mouse
                    clicked_on_player = False
                    for player in player_options:
                        if player.rect.collidepoint(event.pos):
                            clicked_on_player = True
                            selected_player = player.character_type
                            break
                    if not clicked_on_player:
                        back_button.handle_event(event)
            if event.type == pygame.MOUSEMOTION:
                back_button.handle_event(event)
        if game_state != "CUSTOMIZE PLAYER": # Exit loop if state changed
            break

        for player in player_options:
            player.update()
        
        screen.blit(background_cache, (0,0))
        # Draw title
        title_surf = title_font.render("Choose Your Player", True, WHITE)
        title_rect = title_surf.get_rect(center = (SCREEN_WIDTH// 2, 100))
        screen.blit(title_surf, title_rect)

        # Draw players
        for player in player_options:
            player.draw(screen)
            name_surf = char_font.render(player.character_type,True, WHITE)
            name_rect = name_surf.get_rect(center = (player.rect.centerx, player.rect.bottom  + 20 ))

            if player.character_type == selected_player:
                draw_outline(player.image, player.rect, GOLD)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)
def credits_screen(screen, clock):
    """Displays the credits screen."""
    global game_state 
    title_font = pygame.font.Font(CREDITS_FONT_PATH, 40)
    text_font = pygame.font.Font(CREDITS_FONT_PATH, 22)
    
    # --- Create Text and Link Objects ---
    # Line 1
    design_text = TextLink(0, 200, "Design and Programming:", text_font, "https://github.com/Sanjoli04", color=BLACK)
    sanjoli_link = TextLink(0, 200, "Sanjoli Vashisth", text_font, "https://github.com/Sanjoli04") 
    
    # Line 2
    assets_text = TextLink(0, 250, "Pixel Art Assets by:", text_font, "https://craftpix.net/", color=BLACK)
    craftpix_link = TextLink(0, 250, "CraftPix.Net", text_font, "https://craftpix.net/")
    
    # Line 3 - Start Screen Music
    music_text1 = TextLink(0, 300, "Start Screen Music by:", text_font, "https://pixabay.com/users/white_records-32584949/", color=BLACK)
    maksym_link = TextLink(0, 300, "Maksym Dudchyk from Pixabay", text_font, "https://pixabay.com/users/white_records-32584949/")

    # Line 4 - In-Game Music
    music_text3 = TextLink(0, 350, "In-Game Music by:", text_font, "https://pixabay.com/users/lnplusmusic-47631836/", color=BLACK)
    andrii_link = TextLink(0, 350, "Andrii Poradovskyi from Pixabay", text_font, "https://pixabay.com/users/lnplusmusic-47631836/")

    # --- Position the links in a justified two-column layout ---
    center_x = SCREEN_WIDTH // 2
    padding = 10 # Space between the columns

    # Align all "role" text to the right of the center point
    design_text.rect.right = center_x - padding
    assets_text.rect.right = center_x - padding
    music_text1.rect.right = center_x - padding
    music_text3.rect.right = center_x - padding

    # Align all "name/source" text to the left of the center point
    sanjoli_link.rect.left = center_x + padding
    craftpix_link.rect.left = center_x + padding
    maksym_link.rect.left = center_x + padding
    andrii_link.rect.left = center_x + padding
    
    all_links = [design_text, sanjoli_link, assets_text, craftpix_link, music_text1, maksym_link, music_text3, andrii_link]

    while game_state == "CREDITS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_state = "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: game_state = "START"
            for link in all_links: link.handle_event(event)
        if game_state != "CREDITS": break

        screen.fill(BG_COLOR)
        title_surf = title_font.render("Credits", True, GREY)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
        for link in all_links: link.draw(screen)
            
        pygame.display.flip()
        clock.tick(60)
def controls_screen(screen, clock):
    """Displays the controls and cheat codes."""
    global game_state
    title_font = pygame.font.Font(IN_GAME_FONT_PATH, 40)
    text_font = pygame.font.Font(IN_GAME_FONT_PATH, 24)
    controls_text = [
        "A / Left Arrow - Move Left",
        "D / Right Arrow - Move Right",
        "Spacebar - Jump",
        "J - Attack 1",
        "K - Attack 2",
        "L - Attack 3",
        "S - Shield",
        "",
        "Press ESC to return"
    ]
    while game_state == "CONTROLS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_state = "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: game_state = "START"
        if game_state != "CONTROLS": break
        screen.fill(BLACK)
        title_surf = title_font.render("Controls", True, WHITE)
        title_rect = title_surf.get_rect(center = (SCREEN_WIDTH // 2 , 100))
        screen.blit(title_surf, title_rect)
        for i, line in enumerate(controls_text):
            

            line_surf = text_font.render(line, True, GREY)
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 40))
            screen.blit(line_surf, line_rect)
        pygame.display.flip()
        clock.tick(60)
########################################################## MAIN FUNCTION ##########################################################
def main():
    """Main function to set up and run the game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fighter Combat")
    clock = pygame.time.Clock()

    # Load all the assets
    assets = {
        'tiles': {},
        'objects': {},
        'players': [],
        'platforms': []
    }

    # Load environment tiles
    for i in range(1, 182):
        try:
            path = os.path.join(TILE_ASSET_PATH, f"tile{i}.png")
            image = pygame.image.load(path).convert_alpha()
            assets['tiles'][i] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        except FileNotFoundError:
            print(f"Warning: Tile asset {i} not found at {path}.")
        except pygame.error: 
            pass

    # Load environment objects
    unique_objects = set(obj[0] for obj in OBJECT_LIST)
    for name in unique_objects:
        try:
            path = os.path.join(OBJECT_ASSET_PATH, f"{name}.png")
            image = pygame.image.load(path).convert_alpha()
            width = int(TILE_SIZE * (image.get_width() / 16))
            height = int(TILE_SIZE * (image.get_height() / 16))
            assets['objects'][name] = pygame.transform.scale(image, (width, height))
        except pygame.error: pass
        
    # Create a pre-rendered background surface
    background_cache = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_cache.fill(BG_COLOR)
    for row_idx, row in enumerate(LEVEL_MAP):
        for col_idx, tile_num in enumerate(row):
            if tile_num in assets['tiles']:
                background_cache.blit(assets['tiles'][tile_num], (col_idx * TILE_SIZE, row_idx * TILE_SIZE))
    for obj_name, gx, gy in OBJECT_LIST:
        if obj_name in assets['objects']:
            background_cache.blit(assets['objects'][obj_name], (gx * TILE_SIZE, gy * TILE_SIZE))
            
    ########################### Setup for Start Screen ##############################
    # Create player instances for the start screen
    assets['players'].append(Player(150, 450, 'Fighter'))
    assets['players'].append(Player(400, 450, 'Samurai'))
    assets['players'].append(Player(650, 450, 'Shinobi'))
    
    # Create moving platforms
    # Check if the required tiles exist before creating the platform image
    if 18 in assets['tiles'] and 19 in assets['tiles'] and 20 in assets['tiles']:
        platform_img = pygame.Surface((TILE_SIZE * 3, TILE_SIZE), pygame.SRCALPHA)
        platform_img.blit(assets['tiles'][18], (0, 0))
        platform_img.blit(assets['tiles'][19], (TILE_SIZE, 0))
        platform_img.blit(assets['tiles'][20], (TILE_SIZE*2, 0))
        
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            assets['platforms'].append(MovingPlatform(x, y, platform_img))
    else:
        print("Warning: Platform tiles (18, 19, 20) not found. Moving platforms will not be created.")


    ########################################### Game State Manager ################################################
    global game_state
    game_state = "START"
    main_player = Player(100, 500, selected_player)
    while game_state != "QUIT":
        if game_state == "START":
            start_screen(screen, clock, background_cache, assets)
        elif game_state == "PLAY MODE":
            play_mode_screen(screen, clock, background_cache.copy())
        elif game_state == "GAME":
            game_loop(screen, clock, background_cache, assets)
        elif game_state == "CUSTOMIZE PLAYER":
            customize_player_screen(screen, clock, background_cache, assets)
        elif game_state== "CONTROLS": controls_screen(screen, clock)
        elif game_state == "CREDITS":
            credits_screen(screen, clock)

    pygame.quit()

if __name__ == '__main__':
    main()
