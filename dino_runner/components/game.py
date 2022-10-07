from pickle import FALSE
import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.powerups.power_up_manager import PoweUpManager
from dino_runner.components.powerups.shield import Shield
from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, FONT_STYLE, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, SMALL_CACTUS, TITLE, FPS

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
        self.obstacle_manager.reset_obstacles()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        #self.obstacles[0].update(self.game_speed, self.obstacles)
        self.obstacle_manager.update(self.game_speed,self.player,self.on_death,self.reset_score)
        self.score.update(self,self.reset_score)
        self.power_up_manager.update(self.game_speed,self.player,self.score.save_score)
        

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        #self.obstacles[0].draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)

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
        self.screen.fill((255,255,255))  #pintar ventana
        half_screen_height = SCREEN_HEIGHT // 2 
        half_screen_width = SCREEN_WIDTH // 2 
        if self.death_count == 0:  #mostrar mensaje de bienvenida
            self.text("Press any Key to start",half_screen_width,half_screen_height)
        else:
            self.text("Press any Key to play again",half_screen_width,half_screen_height)
            self.text(f"Your Score: {self.score.save_score}",half_screen_width,half_screen_height+100)
            self.text(f"Death Count: {self.death_count}",half_screen_width,half_screen_height+150)
            pass
        self.screen.blit(RUNNING[0],(half_screen_width-30,half_screen_height-140))  #mostrar icono
        pygame.display.update() #actualizar ventana
        self.handle_key_events_on_menu()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()
   
    def on_death(self):
        self.playing = False
        self.death_count +=1
        print("Mori")
        print(f"Numero de muertes: {self.death_count}")

    def reset_score(self):
        if self.playing == False:
            return True

    def text(self,text,screen_width,screen_height):
        font =pygame.font.Font(FONT_STYLE,25)
        text_component =font.render(text,True,(0, 0, 0))
        text_rect = text_component.get_rect()
        text_rect.center = (screen_width,screen_height)
        self.screen.blit(text_component, text_rect)
        
