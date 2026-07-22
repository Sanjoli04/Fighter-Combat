import random
import gymnasium as gym
from gymnasium import spaces
import pygame
from main import Player, SCREEN_WIDTH, SCREEN_HEIGHT,ALMANAC
import numpy as np
from collections import defaultdict


class FighterEnv(gym.Env):
    "Custom Environment for Fighter Combat usingDeep Q-Network"
    metadata = {"render_modes": ["human","rgb_array"], "render_fps": 60}
    def __init__(self, render_mode=None):
        super(FighterEnv, self).__init__()
        self.render_mode = render_mode

        # Fighter has these actions: Idle, walk, run, jump, attack_1, attack_2, attack_3, shield
        self.action_space = spaces.Discrete(8)

        # Observation space: [my_x, my_y, my_health, enemy_x, enemy_y, enemy_health, my_facing_right, enemy_facing_right]
        low = np.array([-SCREEN_WIDTH,0,0,0,-100,0,0,0,0], dtype=np.float32)
        high = np.array([SCREEN_WIDTH, SCREEN_HEIGHT, 100,100,100 ,1,1, 1, 1], dtype=np.float32)
        self.observation_space = spaces.Box(low=low,high=high, dtype = np.float32)

        # Pygame initialization
        if self.render_mode == "human":
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            import os
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Available characters for both AI and human target
        self.available_characters = ["Shinobi", "Samurai", "Fighter"]
        self.opponent_styles = ['AGGRESSIVE', 'DEFENSIVE', 'RANDOM']

        self.floating_texts = []
    def get_obs(self):
        """Extracts engineered relative features for rapid neural not convergence."""
        relative_x = float(self.human_target.rect.x - self.ai_agent.rect.x)
        distance = float(np.abs(relative_x))
        health_diff = float(self.ai_agent.health - self.human_target.health)
        ai_attacking = 1.0 if self.ai_agent.action.startswith("Attack") else 0.0
        enemy_attacking = 1.0 if self.human_target.action.startswith("Attack") else 0.0
        ai_grounded = 1.0 if self.ai_agent.on_ground else 0.0
        enemy_grounded = 1.0 if self.human_target.on_ground else 0.0
        return np.array([
            relative_x,
            distance,
            self.ai_agent.health,
            self.human_target.health,
            health_diff,
            ai_attacking,
            enemy_attacking,
            ai_grounded,
            enemy_grounded
        ], dtype = np.float32)
    
    def reset(self, seed = None, options = None):
        super().reset(seed = seed)
        self.current_step = 0

        chosen_ai_character = random.choice(self.available_characters)
        chosen_human_character = random.choice(self.available_characters)

        self.ai_agent  = Player(650, 578, chosen_ai_character)
        self.human_target = Player(100, 578, chosen_human_character)
        
        self.active_bot_style = random.choice(self.opponent_styles)

        self.floating_texts = []
        
        self.human_target.facing_right = True
        self.ai_agent.facing_right = not self.human_target.facing_right

        return self.get_obs(), {}
    
    def step(self, action):
        self.current_step += 1

        keys = defaultdict(bool)
        if action == 1: keys[pygame.K_a] = True
        elif action == 2: keys[pygame.K_d] = True
        elif action == 3: keys[pygame.K_SPACE] = True
        elif action == 4: keys[pygame.K_j] = True
        elif action == 5: keys[pygame.K_k] = True
        elif action == 6: keys[pygame.K_l] = True
        elif action == 7: keys[pygame.K_LCTRL] = True
        elif action == 8: keys[pygame.K_RCTRL] = True

        prev_enemy_health = self.human_target.health
        prev_ai_health = self.ai_agent.health

        if self.ai_agent.rect.x < self.human_target.rect.x:
            self.human_target.facing_right = False
        else:
            self.human_target.facing_right = True
        self.ai_agent.facing_right = not self.human_target.facing_right
        
        human_keys = defaultdict(bool)
        x_distance = (self.ai_agent.rect.x - self.human_target.rect.x)
        abs_distance = np.abs(x_distance)

        ai_hitbox = self.ai_agent.get_hitbox()
        human_hitbox = self.human_target.get_hitbox()
        hitbox_colliding = ai_hitbox.colliderect(human_hitbox)

        enemy_should_move_right = x_distance > 0
        if self.active_bot_style == 'AGGRESSIVE':
            if not hitbox_colliding and abs_distance > 70:
                if enemy_should_move_right: human_keys[pygame.K_d] = True
                else: human_keys[pygame.K_a] = True

                if random.random() < 0.25: human_keys[pygame.K_LCTRL] = True

            else:
                attack_choice = random.choices([pygame.K_s, pygame.K_j, pygame.K_k, pygame.K_l], weights=[0.15, 0.20, 0.30, 0.35])[0]
                human_keys[attack_choice] = True
        elif self.active_bot_style == 'DEFENSIVE':
            if abs_distance < 110:
                if random.random() < 0.65:human_keys[pygame.K_s] = True
                else: human_keys[pygame.K_j] = True
            else:
                if random.random() < 0.3:
                    if enemy_should_move_right: human_keys[pygame.K_a] = True
                    else: human_keys[pygame.K_d] = True
        else:
            if not hitbox_colliding and abs_distance > 90:
                if enemy_should_move_right: human_keys[pygame.K_d] = True
                else: human_keys[pygame.K_a] = True
            else:
                attack_choice = random.choices([pygame.K_s, pygame.K_j, pygame.K_k, pygame.K_l], weights=[0.15, 0.25, 0.30, 0.30])[0]
                human_keys[attack_choice] = True
        
        self.ai_agent.move(keys)
        self.ai_agent.choose_action(keys)

        self.human_target.move(human_keys)
        self.human_target.choose_action(human_keys)
        self.ai_agent.fight_with_enemy(self.human_target, self.floating_texts)
        self.human_target.fight_with_enemy(self.ai_agent, self.floating_texts)

        self.ai_agent.update()
        self.human_target.update()
        self.ai_agent.update_status()
        self.human_target.update_status()

        reward = 0.0
        if hitbox_colliding:
            if self.human_target.health < prev_enemy_health:
                reward += (prev_enemy_health - self.human_target.health) * 4.0
            else:
                reward += 0.4
        else:
            if action in [4,5,6]:
                reward -= 0.5
            
            if abs_distance < 150:
                reward += 0.3
            else:
                reward -= 0.15

        if self.ai_agent.health < prev_ai_health:
            reward -= (prev_ai_health - self.ai_agent.health) * 2.0

        terminated = False
        if self.ai_agent.health <= 0 or self.human_target.health<=0:
            terminated = True
            if self.human_target.health <=0: reward += 50.0
            if self.ai_agent.health <=0: reward -= 50.0
        truncated = False
        if self.current_step == 799:
            print("Episode End Distance:", abs_distance)

        if self.current_step >= 800:
            truncated = True
        
        return self.get_obs(), reward, terminated, truncated, {}
    
    def render(self):
        if self.render_mode == "human":
            self.clock.tick(self.metadata["render_fps"])
    



