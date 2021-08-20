# -*- coding: utf-8 -*-
from DMD import DMD
from PinLayout import PinLayout
from datetime import datetime
import time
import random

layout = PinLayout(37, 38, 35, 32)
dmd = DMD(1, 1, 32, 16, layout)

#dmd.draw_box(32,0, 63, 15, 0)
#dmd.draw_box(0,0, 20, 20, 0)


while True:
    now = datetime.now()
    dmd.draw_filled_box(0,9,32,16, 1)
    dmd.draw_text(1,1,now.strftime('%d.%m.%y'), '3x5')
    dmd.draw_text(1,9,now.strftime('%H:%M:%S'), '3x5')
    
    dmd.scan()


