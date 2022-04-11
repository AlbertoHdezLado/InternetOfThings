#!/usr/bin/python
# -*- coding:utf-8 -*-

import SSD1331
import time
import config
from dataBase import create_itemlist, add_item, add_units, remove_units, next_item, previous_item, get_item, create_basket, reset_iterator, search_in_basket, add_to_basket, remove_from_basket, get_from_basket, previous_from_basket, next_from_basket, get_total_price_basket
import RFID
import traceback
import os
import RPi.GPIO as GPIO

from PIL import Image,ImageDraw,ImageFont

ENC_A = 27
ENC_B = 17
GPIO.setmode(GPIO.BCM)
#BUTTONS
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#ENCODER
GPIO.setup(ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
clkLastState = GPIO.input(ENC_A)

#SQL
print("Creating or checking item list...")
create_itemlist()
print("Creating or checking beasket...")
create_basket()

#VARIABLES
id = 0
name = ""
price = 0.0
amount = 0
image_path = ""
image = ""
total_price = 0.0
final_price = 0.0

def show_item_info():
    global id
    global name
    global price
    global amount
    global image
    global image_path

    #GETTING ITEM INFO
    get_item()
    id = get_item.id
    name = get_item.name
    price = get_item.price
    amount = get_item.amount
    image_path = get_item.image_path
    image = Image.open(image_path)

    #SHOWING ITEM INFO
    os.system('clear')
    print("Showing item...")
    print("ID: " + id)
    print("NAME: " + name)
    print("PRICE: " + price)
    print("AMOUNT: " + amount)
    disp.ShowImage(image,0,0)

def show_basket_info():
    global id
    global name
    global price
    global amount
    global image_path
    global image
    global total_price
    global final_price

    #GETTING ITEM INFO
    get_from_basket()
    id = get_from_basket.id
    name = get_from_basket.name
    price = get_from_basket.price
    amount = get_from_basket.amount
    image_path = get_from_basket.image_path
    image = Image.open(image_path)
    total_price = get_from_basket.total_price
    final_price = get_total_price_basket()


    #SHOWING ITEM INFO
    os.system('clear')
    print("Showing item...")
    print("ID: " + id)
    print("NAME: " + name)
    print("PRICE: " + price)
    print("AMOUNT: " + amount)
    print("TOTAL PRICE: " + total_price)
    print()
    print("TOTAL BASKET COST: " + final_price)
    
    disp.ShowImage(image,0,0)


try:
    disp = SSD1331.SSD1331()

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    show_item_info()

    while True:
        clkState = GPIO.input(ENC_A)
        if clkState != clkLastState and clkState == GPIO.LOW:
            dtState = GPIO.input(ENC_B)
            if dtState != clkState:
                previous_item() #SELECT PREVIOUS ITEM
                print("Previous item selected.")
            else:
                next_item() #SELECT NEXT ITEM
                print("Next item selected.")
            show_item_info()
        clkLastState = clkState
        if GPIO.input(5) == GPIO.LOW:   #BASKET MENU
            print("Button green pressed.")
            reset_iterator()
            show_basket_info()
            completed = False
            while not completed:
                clkState = GPIO.input(ENC_A)
                if clkState != clkLastState and clkState == GPIO.LOW:
                    dtState = GPIO.input(ENC_B)
                    if dtState != clkState:
                        previous_from_basket() #SELECT PREVIOUS ITEM
                        print("Previous item selected in basket.")
                    else:
                        next_from_basket() #SELECT NEXT ITEM
                        print("Next item selected in basket.")
                    show_basket_info()
                clkLastState = clkState
                if GPIO.input(5) == GPIO.LOW: #BASKET ITEM
                    print()
                    print("How many '" + name + "' units do you want to remove?")
                    n = input()
                    remove_from_basket(id, name, price, n, image_path)
                    show_basket_info()
                if GPIO.input(6) == GPIO.LOW: #RETURN TO SHOP
                    completed = True
            reset_iterator()
            show_item_info()
        if GPIO.input(6) == GPIO.LOW:
            print("Button red pressed.")
            os.system('clear')
            n = -1
            while (n != 3):
                print("How many units do you want to add to the basket?")
                n = input()
                add_to_basket(id, name, price, n, image_path)
                show_item_info()


            


    
except KeyboardInterrupt:
    print ('\r\ntraceback.format_exc():\n%s' % traceback.format_exc())
    config.module_exit()
    exit()

finally:
        GPIO.cleanup()