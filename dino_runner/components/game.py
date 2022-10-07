from cgitb import text
from pickle import FALSE
from unittest.mock import DEFAULT
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.powerups.power_up_manager import PoweUpManager
#from dino_runner.components.powerups.shield import Shield
#from dino_runner.components.powerups.hammer import Hammer
from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, GAME_OVER, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, HAMMER_TYPE,SMALL_CACTUS, TITLE, FPS

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PoweUpManager()
        self.heart_manager= PlayerHeartManager()
        self.death_count = 0
        self.score = Score()
        



    def execute(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
                
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        #self.obstacle_manager.reset_obstacles()
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()
    def reset_game(self):
        self.game_speed=20
        self.obstacle_manager.reset_obstacles()
        self.score.restart_score()
        self.power_up_manager.reset_power_ups()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        #self.obstacles[0].update(self.game_speed, self.obstacles)
        self.obstacle_manager.update(self.game_speed,self.player,self.on_death,self.score.score)
        self.score.update(self)
        self.power_up_manager.update(self.game_speed,self.player,self.score.score)
    
        

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((93,173,226))
        self.draw_background()
        self.player.draw(self.screen)
        #self.obstacles[0].draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.heart_manager.draw(self.screen)
        self.draw_power_up_active()

        pygame.display.update()
        pygame.display.flip()
        

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((93,173,226))  #pintar ventana
        half_screen_height = SCREEN_HEIGHT // 2 
        half_screen_width = SCREEN_WIDTH // 2 
        if self.death_count == 0:  #mostrar mensaje de bienvenida
            self.text("Press any Key to start",half_screen_width,half_screen_height)
            self.text("Good Luck",half_screen_width,half_screen_height+50)
            self.screen.blit(RUNNING[0],(half_screen_width-30,half_screen_height-140))
        else:
            self.screen.blit(GAME_OVER,(half_screen_width-130,half_screen_height-200))
            self.screen.blit(RUNNING[0],(half_screen_width-30,half_screen_height-140)) 
            self.text("Press any Key to play again",half_screen_width,half_screen_height)
            self.text(f"Your Score: {self.score.score}",half_screen_width,half_screen_height+50)
            self.text(f"Death Count: {self.death_count}",half_screen_width,half_screen_height+100)
            pass
          #mostrar icono
        pygame.display.update() #actualizar ventana
        self.handle_key_events_on_menu()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()
   
    def on_death(self):
        is_invincible = self.player.type == SHIELD_TYPE  or self.player.type ==HAMMER_TYPE or self.heart_manager.heart_count>0 
        self.heart_manager.reduce_heart()
        if not is_invincible:
            self.heart_manager.reduce_heart()
            pygame.time.delay(500)
            self.playing = False
            self.death_count +=1
        return is_invincible
        
    def text(self,text,screen_width,screen_height):
        font =pygame.font.Font(FONT_STYLE,20)
        text_component =font.render(text,True,(0, 0, 0))
        text_rect = text_component.get_rect()
        text_rect.center = (screen_width,screen_height)
        self.screen.blit(text_component, text_rect)
        
    def draw_power_up_active(self):
        half_screen_height = SCREEN_HEIGHT // 2 
        half_screen_width = SCREEN_WIDTH // 2 
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks())/1000,2)
            if time_to_show >=0:
                self.text(f"{self.player.type.capitalize()} enable for {time_to_show} seconds",
                    half_screen_width-40,half_screen_height-250)
            else:
                self.player.has_power_up= False
                self.player.type = DEFAULT_TYPE
