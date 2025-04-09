# Joe Wright
# final project
# LatetoWork.py


from graphics import GraphicsError, update # graphics objects used
import pygame # for handling sound in the game
import time # for various things that need timmed
import random # for car speeds and the easter egg
from gameAssets import * # a collections of functions that where orignally housed in this script, they handle objects and files paths and a couple other odds and ends
from collisonDetection import collisionDetector # 3 functions that use to be 2 and some code in the main game loop of this script 

# game loop functions below 

def scoreDisplay(difficulty,collisonCount,remainingTime, scoreLbl):
    if difficulty == "Normal":
        score = (remainingTime * 5_000) - (collisonCount * 50)
    else: # for hard difficulty
        score = (remainingTime * 15_000) - (collisonCount * 200)
    if score < 0: score = 0 # no score below zero
    scoreLbl.setText(score)
    return score 

def mainControl(musicPause, radioStation, tunner, win, mainMenuAssets, menuList, gameState, mainMenu, winOpen, mPick, oPick, difficulty): # menu button controls

    while mainMenu: # main menu key event

        musicPause, tunner, radioStation = radio(musicPause,radioStation,tunner) # keeping the radio acting throught all states and menus

        if mPick < 0: mPick = 4
        elif mPick >4: mPick = 0

        for i in mainMenuAssets[5:10]: i.undraw() # the selection rectangles

        if mPick == 0: mainMenuAssets[mPick+5].draw(win) # 
        elif mPick == 1: mainMenuAssets[mPick+5].draw(win) #     
        elif mPick == 2: mainMenuAssets[mPick+5].draw(win) #  # that improvement is chronchy browy
        elif mPick == 3: mainMenuAssets[mPick+5].draw(win) # 
        elif mPick == 4: mainMenuAssets[mPick+5].draw(win) #
        try:   
            mainWinKey = win.getKey()  # getKey over checkKey allowing for the draw and un draw loop progreses with key presses  
        except GraphicsError: # exeption to handle closing the window using the x while checkKey() is called in a loop with a closed window
            exit()
        if  mainWinKey == "m":  # pausing the music on menu screen
            if musicPause == False:
                pygame.mixer.music.pause() 
                musicPause = True
            elif musicPause == True: 
                pygame.mixer.music.unpause() 
                musicPause = False
        elif mainWinKey == "Up": 
            mPick -= 1
        elif mainWinKey == "Down": 
            mPick += 1
        elif mainWinKey == "r": # able to tune radio at all times
            pygame.mixer.music.stop() # stoppping the track will without changing musicPause will cause the radio to play the next track 
        elif mainWinKey == "Escape":  
            exit()
        elif mainWinKey == "space":
            menuList[5].undraw()  # undrdaw main menu screenu
            if mPick == 0: # start the game
                gameState = True
                mainMenu = False
            elif mPick == 1: # options menu
                menuList[8].draw(win)
                optionMenu = True
                for i in mainMenuAssets[10:18]: i.draw(win) # drawing the option labels and displaying the difficutly based off the setting
                
                if pygame.mixer.music.get_busy(): mainMenuAssets[13].setText("On")
                else: mainMenuAssets[13].setText("Off")

                while optionMenu:
                    musicPause, tunner, radioStation = radio(musicPause,radioStation,tunner) # keeping the radio acting throught all states and menus

                    for i in mainMenuAssets[15:18]: i.undraw() #  undraw the option menu selection rectangles

                    if oPick < 0: oPick = 2
                    elif oPick >2:oPick = 0

                    if oPick == 0: mainMenuAssets[oPick+15].draw(win) #
                    elif oPick == 1: mainMenuAssets[oPick+15].draw(win) 
                    elif oPick == 2: mainMenuAssets[oPick+15].draw(win) 
                    try:
                        optKey = win.getKey()
                    except GraphicsError:
                        exit()
                    if optKey == "Up": 
                        oPick -= 1
                    elif optKey == "Down": 
                        oPick += 1
                    elif optKey == "r": # able to tune radio at all times
                        pygame.mixer.music.stop() # stoping the track without changing musicPause will cause the radio to play the next track      
                    elif optKey == "space":
                        if oPick == 0: # options menu - music toggle
                            if musicPause == False: 
                                pygame.mixer.music.pause() 
                                musicPause = True 
                                mainMenuAssets[13].setText("Off")
                            elif musicPause == True: 
                                pygame.mixer.music.unpause()  
                                musicPause = False  
                                mainMenuAssets[13].setText("On")       
                        elif oPick == 1: # options menu - difficulty toggle
                            if difficulty == "Normal": 
                                mainMenuAssets[11].setText("Hard") 
                                difficulty = "Hard"
                            elif difficulty == "Hard": 
                                mainMenuAssets[11].setText("Normal") 
                                difficulty = "Normal" 
                        elif oPick == 2:  # options menu - exit
                            optionMenu = False 
                            mainMenu = True
                menuList[8].undraw()

                for i in mainMenuAssets[10:18]: i.undraw() # undraw options menu elements      
            elif mPick == 2: # controls menu
                menuList[11].draw(win)
                contr = True
                while contr:
                    try:
                        controlWinKey = win.getKey()
                    except GraphicsError:
                        exit()
                    if controlWinKey == "space":   # working here to pause on controls and exit with cross button or space
                        menuList[11].undraw()
                        contr = False
            elif mPick == 3: # credits scroll
                menuList[10]
                menuList[5].undraw()
                for i in mainMenuAssets[:5]: i.undraw() #
                mainMenuAssets[8].undraw() # mRec3.undraw()              
                menuList[10].draw(win)   
                credits(win, menuList[10])
                menuList[10].undraw()
            elif mPick == 4: # exit option
                exit()
            mainMenu = False # exit into the game
            menuList[5].undraw()

            for i in mainMenuAssets[:5]: i.undraw() # delete currently drawn lables 
            mainMenuAssets[mPick+5].undraw() # delete the rectangle that is currently drawn
            
    return musicPause, radioStation, tunner, gameState, mainMenu, winOpen, difficulty

