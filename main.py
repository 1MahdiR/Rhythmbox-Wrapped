import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import os
import random

xml_file_path = os.path.expanduser("~/.local/share/rhythmbox/rhythmdb.xml")

sum_duration = 0
sum_play_count = 0

tree = ET.parse(xml_file_path)
root = tree.getroot()

for entry in root.findall('./entry[@type="song"]'):
    duration = int(entry.find('duration').text)
    play_count_element = entry.find('play-count')
    play_count = int(play_count_element.text) if play_count_element is not None else 0
    sum_duration += duration
    sum_play_count += play_count

background_images_dir = 'images'

background_images = [file for file in os.listdir(background_images_dir) if file.endswith('.jpg')]

background_image_file = random.choice(background_images)
background_image_path = os.path.join(background_images_dir, background_image_file)

background_image = Image.open(background_image_path).convert("RGBA")
background_image = background_image.resize((556, 556))

no_spotify_image = Image.open("assets/no_spotify.png").convert("RGBA")
no_spotify_image = no_spotify_image.resize((18, 18))

bottom_panel = Image.new(background_image.mode, (556, 20), (0, 0, 0, 255))

fonts_dir = 'fonts'

fonts = [file for file in os.listdir(fonts_dir) if file.endswith('.ttf')]

font_file = random.choice(fonts)
font_path = os.path.join(fonts_dir, font_file)

image = Image.new(background_image.mode, background_image.size)

background_image.paste(bottom_panel, (0, 536))
background_image.paste(no_spotify_image, (1, 537), mask=no_spotify_image)

image.paste(background_image, (0, 0))
	
draw = ImageDraw.Draw(image)

title_font = ImageFont.truetype(font_path, size=48)
summary_font = ImageFont.truetype(font_path, size=36)
panel_font = ImageFont.truetype(font_path, size=10)

draw.text((20, 20), f"Rhythmbox-Wrapped", fill='white', font=title_font)

draw.text((18, 74), f"/"*75, fill='white', font=panel_font)

draw.text((20, 110), f"Duration: {sum_duration}", fill='white', font=summary_font)

draw.text((20, 176), f"Play Count: {sum_play_count}", fill='white', font=summary_font)

draw.text((20, 540), f"By using the \"Rhythmbox-wrapped\" you are implying that you genuinely dislike \"Spotify\" as a platform for listening to music.", fill='white', font=panel_font)

image.save('summary_image.png')
