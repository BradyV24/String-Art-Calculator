from math import sin,cos
from random import randint
from PIL import Image

image = Image.open("input.png") # Input image
image = image.convert('L') # convert image to black and white
img = image.load()
blank = Image.new('L', image.size, (255))
canv = blank.load()

PI = 3.14159265
PINS = 212 #Number of pins
WEIGHT = 24 #Amount that the colour changes on each pass of 'string'

length = 0
DIAM = 17/12 #Real life diameter of art piece
radius = min(image.size[0],image.size[1])//2-2
scale = DIAM/(2*radius)

def line(pin1,pin2,pix):
    global length
    dist = round(((pin2[0]-pin1[0])*(pin2[0]-pin1[0]) + (pin2[1]-pin1[1])*(pin2[1]-pin1[1]))**0.5)
    dx = (pin2[0]-pin1[0])/dist
    dy = (pin2[1]-pin1[1])/dist

    length += dist*scale

    last = (-1,-1)
    for i in range(dist):
        pos = (int(pin1[0]+dx*i),int(pin1[1]+dy*i))
        if pos != last: pix[pos[0],pos[1]] -= WEIGHT 
        last = pos
    
def eval(pin, pins, canv, img):
    maxScore = 0
    best = None
    for to in pins:
        if to == pin: continue
        dist = round(((to[0]-pin[0])*(to[0]-pin[0]) + (to[1]-pin[1])*(to[1]-pin[1]))**0.5)
        dx = (to[0]-pin[0])/dist
        dy = (to[1]-pin[1])/dist

        score = 0
        last = (-1,-1)
        for i in range(dist):
            pos = (int(pin[0]+dx*i),int(pin[1]+dy*i))
            if pos == last: continue
            #if img[pos[0],pos[1]] != 0: 
            score += (2*canv[pos[0],pos[1]]-2*img[pos[0],pos[1]]-WEIGHT)*WEIGHT
            last = pos
            
        if score > maxScore:
            maxScore = score
            best = to
    return best
    

pins = []

for i in range(PINS):
    pins.append((int(radius*cos(2*PI/PINS*i))+image.size[0]/2,int(radius*sin(2*PI/PINS*i))+image.size[1]/2))

ring = Image.new('L', image.size, (255))
ringpix = ring.load()

for pin in pins:

    for i in range (-1,2):
        for j in range (-1,2):
            canv[pin[0]+i,pin[1]+j] = 0

ring.save("template.png")

with open("instructions.txt", "w") as f:
    tally = 0
    on = pins[0]
    while(True):
        f.write(str(tally)+": " + str(pins.index(on)) + "\n")
        next = eval(on,pins,canv,img)
        if next == None: break
        line(on,next,canv)
        on = next
        tally+=1

        if tally % 100 == 0: 
            print("steps:", tally)
            print("length:", length)
        
    f.close()

print("Final length:", length)
blank.save("canv.png")
    


