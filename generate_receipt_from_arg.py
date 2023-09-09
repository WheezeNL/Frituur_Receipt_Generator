import sys, os
import json
from escpos.printer import Serial
from escpos.printer import Network
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
from datetime import datetime

# Variables
filename = "tmpbadge.png"
headerheight = 180
finalRun = False
totalHeight = 8000
maxWidth = 512

# Disable Print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore Print
def enablePrint():
    sys.stdout = sys.__stdout__

def prepare_receipt(message):
    runs = 0
    totalHeight = 8000
    data = json.loads(message)
    account = data["user"]
    items = data["items"]
    
    while runs<2:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        if(runs):
            img = Image.new('RGB', size=(512, totalHeight),color='white')
        else:
            img = Image.new('RGB', size=(512, totalHeight))
        draw = ImageDraw.Draw(img)

        orderfromfont = ImageFont.truetype("./tff/Arialn.ttf", 30)
        nickfont = ImageFont.truetype("./tff//ArialNarrowBold.ttf", 50)
        timefont = ImageFont.truetype("./tff//Arialn.ttf", 30)
        headerfont = ImageFont.truetype("./tff//ArialNarrowBold.ttf", 30)
        font = ImageFont.truetype("./tff//Arialn.ttf", 40)

        #if(len(account)>12):  account=account[0:12]

        # Header
        draw.text([0,0],'Bestelling voor:',fill= 'black',font=orderfromfont)
        draw.text([0,40],account,fill= 'black',font=nickfont)
        draw.text([0,headerheight-80],current_date + " "+ current_time,fill= 'black',font=timefont)
        draw.text([0,headerheight-40],'Snack',fill= 'black',font=headerfont)
        draw.text([280,headerheight-40],'In Pan  Uitgeleverd',fill= 'black',font=headerfont)
        draw.line((0, headerheight, maxWidth, headerheight),fill='black',width=3)

        pi4dec = Image.open('img_pi4dec.png')
        img.paste(pi4dec,[maxWidth - 140,20])

        # Items
        regels = 0
        for item in items:
            quantity = str(item["quantity"])
            name = item["description"].split("(Frituur) ",1)[1]
            if (quantity > '1'):
                completeItem = quantity + "x " + name
            else:
                completeItem = name
            if(len(completeItem)>16):
                completeItem = completeItem + "\n\t"
            draw.text([0,headerheight+(regels*45)],completeItem,fill= 'black',font=font)
            draw.rounded_rectangle([280,headerheight+(regels*45)+10,310,headerheight+(regels*45)+40],5,'white','black',3)
            draw.rounded_rectangle([370,headerheight+(regels*45)+10,400,headerheight+(regels*45)+40],5,'white','black',3)
            regels = regels+1
        draw = ImageDraw.Draw(img)
        test1,test2,test3,totalHeight = img.getbbox()
        totalHeight = totalHeight + 10
        runs = runs + 1
    img.save(filename, "PNG")

def print_frituur_receipt():
    blockPrint()
    """ 9600 Baud, 8N1, Flow Control Enabled """
    '''p = Serial(devfile='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1.00,
        dsrdtr=True
        )'''
    p = Network("192.168.192.168",profile='TM-T88V')
    enablePrint()
    p.image("tmpbadge.png")
    p.cut()

#    print("Receipt sent to printer")

if len(sys.argv)>1: #print accountname and firstname
    print("\nIk stuur de frituurbestelling naar de printer!\n")
    prepare_receipt(sys.argv[1])
    print_frituur_receipt()
else: #give a nice prompt
    print("So, I was hoping for some JSON, but got none")