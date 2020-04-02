

import pygame
import sys 
import random
import time
import math
import json
import os

import game_objects

from pygame.locals import *


pygame.init()
pygame.mixer.init()



class Game:
	def __init__(self):
		self.playing = True
		self.FPS = 60
		self.clock = pygame.time.Clock()
		self.window_width = 50 * 25
		self.window_height = 50 * 15
		self.window = pygame.display.set_mode((self.window_width, self.window_height))
		pygame.display.set_caption("OUST DUTERTE!!!")
		# self.cover_art = pygame.image.load(self.find_data_file("cover_art.jpg"))

		self.uninfected = game_objects.Uninfected()
		self.infected_grp = pygame.sprite.Group()
		# total of 10 infected obj
		for i in range(4):
			x = ((self.window_width // 4) * i + (self.window_width // 4) * (i + 1)) // 2
			self.infected_grp.add(game_objects.Infected((x, 50)))
			self.infected_grp.add(game_objects.Infected((x, self.window_height - 50)))

		self.infected_grp.add(game_objects.Infected((100, self.window_height // 2)))
		self.infected_grp.add(game_objects.Infected((self.window_width - 100, self.window_height // 2)))

		# labels
		self.font_color = (255, 255, 255)
		self.font_obj = pygame.font.SysFont("Terminal", 50, bold=True)
		self.score = 0
		self.texts = {
			"title": self.font_obj.render("A VOID", True, self.font_color),
			"enter": self.font_obj.render("Click To Play!", True, self.font_color),
			"score": self.font_obj.render("Score: {}".format(self.score), True, self.font_color),
		}
		self.text_rects = {
			"title": self.texts["title"].get_rect(),
			"enter": self.texts["enter"].get_rect(),
			"score": self.texts["score"].get_rect(),
		}
		self.text_rects["title"].center = (self.window_width // 2, self.window_height // 2 - 200)
		self.text_rects["enter"].center = (self.window_width // 2, self.window_height // 2 + 100)
		self.text_rects["score"].bottomleft = (0, self.window_height)

	def find_data_file(self, filename):
	    if getattr(sys, 'frozen', False):
	        datadir = os.path.dirname(sys.executable)
	    else:
	        datadir = os.path.dirname(__file__)

	    return os.path.join(datadir, filename)



	def run(self):
		while self.playing:
			self.clicked = pygame.mouse.get_pressed()[0]
			self.mouse_pos = pygame.mouse.get_pos()
			pygame.mouse.set_visible(False)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					self.playing = False
				if self.uninfected.is_dead and self.clicked:
					self.uninfected.is_dead = False
					self.score = 0
			if self.uninfected.is_dead:
				self.window.fill((30, 39, 46))
			else:
				self.window.fill((0, 0, 0))
			self.texts["score"] =  self.font_obj.render("Score: {}".format(self.score), True, self.font_color)
			self.window.blit(self.texts["score"], self.text_rects["score"])
			self.window.blit(self.uninfected.surface, self.uninfected.rect)
			for infected in self.infected_grp:
				self.window.blit(infected.surface, infected.rect)
				infected.update(self.infected_grp, self.window_width, self.window_height)
			self.uninfected.update(self.mouse_pos, self.window_width, self.window_height, self.infected_grp)
			if self.uninfected.is_dead:
				self.window.blit(self.texts["title"], self.text_rects["title"])
				self.window.blit(self.texts["enter"], self.text_rects["enter"])
			else:
				self.score += .01
				self.score = round(self.score, 2)

			pygame.display.update()
			self.clock.tick(self.FPS)


if __name__ == "__main__":
	game = Game()
	game.run()