def gameControl(win,playerCar,playerMaskrec,gameState,gear,menuSelect,pScreen,pStart,timePaused,musicPause,tunner): # handle all the Key inputs
    try: # exeption to handle clsoing the window using the x while checkKey() is called in a loop with a closed window
        key = win.checkKey()
    except GraphicsError:
        exit()
    if key == "m":
        if musicPause == False:
            pygame.mixer.music.pause()
            musicPause = True
            
        elif musicPause == True:
            pygame.mixer.music.unpause()
            musicPause = False
    elif key == "Up":
        gear -= 0.05
    elif key == "Down" and gear < 0: # may need to test if this is redudent < 0
        if gear <0:
            gear += 0.05
    elif key == "Left":
        if gear >= 0:
            playerCar.move(0, 0)
            playerMaskrec.move(0, 0)
        else:
            playerCar.move(-3.5, 0)
            playerMaskrec.move(-3.5, 0)
    elif key == "Right":
        if gear >= 0:
            playerCar.move(0, 0)
            playerMaskrec.move(0, 0)
        else:
            playerCar.move(3.5, 0)
            playerMaskrec.move(3.5, 0)
    elif key == "u":
        menuSelect = 4 # redo screen
        gameState = False                       
    elif key == "r":
        pygame.mixer.music.stop() # stoppping the track will without changing musicPause will cause the radio to play the next track
    elif key == "space":   # you have to use pause and esc to get back to main menu
        pStart = time.time()# stop time
        pScreen.draw(win)
        pygame.mixer.music.pause()
        time.sleep(.5)
        musicOn = False  # this will make it so that if you have music off and pause the music will stay off and the opposite is true. if music is on it goes off during pause and back on when pause is off
        if musicPause == True:
            musicOn = True
        else:
            musicPause = True
        while True:    # main menu key events
                try:
                    v = win.checkKey()
                except GraphicsError:
                    exit()  
                if v == "Escape":
                    gameState = False 
                    menuSelect = 5
                    pScreen.undraw()
                    if musicOn == True:
                        musicPause = True
                        pygame.mixer.music.pause()
                    else:
                        musicPause = False
                        pygame.mixer.music.unpause()
                    break
                elif v == "space":
                    pScreen.undraw()
                    timePaused += time.time()-pStart
                    if musicOn == True:
                        musicPause = True
                        pygame.mixer.music.pause()
                    else:
                        musicPause = False
                        pygame.mixer.music.unpause()
                    break

    return gear, gameState, menuSelect, timePaused, musicPause, tunner
  
