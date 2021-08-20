# -*- coding: utf-8 -*-
from DMD import DMD
from PinLayout import PinLayout
from datetime import datetime
import time
import random

layout = PinLayout(37, 38, 23, 35, 32)
dmd = DMD(2, 3, 1, 32, 16, layout)

#dmd.draw_box(32,0, 63, 15, 0)
#dmd.draw_box(0,0, 20, 20, 0)

routes = [{'route': random.randint(10, 99),'minute': random.randint(1,99)} for i in range(4)]

while True:
    #start_time = time.time()
    #dmd.clear_screen(1)
    
    now = datetime.now()
    dmd.draw_filled_box(32,9,63,16, 1)
    dmd.draw_text(33,1,now.strftime('%d.%m.%y'), '3x5')
    dmd.draw_text(33,9,now.strftime('%H:%M:%S'), '3x5')
    
    
    for i in range(4):
        dmd.draw_text(0,16 + i * 8,routes[i]['route'], '5x7')
        dmd.draw_text(63-10,16 + i * 8,routes[i]['minute'], '5x7')
      
    dmd.scan()
    #print("--- %s seconds ---" % (time.time() - start_time))

