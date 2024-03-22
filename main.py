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
no_spotify_image = open("

background_image_file = random.choice(background_images)
background_image_path = os.path.join(background_images_dir, background_image_file)

background_image = Image.open(background_image_path)
background_image = background_image.resize((486, 486))

fonts_dir = 'fonts'

fonts = [file for file in os.listdir(fonts_dir) if file.endswith('.ttf')]

font_file = random.choice(fonts)
font_path = os.path.join(fonts_dir, font_file)

image = Image.new(background_image.mode, background_image.size)

image.paste(background_image, (0, 0))

draw = ImageDraw.Draw(image)

font_size = 36

font = ImageFont.truetype(font_path, size=font_size)

duration_text_x = 20
duration_text_y = 20
play_count_text_x = 20
play_count_text_y = duration_text_y + 46

draw.text((duration_text_x, duration_text_y), f"Duration: {sum_duration}", fill='white', font=font)

draw.text((play_count_text_x, play_count_text_y), f"Play Count: {sum_play_count}", fill='white', font=font)

image.save('summary_image.png')
