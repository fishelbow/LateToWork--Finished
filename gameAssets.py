# Joe Wright
# final project
# gameAssets.py

from graphics import GraphWin, Image, Text, Point, Rectangle, Entry, GraphicsError, update # graphics objects used
import pygame # for handling sound in the game
from pathlib import Path # testing out the pathLib module 
import pickle # for the highscore data, Could use it for gameStates but ehhh. another time. I will say that pickle in this use is more prone to trouble than just writing to he file I have 3 times as many exemption handling
import gc  # to help gc when restarting the game
import time

# initilize functions 

def window(): # main GraphWin
    win = GraphWin("Late to Work",500,500) # persitant GraphWin
    win.setCoords(0,0,50,50)
    win.setBackground("white")
    return win

def menus(): # an easy way to access the game screens
    p1 = Point(25,25)
    timeUp = Image(p1,"menus/timesUp.png")        # 0
    finish = Image(p1,"menus/finishLine.png")     # 1
    crash = Image(p1,"menus/terminalCrash.png")   # 2
    getReady = Image(p1,"menus/getReady.png")     # 3
    redo = Image(p1,"menus/redo.png")             # 4
    main = Image(p1,"menus/main.png")             # 5 
    pScreen = Image(p1, "menus/pauseScreen.png")  # 6
    startScrn = Image(p1,"menus/start.png")       # 7
    optionScrn = Image(p1,"menus/options.png")    # 8
    introScrn = Image(p1, "menus/intro.png")      # 9
    creditScrn = Image(p1, "menus/credits.png")   # 10
    controlScrn = Image(p1, "menus/controls.png") # 11

    menuList = (timeUp,finish,crash,getReady,redo,main,pScreen,startScrn,optionScrn,introScrn,creditScrn,controlScrn)

    return menuList

def menuAssets(): # main menu / options elemnents 
    mLbl0 = Text(Point(25,24.5),"Play")
    mLbl1 = Text(Point(25,19.5),"Options")
    mLbl2 = Text(Point(25,14.5),"Controls")          # Main menu Option labels
    mLbl3 = Text(Point(25,9.5),"Credits")
    mLbl4 = Text(Point(25,5),"Exit")
    mRec0 = Rectangle(Point(17,22),Point(32.5,27))   # main menu selection rectangles
    mRec1 = Rectangle(Point(17,17),Point(32.5,22)) 
    mRec2 = Rectangle(Point(17,12),Point(32.5,17))
    mRec3 = Rectangle(Point(17,7),Point(32.5,12))     
    mRec4 = Rectangle(Point(17,2),Point(32,7.5))
    oLbl0  = Text(Point(17.5,20),"Difficulty:")
    oLbl0a = Text(Point(32,20),"Normal")             # option menu lables
    oLbl1  = Text(Point(20,25),"Music:")
    oLbl1a = Text(Point(32,25),"On")
    oLbl2  = Text(Point(25,15),"Main Menu")
    oRec0 = Rectangle(Point(8,22.5),Point(40,27.5))
    oRec1 = Rectangle(Point(8,17.5),Point(40,22.5))  # option menu selection rectangles
    oRec2 = Rectangle(Point(8,12.5),Point(40,17.5))

    mPick, oPick = 0, 0
 
    difficulty = "Normal" ;  diffSettings = Text(Point(2,20),difficulty) ; diffSettings.setSize(30)
                 #      0     1       2      3      4      5      6      7      8      9      10     11      12     13      14     15     16     17     18     19        29
    mainMenuAssets = (mLbl0, mLbl1, mLbl2, mLbl3, mLbl4, mRec0, mRec1, mRec2, mRec3, mRec4, oLbl0, oLbl0a, oLbl1, oLbl1a, oLbl2, oRec0, oRec1, oRec2, mPick, oPick, difficulty)

    for i in mainMenuAssets[:5]: i.setSize(30) # main menu 3 option rectangle selection

    for i in mainMenuAssets[10:15]: i.setSize(30) # oLbl0.setSize(30), oLbl0a.setSize(30), oLbl1.setSize(30), oLbl1a.setSize(30), oLbl2.setSize(30)

    return mainMenuAssets

def assets(win: object): # the source for the background images 
    currentDir = Path.cwd()
    bkg1Path, bkg2Path, bkg3Path, bkg4Path, toast = ( currentDir / "background" / "roadPad1.png",currentDir / "background" / "roadPad2.png",
            currentDir / "background" / "roadPad3.png", currentDir / "background" / "roadPad4.png", currentDir / "sprites" / "toasty.png" )
    img1 = Image(Point(25, 25), bkg1Path).draw(win)
    img2 = Image(Point(25, 75), bkg2Path).draw(win)
    img3 = Image(Point(25, 125), bkg3Path).draw(win)
    img4 = Image(Point(25, 175), bkg4Path).draw(win)
    toasty = Image(Point(56, 5), toast).draw(win)

    images = (img1, img2, img3, img4), toasty # storing them in a list to iterate through later
    return images

