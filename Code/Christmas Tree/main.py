#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image, ImageFont, ImageDraw 
import colorsys


def gen_line_str(line_width,prob=0.8):
    direction  = np.random.choice([-1,1])
    min_length = 1
    line_length_counter = 0
    char_len = 0
    line_str = ""
    
    if line_width == 1:
        return "*"
    
    while line_length_counter < line_width:
        if char_len > min_length:
            if np.random.sample() < prob:
                line_str += np.random.choice(["*","@","O","o"])
                direction *= -1
                char_len = 0
            else:
                if direction == 1:
                    line_str += ">"
                else:
                    line_str += "<"
                char_len += 1
        else:
            if direction == 1:
                line_str += ">"
            else:
                line_str += "<"
            char_len += 1
        line_length_counter += 1
    return line_str

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))



BG_COLOUR = (6,7,14)

IMAGE_WIDTH = 2000
IMAGE_HEIGHT = 2000

# List of points
points = []
# List of nodes
pivots = []


FONT_PATH = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
# specified font size
font = ImageFont.truetype(FONT_PATH, 40) 
 
TREE_CHARS = ["<",">"]


# List of tree lines
tree_lines = []


# Number of vertical lines in a tree
N_LINES = 30

# Gen tree
for line_count in range(N_LINES):
    
    line_length = 1+line_count*2
    
    tree_line_text = gen_line_str(line_length)
    
    tree_lines.append(tree_line_text)
    
    
    line_bbox = font.getbbox(tree_line_text)
    
    line_pixel_width,line_pixel_height = line_bbox[2:]
    

# Draw legs
leg_height = 2
leg_width = 2
for line_count in range(leg_height):
    
    line_length = 1+line_count*2
    
    tree_line_text = "|" + " "*leg_width + "|"
    
    tree_lines.append(tree_line_text)
    
    line_bbox = font.getbbox(tree_line_text)
    
    line_pixel_width,line_pixel_height = line_bbox[2:]
    


