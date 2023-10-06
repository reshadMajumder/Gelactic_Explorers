import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import random
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout



kivy.require('2.0.0')  # Make sure you have Kivy version 2.0.0 or higher.

#-------------------------------  ----------------


def collides(x1, y1, w1, h1, x2, y2, w2, h2):
    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
        return True
    else:
        return False


class MainMenu(Screen):
    pass

class AvatarSelection(Screen):
    pass
class SpaceShipSelection(Screen):
    pass
class PlanetSelection(Screen):
    pass
class GameStart(Screen):
    pass


class SpaceGame(Screen):
    pass

#------------------------------
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = False  # Flag to control game activation
        self.time_limit = 30  # Time limit in seconds
        self.remaining_time = self.time_limit  # Initial remaining time

        self._keyboard = Window.request_keyboard(
            self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        with self.canvas:
            self.player = Rectangle(
                source="resourse/spaceship.png", pos=[400, 0], size=[100, 100])
            self.asteroids = []

        self.keysPressed = set()
        Clock.schedule_interval(self.move_step, 1.0 / 60.0)  # Update at 60 FPS
        Clock.schedule_interval(self.update_time, 1.0)  # Update remaining time every second

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self, dt):
        if not self.active:
            return

        currentx, currenty = self.player.pos
        step_size = 300 * dt

        if "w" in self.keysPressed:
            currenty += step_size
        if "s" in self.keysPressed:
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size

        # Update player's position
        self.player.pos = [currentx, currenty]

        # Update asteroid positions and check for collisions
        new_asteroids = []
        for asteroid in self.asteroids:
            asteroid_x, asteroid_y = asteroid.pos
            asteroid_y -= 300 * dt  # Move asteroids down
            asteroid.pos = (asteroid_x, asteroid_y)
            if asteroid_y > -100:  # Keep asteroids on screen
                new_asteroids.append(asteroid)
            if collides(currentx, currenty, self.player.size[0], self.player.size[1],
                         asteroid_x, asteroid_y, asteroid.size[0], asteroid.size[1]):
                print("Game Over!")
                self.active = False
                App.get_running_app().root.current = "game_over"  # Redirect to the game over screen

        self.asteroids = new_asteroids

        # Add new asteroids
        if randint(0, 100) < 2:
            new_asteroid = Rectangle(
                source="resourse/astroid.png", pos=[randint(0, 700), 600], size=[80, 80])
            self.canvas.add(new_asteroid)
            self.asteroids.append(new_asteroid)

    def update_time(self, dt):
        if self.active:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                print("Time's up!")
                self.active = False
                App.get_running_app().root.current = "game_over"  # Redirect to the game over screen

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

    def on_enter(self):
        self.game_widget.active = True  # Start the game when entering this screen
        self.game_widget.remaining_time = self.game_widget.time_limit  # Reset remaining time

    def on_leave(self):
        self.game_widget.active = False  # Stop the game when leaving this screen

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a FloatLayout as the main layout
        layout = FloatLayout()

        # Create the background image
        background = Image(
            source="resourse/nebula_bg.jpg",  # Replace with your background image file
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)  # Cover the entire screen
        )
        layout.add_widget(background)

        # Create the widgets
        label_1 = Label(text='', size_hint=(1, .3))
        button = Button(
            text="Next level",
            size_hint=(0.2, 0.1),
            font_size=24,
            background_color=(0.5, 0, 0.5, 1.0),  # Button color
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        button.bind(on_press=self.restart_game)
        label = Label(text='', size_hint=(1, .3))

        # Add the widgets to the FloatLayout
        layout.add_widget(label_1)
        layout.add_widget(button)
        layout.add_widget(label)

        # Add the FloatLayout to the GameOverScreen
        self.add_widget(layout)

    def restart_game(self, instance):
        sm.current = "quiz_game"  # Redirect to the game screen
        sm.get_screen("quiz_game").on_enter()  # Start the game again

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a FloatLayout as the main layout
        layout = FloatLayout()

        # Create the background image
        background = Image(
            source="resourse/nebula_bg.jpg",  # Replace with your background image file
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)  # Cover the entire screen
        )
        layout.add_widget(background)

        # Create the button


        # Create the image
        image = Image(
            source="resourse/astronaut_avatar.png",  # Replace with your image file
            size_hint=(1, .6),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
        )
        layout.add_widget(image)

        button = Button(
            text="Start Game",
            size_hint=(0.2, 0.1),
            font_size=24,
            background_color=(0.5, 0, 0.5, 1.0),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
        )
        button.bind(on_press=self.start_game)
        layout.add_widget(button)


        label = Label(text='', size_hint=(.1, .1))
        layout.add_widget(label)

        # Add the layout to the StartScreen
        self.add_widget(layout)

    def start_game(self, instance):
        sm.current = "game"


#-------------------------------

class QuizGameQ1(Screen):
    
    pass

class QuizGameQ2(Screen):
    
    pass
class QuizGameQ3(Screen):
    
    pass
class QuizGameQ4(Screen):
    
    pass

class EndText(Screen):
    pass


class GameApp(App):
    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu')) #start page to chose mode
        #selection part
        sm.add_widget(AvatarSelection(name='avatar_selection')) #avato selection page
        sm.add_widget(SpaceShipSelection(name='spaceship_selection')) #spaceship selection page
        sm.add_widget(PlanetSelection(name='planet_selection')) #planet selection page

        #sm.add_widget(GameStart(name='start_game')) #game start button
        sm.add_widget(StartScreen(name="start_game"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="game_over"))
#new code 
        
        #sm.add_widget(SpaceGame(name='space_game'))
        #quiz game starts
        sm.add_widget(QuizGameQ1(name='quiz_game'))
        sm.add_widget(QuizGameQ2(name='quiz_game2'))
        sm.add_widget(QuizGameQ3(name='quiz_game3'))
        sm.add_widget(QuizGameQ4(name='quiz_game4'))
        #result 
        sm.add_widget(EndText(name='end_text'))
        return sm

if __name__ == '__main__':
    GameApp().run()
