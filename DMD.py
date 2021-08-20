from DMDBase import DMDBase
from System5x7 import S5x7, S3x5
from time import sleep
import spidev

class DMD(DMDBase):
    pixelLookupTable = [
           0x80,   # 0, bit 7
           0x40,   # 1, bit 6
           0x20,   # 2. bit 5
           0x10,   # 3, bit 4
           0x08,   # 4, bit 3
           0x04,   # 5, bit 2
           0x02,   # 6, bit 1
           0x01    # 7, bit 0
    ]

    def __init__(self, displayswide, displayshigh, displaybbp, pixelswidth, pixelsheight, layout):
        DMDBase.__init__(self, layout)
        self.displayPixelsWidth = pixelswidth
        self.displayPixelsHeight = pixelsheight
        
        self.displaysTotal = displayshigh * displayswide
        self.screenWidth = pixelswidth * displayswide
        self.screenHeight = pixelsheight * displayshigh
        
        self.screen = [0xFF for x in range(self.displaysTotal * 64)]
        self.phase = 0
        
        self.row_size = self.displaysTotal << 2
        self.row3 = ((self.displaysTotal << 2) * 3) << 2
        self.row2 = self.displaysTotal << 5
        self.row1 = self.displaysTotal << 4
        
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        
        self.spi.max_speed_hz = 4000000
        self.spi.mode = 0b00
        self.spi.bits_per_word = 8
        
    def pixel_to_bitmap_index(self, x, y):
        panel = int(x / self.displayPixelsWidth) + (int((self.screenWidth / self.displayPixelsWidth) * int(y / self.displayPixelsHeight)))
        x = (x % self.displayPixelsWidth) + (self.displayPixelsWidth * panel)
        y = y % self.displayPixelsHeight
        res = x / 8 + y * (self.displaysTotal << 2)
        return int(res)


    def set_pixel(self, x, y, mode): 
        if x >= self.screenWidth or y >= self.screenHeight:
            return
        
        byte_index = self.pixel_to_bitmap_index(x, y)
        bit = self.pixelLookupTable[x & 0x07]
        
        if mode == 0:  #ON
            self.screen[byte_index] &= ~bit
        elif mode == 1: #OFF
            self.screen[byte_index] |= bit
        elif mode == 2: # OR
            self.screen[byte_index] = ~(~self.screen[byte_index] | bit)
        elif mode == 3: # XOR
            self.screen[byte_index] = (~self.screen[byte_index] | bit)
        elif mode == 4: # NOR
            self.screen[byte_index] ^= bit
        
    def scan(self):
        offset = self.row_size * self.phase
    
        for x in range(self.row_size):
            self.spi.writebytes2([self.screen[offset + x + self.row3],
                                  self.screen[offset + x + self.row2],
                                  self.screen[offset + x + self.row1],
                                  self.screen[offset + x]])
            
        
        super(DMD, self).gpio_out(self.layout.OE, 0)    
        super(DMD, self).latch()
        super(DMD, self).gpio_out(self.layout.A, self.phase & 0x01)
        super(DMD, self).gpio_out(self.layout.B, self.phase & 0x02)
        self.phase = (self.phase + 1) % 4
        super(DMD, self).gpio_out(self.layout.OE, 1)
        #super(DMD, self).gpio_pwm_out(20)

    def clear_screen(self, bNormal):
        if (bNormal):
            self.screen = [0xFF for x in range(self.displaysTotal * 64)]
        else:
            self.screen = [0x00 for x in range(self.displaysTotal * 64)]


    def draw_line(self, x1, y1, x2, y2, mode):
        dy = y2 - y1
        dx = x2 - x1
        stepy = 1
        stepx = 1
        if dy < 0:
            dy = -dy
            stepy = -1
        if dx < 0:
            dx = -dx
            stepx = -1
        dy *= 2
        dx *= 2
        self.set_pixel(x1, y1, mode)
        if dx > dy:
            fraction = dy - dx / 2
            while x1 is not x2:
                if fraction >= 0:
                    y1 += stepy
                    fraction -= dx
                x1 += stepx
                fraction += dy
                self.set_pixel(x1, y1, mode)
        else:
            fraction = dx - dy / 2
            while y1 is not y2:
                if fraction >= 0:
                    x1 += stepx
                    fraction -= dy
                y1 += stepy
                fraction += dx
                self.set_pixel(x1, y1, mode)
                
    def draw_clircle(self, xc, yc, r, mode):
        x = -r
        y = 0
        error = 2 - 2 * r
        while (x < 0):
            self.set_pixel(xc - x, yc + y, mode)
            self.set_pixel(xc - y, yc - x, mode)
            self.set_pixel(xc + x, yc - y, mode)
            self.set_pixel(xc + y, yc + x, mode)
            r = error
            if r <= y:
                y += 1
                error += y * 2 + 1
            if (r > x or error > y):
                x += 1
                error += x * 2 + 1

    def draw_box(self, x1, y1, x2, y2, mode):
        self.draw_line(x1,y1,x2,y1, mode)
        self.draw_line(x2,y1,x2,y2, mode)
        self.draw_line(x2,y2,x1,y2, mode)
        self.draw_line(x1,y2,x1,y1, mode)

    def draw_filled_box(self, x1,y1,x2,y2, mode):
        for i in range(x1,x2+1):
            self.draw_line(i, y1, i, y2, mode)

    def draw_text(self,x,y,text,font):
        index = 0
        for ch in list(str(text)):
            if font == '5x7':
                for vector in S5x7[ch]:
                    if vector == []: return
                    self.set_pixel(x + (vector[0] + (index * 6)), vector[1] + y, 0)
            elif font == '3x5':
                for vector in S3x5[ch]:
                    if vector == []: return
                    self.set_pixel(x + (vector[0] + (index * 4)), vector[1] + y, 0)
            index += 1
