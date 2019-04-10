'''
Galavantria
created by SentientDragon5
started March 2019
Art credit to
 - scratch.com users gamerkeep & ninja545
 - FangTrooper56
'''
import pyglet; import keyboard; import time
clock = 0
#window init
winW = 600; winH = 600
window = pyglet.window.Window(winW + 300,winH)
window.set_caption('Gallivantria')
window.set_icon(pyglet.image.load('n_16x16.png'), pyglet.image.load('n_32x32.png'))
invisible = pyglet.image.load('invisible.png')
#tile init
houseA = 'house'
defaultMap = 'defaultMap'
globalWorld = defaultMap
tileW = 20 ; tileH =20
tile = {}
tile['w'] = pyglet.image.load('t_water.png')
tile['s'] = pyglet.image.load('t_sand.png')
tile['q'] = pyglet.image.load('t_darkSand.png')
tile['a'] = pyglet.image.load('t_shallow.png')
tile['g'] = pyglet.image.load('t_grass.png')
tile['m'] = pyglet.image.load('t_grassWeed.png')
tile['n'] = pyglet.image.load('t_grassWeed2.png')
tile['o'] = pyglet.image.load('t_grassWeed3.png')
tile['d'] = pyglet.image.load('t_dirt.png')
tile['f'] = pyglet.image.load('t_shallowDirt.png')
tile['e'] = pyglet.image.load('t_stone.png')
tile['p'] = pyglet.image.load('t_polished.png')
tile['x'] = pyglet.image.load('t_wood.png')
tile['l'] = pyglet.image.load('t_lightRock.png')
tile['k'] = pyglet.image.load('t_darkRock.png')
tile['r'] = pyglet.image.load('t_grassRock.png')
tile['.'] = pyglet.image.load('t_empty.png')
ren = pyglet.sprite.Sprite(tile['s'], x=60, y=60)
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
objectkey['bd'] = pyglet.image.load('o_bed.png')
objectkey['t'] = pyglet.image.load('o_table.png')
objectkey['sb'] = pyglet.image.load('o_smallAdobe.png')
objectkey['bo'] = pyglet.image.load('o_boat.png')
objectkey['bs'] = pyglet.image.load('o_bookshelf.png')
objectkey['ch'] = pyglet.image.load('o_chair.png')
objectkey['br'] = pyglet.image.load('o_barrel.png')
objectkey['gt'] = pyglet.image.load('o_giantTree.png')
objectkey['s'] = pyglet.image.load('o_woodShade.png')
objectkey['v'] = pyglet.image.load('o_Vase.png')
objectkey['vf'] = pyglet.image.load('o_vaseFlowers.png')
objRen = pyglet.sprite.Sprite(objectkey['b'], x=40, y=40)
objRen.update(None,None,None,None,float(0.4),float(0.4))
#inventory init
inventoryBG = pyglet.image.load('bg_inventoryo.png')
itemBorder = pyglet.image.load('bg_border.png')
itemBorderActive = pyglet.image.load('bg_border_active.png')
sideRen = pyglet.sprite.Sprite(inventoryBG, x=200, y=600)
itemRen = pyglet.sprite.Sprite(itemBorder, x=60, y=60)
itemRen.update(None,None,None,None,float(1/2),float(1/2))
itemImage = {}
for itemTexture in ['leatherBag','sword','ring','eyeOfTheSea','helm','breastplate','boots','cheese','ore','sværd','magic_blade','iron_sword','gold_sword']:
    itemImage[itemTexture] = pyglet.image.load(''.join(['i_',itemTexture,'.png']))
#action window init
door = pyglet.image.load('w_door.png')
action = pyglet.sprite.Sprite(door, x=200, y=200)
action.update(None,None,None,None,float(2),float(2))
#player init
skins = ['p','d','w']
skinNum = 1 #change number to change default skin 0 ~ original, 1 ~ dress girl, 2 ~ wizard
playerSkin = skins[skinNum]
playerImage = {}
for character in skins:
    for direction in ['d','l','r','u']:
        for tick in ['0','1','2','3']:
            playerImage[''.join([character,direction,tick])] = pyglet.image.load(''.join(['c_',character,direction,tick,'.png']))
player = pyglet.sprite.Sprite(playerImage[''.join([playerSkin,'d','0'])], x=40, y=40)
player.update(None,None,None,None,float(0.45),float(0.45))
gx = 0 ; gy = 0
#read player data
playerData = {}
save_key = ['x','y','storage','active0','active1','item0','item1','item2','item3','armour0','armour1','armour2']
def readPlayer():
    global playerData, save_key, gx, gy
    with open(''.join(['s_save_',playerSkin,'.txt']), 'r') as file:
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
readPlayer()
#read Chest
chest_save_key = ['item0','item1','item2','item3','item4','item5','item6','item7',]
chests = {}
with open('s_chest.txt', 'r') as file:
    Count = 0
    for lineStr in file:
        line = (lineStr.split(' '))
        for char in line:
            if char == '\n':
                continue
            else:
                chests[chest_save_key[Count]] = char
                Count += 1
