from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Paddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):	#inverts ball vector when bouncing
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_x - self.center_y) / (self.width / 3)
            vel = Vector(-1 * vy, vx)
            ball.velocity = vel.x, vel.y + offset


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Game(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)

    def serve_ball(self, vel=(0, 10)):	#serving ball position and vector
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)	#bounces ball off paddles

        if (self.ball.x < self.x) or (self.ball.right > self.right): #bounces ball off left and right
            self.ball.velocity_x *= -1
        if (self.ball.top > self.top):	#bounces ball off top
        	self.ball.velocity_y *= -1

        if (self.ball.y < self.y):	#serves ball if if it goes bellow x axist
        	self.serve_ball(vel=(0, -4))




    def on_touch_move(self, touch):	#moves the player's paddle
        if touch.y < self.top:
            self.player1.center_x = touch.x

class BreakingApp(App):
    def build(self):
        game = Game()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    BreakingApp().run()

#TO DO:
#Add destroyable bricks
#Limit paddle moving speed
#ball bounces off paddle strangely, fix.
