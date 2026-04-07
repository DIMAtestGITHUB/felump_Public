import pygame  as pg
import sys
pg.init()
X,Y = 500, 500
sc = pg.display.set_mode((X,Y))

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			sys.exit()
	sc.fill("green")
	pg.draw.rect(sc, "yellow", ((X/2)-150,(Y/2)-150,300,300))	
	pg.draw.circle(sc, "red", (X/2,Y/2), 150)
	pg.display.flip()
