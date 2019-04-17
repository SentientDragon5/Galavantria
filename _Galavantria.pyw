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
tileW = 20 ; tileH =20
tile = {}
for info in ['.','a','d','e','f','g','k','l','p','q','r','s','w','x']:
    tile[info] = pyglet.image.load(''.join(['t_',info,'.png']))
ren = pyglet.sprite.Sprite(tile['s'], x=60, y=60)
ren.update(None,None,None,None,float(1/3),float(1/3))
#objects init
objectkey = {}
for info in ['b','bd','bd','bd2','br','bo','bs','c','ch','f0','f1','f2','fs','gt','lt','mt','ps','s','sb','lb','st','sg','sy','t','v','vf','w']:
    objectkey[info] = pyglet.image.load(''.join(['o_',info,'.png']))
objRen = pyglet.sprite.Sprite(objectkey['b'], x=40, y=40)
objRen.update(None,None,None,None,float(0.4),float(0.4))
#inventory init
inventoryBG = pyglet.image.load('bg_inventory.png')
itemBorder = pyglet.image.load('bg_border.png')
itemBorderActive = pyglet.image.load('bg_border_active.png')
itemRen = pyglet.sprite.Sprite(itemBorder, x=60, y=60)
itemRen.update(None,None,None,None,float(1),float(1))
itemImage = {}
for info in ['leatherBag','sword','eyeOfTheSea','helm','breastplate','boots','cheese','ore','sværd']:
    itemImage[info] = pyglet.image.load(''.join(['i_',info,'.png']))
#action window init
door = pyglet.image.load('w_door.png')
action = pyglet.sprite.Sprite(door, x=200, y=200)
action.update(None,None,None,None,float(2),float(2))
#player init
skins = ['d']
skinNum = 0 #change number to change default skin 0 ~ original, 1 ~ dress girl, 2 ~ wizard
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
houseA = '3h0'
house = {}
house['3h0'] = ''
defaultMap = '2'#'defaultMap'
islands = {}
islands[0] = '2'
islands[1] = '3'
islands[2] = '4'
playerData = {}
save_key = ['world','x','y','storage','active0','active1','item0','item1','item2','item3','armour0','armour1','armour2']
inventoryKey = ['storage','active0','active1','item0','item1','item2','item3','armour0','armour1','armour2']
def readPlayer():
    global playerData, save_key, gx, gy, globalWorld
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
    globalWorld = playerData['world']
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
    with open(''.join(['m_',world,'.txt']), 'r') as file:
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
                collisions[(x,y)] = True
            elif colorInfo == '.':
                collisions[(x,y)] = True
            ren.image = tile[colorInfo]
            ren.draw()
#read & render island data
objects = {}
acessLoc = {'3h0':'empty','4h0':'empty','4h1':'empty','4h2':'empty','4h3':'empty','4h4':'empty','chest':'empty','boat':'empty'}
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
    def makeHouse(num):
        pass
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
            objRen.image = objectkey[texture]
        elif texture == 'mt':
            objRen.image = objectkey[texture]
        elif texture == 'sb.0':
            l = texture.split('.')
            objRen.image = objectkey[l[0]]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc[''.join(['3h',str(l[1])])] = (int(c[0]) + 40,int(c[1]) - 20)
        elif texture == 'sb.1':
            l = texture.split('.')
            objRen.image = objectkey[l[0]]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc[''.join(['4h',str(l[1])])] = (int(c[0]) + 40,int(c[1]) - 20)
        elif texture == 'sb.2':
            l = texture.split('.')
            objRen.image = objectkey[l[0]]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc[''.join(['4h',str(l[1])])] = (int(c[0]) + 40,int(c[1]) - 20)
        elif texture == 'sb.3':
            l = texture.split('.')
            objRen.image = objectkey[l[0]]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc[''.join(['4h',str(l[1])])] = (int(c[0]) + 40,int(c[1]) - 20)
        elif texture == 'sb.4':
            l = texture.split('.')
            objRen.image = objectkey[l[0]]
            for sby in [0,20]:
                for sbx in [0,20,40,60,80]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc[''.join(['4h',str(l[1])])] = (int(c[0]) + 40,int(c[1]) - 20)
        elif texture == 'lb.0':
            l = texture.split('.')
            objRen.image = objectkey[l[0]]
            for sby in [0,20,40,60]:
                for sbx in [0,20,40,60,80,100,120]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc[''.join(['4h',str(l[1])])] = (int(c[0]) + 60,int(c[1]) - 20)
        elif texture == 'bo':
            objRen.image = objectkey[texture]
            for sby in [0]:
                for sbx in [0,20,40]:
                    collisions[(int(c[0]) + sbx,int(c[1]) + sby)] = True
            acessLoc['boat'] = (int(c[0]) + 20,int(c[1]) + 20)
        elif texture == 'fs':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [0,20,40]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'bd':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [0,20]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'bd2':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [0,20]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'ps':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [0,20]:
                    collisions[(int(c[0]) + bdx,int(c[1]) + bdy)] = True
        elif texture == 'lt':
            objRen.image = objectkey[texture]
            for bdy in [0,20]:
                for bdx in [20,40]:
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
active = {}
def clearActive():
    for key in inventoryKey:
        active[key] = False
