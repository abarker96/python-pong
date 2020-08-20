import sys, pygame, time

# global variables
screen = None
height = 400
width = height * 16 // 9
size = width, height


# main game function
def pong():
	global screen
	# initialization
	pygame.init()
	screen = pygame.display.set_mode(size)

	# create pong object and play
	board = Board(width, height, screen)
	board.play()


# game object class for managing objects in game
class GameObject(pygame.sprite.Sprite):
	def __init__(self, color, width, height, board):
		pygame.sprite.Sprite.__init__(self)
		self.board = board
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.controller = None

	def draw(self, scr):
		scr.blit(self.image, self.rect)

	def move(self, speed):
		self.rect = self.rect.move(speed)

	def update(self):
		if self.controller is None:
			return
		self.controller.controll()


# paddle class for managing pong paddles
class Paddle(GameObject):
	def __init__(self, color, width, height, board):
		GameObject.__init__(self, color, width, height, board)


# ball class for managing pong ball
class Ball(GameObject):
	def __init__(self, color, size, board):
		GameObject.__init__(self, color, size, size, board)
		pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
		self.speed = [3, 2.5]

	def move(self, speed):
		self.rect = self.rect.move(speed)

	def update(self):
		GameObject.update(self)
		self.move(self.speed)
		if self.rect.top < 0 or self.rect.bottom > self.board.height:
			self.speed[1] = -self.speed[1]


# board for managing screen and game
class Board:
	# static class variables
	background_color = 0xddddff

	def __init__(self, w, h, scr):
		self.screen = scr
		self.width = w
		self.height = h
		self.background = 0xddddff

		ball_size = 16
		paddle_width = 10
		paddle_height = 40

		self.ball = Ball(0xffaaaa, ball_size, self)
		self.ball.rect.x = w // 2
		self.ball.rect.y = h // 2

		self.p1 = Paddle(0xff4444, paddle_width, paddle_height, self)
		self.p1.rect.x = w - 10 - paddle_width
		self.p1.rect.y = h // 2
		self.p1.controller = PlayerController(self.p1, self)

		self.p2 = Paddle(0xff4444, paddle_width, paddle_height, self)
		self.p2.rect.x = 10
		self.p2.rect.y = h // 2
		self.p2.controller = AIController(self.p2, self)

	def play(self):
		update_time = 1 / 60
		last_update = time.time()
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
			# main game function
			should_render = 0
			now = time.time()
			while now - last_update >= update_time:
				self.update()
				last_update = now
				now += update_time
				should_render = 1
			if should_render: self.render()

	# update objects
	def update(self):
		self.p1.update()
		self.p2.update()
		self.ball.update()

		b_left = self.ball.rect.left
		b_right = self.ball.rect.right
		b_top = self.ball.rect.top
		b_bottom = self.ball.rect.bottom

		if b_left < self.p2.rect.right and (self.p2.rect.top < b_bottom and b_top < self.p2.rect.bottom):
			self.ball.speed[0] = -self.ball.speed[0]
		elif b_right > self.p1.rect.left and (self.p1.rect.top < b_bottom and b_top < self.p1.rect.bottom):
			self.ball.speed[0] = -self.ball.speed[0]
		elif b_left < 0 or b_right > self.width:
			self.game_over()

	# end the game
	def game_over(self):
		self.ball.speed = [0, 0]
		print("Game Over!!")
		sys.exit()

	# render objects
	def render(self):
		self.screen.fill(Board.background_color)
		self.p1.draw(self.screen)
		self.p2.draw(self.screen)
		self.ball.draw(self.screen)
		pygame.display.update()


class Controller:
	def __init__(self, target, board):
		self.target = target
		self.board = board

	def controll(self):
		pass


class AIController(Controller):
	def controll(self):
		if self.board.ball.speed[0] > 0: return
		t = self.target
		b = self.board.ball
		if b.rect.top > t.rect.top:
			t.move([0, 2])
		elif b.rect.bottom < t.rect.bottom:
			t.move([0, -2])


class PlayerController(Controller):
	def controll(self):
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.target.rect.top > 0:
			self.target.move([0, -3])
		elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.target.rect.top < self.board.height:
			self.target.move([0, 3])


if __name__ == "__main__":
	pong()
