import pygame
import random
		
class Uninfected(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.is_dead = True
		self.radius = 30
		self.color = (26, 188, 156)
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
		self.rect = self.surface.get_rect()
		
	def update(self, mouse_pos, window_width, window_height, infected_group):
		self.rect.center = mouse_pos
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > window_width:
			self.rect.right = window_width
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > window_height:
			self.rect.bottom = window_height
		if not self.is_dead:
			self.check_collision(infected_group, window_width, window_height)

	def check_collision(self, infected_group, window_width, window_height):
		if pygame.sprite.spritecollideany(self, infected_group, pygame.sprite.collide_circle):
			self.is_dead = True
		return

class Infected(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.radius = 30
		self.color = (230, 126, 34)
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
		self.rect = self.surface.get_rect()
		self.rect.center = list(pos)
		self.direction = [random.random() * random.choice([1, -1])] # dx direction
		self.direction.append((1 - self.direction[0] ** 2) ** (1 / 2)) # dy direction
		self.speed = random.randrange(5, 10)

	def update(self, group, window_width, window_height):
		self.rect.center = (self.rect.center[0] + self.speed * self.direction[0], self.rect.center[1] + self.speed * self.direction[1])
		group.remove(self)
		collided = self.check_collision(group)
		self.change_direction(collided, window_width, window_height)
		group.add(self)

	def change_direction(self, collided, window_width, window_height):
		if self.rect.left < 0 or self.rect.right > window_width:
			self.direction[0] = -self.direction[0]
			if self.rect.left < 0:
				self.rect.left = 0
			elif self.rect.right > window_width:
				self.rect.right = window_width

		if self.rect.top < 0 or self.rect.bottom > window_height:
			self.direction[1] = -self.direction[1]
			if self.rect.top < 0:
				self.rect.top = 0
			elif self.rect.bottom > window_height:
				self.rect.bottom = window_height
		if collided:
			self.speed, collided.speed = (collided.speed, self.speed)
			self.direction, collided.direction = (collided.direction, self.direction)


	def check_collision(self, group):
		return pygame.sprite.spritecollideany(self, group, pygame.sprite.collide_circle)


