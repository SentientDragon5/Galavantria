import pyglet; import keyboard; import time
clock = 0
#window init
winW = 600; winH = 600
window = pyglet.window.Window(winW + 300,winH)
window.set_caption('RPG by SentientDragon5')
icon1 = pyglet.image.load('n_16x16n.png')
icon2 = pyglet.image.load('n_32x32n.png')
window.set_icon(icon1, icon2)
#mouse init
'''curImage = pyglet.image.load('cur_cursor.png')
cursor = pyglet.window.ImageMouseCursor(curImage, 16, 16)
window.set_mouse_cursor(cursor)'''
#tile init
tileW = 20 ; tileH =20
water = pyglet.image.load('t_water.png')
sand = pyglet.image.load('t_sand.png')
shallow = pyglet.image.load('t_shallow.png')
grass = pyglet.image.load('t_grass.png')
dirt = pyglet.image.load('t_dirt.png')
shallowDirt = pyglet.image.load('t_shallowDirt.png')
stone = pyglet.image.load('t_stone.png')
wood = pyglet.image.load('t_lightRock.png')
ren = pyglet.sprite.Sprite(sand, x=60, y=60)
ren.update(None,None,None,None,float(1/3),float(1/3))
#objects init
objectkey = {}
objectkey['b'] = pyglet.image.load('o_smallBush.png')
objectkey['st'] = pyglet.image.load('o_smallTree.png')
objectkey['lt'] = pyglet.image.load('o_largeTree.png')
objectkey['f0'] = pyglet.image.load('o_fire0.png')
objectkey['f1'] = pyglet.image.load('o_fire1.png')
objectkey['f2'] = pyglet.image.load('o_fire2.png')
objectkey['w'] = pyglet.image.load('o_well.png')
objectkey['c'] = pyglet.image.load('o_chest.png')
objectkey['sb'] = pyglet.image.load('o_smallAdobe.png')
#objectkey[''] = pyglet.image.load('o_.png')
objRen = pyglet.sprite.Sprite(objectkey['b'], x=40, y=40)
objRen.update(None,None,None,None,float(0.4),float(0.4))
#inventory init
inventoryBG = pyglet.image.load('bg_inventory.png')
itemBorder = pyglet.image.load('bg_border.png')
sideRen = pyglet.sprite.Sprite(inventoryBG, x=200, y=600)
itemRen = pyglet.sprite.Sprite(itemBorder, x=60, y=60)
itemRen.update(None,None,None,None,float(1/2),float(1/2))
itemImage = {}
for itemTexture in ['leatherBag','sword','ring','helm','breastplate','boots','cheese']:
    itemImage[itemTexture] = pyglet.image.load(''.join(['i_',itemTexture,'.png']))
#player init
playerSkin = 'd'
playerImage = {}
for character in ['p','d','w']:
    for direction in ['d','l','r','u']:
        for tick in ['0','1','2','3']:
            playerImage[''.join([character,direction,tick])] = pyglet.image.load(''.join(['c_',character,direction,tick,'.png']))
player = pyglet.sprite.Sprite(playerImage[''.join([playerSkin,'d','0'])], x=40, y=40)
player.update(None,None,None,None,float(0.45),float(0.45))
gx = 0 ; gy = 0
#read player data
playerData = {}
save_key = ['x','y','storage','active0','active1','item0','item1','item2','item3','item4','item5','item6','item7','armour0','armour1','armour2']
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
#read & render island data
colorIndex = {}
collisions = {}
def readWorData():
    colorIndex.clear()
    with open('s_default_island_big.txt', 'r') as file:
        x = 0 ; y = 580
        for lineStr in file:
            line = (lineStr.split(' '))
            for char in line:
                if char == '\n':
                    continue
                else:
                    colorIndex[(x,y)] = char
                x += tileW
            y -= tileH
            x = 0
def renWorBg():
    readWorData()
    for y in range(0,winH,20):
        for x in range(0,winW,20):
            colorInfo = colorIndex[(x,y)]
            ren.set_position(x,y)
            if colorInfo == 'w':
                ren.image = water
                collisions[(x,y)] = True
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
            elif colorInfo == 'p':
                ren.image = stone
            elif colorInfo == 'l':
                ren.image = wood
            ren.draw()
#read & render island data
objects = {}
chests = {}
fireCount = 0
for a in range(-20,580,20):
    collisions[(-20,a)] = True
    collisions[(a,-20)] = True
    collisions[(580,a)] = True
    collisions[(a,580)] = True
