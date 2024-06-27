import os
import tarfile
import shutil
import subprocess
import urllib.request
import pygame
import glob

def display_loading_screen(screen, font, message):
    screen.fill(BLACK)
    text_surface = font.render(message, True, WHITE)
    screen.blit(text_surface, (WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2,
                               WINDOW_SIZE[1] // 2 - text_surface.get_height() // 2))
    pygame.display.flip()

pygame.init()
WINDOW_SIZE = (320, 240)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.mouse.set_visible(False)
font = pygame.font.Font(pygame.font.get_default_font(), 14)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

repo_owner = "forkymcforkface"
repo_name = "RGBPi-Extra"
branch = "dev"
path = "RGBPi-Extra"

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
os.chdir(grandparent_dir)

archive_file = os.path.join(grandparent_dir, f"{repo_name}-{branch}.tar.gz")
if os.path.exists(archive_file):
    os.remove(archive_file)

archive_url = f"https://github.com/{repo_owner}/{repo_name}/archive/{branch}.tar.gz"
display_loading_screen(screen, font, "Downloading Update")
try:
    urllib.request.urlretrieve(archive_url, archive_file)
except KeyboardInterrupt:
    display_loading_screen(screen, font, "Download Interrupted, Rebooting")
    pygame.time.wait(5000) 
    os.system('reboot')
except urllib.error.URLError:
    display_loading_screen(screen, font, "Download Failed, Rebooting")
    pygame.time.wait(5000)  
    os.system('reboot')
except Exception as e:
    display_loading_screen(screen, font, "Check Internet Connection, Rebooting")
    pygame.time.wait(5000)  
    os.system('reboot') 

temp_dir = os.path.join(grandparent_dir, "rgbpitemp")
os.makedirs(temp_dir, exist_ok=True)
with tarfile.open(archive_file, "r:gz") as tar:
    tar.extractall(path=temp_dir)

source_dir = os.path.join(temp_dir, f"{repo_name}-{branch}", path)
destination_dir = os.path.join(grandparent_dir, path)

if os.path.exists(destination_dir):
    shutil.rmtree(destination_dir)

shutil.move(source_dir, destination_dir)

shutil.rmtree(temp_dir)
os.remove(archive_file)

with subprocess.Popen(['df', '-P', grandparent_dir], stdout=subprocess.PIPE) as proc:
    output = proc.stdout.readlines()
    mount_point = output[1].decode().split()[5]

display_loading_screen(screen, font, "Update Complete, Rebooting")
pygame.time.wait(5000)  
os.system('reboot')
