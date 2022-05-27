from glob import glob
from time import sleep
import pygame
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from PIL import Image
import requests
import math
from urllib.request import urlopen
import io
# TODO : First auth --> don't refresh

def inits():
    global debug, currentURL, currentIndex, imgdef, playbackstate, BLUE, RED, sysfont, font, target_size, display_surface, REFRESHEVENT, scope, angle, mask, sp,target_w,target_h
    load_dotenv()
    debug = True
    scope = "user-read-currently-playing"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    pygame.init()
    currentURL="AAAA"
    clock = pygame.time.Clock()
    definitions = {"low":64,"medium":300,"high":640}
    currentDef = "medium"
    #imgdef=definitions[currentDef]
    imgdef=480
    currentIndex = 1
    playbackstate = {}
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    sysfont = pygame.font.get_default_font()
    font = pygame.font.SysFont(None, 48)
    if(debug):
        print('system font :', sysfont)
    target_w = pygame.display.Info().current_w
    target_h = pygame.display.Info().current_h
    if(debug):
        print('target_w :', target_w)
        print('target_h :', target_h)
    display_surface = pygame.display.set_mode((target_w,target_h), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    REFRESHEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(REFRESHEVENT, 5000)
    angle = 0 
    if(debug):
        print("-- creating mask")
    mask = pygame.Surface((imgdef, imgdef), pygame.SRCALPHA)
#    circleradius = int(imgdef/2)
    circleradius = int(target_h/2)

    if(debug):
        print('circle_radius ',circleradius)
    pygame.draw.circle(mask,pygame.Color("white"),(int(imgdef/2),int(imgdef/2)),circleradius)
    if(debug):
        print("-- done creating mask")

# source and explanation : https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def blitRotate(surface, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    # rotate and blit the image
    surface.blit(rotated_image, rotated_image_rect)

def getCover():
    global currentURL, image, playbackstate
    #if(debug):
    #    print("-- getCover")
    try:
        playbackstate = sp.current_user_playing_track()
        #if(debug):
        #    print(playbackstate)
        if(playbackstate):
            type = playbackstate['currently_playing_type']
            if(type == "track"):
                url =  playbackstate['item']['album']['images'][currentIndex]['url']
                #print(url)
                if(url != currentURL):
                    if(debug):
                        print("-- New image")
                    currentURL = url
                    image = DownloadCover(currentURL)
                else:
                    if(debug):
                        print("-- Same image")            
            if(type=="episode"):
                if(debug):
                    print("-- podcast")
                image = generateCover()
        else:
            if(debug):
                print("-- Pb empty")
            image = generateCover()
        return image            

    except:
        print("-- An exception occurred") 
        image = generateCover()
        print(playbackstate)

def DownloadCover(url):
    if(debug):    
        print("-- Now downloading")
    response = requests.get(url)
    image_str = urlopen(url).read()
    image_file = io.BytesIO(image_str)
    image = pygame.image.load(image_file)
    if(debug):
        print("-- Done downloading")
    return image

def generateCover():
    cover = pygame.Surface((imgdef, imgdef), pygame.SRCALPHA)
    font = pygame.font.SysFont(None, 48)
    img = font.render("Nothing playing", True, RED)
    rect = img.get_rect()
    pygame.draw.rect(img, BLUE, rect, 1)
    cover.fill(BLUE)
    cover.blit(img, (20, 20))
    if(debug):
        print("-- Generated")
    return cover

inits()
img = getCover()

while True:
    #clock.tick(60)
    for event in pygame.event.get():
        if event.type == REFRESHEVENT:
            if(debug):
                print("-- refresh")
            img = getCover()
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    if(img):
       #if(debug):
       #   print("-- if img") 
       masked = img.copy()
       DEFAULT_IMAGE_SIZE = (480, 480)
       masked = pygame.transform.scale(masked, DEFAULT_IMAGE_SIZE)
       masked.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
       #display_surface.blit(masked,(0,0))
       pygame.draw.circle(masked,pygame.Color("black"),(int(imgdef/2),int(imgdef/2)),int(imgdef/2*0.8),int(imgdef/2*0.05))
       blitRotate(display_surface, masked, (target_w-480,target_h/2), (int(imgdef/2), int(imgdef/2)), angle)
       if(playbackstate and playbackstate['is_playing'] == True):
           angle+=1
#        pygame.draw.circle(display_surface, pygame.Color(255, 255, 255), (target_size/2,target_size/2), 150, 0)
    pygame.display.flip()