def hud(win: object):# Graphics for displaying gear and time remaining
    p1, p2, p3, p4 = Point(0, 43), Point(9, 49), Point(1, 44), Point(8, 48)

    gearBoxRec = Rectangle(p1, p2).draw(win)
    gearBoxRec.setFill("grey")

    innerGearBoxRec = Rectangle(p3, p4).draw(win)
    innerGearBoxRec.setFill("pink")

    gearDisplay = Text(Point(2.5, 47), "P").draw(win)

    gearLbl = Text(Point(5.75, 47), "Gear").draw(win)

    timeDisplay = Text(Point(4,45),"").draw(win)

    hudList = [gearBoxRec, innerGearBoxRec, gearDisplay, gearLbl, timeDisplay]
    scoreLbl = Text(Point(7,40),"0").draw(win)
    scoreLbl.setSize(30)                # score display during game
    scoreLbl.setTextColor("white")

    return hudList, scoreLbl

def createNorthCars(win):   # I need to do the same for southbound cars 
    car_origin = Point(1.5, 3.5)
    rec_op1 = Point(0,0)
    rec_op2 = Point(3,7)
    lane_x = (14.5, 20.5, 27.5, 32.5) # x-coordinates for both car images and rectangles

    carsData = (
        ("sprites/greenCar5.png", lane_x[2], 330),
        ("sprites/copCar1.png", lane_x[2], 310),("sprites/copCar1.png", lane_x[3], 350),
                                         
        ("sprites/redCar1.png", lane_x[2], 270),("sprites/redCar2.png", lane_x[3], 330),     
        ("sprites/purpleCar1.png", lane_x[2], 250),("sprites/redCar4.png", lane_x[3], 290),     
        ("sprites/redCar5.png", lane_x[2], 230),("sprites/blueCar1.png", lane_x[3], 250),
        ("sprites/blueCar2.png", lane_x[2], 210),("sprites/greenCar4.png", lane_x[3], 230),
        ("sprites/greyCar4.png", lane_x[2], 200),("sprites/greyCar5.png", lane_x[3], 170),
        ("sprites/purpleCar5.png", lane_x[2], 190),("sprites/purpleCar4.png", lane_x[3], 140),

        ("sprites/redCar3.png", lane_x[2], 170),("sprites/purpleCar2.png", lane_x[3], 130),
        ("sprites/purpleCar3.png", lane_x[2], 140),("sprites/greyCar3.png", lane_x[3], 120),
        ("sprites/blueCar4.png", lane_x[2], 110),("sprites/blueCar5.png", lane_x[3], 110),
        ("sprites/greenCar1.png", lane_x[2], 90),("sprites/greenCar2.png", lane_x[3], 70),
        ("sprites/blueCar3.png", lane_x[2], 40),("sprites/greyCar3.png", lane_x[3], 60), # need create these cars in front of mine   
        ("sprites/greyCar1.png", lane_x[2], 20),("sprites/greyCar2.png", lane_x[3], 20),                                        
    )
    northCarMaskPairsL = []
    for car_img, moveX, moveY in carsData:
        car = Image(car_origin, car_img)
        car.move(moveX, moveY)
        mask = Rectangle(rec_op1, rec_op2)
        mask.move(moveX, moveY)  # Use the same lane_x for rectangles
        northCarMaskPairsL.append((car, mask))
    northCarMaskPairs = () 
    northCarMaskPairs = northCarMaskPairsL # move the list to a tuple for use in the main game loop # this dosent really seem nessacry but my though is in a bigger application maybe would help in performance
    
    for car, mask in northCarMaskPairs:
        car.draw(win)
        
    return northCarMaskPairs

def createSouthCars(win):# Creates the cars in the southlane
    sLane_x = (14.5, 20.5)
    scar_origin = Point(1.5, 3.5)
    srec_op1 = Point(0,0)
    srec_op2 = Point(3,7)
    scars_data = (
        
        ("sprites/blueCar1S.png", sLane_x[1], 350),  # 
        ("sprites/purpleCar2S.png", sLane_x[0], 250),
        ("sprites/blueCar5S.png", sLane_x[0], 150),
        ("sprites/greenCar4S.png", sLane_x[1], 50),    # need call these cars in front of mine       
        ("sprites/greyCar1S.png",  sLane_x[0], 450),  
        ("sprites/redCar1S.png", sLane_x[1], 450)                                   
    )
    southCarMaskPairsL = []
    for car_img, move_x, move_y in scars_data:
        car = Image(scar_origin, car_img)
        car.move(move_x, move_y)
        mask = Rectangle(srec_op1, srec_op2)
        mask.move(move_x, move_y)  # Use the same lane_x for rectangles
        southCarMaskPairsL.append((car, mask))
    southCarMaskPairs = ()
    southCarMaskPairs = southCarMaskPairsL # moving the list into a tuple for performance gains in the main game loop
    for car, mask in southCarMaskPairs:
        car.draw(win)
    return southCarMaskPairs

