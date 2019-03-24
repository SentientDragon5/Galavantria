import pyglet; import keyboard; import time
clock = 0
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
#objects init
bush = pyglet.image.load('o_smallBush.png')
smallTree = pyglet.image.load('o_smallTree.png')
largeTree = pyglet.image.load('o_largeTree.png')
objRen = pyglet.sprite.Sprite(bush, x=40, y=40)
objRen.update(None,None,None,None,float(0.6),float(0.6))
#player init
playerimage = pyglet.image.load('c_Player.png')
player = pyglet.sprite.Sprite(playerimage, x=40, y=40)
player.update(None,None,None,None,float(0.5),float(0.5))
playerImage = {}
playerImage['pd0'] = pyglet.image.load('pd0.png')
playerImage['pd1'] = pyglet.image.load('pd1.png')
playerImage['pd2'] = pyglet.image.load('pd2.png')
playerImage['pd3'] = pyglet.image.load('pd3.png')
playerImage['pl0'] = pyglet.image.load('pl0.png')
playerImage['pl1'] = pyglet.image.load('pl1.png')
playerImage['pl2'] = pyglet.image.load('pl2.png')
playerImage['pl3'] = pyglet.image.load('pl3.png')
playerImage['pr0'] = pyglet.image.load('pr0.png')
playerImage['pr1'] = pyglet.image.load('pr1.png')
playerImage['pr2'] = pyglet.image.load('pr2.png')
playerImage['pr3'] = pyglet.image.load('pr3.png')
playerImage['pu0'] = pyglet.image.load('pu0.png')
playerImage['pu1'] = pyglet.image.load('pu1.png')
playerImage['pu2'] = pyglet.image.load('pu2.png')
playerImage['pu3'] = pyglet.image.load('pu3.png')
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
                continue
            else:
                playerData[save_key[Count]] = char
                Count += 1
    gx = int(playerData['x']) ; gy = int(playerData['y'])


playerticking = 0
lastd = 'd'
def animateStep(bAnimate,direction):
    global playerticking,lastd
    if bAnimate == True:
        playerticking += 1
        if playerticking == 4:
            playerticking = 0
        lastd = direction
    else:
        playerticking = 0
    player.image = playerImage[''.join(['p',direction,str(playerticking)])]
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
#read & render island data
objects = {}
collisions = {}
def renObjects(height):
    global gy
    objects.clear()
    with open('s_objects.txt', 'r') as file:
        for lineStr in file:
            line = (lineStr.split(' '))
            objects[line[0]] = line[1]
            line.clear()
    for item in objects:
        texture = objects[item]
        a = item.split('(')
        b = a[1].split(')')
        c = b[0].split(',')
        objRen.set_position(int(c[0]),int(c[1]))
        if texture == 'st':
            objRen.image = smallTree
        if texture == 'b':
            objRen.image = bush
        if texture == 'lt':
            objRen.image = largeTree
        collisions[(int(c[0]),int(c[1]))] = True
        if height == 'above':
            if int(c[1]) >= gy:
                objRen.draw()
        else:
            if int(c[1]) < gy:
                objRen.draw()
for a in range(-40,600,40):
    collisions[(-40,a)] = True
    collisions[(a,-40)] = True
    collisions[(600,a)] = True
    collisions[(a,600)] = True
    
#rerender
def redraw():
    global gx,gy
    window.clear()
    renWorBg()
    renObjects('above')
    player.set_position(gx,gy)
    player.draw()
    renObjects('below')
def update(dt):
    global clock,gx,gy
    redraw()
    reversex = 0 ; reversey = 0
    keypress = False
    if keyboard.is_pressed('w'):
        gy += 40
        animateStep(True,'u')
        reversey = -40
        keypress = True
    elif keyboard.is_pressed('a'):
        gx -= 40
        animateStep(True,'l')
        reversex = 40
        keypress = True
    elif keyboard.is_pressed('s'):
        gy -= 40
        animateStep(True,'d')
        reversey = 40
        keypress = True
    elif keyboard.is_pressed('d'):
        gx += 40
        animateStep(True,'r')
        reversex = -40
        keypress = True
    else:
        animateStep(False,lastd)
    if (gx,gy) in collisions:
        gx += reversex ; gy += reversey
        animateStep(False,lastd)
    if keypress == True:
        Savefile = open('s_save_info.txt','w')
        writeList = [str(gx) , ' \n' , str(gy)]
        Savefile.write(str(''.join(writeList))) 
        Savefile.close()
    time.sleep(0.15)
    clock += 1
def main():
    pyglet.clock.schedule_interval(update, 0.05)
    pyglet.app.run()
main()
exit()