#read & render island data
colorIndex = {}
collisions = {}
def renWorBg(world):
    collisions.clear()
    colorIndex.clear()
    with open(''.join(['m_',world,'.txt']), 'r') as file: #default_island_big
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
    for y in range(0,winH,20):
        for x in range(0,winW,20):
            colorInfo = colorIndex[(x,y)]
            ren.set_position(x,y)
            if colorInfo == 'w':
                ren.image = tile['w']
                collisions[(x,y)] = True
            elif colorInfo == '.':
                ren.image = tile['.']
                collisions[(x,y)] = True
            else:
                ren.image = tile[colorInfo]
            ren.draw()
#read & render island data
objects = {}
acessLoc = {'house':'empty','chest':'empty'}
fireCount = 0
def edgeCollisions():
    for a in range(-20,580,20):
        collisions[(-20,a)] = True
        collisions[(a,-20)] = True
        collisions[(580,a)] = True
        collisions[(a,580)] = True
    for a in range(0,600,20):
        collisions[(0,a)] = True
        collisions[(a,0)] = True
        collisions[(600,a)] = True
        collisions[(a,600)] = True
def renObjects(world,height):
    global clock, gy, fireCount, acessLoc
    objects.clear()
    with open(''.join(['mo_',world,'.txt']), 'r') as file:
        for lineStr in file:
            line = (lineStr.split(' '))
            objects[line[0]] = line[1]
            line.clear()
    for item in objects:
        texture = objects[item]
        a = item.split('(')
        b = a[1].split(')')
        c = b[0].split(',')
        if texture == 's':
            objRen.image = objectkey[texture]
            objRen.set_position(int(c[0]),int(c[1]) + 20)
        else:
            objRen.set_position(int(c[0]),int(c[1]))
        if texture == 'f':
            if fireCount >= 3:
                fireCount = 0
            objRen.image = objectkey[''.join(['f',str(fireCount)])]
        elif texture == 's':
            pass
        elif texture == 'sb':
            objRen.image = objectkey[texture]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc['house'] = (int(c[0]) + 40,int(c[1]) - 20)
        elif texture == 'bo':
            objRen.image = objectkey[texture]
            for sby in [0,20]:
                for sbx in [0,20,40]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc['boat'] = (int(c[0]),int(c[1]) + 20)
        elif texture == 'bd':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [0,20]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'lt':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [0,20]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'gt':
            objRen.image = objectkey[texture]
            for bdy in [20,40]:
                for bdx in [40,60]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'bs':
            objRen.image = objectkey[texture]
            for bdy in [0]:
                for bdx in [0,20,40,60,80,100]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'c':
            objRen.image = objectkey[texture]
            collisions[(int(c[0]),int(c[1]))] = True
            acessLoc['chest'] = (int(c[0]),int(c[1]) - 20)
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
    global gx, gy, acessLoc
    #draw Background
    sideRen.image = inventoryBG
    sideRen.set_position(600,0)
    sideRen.draw()
    itemRen.update(None,None,None,None,float(1/2),float(1/2))
    itemRen.image = itemBorder
    itemLoc = {}
    for y in [520]:
        for x in [793]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc['storagex'] = x + 10 ; itemLoc['storagey'] = y + 10
    itemNum = 0
    for y in [450,380]:
        for x in [760,830]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc[''.join(['item',str(itemNum),'x'])] = x + 10 ; itemLoc[''.join(['item',str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemNum = 0
    for y in [500,430,360]:
        for x in [690]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc[''.join(['armour',str(itemNum),'x'])] = x + 10 ; itemLoc[''.join(['armour',str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemNum = 0
    for y in [290]:
        for x in [650,800]:
            itemRen.set_position(x,y)
            itemRen.draw()
            itemLoc[''.join(['active',str(itemNum),'x'])] = x + 10 ; itemLoc[''.join(['active',str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemRen.update(None,None,None,None,float(1.2),float(1.2))
    itemRen.image = pyglet.image.load(''.join(['c_',playerSkin,'d0.png']))
    itemRen.set_position(610,410)
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
    action.image = invisible
    action.update(None,None,None,None,float(2),float(2))
    if globalWorld == defaultMap:
        if (gx, gy) == acessLoc['house']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['chest']:
            itemRen.update(None,None,None,None,float(1/2),float(1/2))
            itemRen.image = itemBorder
            itemLoc = {}
            itemNum = 0
            for y in [10,80,150,220]:
                for x in [760,830]:
                    itemRen.set_position(x,y)
                    itemRen.draw()
                    itemLoc[''.join(['item',str(itemNum),'x'])] = x + 10 ; itemLoc[''.join(['item',str(itemNum),'y'])] = y + 10
                    itemNum += 1
            #draw Chest Items
            for item in chest_save_key:
                if chests[item] == 'empty':
                    drawItem = False
                else:
                    itemRen.image = itemImage[str(chests[item])]
                    itemRen.set_position(itemLoc[''.join([item,'x'])],itemLoc[''.join([item,'y'])])
                    itemRen.update(None,None,None,None,float(0.75),float(0.75))
                    itemRen.draw()
            action.update(None,None,None,None,float(1.5),float(1.5))
            ptext('click to switch\nthe boxes',630,70,10)
            action.image = objectkey['c']
            action.set_position(630,120)
def inventoryEdit():
    pass
def executeAction(actionType):
    global gx, gy, globalWorld, exitTox, exitToy, playerSkin, lastd
    tempx = gx
    tempy = gy
    if actionType == 'h':
        if globalWorld == houseA:
            globalWorld = defaultMap
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        if (tempx,tempy) == acessLoc['house']:
            print('enter/exit house')
            if globalWorld == defaultMap:
                globalWorld = houseA
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 120#enter house location
                animateStep(False,'u',playerSkin) ; lastd = 'u'
    #if actionType == 'b':
        
#player
exitTox = gx ; exitToy = gy
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
pressedLast = True
def runPlayer(image):
    global gx, gy, globalWorld, pressedLast, skins, skinNum, playerSkin, exitTox, exitToy, gmessage
    reversex = 0 ; reversey = 0
    keypress = False ; drawChest = False
    if keyboard.is_pressed('w'):#move up
        gy += 20
        animateStep(True,'u',image)
        reversey = -20
        keypress = True; pressedLast = True
    elif keyboard.is_pressed('a'):#move left
        gx -= 20
        animateStep(True,'l',image)
        reversex = 20
        keypress = True ; pressedLast = True
    elif keyboard.is_pressed('s'):#move down
        gy -= 20
        animateStep(True,'d',image)
        reversey = 20
        keypress = True ; pressedLast = True
    elif keyboard.is_pressed('d'):#move right
        gx += 20
        animateStep(True,'r',image)
        reversex = -20
        keypress = True ; pressedLast = True
    elif keyboard.is_pressed('e'):#enter house
        pressedLast = False
        executeAction('h')
        executeAction('b')
    elif keyboard.is_pressed('q'):#change player
        pressedLast = False
        skinNum += 1
        if skinNum >= 3:
            skinNum = 0
        playerSkin = skins[skinNum]
        readPlayer()
    elif keyboard.is_pressed('enter'):#function 1
        print('function 1')
    elif keyboard.is_pressed('shift'):#function 2
        print('function 2')
    else:
        animateStep(False,lastd,image)
        keypress = False
    #ren Inventory (chest)
    if (gx,gy) in collisions:
        gx += reversex ; gy += reversey
        animateStep(False,lastd,image)
    if keypress == True:
        print(gx,gy)
        Savefile = open(''.join(['s_save_',playerSkin,'.txt']),'w')
        writeList = []
        for info in save_key:
            if globalWorld == houseA:
                if info == 'x':
                    writeList.append(str(exitTox))
                elif info == 'y':
                    writeList.append(str(exitToy))
                else:
                    writeList.append(str(playerData[info]))
            else:
                writeList.append(str(playerData[info]))
            writeList.append(' \n')
        del writeList[-1]
        Savefile.write(str(''.join(writeList))) 
        Savefile.close()
def ptext(info,x,y,size):
    lines = info.split('\n')
    yOffset = 0
    for line in lines:
        text = pyglet.text.Label(line, font_name='Arial', font_size=10,x=x, y=(y + yOffset))
        text.draw()
        yOffset -= size * 1.5
#rerender
def update(dt):
    global clock,gx,gy,playerSkin,globalWorld, textx, texty, textinfo
    #drawChest = False
    window.clear()
    runPlayer(playerSkin)
    drawInventory(playerSkin)
    renWorBg(globalWorld)
    renObjects(globalWorld,'above')
    player.set_position(gx,gy)
    player.draw()
    renObjects(globalWorld,'below')
    action.draw()
    clock += 1
def main():
    pyglet.clock.schedule_interval(update, 0.05)
    pyglet.app.run()
main()
exit()