def draw_image(N_LINES,HIGHLIGHTED_LINE,c,line_mult = 2):
    # HSV is Hue Saturation Value
    
    img = Image.new("RGB", (IMAGE_WIDTH,IMAGE_HEIGHT), BG_COLOUR) # last part is image dimensions

    draw = ImageDraw.Draw(img) 
    
    # Hue is a circle, each line steps 1/N_COLOUR_STEPS across the circle
    N_COLOUR_STEPS = 80
    # Initial hue offset
    HUE_OFFSET = 0.1
    
    # Minimal Value drawn in the tree. Value of the "off" lines
    MIN_VAL_VAL = 0.4
    # Number of lines to highlight on each pass
    VAL_LINES_COUNT = 2
    
    # STAR LOGIC STARTS HERE
    
    
    # Compute circular gradient 
    gradient_frac = abs((N_LINES//2 - HIGHLIGHTED_LINE)/(N_LINES//2))
    # gradient_col used to create a colour of the circle, 50 shades of gray
    gradient_col = int(255*gradient_frac)
    
    innerColor = [gradient_col,gradient_col,gradient_col] #Color at the center
    outerColor = BG_COLOUR #Color at the corners
    
    
    glow_radius = 75  # Radius of the glow
    radius = 50  # Radius of the star
    y_offset = 250  # y down position
    
    prev_y = radius + y_offset - 50
    padding_box_size = 100  # Gradient is computed in a box
    
    for y in np.linspace(y_offset-glow_radius-padding_box_size,y_offset+glow_radius+padding_box_size,glow_radius+padding_box_size+1):
        for x in np.linspace(IMAGE_WIDTH//2-glow_radius-padding_box_size,
                             IMAGE_WIDTH//2+glow_radius+padding_box_size,glow_radius+padding_box_size+1):
    
            #Find the distance to the center
            distanceToCenter = np.sqrt((x - IMAGE_WIDTH//2) ** 2 + (y - 250) ** 2)
            
            if distanceToCenter > glow_radius:
                r,g,b = outerColor
            else:
                #Make it on a scale from 0 to 1
                distanceToCenter = float(distanceToCenter) / (glow_radius)
                
                # print(distanceToCenter)
        
                #Calculate r, g, and b values
                r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
                g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
                b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)
            
            
            
            #Place the pixel        
            img.putpixel((int(x), int(y)), (int(r), int(g), int(b)))
    
    # Draw the star's lines
    for i in range(5):
        theta = i*np.pi * 2/5 + np.pi/2 + np.pi
        draw.line((IMAGE_WIDTH//2,y_offset, 
                   IMAGE_WIDTH//2 + radius * np.cos(theta),y_offset + radius*np.sin(theta)), 
                  fill=hsv2rgb(0.2,1,gradient_frac),
                  width=7)
    
    
    # STAR LOGIC ENDS HERE
    
    for line_count in range(N_LINES):
        
        line_length = 1+line_count*2
        
        tree_line_text = gen_line_str(line_length)
        
        tree_line_text = tree_lines[line_count]
        line_bbox = font.getbbox(tree_line_text)
        
        line_pixel_width,line_pixel_height = line_bbox[2:]
        
        line_start_x = IMAGE_WIDTH//2 - line_pixel_width//2
        line_start_y = prev_y + (line_pixel_height + 10)
        
        prev_y = line_start_y
            
        
        hue_col = np.ceil(HUE_OFFSET + 1/N_COLOUR_STEPS*line_count) - (HUE_OFFSET + 1/N_COLOUR_STEPS*line_count)
        
        if abs(line_count - HIGHLIGHTED_LINE) > VAL_LINES_COUNT:
            VAL_VAL = MIN_VAL_VAL
        else:
            VAL_VAL = 1 - 0.5*abs(line_count - HIGHLIGHTED_LINE)/VAL_LINES_COUNT
            # print(line_count,VAL_VAL)
        
        line_col = hsv2rgb(hue_col,1,VAL_VAL)
        # drawing text size
        draw.text((line_start_x, line_start_y), tree_line_text, font = font, align ="left",
                  
                  fill=line_col) 
    
    
    
    # Draw legs
    leg_height = 2
    leg_width = 2
    for line_count in range(leg_height):
        
        line_length = 1+line_count*2
        
        tree_line_text = "|" + " "*leg_width + "|"
        
        line_bbox = font.getbbox(tree_line_text)
        
        line_pixel_width,line_pixel_height = line_bbox[2:]
        
        line_start_x = IMAGE_WIDTH//2 - line_pixel_width//2
        line_start_y = prev_y + (line_pixel_height + 10)
        
        prev_y = line_start_y
             
        # drawing text size
        draw.text((line_start_x, line_start_y), tree_line_text, font = font, align ="left",fill="#FFFFFF") 
    
    # Draw floor
    
    tree_line_text = "_ _ _ __|" + "_"*leg_width + "|__ _ _ _"
    
    line_bbox = font.getbbox(tree_line_text)
    
    line_pixel_width,line_pixel_height = line_bbox[2:]
    
    line_start_x = IMAGE_WIDTH//2 - line_pixel_width//2
    line_start_y = prev_y + (line_pixel_height + 10)
    
    prev_y = line_start_y
         
    # drawing text size
    draw.text((line_start_x, line_start_y), tree_line_text, font = font, align ="left",fill="#FFFFFF") 
    
    
    img = img.resize((IMAGE_WIDTH // 2, IMAGE_HEIGHT // 2), resample=Image.ANTIALIAS)
    img.save("images/test_{}.png".format(str(c).rjust(5,"0"))) # this image gets saved to same folder as the script
    
# Number of lines in a tree
MAX_N = 30
# For each line, compute 8 extra interpolations
INTERP_SCALAR = 8
vals = list(np.linspace(MAX_N,0,INTERP_SCALAR*MAX_N+1,INTERP_SCALAR))
for c,i in enumerate(vals):
    print("{} out of {} \t {:.2f}%".format(c,len(vals),100*c/len(vals)))
    draw_image(N_LINES,i,c,INTERP_SCALAR)

    





