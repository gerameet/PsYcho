from scenes import *
screen = Stage((255, 255, 255), width= 1000, height= 800)
timer = Timer(screen, 50)
screen.createWindow(800, 600, 'Dot Example')
plus = Movement((255,255,0), [390, 290], screen, timer)
plus.createObject('arrow', arrow_dims=[100, 20, 30, 'right'])
plus.move('left', 250, 1)

dot = Movement((255,0,0), [390, 290], screen, timer)
dot.createObject('dot', 20)
dot.move('right', 400, 1)

beep1  = Sound(screen, timer)
beep1.createBeep(500, 2, 10)
beep1.play('left')
