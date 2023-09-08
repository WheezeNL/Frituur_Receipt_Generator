import sys, os
import json
from escpos.printer import Serial
from escpos.printer import Network
from PIL import Image, ImageOps, ImageDraw
from datetime import datetime

# Disable Print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore Print
def enablePrint():
    sys.stdout = sys.__stdout__

def print_frituur_receipt(message):
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
    p = Network("192.168.192.168")
    enablePrint()
    data = json.loads(message)
    account = data["user"]
    items = data["items"]

    now = datetime.now()

    p.set(align='left', font='a', bold=True, underline=0, width=1, height=1, density=9, invert=False, smooth=False, flip=False, double_width=False, double_height=True, custom_size=False)
    p.text("Bestelling voor: ")
    if len(account)>12 : p.text("\n")
    p.set(align='left', font='a', bold=True, underline=0, width=1, height=1, density=9, invert=False, smooth=False, flip=False, double_width=True, double_height=True, custom_size=False)
    p.text(account + "\n")

    p.set(align='left', font='a', bold=False, underline=0, width=1, height=1, density=9, invert=False, smooth=False, flip=False, double_width=False, double_height=False, custom_size=False)
    current_time = now.strftime("%H:%M:%S")
    p.text("Besteld om: "+ current_time +"\n\n")

    p.set(align='left', font='a', bold=True, underline=1, width=1, height=1, density=9, invert=False, smooth=False, flip=False, double_width=False, double_height=True, custom_size=False)
    p.text("Snack\t\tIn Pan\tUitgeleverd\n")

    p.set(align='left', font='a', bold=False, underline=0, width=1, height=2, density=9, invert=False, smooth=False, flip=False, double_width=False, double_height=True, custom_size=False)
    for item in items:
        quantity = str(item["quantity"])
        name = item["description"].split("(Frituur) ",1)[1]
        completeItem = quantity + "x: " + name
        if(len(completeItem)>16):
            completeItem = completeItem + "\n\t"
        p.text(completeItem + "\t[  ]\t[  ]\n")
    p.cut()

#    print("Receipt sent to printer")

if len(sys.argv)>1: #print accountname and firstname
    print("\nIk stuur de frituurbestelling naar de printer!\n")
    print_frituur_receipt(sys.argv[1])
else: #give a nice prompt
    print("So, I was hoping for some JSON, but got none")