def engine(difficulty): # handles all the values for determining speed and finishLine distance using difficulty
                #.15, .16, .17, .18, .19, .2, .21,   ____ ,.29,.30,.31,.32,.33,.34,.35,.36,.37,.38,.39,.4
    if difficulty == "Normal": #.22,.23,.24,
        aigears = (.25,.26,.27,.28)
        fDist = 1_750
    else: # Hard
        aigears = (.29,.30,.31,.32,.33)
        fDist = 2_000
    gear =  -.15
    return aigears, gear, fDist

def govner(gear,gearDisplay): # set the top and bottom limit of gear, and display current gear
            if gear <= -0.35:
                gear = -0.35
            if gear > 0:  
                gear = 0
            if round(gear, 2) == 0:
                gearDisplay.setText("P")
            elif round(gear, 2) > -.1:
                gearDisplay.setText("1st")
            elif round(gear, 2) == -0.1:               # gear display and speed control
                gearDisplay.setText("2nd")
            elif round(gear, 2) == -0.15:
                gearDisplay.setText("3rd")
            elif round(gear, 2) == -0.2:
                gearDisplay.setText("4th")
            elif round(gear, 2) == -0.25:
                gearDisplay.setText("5th")
            elif round(gear, 2) == -.30:                   
                gearDisplay.setText("6th")
            elif round(gear, 2) == -.35:
                gearDisplay.setText("7th")     
            elif round(gear, 2) == -.40:          # experimenting with diffrent speeds
                gearDisplay.setText("8th")
            
            return gear, gearDisplay

def carAlign(playerCar,playerMaskrec): # checks car position and moves car back on the road 
    carPos = playerCar.getAnchor() # this is just to check the car's position for alignment with in the road
    temp1 = carPos.getX()
           # print(carPos)    # a great trace for finding the lanes
    if temp1 <=14.5: # left most
        playerCar.move(3.5,0)
        playerMaskrec.move(3.5,0)    # this bit makes sure to always move the car back on road
                                             # this just keeps the game solid
    elif temp1 >=38:  # right most                                                                                        
        playerCar.move(-3.5,0)
        playerMaskrec.move(-3.5,0)
    return playerCar, playerMaskrec 

def scroller(win: object, gear: int, images: Image):# scrolls the images in assets 
    for img in images:
        img.move(0, gear) # pulling the images out of the list and moving them along the y axies by the gear speed  # side note the image files are larger than the window and drawn in a way to create over lap this way any lag will be hidden
        if img.getAnchor().getY() <= -25: # when the reach past the bottom I reset them to the top                  # no more random lines as images mis-match 
            img.move(0, 200)

def northAi(aigears, gear, northCarMaskPairs): # just like south ai but going north in the right lane
    for car, mask in northCarMaskPairs:
        aispd = random.choice(aigears)
        car.move(0, aispd + gear)
        mask.move(0, aispd + gear)

def southAi(aigears, gear, southCarMaskPairs): # determines a speed for the south cars randomly from the gears listed in the engine function
    for car, mask in southCarMaskPairs:
        aispd = random.choice(aigears)
        car.move(0, -(aispd - gear))  # Move southbound
        mask.move(0, -(aispd - gear))

