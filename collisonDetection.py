# Joe Wright
# final project
# collisonDetection.py



# Collison detection moved to seperate script

# https://www.geeksforgeeks.org/find-two-rectangles-overlap/ provided assitance in understanding along with co-pilot

def detectCollision(car1Mask, car2Mask):# AABB Collison Detection using car mask aka rectangle

    x1, y1 = car1Mask.getP1().getX(), car1Mask.getP1().getY() # first car
    x2, y2 = car1Mask.getP2().getX(), car1Mask.getP2().getY()

    ox1, oy1 = car2Mask.getP1().getX(), car2Mask.getP1().getY() # other car
    ox2, oy2 = car2Mask.getP2().getX(), car2Mask.getP2().getY()
    
    if x1 < ox2 and x2 > ox1 and y1 < oy2 and y2 > oy1: # checking for overlap from first car and second car
        overlapLeft = ox2 - x1
        overlapRight = x2 - ox1 # finding out how much the rectangle overlaps in with respect to direction
        overlapTop = y2 - oy1
        overlapBottom = oy2 - y1
        minOverlap = min(overlapLeft, overlapRight, overlapTop, overlapBottom) # to deteremine where the collison occured, which ever of the four is the min is the side the rectangle is colliding from
        if minOverlap == overlapLeft:
            return "left"
        elif minOverlap == overlapRight:
            return "right"
        elif minOverlap == overlapTop:
            return "top"
        elif minOverlap == overlapBottom:
            return "bottom"
    return None # since this is always being checked return none when no collison is occuring 

def handleCollision(minOverlap, car1, car1Mask, car2, car2Mask, gear): # responding to the detected collison 
    if minOverlap == "left":
      #  print("another car is in that lane!")
        car1.move(3.5, 0) #
        car1Mask.move(3.5, 0) #
    elif minOverlap == "right":
       # print("another car is in that lane!")
        car1.move(-3.5, 0)
        car1Mask.move(-3.5, 0)
    elif minOverlap == "top":
        gear += 0.1 
        car2.move(0, 2)
        car2Mask.move(0, 2)
    elif minOverlap == "bottom":
        gear -= 0.1  
        car2.move(0, -2)
        car2Mask.move(0, -2)
    return gear

def collisionDetector(northCarMaskPairs, playerMaskrec, playerCar, crash1, southCarMaskPairs,collisonCount, gear, menuSelect, gameState):

    for enemyCar, enemyMask in northCarMaskPairs:  # checking collison against player car and north bound traffic
        minOverlap = detectCollision(playerMaskrec, enemyMask)
        if minOverlap == "top" or minOverlap == "bottom": # keeping track of the number of collisions the player makes
            collisonCount += 1 # spot to count collisons with north bound traffic  
        if minOverlap: # this is why we retur none if there is no collison 
            gear = handleCollision(minOverlap, playerCar, playerMaskrec, enemyCar, enemyMask, gear)
            crash1.play()
    
        for otherCar, otherMask in northCarMaskPairs: # checks and handles collison for north bound traffic against other north bound traffic
                if enemyCar != otherCar:
                    aiMinOverlap = detectCollision(enemyMask, otherMask)
                    if aiMinOverlap:
                        handleCollision(aiMinOverlap, enemyCar, enemyMask, otherCar, otherMask, gear)
                        crash1.play()
                    
    for car, mask in southCarMaskPairs: # Collision Detection for player car against southbound traffic
        minOverlapSouth = detectCollision(playerMaskrec, mask)
        if minOverlapSouth == "top": 
            gear = handleCollision(minOverlapSouth, playerCar, playerMaskrec, car, mask, gear)
            crash1.play() # car crash head on might find better audio
            menuSelect = 2 # crash screen
            gameState = False  # game exit condition Terminal Crash!!! death    
             
    return menuSelect, gameState, collisonCount, gear