clearActive()
def switch(one,two):
    global active
    oldone = playerData[one]
    oldtwo = playerData[two]
    playerData[one] = oldtwo
    playerData[two] = oldone
def inventoryEdit():
    if keyboard.is_pressed('q'):
        pass
def drawInventory(playerImage):
    global gx, gy, acessLoc, active
    def checkActive(catagory,num):
        if active[''.join([catagory,str(num)])] == True:
            itemRen.update(None,None,None,None,float(1/4),float(1/4))
            itemRen.image = itemBorderActive
        else:
            itemRen.update(None,None,None,None,float(1/2),float(1/2))
            itemRen.image = itemBorder
        itemRen.draw()
    #draw Background
    itemRen.update(None,None,None,None,float(1),float(1))
    itemRen.image = inventoryBG
    itemRen.set_position(600,0)
    itemRen.draw()
    itemLoc = {}
    for y in [520]:
        for x in [793]:
            itemRen.set_position(x,y)
            checkActive('storage','')
            itemLoc['storagex'] = x + 10 ; itemLoc['storagey'] = y + 10
    itemNum = 0
    catagory = 'item'
    for y in [450,380]:
        for x in [760,830]:
            itemRen.set_position(x,y)
            checkActive(catagory,itemNum)
            itemLoc[''.join([catagory,str(itemNum),'x'])] = x + 10 ; itemLoc[''.join([catagory,str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemNum = 0
    catagory = 'armour'
    for y in [500,430,360]:
        for x in [690]:
            itemRen.set_position(x,y)
            checkActive(catagory,itemNum)
            itemLoc[''.join([catagory,str(itemNum),'x'])] = x + 10 ; itemLoc[''.join([catagory,str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemNum = 0
    catagory = 'active'
    for y in [290]:
        for x in [650,800]:
            itemRen.set_position(x,y)
            checkActive(catagory,itemNum)
            itemLoc[''.join([catagory,str(itemNum),'x'])] = x + 10 ; itemLoc[''.join([catagory,str(itemNum),'y'])] = y + 10
            itemNum += 1
    itemRen.update(None,None,None,None,float(1.2),float(1.2))
    itemRen.image = pyglet.image.load(''.join(['c_',playerSkin,'d0.png']))
    itemRen.set_position(610,410)
    itemRen.draw()
    #draw Items
    for item in save_key:
        if item == 'world':
            drawItem = False
            playerData['x'] = gx
            continue
        elif item == 'x':
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
    if globalWorld == '2':
        if (gx, gy) == acessLoc['boat']:
            ptext('press E to go to another island',670,20,10)
            action.image = objectkey['bo']
            action.update(None,None,None,None,float(1.2),float(1.2))
            action.set_position(650,50)
    if globalWorld == '3':
        if (gx, gy) == acessLoc['3h0']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['boat']:
            ptext('press E to go to another island',670,20,10)
            action.image = objectkey['bo']
            action.update(None,None,None,None,float(1.2),float(1.2))
            action.set_position(650,50)
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
    if globalWorld == '4':
        if (gx, gy) == acessLoc['4h0']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['4h1']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['4h2']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['4h3']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['4h4']:
            ptext('press E to enter the house',670,20,10)
            action.image = door
            action.set_position(700,50)
        if (gx, gy) == acessLoc['boat']:
            ptext('press E to go to another island',670,20,10)
            action.image = objectkey['bo']
            action.update(None,None,None,None,float(1.2),float(1.2))
            action.set_position(650,50)
islandCount = 0
islandLoc = {}
islandLoc['2'] = (260,360)
islandLoc['3'] = (500,60)
islandLoc['4'] = (100,80)
def executeAction(actionType):
    global gx, gy, globalWorld, exitTox, exitToy, playerSkin, lastd, islandCount, islands, islandLoc, acessLoc
    tempx = gx
    tempy = gy
    if actionType == 'h':
        if globalWorld == houseA:
            globalWorld = '3'
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        if (tempx,tempy) == acessLoc['3h0']:
            if globalWorld == '3':
                print(globalWorld)
                globalWorld = houseA
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 120#enter house location
                animateStep(False,'u',playerSkin) ; lastd = 'u'

        if globalWorld == '4h0':
            globalWorld = '4'
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        if globalWorld == '4h1':
            globalWorld = '4'
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        if globalWorld == '4h2':
            globalWorld = '4'
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        if globalWorld == '4h3':
            globalWorld = '4'
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        if globalWorld == '4h4':
            globalWorld = '4'
            edgeCollisions()
            fireCount = 0
            gx = exitTox
            gy = exitToy
            animateStep(False,'d',playerSkin) ; lastd = 'd'
        
        if (tempx,tempy) == acessLoc['4h0']:
            if globalWorld == '4':
                print(globalWorld)
                globalWorld = '4h0'
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 200#enter house location
                animateStep(False,'u',playerSkin) ; lastd = 'u'
        if (tempx,tempy) == acessLoc['4h1']:
            if globalWorld == '4':
                print(globalWorld)
                globalWorld = '4h1'
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 200
                animateStep(False,'u',playerSkin) ; lastd = 'u'
        if (tempx,tempy) == acessLoc['4h2']:
            if globalWorld == '4':
                print(globalWorld)
                globalWorld = '4h2'
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 200
                animateStep(False,'u',playerSkin) ; lastd = 'u'
        if (tempx,tempy) == acessLoc['4h3']:
            if globalWorld == '4':
                print(globalWorld)
                globalWorld = '4h3'
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 200
                animateStep(False,'u',playerSkin) ; lastd = 'u'
        if (tempx,tempy) == acessLoc['4h4']:
            if globalWorld == '4':
                print(globalWorld)
                globalWorld = '4h4'
                edgeCollisions()
                exitTox = gx ; exitToy = gy
                gx = 300 ; gy = 200
                animateStep(False,'u',playerSkin) ; lastd = 'u'
        
    if actionType == 'b':
        if acessLoc['boat'] == (gx,gy):
            islandCount += 1
            if islandCount == 3:
                islandCount = 0
            globalWorld = islands[islandCount]
            print(islandLoc[islands[islandCount]])
            locStr = str(islandLoc[islands[islandCount]])
            a = locStr.split('(')
            b = a[1].split(')')
            c = b[0].split(',')
            gx = int(c[0])
            gy = int(c[1])
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
mode = 'play'
activeNum = 9
switchTemp = ''
def runPlayer(image):
    global gx, gy, mode, globalWorld, pressedLast, activeNum, switchTemp, skins, skinNum, playerSkin, exitTox, exitToy, gmessage
    reversex = 0 ; reversey = 0
    keypress = False ; drawChest = False
    if keyboard.is_pressed('q'):#mode switch
        activeNum = 0
        switchTemp = ''
        if mode == 'play':
            mode = 'inventory'
        elif mode == 'inventory':
            mode = 'play'
            clearActive()
        print(mode)
    if keyboard.is_pressed('r'):
        ptext(' INSTRUCTIONS:/npress W to move up\npress A to move left\npress S to move down\npress D to move right\npress E to enter buildings\n   or enter boats\npress Q to edit inventory',680,240,20)
    if mode == 'play':
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
            '''
        elif keyboard.is_pressed('q'):#change player
            pressedLast = False
            skinNum += 1
            if skinNum >= (len(skins)+ 1):
                skinNum = 0
            playerSkin = skins[skinNum]
            readPlayer()'''
        elif keyboard.is_pressed('enter'):#function 1
            print('function 1')
        elif keyboard.is_pressed('shift'):#function 2
            print('function 2')
        else:
            animateStep(False,lastd,image)
            keypress = False
    if mode == 'inventory':
        if keyboard.is_pressed('w'):
            clearActive()
            activeNum += 1
        if keyboard.is_pressed('s'):
            clearActive()
            activeNum -= 1
        if activeNum > 9:
            activeNum = 0
        if activeNum < 0:
            activeNum = 9
        active[inventoryKey[activeNum]] = True
        if switchTemp == '':
            ptext('press W and S to scroll\npress ENTER to select',680,240,20)
            if keyboard.is_pressed('enter'):#select
                switchTemp = activeNum
        elif not (switchTemp == ''):
            active[inventoryKey[int(switchTemp)]] = True
            if keyboard.is_pressed('enter'):#switch
                switch(str(inventoryKey[activeNum]),str(inventoryKey[int(switchTemp)]))
                switchTemp = ''
                clearActive()
    #ren Inventory (chest)
    if (gx,gy) in collisions:
        gx += reversex ; gy += reversey
        animateStep(False,lastd,image)
    playerData['world'] = globalWorld
    if keypress == True:
        print(gx,gy)
        Savefile = open(''.join(['s_save_',playerSkin,'.txt']),'w')
        writeList = []
        for info in save_key:
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
    drawInventory(playerSkin)
    runPlayer(playerSkin)
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