def southTrafficReset(southspd,southCarMaskPairs): # scrolls the south traffic as they are not persitant like the north bound lane cars
        for car, mask in southCarMaskPairs:
            if mask.getP2().getY() <= -200:
                mask.move(0, 560)
            if car.getAnchor().getY() <= -200:
                car.move(0, 560)
            mask.move(0, -abs(southspd))
            car.move(0, -abs(southspd))

def radio(musicPause,radioStation,tunner): # playing the radio
        if not(pygame.mixer.music.get_busy() or musicPause): # if music is not busy or paused play the next track
            tunner +=1  # change to next station
            if tunner >4: # keeeping the index in bounds
                tunner = 0
            pygame.mixer.music.load(radioStation[tunner])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
        return musicPause, tunner, radioStation

def zelleEgg(toastyDraw, toasty, eggAudio, move, moveRight, zellePause): # for the easter egg event
        randomNum = 0
        luckyNum = 5 # the number for the easter egg to trigger
        if time.time() > zellePause: # using a cool down for going again
            if toastyDraw:
                randomNum = random.randrange(1, 500)  # running numbers looking for luckyNum
            if randomNum == luckyNum and toastyDraw == True:
                    toastyDraw = False   
                    zellePause = time.time() + 30 # adding a cool down between zelle visits
        if not toastyDraw and not moveRight: # this handles the animation of the john zelle image
                toasty.move(-.08,0) #   <------##
        elif moveRight and move: 
                toasty.move(.08,0) #    ##------>
        zelleLocation = toasty.getAnchor().getX()
        if zelleLocation < 46:
                eggAudio.play() # zelle sound effect
                moveRight = True 
        elif zelleLocation > 56: # 
                move = True
                moveRight = False
                toastyDraw = True           

        return move, moveRight, toasty, toastyDraw, zellePause

