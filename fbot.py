from pyrogram import Client, filters
import time
from datetime import datetime
from pytz import *
import pytz
import requests
import os
from threading import Thread
import json
from datetime import timedelta
import random
from PIL import Image

from pyrogram import enums
from pyrogram.types import InputMediaPhoto

up = {"ytdl": False, "Total": 0}

api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
bot_token = "6593397412:AAFmJ8Hj9jnZuvLs_rLcu63bQwCp0EV829w"

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

# Playlist Links
links = [
    "https://www.pornhub.com/playlist/301331341"
    #"https://www.pornhub.com/playlist/275691841",
    #"https://www.pornhub.com/playlist/293168491",
    #"https://www.pornhub.com/playlist/263313231"
]


def ytdlpp(link):
    time.sleep(2)
    os.system(
        """./yt-dlp --downloader aria2c --match-filter "duration>180"  -N 4 --max-download 200  -o '%(title)s.%(ext)s' -f '(mp4)[height=?720]' --write-thumbnail --embed-metadata """ + link)
    print("Download Completed")
    time.sleep(20)
    up["ytdl"] = True


async def progress(current, total, task_name="Task"):
    percentage = current * 100 / total
    bar_length = 20
    completed_blocks = int(bar_length * current / total)

    bar = "█" * completed_blocks + " " * (bar_length - completed_blocks)

    print(f"{task_name} Progress: [{bar}] {percentage:.1f}% Complete")

# Remove unnecessary code related to rclone, gofilo, and other functionalities


async def main():
    async with app:
        filenames = []
        for link in links:

            up[link.split("/")[-1]] = 0

            crtda = datetime.now(
                pytz.timezone("Asia/Kolkata")).strftime("%m/%d %H:%M %p")
            if up["ytdl"]:
                time.sleep(2)
                await app.edit_message_text(-1002034630043, 3, text='Starting Bot')
                up["ytdl"] = False
                time.sleep(2)

            await app.edit_message_text(-1002034630043, 3, text=f"Active - {link}")

            dl = Thread(target=ytdlpp, args=(link,))
            dl.start()

            while (not up["ytdl"]) or (file()[1] > 0):
                files = file()
                if files[1] > 0:
                    for filename in files[0]:
                        if filename not in filenames:
                            try:
                                sample_filename = filename.split(".")[0] + \
                                    f"_sample_." + filename.split(".")[-1]

                                if not os.path.exists(filename.replace('.mp4', '.png')):
                                    os.system(
                                        f'''vcsi """{filename}""" -g 2x2 --metadata-position hidden -o """{filename.replace('.mp4','.png')}""" ''')
                                # images.append(filename.replace(".mp4",".png"))

                                ssn = 10
                                imgs = []
                                ssimgs = []
                                dur = duration(filename)[0]
                                interval = duration(filename)[0] // ssn

                                im = [img for img in os.listdir() if filename.replace(
                                    ".mp4", "-") in img]

                                if len(im) != ssn:
                                    cmd = f'''ffmpeg -i """{filename}""" -vf fps=1/{interval} "{filename.replace(".mp4","-")}"%3d.png'''
                                    os.system(cmd)
                                    for i in range(1, 11):
                                        if i < 10:
                                            ss = f'{filename.replace(".mp4","-")}00{i}.png'
                                        elif i == 10:
                                            ss = f'{filename.replace(".mp4","-")}0{i}.png'
                                        if os.path.exists(ss):
                                            ssimgs.append(ss)
                                            imgs.append(
                                                InputMediaPhoto(media=ss, caption=ss))
                                else:
                                    for i in im:
                                        if os.path.exists(i):
                                            ssimgs.append(i)
                                            imgs.append(
                                                InputMediaPhoto(media=i, caption=i))

                                if not os.path.exists(filename.replace(".mp4", ".jpg")):
                                    os.system(
                                        f'''vcsi """{filename}""" -g 1x1 --metadata-position hidden -o """{filename.replace('.mp4','.jpg')}""" ''')

                                # Sample Video
                                sample = await app.send_video(-1002034630043, video=sample_filename, caption=sample_filename.replace(
                                    ".mp4", ""), thumb=sample_filename.replace("mp4", "png"), supports_streaming=True, duration=int(duration(sample_filename)[0]), progress=progress)

                                # Main Video
                                video = await app.send_video(-1002034630043, video=filename, caption=filename.replace(
                                    ".mp4", ""), thumb=filename.replace(".mp4", ".jpg"), supports_streaming=True, duration=int(duration(filename)[0]), progress=progress)

                                if len(imgs) > 0:
                                    pic = await app.send_media_group(
                                        -1002034630043, imgs)
                                    pic = pic[0]
                                else:
                                    os.system(
                                        f'''vcsi """{filename}""" -g 3x3--metadata-position hidden -o """{filename.replace('.mp4','.jpeg')}""" ''')
                                    pic = await app.send_photo(
                                        -1002034630043, photo=filename.replace('.mp4', '.jpeg'))

                                await app.send_photo(-1002034630043, photo=filename.replace(
                                    '.mp4', '.png'), caption=filename.replace(".mp4", ""), progress=progress)

                                filenames.append(filename)

                                try:
                                    rmfiles = [filename, sample_filename,
                                               filename.replace(".mp4", ".jpg"), filename.replace(".mp4", ".png"), sample_filename.replace(".mp4", ".png")]
                                    for i in rmfiles:
                                        os.remove(i)
                                    for i in ssimgs:
                                        os.remove(i)
                                except Exception as e:
                                    print(e)

                                up[link.split("/")[-1]] += 1
                                up["Total"] += 1

                                txt = f'Active - {link} | Uploading: {up[link.split("/")[-1]]} | Total: {up["Total"]}'
                                await app.edit_message_text(-1002034630043, 3, text=txt)

                            except Exception as e:
                                print(e)
                                await app.edit_message_text(
                                    -1002034630043, 3, text=f"Error: {e}")

            await app.edit_message_text(-1002034630043, 3, text=f"Offline - {link}")


print("Bot is up")
app.run(main())