def finishLine(win,fDist): # doing this just to create a another layer so cars go under this object but above the road lol oof when will i just switch to pygame and leave john zelles graphic module in the dust
    finishLine = Image(Point(25,25),"sprites/finishLine.png")
    halfMarker = Image(Point(25,25), "sprites/halfMarker.png")
    finishLine.move(0,fDist)
    halfMarker.move(0,fDist/2) # notices these show up on restart // trying to move them before drawing 
    halfMarker.draw(win)
    finishLine.draw(win)
    return finishLine, halfMarker

def pCar(win): # handles drawing and various specs of the player car
    pcarOrigin = Point(1, 3.5)
    precOp1 = Point(0,0)
    precOp2 = Point(4, 7) # larger than ai hit boxes
    playerCar = Image(pcarOrigin, "sprites/blueCar4.png")
    playerMaskrec = Rectangle(precOp1, precOp2)
    playerCar.move(27, 10)
    playerMaskrec.move(26, 10) # slightly out of sync to account for larger hitbox for player
    playerCar.draw(win)
    return playerCar, playerMaskrec

def intilizeRadio(): # to load the radio 
    musicPause = False
    tunner = 0
    pygame.mixer.init()
                                # Audacity to make the files from pixabay adding a radio tunning sound to the intros
    radioStation = ("music/Tradio2Tango.wav", "music/Tradio3Epic.wav","music/Tradio4Bread.wav","music/Tradio5Crunch.wav","music/Tradio6Orch.wav")

    return musicPause, tunner, radioStation

def soundEffects(): # intilizing sounds for sound effects 1 so far
    crash1 = pygame.mixer.Sound("soundEffects/crash1.mp3")
    crash1.set_volume(.2)
    eggAudio = pygame.mixer.Sound("soundEffects/graphics.wav") # voiced by Justin Jans
    eggAudio.set_volume(.6) # self explanitory sets volume

    return crash1, eggAudio

def intro(menuList, win): # intro splash screen
    menuList.draw(win)
    time.sleep(1)     # one time intro screen
    menuList.undraw()

def hsDisplay(win,score): # saving highscore to a .pkl file and displaying from this pickle file
    
    hSScreen = Image(Point(25,25), "menus/highscoreScreen.png") # move this to menus at some point
    hSScreen.draw(win)

    try:  # if highScore.pkl is missing we will just make topscore = [] and create a pickle file after the initials are gathered
        saveFile = "highScore.pkl"
        with open(saveFile, 'rb') as file: # yes it does close the file.   
                                # 3rd option is file is there and empty with no contents in which case we just make the list and create a file at the end with data
            topScore = pickle.load(file) # take out the pickle info f
    except EOFError: # for when the file dosen't exist or is corupted 
        topScore = [] # add dialog window's for these 3 execptions so I know for sure what is happening 
    except FileNotFoundError: # file is missing I make my own list and create the file at time of wrting
        topScore = []
    except MemoryError: # if some of the data is erased it will still function and make a new file overwriting the messed up file
        topScore = []

    if len(topScore) < 10 or score > topScore[-1][0]: # checking to see if I have an empty list with an or so I dont gt an error for going out of bounds. if there are items compare to the lowest for high score entry

        popUp = Image(Point(25,25), "menus/popUp.png")
        popUp.draw(win)
        entryBox = Entry(Point(25,25), 5)
        entryBox.draw(win)
        hslbl = Text(Point(25,29), "You made the highscore list")
        hslbl2 = Text(Point(25,20), " Please enter your Initals") 
        hslbl3 = Text(Point(25,22), f"your score: {score}")
        hslbl.draw(win)
        hslbl2.draw(win)
        hslbl3.draw(win)
        
        while True:
            try:
                k = win.getKey()
            except GraphicsError:
                exit()
            if k == "Return": # the logic for setting initias if empty default to AAA otherwise truncate down to 3 digits
                textBoxText = entryBox.getText()
                temp = textBoxText.strip().upper().replace(" ","") # in order remove leading and trailing whitespaces/ make upper case / remove blank spaces
                initials = temp[:3] # slice the first 3 letters
                if not initials: # if initials is empty set some initals 
                    initials = "JOE" # ha ha my score if you dont claim it!!!!
                break # after enter has gathered its input

        popUp.undraw()
        entryBox.undraw()
        hslbl.undraw()
        hslbl2.undraw()
        hslbl3.undraw()

    if len(topScore) < 10: # if there are fewer than 10 scores on the board your score is auto publish
        topScore.append((score, initials))                                                    
        topScore.sort(reverse=True, key=lambda x: x[0])  # Sort by score in descending order  lambda a throw away function x is the iterable itemms contnts x[0] says to sort in deceding order 
    elif score > topScore[-1][0]: # grabes the lowest value in the list,  # If there are 10 high scores, check if the new score should be addedt
        topScore.append((score, initials)) # if score is higher add score and initals to list
        topScore.sort(reverse=True, key=lambda x: x[0])  # lambda function to pick wich element to sort by 0 for score 1 for initals 
        topScore.pop()  # Remove the lowest score to maintain the list size

    with open(saveFile, "wb") as file: 
        pickle.dump(topScore, file)  # Write text to the file
    
    hsLbls = []
    lblanchor = Point(25,50)
                #  put these bad boys in a list and iterate through them
    for i in range(len(topScore)): # creates a list of 10 labels 
        hsLbls.append(Text(lblanchor,""))
        vertYspacer = -10 # inital placement of first highscore
    for i in range(len(hsLbls)):   # displays the current highscores 
        temp = hsLbls[i]
        temp.draw(win)
        temp.setSize(25)
        temp.move(0,vertYspacer) # needs a variable to increment drawing downwards
        vertYspacer -= 4 # incrementing for the next number
    for i in range(len(hsLbls)): #  first i is selecting the score , the second is going for the initials 
        hsLbls[i].setText((topScore[i][0],topScore[i][1]))
    return hsLbls, hSScreen

