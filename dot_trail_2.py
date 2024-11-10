from scenes import *
screen = Stage((255, 255, 255), width= 800, height= 600)
screen.createWindow(800, 600, 'Dot Example')
dot = Movement((255,255,255), [390, 290], screen)
dot.createObject('dot', 50)
dot.move('left', 50, 5)