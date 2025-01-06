import sys, os
import json
from escpos.printer import Serial
from escpos.printer import Network
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
from datetime import datetime

debug = True

# Variables
filename = "receipt.png"
headerheight = 180
finalRun = False
maxWidth = 512
printer = "network" #serial or network

# Disable Print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore Print
def enablePrint():
    sys.stdout = sys.__stdout__

def prepare_receipt(message):
    if debug:
        print(message)
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

        logo = Image.open('logo.png')
        img.paste(logo,[maxWidth - 140,20])

        # Items
        rows = 0
        for item in items:
            extrarow = False
            quantity = str(item["quantity"])
            itemname = item["description"].split("(Frituur) ",1)[1]
            if (quantity > '1'):
                itemname = quantity + "x " + itemname
            if(len(itemname)>20):
                print(itemname + " too long!")
                extrarow = True
            draw.text([0,headerheight+(rows*45)],itemname,fill='black',font=font)
            if extrarow:
                rows = rows+1
            draw.rounded_rectangle([280,headerheight+(rows*45)+10,310,headerheight+(rows*45)+40],5,'white','black',3)
            '''draw.rounded_rectangle([370,headerheight+(rows*45)+10,400,headerheight+(rows*45)+40],5,'white','black',3)
            if "frytime" in item:
                draw.text([maxWidth-10,headerheight+(rows*45)],str(item["frytime"])+"m",fill= 'black',anchor="ra",font=font)
            rows = rows+1'''
            draw.rounded_rectangle([maxWidth-40,headerheight+(rows*45)+10,maxWidth-10,headerheight+(rows*45)+40],5,'white','black',3)
            if "frytime" in item:
                draw.text([430,headerheight+(rows*45)],str(item["frytime"])+" min",fill= 'black',anchor="ra",font=font)
            rows = rows+1
        draw = ImageDraw.Draw(img)
        test1,test2,test3,totalHeight = img.getbbox()
        totalHeight = totalHeight + 10
        runs = runs + 1
    img.save(filename, "PNG")

def print_frituur_receipt():
    blockPrint()
    if printer == "serial":
        """ 9600 Baud, 8N1, Flow Control Enabled """
        p = Serial(devfile='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1.00,
        dsrdtr=True
        )
    elif printer == "network":
        p = Network("10.33.0.22",profile='TM-T88V')
    enablePrint()
    p.image(filename)
    p.cut()

if len(sys.argv)>1: #print accountname and firstname
    print("\nIk stuur de frituurbestelling naar de printer!\n")
    prepare_receipt(sys.argv[1])
    if debug:
        print("Debug enabled: Not printing!")
    else:
        print_frituur_receipt()
elif debug:
    print("\nDebug enabled, just testing, not printing\n")
    testdata = r'''{"user":"PA3L","items":[{"quantity":1,"description":"(Frituur) Frikandel","product_id":"frikandel","frytime":"4"},{"quantity":2,"description":"(Frituur) Bitterballen 6 stuks","product_id":"bitterballen","frytime":"5"},{"quantity":1,"description":"(Frituur) Patat","product_id":"patat"}]}'''
    prepare_receipt(str(testdata))  
else: #give a nice prompt
    print("So, I was hoping for some JSON, but got none")