def credits(win, menu): # roll credits 
        # the raw strings of the credits 
    sList = ("Late to Work","Lead Graphic Artist", "Sonya Wright", "Voice Acting", "Justin Jans", "Programming", "Joe Wright",
             "Game Testers", "Sonya Clara Alex Emily Mike Carly", "Audio Files", "Pixabay.com")
    ssList = sList[::-1] # selecting the whole list with a blank start and stop and reversing the order for display using -1 in the step
    creditList = [] # a list to hold the text objects 
    x = -50 # spacer for placing the credits 
    for i in range(len(ssList)): # creating a list of text objects with the desired text 
        creditList.append(Text(Point(25,x),ssList[i]))
        x += 5 # the spaceing between credits
    for i in creditList[1::2]: # the titles sized up
        i.setSize(20)
    for i in creditList[2::2]: # the names sized up # skip first element take list to end skipping by 2 in order to make titles larger 
        i.setSize(15)
    creditList[10].setSize(30) # the first list entry breaks the pattern just gonna force it
    for i in creditList: # draw credits 
        i.draw(win)
    y = True
    while y:
        try:
            credKey = win.checkKey()
        except GraphicsError:
            exit()
        creditLoc = creditList[0].getAnchor().getY()
        menuLoc = menu.getAnchor().getY() # get the location of the credits screen
        if creditLoc >= 52:
            menu.move(0,-(menuLoc-25))  #  and move it back the amount it has moved 
            y = False
        if creditLoc >= -13:
            menu.move(0,.1)
        if credKey == "space":
            try:
                win.getKey() # to pause the credits
            except GraphicsError:
                exit()                    
        for i in creditList:
            i.move(0,.1)
        update(120)

    for i in creditList: # undraw credits
        i.undraw()
    menu.undraw()


def emptyTheWindow(fLine,halfMarker,southCarMaskPairs,northCarMaskPairs,hudList,playerCar,playerMaskrec,images,toasty,scoreLbl): # undraws all the graphic objects and performs gc
            
            scoreLbl.undraw() # removing the score display
           
            toasty.undraw() # goodnight Mr. Zelle

            fLine.undraw(), halfMarker.undraw()  # removing the finsh line and half way marker

            for car, mask in southCarMaskPairs: # undraw the cars in the south lane
                car.undraw()
                mask.undraw()

            for car, mask in northCarMaskPairs: # removing the cars in the north bound lane right 2 lanes
                car.undraw()
                mask.undraw()

            for obj in hudList: # removing everything draw with the Heads Up Display 
                obj.undraw()

            playerCar.undraw(), playerMaskrec.undraw() # remove pcar object

            for image in images: #  removes the scrolling background 
                image.undraw()
          
            # the proper menus is displayed, via the exiting of the game loop a value is assigned to menu select that corosponds to the screen that should be displayed
            gc.collect() # trying to make sure the I have a clean game state