if __name__ == "__main__": 

    win = window() # GraphWin

    mainMenuAssets = menuAssets()  # menu Selection assets i.e. labels background images 

    musicPause, tunner, radioStation = intilizeRadio() # start the radio  ####   musicPause, tunner, radioStation

    menuList = menus() # making the game screens avaliable

    intro(menuList[9], win) # intro splash screen

    mPick, oPick, difficulty = mainMenuAssets[18], mainMenuAssets[19], mainMenuAssets[20] # new way to do things just learned new

    winOpen = True

    while winOpen: # main GraphWin Containing all the game logic 

        # go back to main menu screen
        menuList[5].draw(win) 
        for i in mainMenuAssets[:5]: i.draw(win) 

        menuSelect = 5 # lining up the menuselect with the main menu
        mainMenu = True # show the main menu
        gameState = False # menuscreen and key loop exiting gameState = False only selecting play on main menu will make gameState = True
        gameRan = False # to keep track of drawn objects 
 
        # make a list or tuple
        musicPause, radioStation, tunner, gameState, mainMenu, winOpen, difficulty = mainControl(musicPause, radioStation, tunner, win, mainMenuAssets, menuList, gameState, mainMenu, winOpen, mPick, oPick, difficulty)

        if gameState: # create objects and variables
           # pygame.mixer.init() # Start the mixer for sound's 
            frame = 120  # controls the update(frame) in the game loop                                
            seconds = 55  # 55 seconds before a game over screen
            aigears, gear, fDist = engine(difficulty) # controls the gears for the other cars and gear for player car and scrolling the background # distance of finishLine was 1_600 now 2_000 to account for the new gears
            southspd = .25  # Movement speed
            collisonCount = 0 # number of collisons with the cars in the north bound lane not sure I want to count them in the south lane as you cant score after a south lane crash
            remainingTime = 0 # 
            timePaused = 0 # keep elasped paused time tracked for timer
            pStart = 0 # the timestamp point for the start of a pause duration
            toastyDraw = True # allows the egg event to occur 
            moveRight = False # connected to easter egg
            move = True # another part of animating the easteer egg
            gameRan = True # for undrawing elements and gc. options/controls/credits loop back into main menu without drawing game assets that emptywindow would call
            crash1, eggAudio = soundEffects() # loads the sound effect
            images, toasty = assets(win) # background images for scrolling and john zelle easter egg image
            hudList, scoreLbl = hud(win) # gearBoxRec, innerGearBoxRec, gearDisplay, gearLbl, timeDisplay hudList ##
            playerCar, playerMaskrec = pCar(win) # loading and drawing the player are with the rectangle for collison detection 
            northCarMaskPairs = createNorthCars(win) # loading in and postioing the north bound cars 
            southCarMaskPairs = createSouthCars(win) # creat the south lane cars 
            fLine, halfMarker = finishLine(win,fDist) # layering the finish line should be place so that the player goes under
            startTime = time.time() # start time
            zellePause = 0 # initilized variables need to go back out side this function

            while gameState: # the actual game loop 
                score = scoreDisplay(difficulty,collisonCount,remainingTime,scoreLbl)  # displaying the score during the game and preparing a score for the highscore page at the end.
                musicPause, tunner, radioStation = radio(musicPause,radioStation,tunner) # keeping the radio acting throught all states and menus

                move, moveRight, toasty, toastyDraw, zellePause = zelleEgg(toastyDraw, toasty, eggAudio, move, moveRight,zellePause)

                elaspedTime = time.time() - (startTime + timePaused)
                remainingTime = int(round(seconds - elaspedTime,0)) 
                hudList[4].setText(remainingTime) # time Display update

                gear, gameState, menuSelect, timePaused,musicPause,tunner = gameControl(win,playerCar,playerMaskrec,gameState,gear,menuSelect,menuList[6],pStart,timePaused,musicPause,tunner) # key events 
                gear, hudList[2] = govner(gear,hudList[2]) # sets gear display and limits gear # check the hudList index 2 is the gearDisplay
                scroller(win, gear, images) # scrolling the back ground images 
                playerCar, playerMaskrec = carAlign(playerCar,playerMaskrec) # keeping the players car on the road
                northAi(aigears, gear, northCarMaskPairs) # moving the cars in the north lanes at random speeds with-in a predetermined set of speeds 
                southAi(aigears,gear, southCarMaskPairs) # moving the south cars 
                southTrafficReset(southspd,southCarMaskPairs) # south traffic pattern loops back around in same order 

                fLine.move(0,gear),halfMarker.move(0,gear) # moves the finish line & halfway marker towards the player car which is stationary

                menuSelect, gameState, collisonCount, gear = collisionDetector(northCarMaskPairs, playerMaskrec, playerCar, crash1, southCarMaskPairs, collisonCount, gear, menuSelect, gameState,)
                                             # this along with its functions have been moved to a seperate script
        
                if remainingTime == 0:  # game exit condition Times Up!!!!
                    menuSelect = 0
                    gameState = False

                fLineY, playerY = fLine.getAnchor().getY(), playerCar.getAnchor().getY() #  checking if the car passed the finishline. In reality the finish line came to the car
                if fLineY < playerY: # player has passed the finish line
                    menuSelect = 1 # here I pass a value to display the corosponding menu.
                    gameState = False    # game exit Condition Finish Line

                update(frame) # just regulating the frame rate 

        if menuSelect == 1:  # display Highscore screen after Finish line screen       # game over display proper screen and empty the window
            menuList[menuSelect].draw(win)
            time.sleep(1)
            menuList[menuSelect].undraw()           
            hsLbls, hSScreen = hsDisplay(win,score) # 
            try:
                win.getKey()
            except GraphicsError:
                exit()
            for i in hsLbls: # remove the highscores that were displayed 
                i.undraw()
            hSScreen.undraw()  # removing highscore background
        else:
            if not menuSelect == 5: # checking for mainmenu or exiting a game for proper screen display
                menuList[menuSelect].draw(win) # for crash, redo , time up main menu
                time.sleep(1)
                menuList[menuSelect].undraw()
 
        if gameRan == True: # if the game was ran delete the elements that where drawn
            emptyTheWindow(fLine,halfMarker,southCarMaskPairs,northCarMaskPairs,hudList,playerCar,playerMaskrec,images,toasty,scoreLbl) 
