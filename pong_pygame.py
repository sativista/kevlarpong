import sys
from math import sqrt
from random import uniform, choice

from pygame import *
from pygame.font import *
from pygame.sprite import *
from pygame.locals import *

########################
###### POG palace ######
# Do not disturb ! >:[ #
########################

_fps = 40

_width = 800
_height = 500

_court_padding = (50,50)

_vel_racket_y = 150

_racket_sizes = (20, 100)

_rackets_x = (_court_padding[0] + 25, _width - _court_padding[1] - 25)

_max_ball_vel = 10

_score_format = '%-10s %-3d x %3d %10s'


def is_bounded(x, a, b):
  return x >= a and x <= b

class Ball(Sprite):
  radius = 9
  mod_vel = 265
  color = Color('white')

  def __init__(self, pos, vel):
    Sprite.__init__(self)

    r = Ball.radius

    self.image = Surface((r*2,r*2))
    self.image.set_colorkey(Color('black'))

    draw.circle(self.image, Ball.color, (r,r), r)

    self.rect = self.image.get_rect(center = pos)

    self.set_velocity(vel)  

  def set_velocity(self, vel):
    mod = sqrt(vel[0] ** 2 + vel[1] ** 2)
    self.vel = map(lambda x : (x / mod) * Ball.mod_vel, vel)

  def update(self, time):
    self.rect.centerx += self.vel[0] * time
    self.rect.centery += self.vel[1] * time

  def reset(self):
    self.rect.center = [_width / 2., _height / 2.]

    random_n = lambda : uniform(1, _max_ball_vel) * choice([1,-1])

    self.set_velocity((random_n(), random_n()))  
    
  def bound_ball(self, court, r1, r2):
    self.check_court(court)
    self.check_rackets(r1, r2)
    return self.check_win(court)
  
  def check_court(self, court):
    p = self.rect

    if (p.bottom > court.bottom):
      self.vel[1] *= -1
      p.bottom = court.bottom
    elif (p.top < court.top):
      self.vel[1] *= -1
      p.top = court.top

  def check_rackets(self, r1, r2):
    p = self.rect
    
    for r in (r1, r2):
      if (not p.colliderect(r)):
        continue

      if (r == r1 and is_bounded(p.left, r.left, r.right)):
        p.left = r.right+1
        self.vel[0] *= -1
        continue
      elif (r == r2 and is_bounded(p.right, r.left, r.right)):
        p.right = r.left-1
        self.vel[0] *= -1
        continue

      if (is_bounded(p.bottom, r.top, r.bottom)):
        p.bottom = r.top-1
        self.vel[1] *= -1
      if (is_bounded(p.top, r.top, r.bottom)):
        p.top = r.bottom+1
        self.vel[1] *= -1

  def check_win(self, court):
    p = self.rect

    if (p.left < court.left):
      self.vel[0] *= -1
      p.left = court.left
      return 2
    elif (p.right > court.right):
      self.vel[0] *= -1
      p.right = court.right
      return 1
    else:
      return 0


class Player(Sprite):
  def __init__(self, name, racket_x):
    Sprite.__init__(self)

    self.name = name

    self.score = 0

    self.image = Surface(_racket_sizes)
    self.image.fill(Color('green'))

    self.rect = self.image.get_rect(center = (racket_x, _height / 2.))

    self.movement = 0

  def update(self, time):
    m = self.movement
    vy = _vel_racket_y

    if (m != 0):
      self.rect.centery += (m * vy) * time

  def reset(self):
    self.points = 0
    self.movement = 0
    self.rect.centery = _height / 2.

  def bound_racket(self, court):
    self.rect.clamp_ip(court)


class Court(Sprite):
  def __init__(self):
   Sprite.__init__(self)

   px, py = _court_padding
   self.image = Surface((_width - 2 * px, _height - 2 * py))
   self.image.fill(Color('blue'))
   self.rect = self.image.get_rect(topleft = _court_padding)

  def update(self, time):
   pass


class Interface(Sprite):
  def __init__(self, game):
    Sprite.__init__(self)

    self.game = game

    self.bg_color = Color('white')
    self.main_color = Color('black')

    self.image = Surface((_width, _height))
    self.rect = self.image.get_rect(topleft = (0,0))

    self.main_font = Font('star_jedi.ttf', 25)
    self.number_font = Font('space_age.ttf', 25)

  def update(self, time):
    g = self.game

    r = Rect(0,0,0,0)
    self.image.fill(self.bg_color)

    s = self.main_font.render('Kevlar Pong', True, self.main_color)
    self.image.blit(s, s.get_rect(center = (_width / 2., 22.5)))

    str = _score_format % (g.p1.name, g.p1.score, g.p2.score, g.p2.name)
    s = self.number_font.render(str, True, self.main_color)
    self.image.blit(s, s.get_rect(center = (_width / 2., _height - 25)))


class Game():
  def __init__(self, p1_name, p2_name, screen):
    self.set = 0
    self.duration = 0.

    self.screen = screen

    self.ball = Ball([1,1],[1,1])

    self.p1 = Player(p1_name, _rackets_x[0])
    self.p2 = Player(p2_name, _rackets_x[1])

    self.court = Court()

    self.interface = Interface(self)

    self.group = LayeredUpdates()
    self.group.add(self.interface, layer = 0)
    self.group.add(self.court, layer = 1)
    self.group.add(self.p1, self.p2, layer = 2)
    self.group.add(self.ball, layer = 3)

    self.init_set()

  def init_set(self):
    self.ball.reset()
    self.p1.reset()
    self.p2.reset()

  def key_pressed(self, key):
    if (key == K_UP):
      self.p2.movement -= 1
    elif (key == K_DOWN):
      self.p2.movement += 1
    elif (key == K_a):
      self.p1.movement -= 1
    elif (key == K_z):
      self.p1.movement += 1

  def key_released(self, key):
    if (key == K_UP):
      self.p2.movement += 1
    elif (key == K_DOWN):
      self.p2.movement -= 1
    elif (key == K_a):
      self.p1.movement += 1
    elif (key == K_z):
      self.p1.movement -= 1

  def update(self, time):
    self.duration += time

    self.group.update(time)
    self.check()

  def check(self):
    p1, p2, court = self.p1, self.p2, self.court

    p1.bound_racket(court)
    p2.bound_racket(court)
    p = self.ball.bound_ball(court.rect, p1.rect, p2.rect)

    if (p != 0):
      self.init_set()
      (p1, p2)[p-1].score += 1

  def draw(self):
    return self.group.draw(self.screen)


def main():
  import os
  os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

  pygame.init()
  screen = display.set_mode((_width, _height))
  display.set_caption('Kevlar Pong')

  p1_name = 'Ivan' #raw_input('Player 1 name: ')
  p2_name = 'Juaquim' #raw_input('Player 2 name: ')
  game = Game(p1_name, p2_name, screen)

  clock = time.Clock()

  screen.fill(Color('white'))
  display.flip()

  while True:
    elapsed = clock.tick(_fps) / 1000.

    for ev in event.get():
      if (ev.type == QUIT):
        return
      elif (ev.type == KEYDOWN):
        game.key_pressed(ev.key)
      elif (ev.type == KEYUP):
        if (ev.key == K_ESCAPE):
          return
        game.key_released(ev.key)

    game.update(elapsed)
    rl = game.draw()
    display.update(rl)

if __name__ == '__main__':
  main()
