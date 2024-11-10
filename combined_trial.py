from scenes import *
screen = Stage((255, 255, 255), width= 1000, height= 800)
timer = Timer(screen, 50)
screen.createWindow(1500, 900, 'Dot Example')
# plus = Movement((255,255,0), [390, 290], screen, timer)
# plus.createObject('plus', plus_dims=[100, 100])
# plus.move('left', 250, 1)

beep = Movement((255,0,0), [390, 290], screen, timer)
beep.createObject(['beep', 'arrow'], arrow_dims=[100, 20, 30, 'left'], sound_dims=[500, 2, 10])
beep.move(['left','left'], 400, 1)

# beep1  = Sound(screen, timer)
# beep1.createBeep(500, 2, 10)
# beep1.play('left')
