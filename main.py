import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import os
import random

xml_file_path = os.path.expanduser("~/.local/share/rhythmbox/rhythmdb.xml")

sum_duration = 0
sum_play_count = 0

most_played_song = None
most_played_song_play_count = 0

second_most_played_song = None
second_most_played_song_play_count = 0

tree = ET.parse(xml_file_path)
root = tree.getroot()

for entry in root.findall('./entry[@type="song"]'):
    duration = int(entry.find('duration').text)
    play_count_element = entry.find('play-count')
    play_count = int(play_count_element.text) if play_count_element is not None else 0
    sum_duration += duration
    sum_play_count += play_count
    
    if most_played_song_play_count < play_count:
    	second_most_played_song = most_played_song
    	second_most_played_song_play_count = most_played_song_play_count
    
    	most_played_song = entry
    	most_played_song_play_count = play_count
    	
sum_duration_minutes = sum_duration // 60
sum_duration_secends = sum_duration % 60

sum_duration_hours = sum_duration_minutes // 60
sum_duration_minutes = sum_duration_minutes % 60

background_images_dir = 'images'

background_images = [file for file in os.listdir(background_images_dir) if file.endswith('.jpg')]

background_image_file = random.choice(background_images)
background_image_path = os.path.join(background_images_dir, background_image_file)

background_image = Image.open(background_image_path).convert("RGBA")
background_image = background_image.resize((556, 556))

no_spotify_image = Image.open("assets/no_spotify.png").convert("RGBA")
no_spotify_image = no_spotify_image.resize((18, 18))

bottom_panel = Image.new(background_image.mode, (556, 20), (0, 0, 0, 255))

image = Image.new(background_image.mode, background_image.size)

background_image.paste(bottom_panel, (0, 536))
background_image.paste(no_spotify_image, (1, 537), mask=no_spotify_image)

image.paste(background_image, (0, 0))
	
draw = ImageDraw.Draw(image)

title_font = ImageFont.truetype("fonts/Campton-BoldDEMO.otf", size=36)
summary_font = ImageFont.truetype("fonts/Manjari-Regular.otf", size=26)
sub_summary_font = ImageFont.truetype("fonts/Manjari-Thin.otf", size=22)
panel_font = ImageFont.truetype("fonts/Manjari-Thin.otf", size=10)

draw.text((20, 20), f"Rhythmbox-Wrapped", fill='white', font=title_font)

draw.text((18, 44), f"_"*30, fill='white', font=summary_font)

draw.text((20, 85), f"Total Time Listened: {sum_duration_hours}:{sum_duration_minutes}':{sum_duration_secends}\"", fill='white', font=summary_font)

draw.text((20, 123), f"Play Count: {sum_play_count}", fill='white', font=summary_font)

draw.text((20, 157), f"1st Most Played Song:", fill='white', font=summary_font)
draw.text((40, 187), f"Title: {most_played_song.find('title').text}", fill='white', font=sub_summary_font)
draw.text((40, 217), f"Artist: {most_played_song.find('artist').text}", fill='white', font=sub_summary_font)
draw.text((40, 247), f"Album: {most_played_song.find('album').text}", fill='white', font=sub_summary_font)
draw.text((40, 277), f"Genre: {most_played_song.find('genre').text}", fill='white', font=sub_summary_font)
draw.text((40, 307), f"Play Count: {most_played_song.find('play-count').text}", fill='white', font=sub_summary_font)

draw.text((20, 343), f"2nd Most Played Song:", fill='white', font=summary_font)
draw.text((40, 373), f"Title: {second_most_played_song.find('title').text}", fill='white', font=sub_summary_font)
draw.text((40, 403), f"Artist: {second_most_played_song.find('artist').text}", fill='white', font=sub_summary_font)
draw.text((40, 433), f"Album: {second_most_played_song.find('album').text}", fill='white', font=sub_summary_font)
draw.text((40, 463), f"Genre: {second_most_played_song.find('genre').text}", fill='white', font=sub_summary_font)
draw.text((40, 493), f"Play Count: {second_most_played_song.find('play-count').text}", fill='white', font=sub_summary_font)


draw.text((20, 540), f"By using the \"Rhythmbox-wrapped\" you are implying that you genuinely dislike \"Spotify\" as a platform for listening to music.", fill='white', font=panel_font)

image.save('summary_image.png')