def renObjects(height):
    global clock, gy, fireCount
    objects.clear()
    with open('s_objects_big.txt', 'r') as file:
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
        if texture == 'f':
            if fireCount == 3:
                fireCount = 0
            objRen.image = objectkey[''.join(['f',str(fireCount)])]
        elif texture == 'sb':
            objRen.image = objectkey[texture]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
        elif texture == 'c':
            objRen.image = objectkey[texture]
            chests[1] = 'item'
        else:
            objRen.image = objectkey[texture]
            collisions[(int(c[0]),int(c[1]))] = True
        if height == 'above':
            if int(c[1]) >= gy:
                objRen.draw()
        else:
            if int(c[1]) < gy:
                objRen.draw()
    fireCount += 1
playerticking = 0
lastd = 'd'
def drawInventory(playerImage):
    #draw Background
    sideRen.image = inventoryBG
    sideRen.set_position(600,0)
    sideRen.draw()
    itemRen.update(None,None,None,None,float(1/2),float(1/2))
    itemRen.image = itemBorder
    itemLoc = {}
    for y in [520]:
        for x in [620]:
            itemRen.set_position(x,y)#for bag type
            itemRen.draw()
            itemLoc['storagex'] = x + 10
            itemLoc['storagey'] = y + 10
    itemNum = 0
    for y in [450,380]:
        for x in [620,690,760,830]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc[''.join(['item',str(itemNum),'x'])] = x + 10
            itemLoc[''.join(['item',str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemNum = 0
    for y in [130,70,10]:
        for x in [720]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc[''.join(['armour',str(itemNum),'x'])] = x + 10
            itemLoc[''.join(['armour',str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemNum = 0
    for y in [260]:
        for x in [650,800]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc[''.join(['active',str(itemNum),'x'])] = x + 10
            itemLoc[''.join(['active',str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemRen.update(None,None,None,None,float(1.2),float(1.2))
    itemRen.image = pyglet.image.load(''.join(['c_',playerSkin,'d0.png']))
    itemRen.set_position(620,40)
    itemRen.draw()
    #draw Items
    for item in save_key:
        if item == 'x':
            drawItem = False
            playerData['x'] = gx
            continue
        elif item == 'y':
            drawItem = False
            playerData['y'] = gy
            continue
        if playerData[item] == 'empty':
            drawItem = False
        else:
            itemRen.image = itemImage[str(playerData[item])]
            itemRen.set_position(itemLoc[''.join([item,'x'])],itemLoc[''.join([item,'y'])])
            itemRen.update(None,None,None,None,float(0.75),float(0.75))
            itemRen.draw()
    
def animateStep(bAnimate,direction,image):
    global playerticking,lastd
    if bAnimate == True:
        playerticking += 1
        if playerticking == 4:
            playerticking = 0
        lastd = direction
    else:
        playerticking = 0
    player.image = playerImage[''.join([image,direction,str(playerticking)])]
def runPlayer(image):
    global gx, gy
    reversex = 0 ; reversey = 0
    keypress = False
    if keyboard.is_pressed('w'):
        gy += 20
        animateStep(True,'u',image)
        reversey = -20
        keypress = True
    elif keyboard.is_pressed('a'):
        gx -= 20
        animateStep(True,'l',image)
        reversex = 20
        keypress = True
    elif keyboard.is_pressed('s'):
        gy -= 20
        animateStep(True,'d',image)
        reversey = 20
        keypress = True
    elif keyboard.is_pressed('d'):
        gx += 20
        animateStep(True,'r',image)
        reversex = -20
        keypress = True
    else:
        animateStep(False,lastd,image)
    if (gx,gy) in collisions:
        gx += reversex ; gy += reversey
        animateStep(False,lastd,image)
    if keypress == True:
        print(gx,gy)
        Savefile = open('s_save_info.txt','w')
        writeList = []
        for info in save_key:
            writeList.append(str(playerData[info]))
            writeList.append(' \n')
        del writeList[-1]
        Savefile.write(str(''.join(writeList))) 
        Savefile.close()
def on_mouse_motion(x, y, dx, dy):
    print(x,y)
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print(x,y)
    if buttons & mouse.LEFT:
        pass
#rerender
def redraw():
    global gx,gy,playerSkin
    window.clear()
    renWorBg()
    renObjects('above')
    player.set_position(gx,gy)
    player.draw()
    renObjects('below')
    drawInventory(playerSkin)
def update(dt):
    global clock,gx,gy
    redraw()
    runPlayer('d')
    #time.sleep(0.075)
    clock += 1
def main():
    pyglet.clock.schedule_interval(update, 0.05)
    pyglet.app.run()
main()
exit()
