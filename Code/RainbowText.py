# It changes the colors of the letters of a text when you click the screen
     
     
import pygame
import pygame.font
import random
from pygame.locals import *

def GetGlyphs(surf, COLOR):
     """ Pull All Glyphs and Shapes of a certain color from a certain surface """
     print("Looking for glyphs and shapes...")
     TempGlyph = []     
     GlyphList = []      
     Active = []        
     
     # Make a copy 
     SurfCopy = pygame.Surface(surf.get_size())   
     SurfCopy.blit(surf, (0,0))

     DONECOLOR = (random.randrange(10,250),random.randrange(10,250),random.randrange(10,250))
     if DONECOLOR == COLOR:
          DONECOLOR += 1        

     for x in range(SurfCopy.get_width()):             
          for y in range(SurfCopy.get_height()):
               if SurfCopy.get_at([x,y])[:3] == COLOR:     
                    TempGlyph = []
                    Active = []
                    Active.append([x,y])
                    while len(Active):                      
                         CurrPoint = Active.pop(0)               
                         Point = [CurrPoint[0],CurrPoint[1]]    
                         
                         try:
                              if SurfCopy.get_at(  [Point[0]+1, Point[1]]  )[:3] == COLOR:
                                   Active.append(  [Point[0]+1, Point[1]]    )
                                   SurfCopy.set_at([Point[0]+1, Point[1]], DONECOLOR)
                         except IndexError:
                              pass                       

                         try:                            
                              if SurfCopy.get_at(  [Point[0]-1, Point[1]]  )[:3] == COLOR:
                                   Active.append(  [Point[0]-1, Point[1]]    )
                                   SurfCopy.set_at([Point[0]-1, Point[1]], DONECOLOR)
                         except IndexError:
                              pass                          

                         try:                              
                              if SurfCopy.get_at(  [Point[0], Point[1]+1]  )[:3] == COLOR:
                                   Active.append(  [Point[0], Point[1]+1]    )
                                   SurfCopy.set_at([Point[0], Point[1]+1], DONECOLOR)
                         except IndexError:
                              pass
                              
                         try:
                              if SurfCopy.get_at(  [Point[0], Point[1]-1]  )[:3] == COLOR:
                                   Active.append(  [Point[0], Point[1]-1]    )
                                   SurfCopy.set_at([Point[0], Point[1]-1], DONECOLOR)
                         except IndexError:
                              pass

                         TempGlyph.append(Point)                 
                    GlyphList.append(TempGlyph)                  
                    pygame.display.flip()

     print("There are " + str(len(GlyphList)) + " glyphs found altogether") 
     return GlyphList                                            
     




if __name__ == '__main__':    

     pygame.init()           

     FALSE = 0                
     TRUE = 1

     ANTIALIAS = FALSE      

     WHITE = (255,255,255)   
     BLACK = (0,0,0)
     RED = (255,0,0)
     GRAY = (128,128,128)
      
     OLDCOLOR = BLACK         
     NEWCOLOR = RED          
     BACKGROUND = WHITE       
     
     FONTSIZE = 50          
     
     Messages = []            
     Surfaces = []           
          
     # Displaying message
     Messages.append("Hello there, how are you?")     
     Messages.append("This program is dull...")
     Messages.append("But is pretty when you click?!")

     # Set a default font
     CurrentFont = pygame.font.Font(None, FONTSIZE)  

     for x in Messages:      
          Surfaces.append(CurrentFont.render(x, ANTIALIAS, OLDCOLOR, BACKGROUND)) 


     MaxWidth = []
     TotalHeight = 0
     CurrentHeight = 0

     for x in Surfaces:
          MaxWidth.append(x.get_width())

     for x in Surfaces:
          TotalHeight += x.get_height()

     screen = pygame.display.set_mode([max(MaxWidth),TotalHeight] )
     screen.fill(BACKGROUND)     

     for x in Surfaces:
          screen.blit(x, (0,CurrentHeight))
          CurrentHeight += x.get_height()
          
     pygame.display.flip()


     # Finally, we are done with the test surface. Now to pull out the letters.
     
     Glyphs = GetGlyphs(screen, OLDCOLOR)

     # Color the letters
     for G in Glyphs:
          RANDCOLOR = (random.randrange(0,256),random.randrange(0,256),random.randrange(0,256))
          for Point in G:
               screen.set_at(Point, RANDCOLOR)


     while pygame.event.poll().type != QUIT:
          if pygame.mouse.get_pressed()[0]:
               for G in Glyphs:
                    RANDCOLOR = (random.randrange(0,256),random.randrange(0,256),random.randrange(0,256))
                    for Point in G:
                         screen.set_at(Point, RANDCOLOR)
          pygame.display.flip()

pygame.quit()
          
