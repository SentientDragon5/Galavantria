import pyglet; import keyboard; import time
#window init
winW = 600; winH = 600
window = pyglet.window.Window(winW,winH)
window.set_caption('RPG by SentientDragon5')
icon1 = pyglet.image.load('i_16x16n.png')
icon2 = pyglet.image.load('i_32x32n.png')
window.set_icon(icon1, icon2)
#tile init
tileW = 40 ; tileH =40
water = pyglet.image.load('t_water.png')
sand = pyglet.image.load('t_sand.png')
shallow = pyglet.image.load('t_shallow.png')
grass = pyglet.image.load('t_grass.png')
dirt = pyglet.image.load('t_dirt.png')
shallowDirt = pyglet.image.load('t_shallowDirt.png')
ren = pyglet.sprite.Sprite(sand, x=tileW, y=tileH)
#player init
playerimage = pyglet.image.load('c_Player.png')
player = pyglet.sprite.Sprite(playerimage, x=40, y=40)
player.update(None,None,None,None,float(0.6),float(0.6))
gx = 0 ; gy = 0

#read player data
playerData = {}
save_key = ['x','y']
with open('s_save_info.txt', 'r') as file:
    Count = 0
    for lineStr in file:
        line = (lineStr.split(' '))
        for char in line:
            if char == '\n':
                #skip
                print()
            else:
                playerData[save_key[Count]] = char
                Count += 1
gx = int(playerData['x']) ; gy = int(playerData['y'])

#read & render island data
colorIndex = {}
def readWorData():
    colorIndex.clear()
    with open('s_default_island.txt', 'r') as file:
        x = 0 ; y = 0
        for lineStr in file:
            line = (lineStr.split(' '))
            for char in line:
                if char == '\n':
                    continue
                else:
                    colorIndex[(x,y)] = char
                x += tileW
            y += tileH
            x = 0
def renWorBg():
    readWorData()
    for y in range(0,600,40):
        for x in range(0,600,40):
            colorInfo = colorIndex[(x,y)]
            ren.set_position(x,y)
            if colorInfo == 'w':
                ren.image = water
            elif colorInfo == 's':
                ren.image = sand
            elif colorInfo == 'a':
                ren.image = shallow
            elif colorInfo == 'g':
                ren.image = grass
            elif colorInfo == 'd':
                ren.image = dirt
            elif colorInfo == 'f':
                ren.image = shallowDirt
            ren.draw()
#rerender
def redraw():
    global gx,gy
    window.clear()
    renWorBg()
    player.set_position(gx,gy)
    player.draw()
def update(dt):
    global gx,gy
    redraw()
    if keyboard.is_pressed('w'):
        gy += 40
    if keyboard.is_pressed('a'):
        gx -= 40
    if keyboard.is_pressed('s'):
        gy -= 40
    if keyboard.is_pressed('d'):
        gx += 40
    time.sleep(0.075)
    if gx >= 600:
        gx -= 40
    if gx <= -40:
        gx += 40
    if gy >= 600:
        gy -= 40
    if gy <= -40:
        gy += 40
    Savefile = open('s_save_info.txt','w')
    writeList = [str(gx) , ' \n' , str(gy)]
    Savefile.write(str(''.join(writeList))) 
    Savefile.close() 
def main():
    pyglet.clock.schedule_interval(update, 0.05)
    pyglet.app.run()
main()
exit()
