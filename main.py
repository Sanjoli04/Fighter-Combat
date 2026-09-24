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

    # Window state
is_fullscreen = False
last_window_restore_time = 0
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
        "description": "The Fighter is a resilient warrior who balances powerful attacks with dependable defense. Skilled in close combat, this versatile fighter combines heavy strikes, agile dodges, and a sturdy shield stance. With a tactical approach to every battle, the Fighter adapts to different opponents while maintaining strength, endurance, and control throughout combat.",
        "Attack_1": {"damage": 5},
        "Attack_2": {"damage": 8},
        "Attack_3": {"damage": 12},
        "Shield": {"block_percentage": 20},
    },

    "Samurai": {
        "description": "The Samurai is a swift warrior who relies on speed, precision, and perfectly timed attacks. Combining rapid sword strikes with graceful evasive movements, this skilled fighter overwhelms opponents through calculated aggression. A unique parry technique enables effective counterattacks, rewarding players who master timing, maintain momentum, and strike at the perfect moment.",
        "Attack_1": {"damage": 4},
        "Attack_2": {"damage": 7},
        "Attack_3": {"damage": 15},
        "Shield": {"block_percentage": 25},
    },
    "Shinobi": {
        "description" : "The Shinobi is a stealthy warrior who combines agility, deception, and unpredictable attacks. Armed with a katana, shurikens, and smoke bombs, this elusive fighter outmaneuvers opponents through surprise and strategic movement. By blending swift offensive strikes with evasive techniques, the Shinobi adapts to changing battles and keeps enemies constantly guessing.",
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
def present_scaled(window, game_surface):
    """Scale the logical game surface to fit the current window."""

    window_width, window_height = window.get_size()
    game_width, game_height = game_surface.get_size()

    scale = min(
        window_width / game_width,
        window_height / game_height
    )

    scaled_width = max(1, round(game_width * scale))
    scaled_height = max(1, round(game_height * scale))

    # Scale the completed game frame.
    scaled_game = pygame.transform.smoothscale(
        game_surface,
        (scaled_width, scaled_height)
    )

    # Center the game; black bars preserve its aspect ratio.
    x = (window_width - scaled_width) // 2
    y = (window_height - scaled_height) // 2

    window.fill((0, 0, 0))
    window.blit(scaled_game, (x, y))

    pygame.display.flip()
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
def to_game_pos(window, game_surface, pos):
    ww, wh = window.get_size()
    gw, gh = game_surface.get_size()

    scale = min(ww / gw, wh / gh)
    sw, sh = round(gw * scale), round(gh * scale)

    ox = (ww - sw) // 2
    oy = (wh - sh) // 2

    x = (pos[0] - ox) / scale
    y = (pos[1] - oy) / scale

    if not (0 <= x < gw and 0 <= y < gh):
        return (-1, -1)

    return (x, y)
def draw_fight_result(screen, result, font):
    if result is None:
        return

    result_text = font.render(result, True, WHITE)

    result_rect = result_text.get_rect(
        center=(SCREEN_WIDTH // 2, 100)
    )

    screen.blit(result_text, result_rect)

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


def start_screen(screen, game_surface, clock, background_cache, assets):

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
            if event.type == pygame.QUIT:
                game_state = "QUIT"

            # Convert window mouse coordinates to game coordinates
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                event.pos = to_game_pos(screen, game_surface, event.pos)

            for btn in buttons:
                btn.handle_event(event)

        if game_state != "START":
            break

        # Draw the world on the logical game surface
        draw_game_world(game_surface, background_cache, assets)

        pod_char = assets["players"][selected_player_index]
        pod_char.rect.midbottom = (90, SCREEN_HEIGHT - 30)
        pod_char.update()
        pod_char.draw(game_surface)

        # PANEL BACKPLATE
        glass = pygame.Surface(
            (panel_rect.width, panel_rect.height),
            pygame.SRCALPHA
        )
        glass.fill((20, 20, 35, 215))

        game_surface.blit(glass, panel_rect.topleft)

        pygame.draw.rect(
            game_surface,
            GOLD,
            panel_rect,
            2,
            border_radius=18
        )

        # Title Text
        title_text = title_font.render("FIGHTER COMBAT", True, WHITE)
        title_x = SCREEN_WIDTH // 2
        title_y = panel_rect.y - 75

        game_surface.blit(
            title_text,
            title_text.get_rect(center=(title_x, title_y))
        )

        # Draw buttons
        for btn in buttons:
            btn.draw(game_surface)

        # Scale the completed frame to the actual window
        present_scaled(screen, game_surface)

        clock.tick(60)

def play_mode_screen(screen, game_surface, clock, background_cache):
    """Display the Play Mode screen with proper window scaling."""

    global game_state
    global selected_player_index

    button_font = pygame.font.Font(IN_GAME_FONT_PATH, 28)

    glass_surface = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA
    )
    glass_surface.fill((0, 0, 0, 150))

    def play_ai_cb():
        global game_state
        game_state = "GAME"

    buttons = [
        Button(
            SCREEN_WIDTH // 2 - 150,
            330,
            300,
            60,
            "Play with AI",
            button_font,
            play_ai_cb
        )
    ]

    while game_state == "PLAY MODE":

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_state = "QUIT"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "START"

            # Convert actual window coordinates to logical game coordinates
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                event.pos = to_game_pos(screen, game_surface, event.pos)

            for button in buttons:
                button.handle_event(event)

        if game_state != "PLAY MODE":
            break

        # Draw everything on the fixed-size logical surface
        game_surface.blit(background_cache, (0, 0))
        game_surface.blit(glass_surface, (0, 0))

        for button in buttons:
            button.draw(game_surface)

        # Present the completed frame at the current window size
        present_scaled(screen, game_surface)

        clock.tick(60)

def game_loop(
    screen,
    game_surface,
    clock,
    background_cache,
    assets
):
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
    fight_end_started = False
    fight_result = None
    paused = False

    floating_texts = []
    name_font = pygame.font.Font(IN_GAME_FONT_PATH, 20)
    countdown_font = pygame.font.Font(IN_GAME_FONT_PATH, 55)
    result_font = pygame.font.Font(IN_GAME_FONT_PATH, 50)
    pause_title_font = pygame.font.Font(IN_GAME_FONT_PATH, 50)
    pause_button_font = pygame.font.Font(IN_GAME_FONT_PATH, 24)

    pause_controls = False
    exit_confirmation = False
    def continue_game():
        nonlocal paused, pause_controls, exit_confirmation
        paused = False
        pause_controls = False
        exit_confirmation = False

    def show_pause_controls():
        nonlocal pause_controls, exit_confirmation
        pause_controls = True
        exit_confirmation = False

    def show_exit_confirmation():
        nonlocal exit_confirmation
        exit_confirmation = True

    def cancel_exit():
        nonlocal exit_confirmation
        exit_confirmation = False

    def exit_game():
        nonlocal paused, pause_controls, exit_confirmation
        global game_state

        # Current fight is intentionally abandoned.
        paused = False
        pause_controls = False
        exit_confirmation = False
        game_state = "START"

    pause_buttons = [
        Button(
            SCREEN_WIDTH // 2 - 150,
            260,
            300,
            55,
            "CONTINUE",
            pause_button_font,
            continue_game
        ),

        Button(
            SCREEN_WIDTH // 2 - 150,
            330,
            300,
            55,
            "CONTROLS",
            pause_button_font,
            show_pause_controls
        ),

        Button(
            SCREEN_WIDTH // 2 - 150,
            400,
            300,
            55,
            "EXIT",
            pause_button_font,
            show_exit_confirmation
        )
    ]

    exit_yes_button = Button(
        SCREEN_WIDTH // 2 - 145,
        360,
        125,
        50,
        "YES",
        pause_button_font,
        exit_game
    )

    exit_no_button = Button(
        SCREEN_WIDTH // 2 + 20,
        360,
        125,
        50,
        "NO",
        pause_button_font,
        cancel_exit
    )
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
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                event.pos = to_game_pos(screen, game_surface, event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Pause button pressed. Toggling pause menu.")
                if exit_confirmation:
                    # EXIT confirmation -> pause menu
                    exit_confirmation = False

                elif pause_controls:
                    # Controls -> pause menu
                    pause_controls = False

                else:
                    # Game <-> pause menu
                    paused = not paused
                print("paused =", paused)
            if paused and not pause_controls and not exit_confirmation:

                for button in pause_buttons:
                    button.handle_event(event)

            # Exit confirmation buttons
            elif paused and exit_confirmation:

                exit_yes_button.handle_event(event)
                exit_no_button.handle_event(event)

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


        if not in_countdown and combat_active:
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
            fight_end_started = True
            fight_result = "YOU ARE DEFEATED"
            target_zoom_level = 1.8
            camera_x = main_player.rect.centerx
            camera_y = main_player.rect.centery-30
            main_player.move(empty_keys)
            main_player.update_status()
        if ai_player.health <= 0:
            ai_player.health = 0
            ai_player.action = "Dead"
            combat_active = False
            fight_end_started = True
            fight_result = "YOU WON"
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
        game_surface.fill(BG_COLOR)

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
        draw_fight_result(shake_surface, fight_result, result_font)
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
        game_surface.blit(shake_surface, (offset_x, offset_y))
        
        if in_countdown:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,150))

            game_surface.blit(overlay, (0,0))
            current_text = countdown_items[countdown_index]
            text_surf = countdown_font.render(current_text, True, WHITE)
            game_surface.blit(text_surf, text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

            if current_time - last_countdown_tick > 800:
                last_countdown_tick = current_time
                countdown_index += 1
                if countdown_index >= len(countdown_items):
                    in_countdown = False
        if not combat_active:
            end_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            end_overlay.fill((10, 8, 12,180))
            game_surface.blit(end_overlay,(0,0))

            if main_player.health <= 0:
                result_text = "You are Defeated"
                text_color = RED
            else:
                result_text = "You Won"
                text_color = GREEN

        # =========================================================
        # PAUSE MENU / CONTROLS / EXIT CONFIRMATION
        # =========================================================
        if paused:

            # Dark transparent layer over the current game
            pause_overlay = pygame.Surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.SRCALPHA
            )
            pause_overlay.fill((0, 0, 0, 170))
            game_surface.blit(pause_overlay, (0, 0))

            # Central panel
            pause_panel = pygame.Rect(
                SCREEN_WIDTH // 2 - 210,
                140,
                420,
                390
            )

            pygame.draw.rect(
                game_surface,
                (20, 15, 25),
                pause_panel,
                border_radius=18
            )

            pygame.draw.rect(
                game_surface,
                GOLD,
                pause_panel,
                2,
                border_radius=18
            )

            # -----------------------------------------------------
            # EXIT CONFIRMATION
            # -----------------------------------------------------
            if exit_confirmation:

                title = pause_title_font.render(
                    "EXIT GAME?",
                    True,
                    WHITE
                )

                game_surface.blit(
                    title,
                    title.get_rect(
                        center=(SCREEN_WIDTH // 2, 205)
                    )
                )

                message = pause_button_font.render(
                    "Are you sure you want to exit?",
                    True,
                    WHITE
                )

                game_surface.blit(
                    message,
                    message.get_rect(
                        center=(SCREEN_WIDTH // 2, 275)
                    )
                )

                exit_yes_button.draw(game_surface)
                exit_no_button.draw(game_surface)

            # -----------------------------------------------------
            # CONTROLS OVERLAY
            # -----------------------------------------------------
            elif pause_controls:

                title = pause_title_font.render(
                    "CONTROLS",
                    True,
                    WHITE
                )

                game_surface.blit(
                    title,
                    title.get_rect(
                        center=(SCREEN_WIDTH // 2, 190)
                    )
                )

                controls = [
                    "A / Left Arrow  -  Move Left",
                    "D / Right Arrow -  Move Right",
                    "Spacebar        -  Jump",
                    "J               -  Attack 1",
                    "K               -  Attack 2",
                    "L               -  Attack 3",
                    "S               -  Shield",
                ]

                for i, line in enumerate(controls):

                    text = pause_button_font.render(
                        line,
                        True,
                        GREY
                    )

                    game_surface.blit(
                        text,
                        text.get_rect(
                            center=(
                                SCREEN_WIDTH // 2,
                                245 + i * 32
                            )
                        )
                    )

                back_text = pause_button_font.render(
                    "Press ESC to return",
                    True,
                    GOLD
                )

                game_surface.blit(
                    back_text,
                    back_text.get_rect(
                        center=(
                            SCREEN_WIDTH // 2,
                            480
                        )
                    )
                )

            # -----------------------------------------------------
            # MAIN PAUSE MENU
            # -----------------------------------------------------
            else:

                title = pause_title_font.render(
                    "PAUSED",
                    True,
                    WHITE
                )

                game_surface.blit(
                    title,
                    title.get_rect(
                        center=(SCREEN_WIDTH // 2, 205)
                    )
                )

                for button in pause_buttons:
                    button.draw(game_surface)
        present_scaled(screen, game_surface)
        clock.tick(60)


def customize_player_screen(screen, game_surface, clock, background_cache, assets):
    global game_state, selected_player, selected_player_index

    title_font = safe_load_font(IN_GAME_FONT_PATH, 46)
    name_font = safe_load_font(IN_GAME_FONT_PATH, 26)
    button_font = safe_load_font(IN_GAME_FONT_PATH, 20)
    detail_font = safe_load_font(IN_GAME_FONT_PATH, 21)

    # Separate previews so gameplay characters are not modified.
    roster = [
        Player(150, 330, "Fighter", scale=1.7),
        Player(400, 330, "Samurai", scale=1.7),
        Player(650, 330, "Shinobi", scale=1.7)
    ]

    active_detail = None

    def open_details(name):
        nonlocal active_detail
        active_detail = name

    def close_details():
        nonlocal active_detail
        active_detail = None

    def choose_character(name):
        global selected_player, selected_player_index
        selected_player = name
        selected_player_index = players.index(name)
        close_details()

    def go_back():
        global game_state
        game_state = "START"

    view_buttons = [
        Button(65, 390, 170, 45, "VIEW DETAILS",
               button_font, lambda: open_details("Fighter")),
        Button(315, 390, 170, 45, "VIEW DETAILS",
               button_font, lambda: open_details("Samurai")),
        Button(565, 390, 170, 45, "VIEW DETAILS",
               button_font, lambda: open_details("Shinobi"))
    ]

    select_button = Button(
        275, 475, 250, 48, "SELECT CHARACTER",
        button_font,
        lambda: choose_character(active_detail)
    )

    details_back_button = Button(
        275, 535, 250, 45, "BACK TO ROSTER",
        button_font, close_details
    )

    menu_back_button = Button(
        325, 520, 150, 45, "BACK",
        button_font, go_back
    )

    # Cache enlarged Idle previews once, not every frame.
    detail_previews = {
        name: Player(160, 325, name, scale=2.5)
        for name in players
    }

    def draw_wrapped_text(surface, text, font, color, x, y, max_width, line_height):
        words = text.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if font.size(candidate)[0] > max_width and line:
                rendered = font.render(line, True, color)
                surface.blit(rendered, (x, y))
                y += line_height
                line = word
            else:
                line = candidate

        if line:
            rendered = font.render(line, True, color)
            surface.blit(rendered, (x, y))
            y += line_height

        return y

    while game_state == "CUSTOMIZE PLAYER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "QUIT"
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if active_detail:
                    close_details()
                else:
                    go_back()

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                logical_pos = to_game_pos(screen, game_surface, event.pos)
                event = pygame.event.Event(
                    event.type,
                    {**event.dict, "pos": logical_pos}
                )

            if active_detail:
                select_button.handle_event(event)
                details_back_button.handle_event(event)
            else:
                for button in view_buttons:
                    button.handle_event(event)
                menu_back_button.handle_event(event)

        if game_state != "CUSTOMIZE PLAYER":
            break

        game_surface.blit(background_cache, (0, 0))

        # Darken the level background for readability.
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((15, 12, 30, 175))
        game_surface.blit(overlay, (0, 0))

        if active_detail is None:
            title = title_font.render("Choose Your Player", True, WHITE)
            game_surface.blit(
                title, title.get_rect(center=(400, 75))
            )

            for character in roster:
                character.action = "Idle"
                character.update()
                character.draw(game_surface)

                name = name_font.render(
                    character.character_type.upper(), True, WHITE
                )
                game_surface.blit(
                    name,
                    name.get_rect(
                        center=(character.rect.centerx, 365)
                    )
                )

            for button in view_buttons:
                button.draw(game_surface)

            menu_back_button.draw(game_surface)

        else:
            data = ALMANAC[active_detail]
            character = detail_previews[active_detail]

            heading = title_font.render(active_detail.upper(), True, GOLD)
            game_surface.blit(
                heading, heading.get_rect(center=(400, 55))
            )

            # Enlarged, looping breathing/Idle animation.
            character.action = "Idle"
            character.update()
            character.draw(game_surface)

            description_y = draw_wrapped_text(
                game_surface,
                data["description"],
                detail_font,
                WHITE,
                295,
                125,
                455,
                25
            )

            stats_y = max(355, description_y + 15)

            stats = (
                f"Attack 1: {data['Attack_1']['damage']}     "
                f"Attack 2: {data['Attack_2']['damage']}     "
                f"Attack 3: {data['Attack_3']['damage']}"
            )

            stats_surface = detail_font.render(stats, True, GOLD)
            game_surface.blit(stats_surface, (65, stats_y))

            shield_text = (
                f"Shield Block: "
                f"{data['Shield']['block_percentage']}%"
            )
            shield_surface = detail_font.render(
                shield_text, True, WHITE
            )
            game_surface.blit(
                shield_surface, (65, stats_y + 32)
            )

            select_button.draw(game_surface)
            details_back_button.draw(game_surface)

        present_scaled(screen, game_surface)
        clock.tick(60)

def credits_screen(screen, game_surface, clock):
    global game_state

    title_font = safe_load_font(START_SCREEN_FONT_PATH, 39)
    heading_font = safe_load_font(CREDITS_FONT_PATH, 25)
    text_font = safe_load_font(CREDITS_FONT_PATH, 22)
    small_font = safe_load_font(IN_GAME_FONT_PATH, 18)

    def go_back():
        global game_state
        game_state = "START"

    back_button = Button(
        300, 530, 200, 45,
        "BACK TO MENU", small_font, go_back
    )

    links = [
        TextLink(
            0, 0, "Sanjoli Vashisth",
            heading_font,
            "https://github.com/Sanjoli04",
            color=WHITE,
            hover_link_color=GOLD
        ),
        TextLink(
            0, 0, "CraftPix.Net",
            text_font,
            "https://craftpix.net/",
            color=WHITE,
            hover_link_color=GOLD
        ),
        TextLink(
            0, 0, "Maksym Dudchyk",
            text_font,
            "https://pixabay.com/users/white_records-32584949/",
            color=WHITE,
            hover_link_color=GOLD
        ),
        TextLink(
            0, 0, "Andrii Poradovskyi",
            text_font,
            "https://pixabay.com/users/lnplusmusic-47631836/",
            color=WHITE,
            hover_link_color=GOLD
        )
    ]

    link_positions = [205, 310, 402, 465]

    for link, y in zip(links, link_positions):
        link.rect.centerx = SCREEN_WIDTH // 2
        link.rect.y = y

    while game_state == "CREDITS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "QUIT"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    go_back()

            if event.type in (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONDOWN
            ):
                event = pygame.event.Event(
                    event.type,
                    {
                        **event.dict,
                        "pos": to_game_pos(
                            screen, game_surface, event.pos
                        )
                    }
                )

            for link in links:
                link.handle_event(event)

            back_button.handle_event(event)

        if game_state != "CREDITS":
            break

        game_surface.fill(BG_COLOR)

        title = title_font.render(
            "HALL OF LEGENDS", True, WHITE
        )
        game_surface.blit(
            title, title.get_rect(center=(400, 60))
        )

        subtitle = small_font.render(
            "Every legend has a story.",
            True, GOLD
        )
        game_surface.blit(
            subtitle,
            subtitle.get_rect(center=(400, 108))
        )

        panel = pygame.Rect(155, 140, 490, 375)
        pygame.draw.rect(
            game_surface, (22, 20, 42),
            panel, border_radius=18
        )
        pygame.draw.rect(
            game_surface, GOLD,
            panel, 2, border_radius=18
        )

        headings = [
            ("GAME DESIGN & PROGRAMMING", 170),
            ("PIXEL ART ASSETS", 275),
            ("START SCREEN MUSIC", 365),
            ("IN-GAME MUSIC", 430)
        ]

        for label, y in headings:
            heading = small_font.render(
                label, True, GOLD
            )
            game_surface.blit(
                heading,
                heading.get_rect(center=(400, y))
            )

        for link in links:
            link.draw(game_surface)

        back_button.draw(game_surface)
        present_scaled(screen, game_surface)
        clock.tick(60)

def controls_screen(screen, game_surface, clock):
    global game_state

    title_font = safe_load_font(START_SCREEN_FONT_PATH, 38)
    section_font = safe_load_font(IN_GAME_FONT_PATH, 27)
    text_font = safe_load_font(IN_GAME_FONT_PATH, 22)
    small_font = safe_load_font(IN_GAME_FONT_PATH, 18)

    def go_back():
        global game_state
        game_state = "START"

    back_button = Button(
        300, 520, 200, 50,
        "BACK TO MENU", text_font, go_back
    )

    movement = [
        ("A", "MOVE LEFT"),
        ("D", "MOVE RIGHT"),
        ("SPACE", "JUMP"),
        ("CTRL", "RUN")
    ]

    combat = [
        ("J", "ATTACK I"),
        ("K", "ATTACK II"),
        ("L", "ATTACK III"),
        ("S", "SHIELD")
    ]

    while game_state == "CONTROLS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "QUIT"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    go_back()

            if event.type in (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONDOWN
            ):
                event = pygame.event.Event(
                    event.type,
                    {
                        **event.dict,
                        "pos": to_game_pos(
                            screen, game_surface, event.pos
                        )
                    }
                )

            back_button.handle_event(event)

        if game_state != "CONTROLS":
            break

        game_surface.fill(BG_COLOR)

        title = title_font.render(
            "COMBAT MANUAL", True, WHITE
        )
        game_surface.blit(
            title, title.get_rect(center=(400, 65))
        )

        subtitle = small_font.render(
            "Master your movement. Perfect your attacks.",
            True, (215, 185, 125)
        )
        game_surface.blit(
            subtitle, subtitle.get_rect(center=(400, 110))
        )

        panels = [
            (pygame.Rect(55, 155, 330, 315),
             "MOVEMENT", movement),
            (pygame.Rect(415, 155, 330, 315),
             "COMBAT", combat)
        ]

        for rect, heading, entries in panels:
            pygame.draw.rect(
                game_surface, (23, 21, 42),
                rect, border_radius=15
            )
            pygame.draw.rect(
                game_surface, GOLD,
                rect, 2, border_radius=15
            )

            heading_surf = section_font.render(
                heading, True, GOLD
            )
            game_surface.blit(
                heading_surf,
                heading_surf.get_rect(
                    center=(rect.centerx, rect.y + 40)
                )
            )

            for i, (key, action) in enumerate(entries):
                y = rect.y + 95 + i * 48

                key_rect = pygame.Rect(
                    rect.x + 20, y - 6, 85, 36
                )
                pygame.draw.rect(
                    game_surface, (75, 52, 35),
                    key_rect, border_radius=7
                )
                pygame.draw.rect(
                    game_surface, GOLD,
                    key_rect, 1, border_radius=7
                )

                key_surf = small_font.render(
                    key, True, WHITE
                )
                game_surface.blit(
                    key_surf,
                    key_surf.get_rect(center=key_rect.center)
                )

                action_surf = text_font.render(
                    action, True, WHITE
                )
                game_surface.blit(
                    action_surf,
                    (rect.x + 120, y)
                )

        back_button.draw(game_surface)
        present_scaled(screen, game_surface)
        clock.tick(60)
########################################################## MAIN FUNCTION ##########################################################
def main():
    """Main function to set up and run the game."""
    global is_fullscreen, last_window_restore_time, selected_player_index, selected_player
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
         pygame.RESIZABLE
    )
    pygame.display.set_caption("Fighter Combat")
    clock = pygame.time.Clock()

    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "QUIT"

            elif event.type == pygame.WINDOWMAXIMIZED:
                current_time = pygame.time.get_ticks()

                # First click = normal maximized window
                # Second click quickly = fullscreen
                if current_time - last_window_restore_time < 500:
                    is_fullscreen = True
                    screen = pygame.display.set_mode(
                        (0, 0),
                        pygame.FULLSCREEN
                    )

                last_window_restore_time = current_time

            elif event.type == pygame.WINDOWRESTORED:
                current_time = pygame.time.get_ticks()

                # Restore from fullscreen -> normal window
                if is_fullscreen:
                    is_fullscreen = False
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT),
                        pygame.RESIZABLE
                    )

                last_window_restore_time = current_time

        if game_state == "START":
            start_screen(screen, game_surface, clock, background_cache, assets)
        elif game_state == "PLAY MODE":
            play_mode_screen(screen, game_surface, clock, background_cache.copy())
        elif game_state == "GAME":
            game_loop(screen,game_surface,clock,background_cache,assets)
        elif game_state == "CUSTOMIZE PLAYER":
            customize_player_screen(screen, game_surface, clock, background_cache, assets)
        elif game_state== "CONTROLS": controls_screen(screen, game_surface, clock)
        elif game_state == "CREDITS":
            credits_screen(screen, game_surface, clock)
        

    pygame.quit()

if __name__ == '__main__':
    main()
