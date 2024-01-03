import os
from threading import Thread
os.system("pip install pyrofork==2.2.11")
from pyrogram import Client, filters
import random
import time


api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
bot_token2 = "6593397412:AAFmJ8Hj9jnZuvLs_rLcu63bQwCp0EV829w"

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token2)


up = { "ytdl": False,'Total':0}



links=[
    "https://youtube.com/playlist?list=PLMC9KNkIncKvYin_USF1qoJQnIyMAfRxl&si=w7qSDmBdsGWslf4u"
    #"https://www.pornhub.com/playlist/85569291"
      ]



#async def progress(current, total):
    #print(f"{current * 100 / total:.1f}%")

async def progress(current, total, task_name="Task"):
    percentage = current * 100 / total
    bar_length = 20
    completed_blocks = int(bar_length * current / total)

    bar = "█" * completed_blocks + " " * (bar_length - completed_blocks)

    print(f"{task_name} Progress: [{bar}] {percentage:.1f}% Complete")


def ytdlpp(link):
     #time.sleep(2)
     os.system("""./yt-dlp --downloader aria2c --match-filter "duration>180"   --max-downloads  200  -N 10 -o '%(title)s.%(ext)s' -f '(mp4)[height=?720]' --write-thumbnail --embed-metadata """ + link )
     print(f"Download Completed{link}")
     time.sleep(120)
     up["ytdl"] = True



async def main():
   async with app: 
     for link in links:
        dl = Thread(target=ytdlpp, args=(link,))
        dl.start()
        upl = True
        while upl:
            print(f"Downloading {link}")
            sts = await app.send_message(-1002034630043,f"Downloading {link}")
            time.sleep(6)
            while upl:
                for filename in os.listdir():
                    if filename.endswith(".mp4"):
                        try:
                            os.system(f'''vcsi """{filename}""" -g 2x2 --metadata-position hidden -o """{filename.replace('.mp4','.png')}""" ''')
                            await app.edit_message_text(-1002034630043,sts.id,f"Uploaded Videos:{up['Total']}\nUploading {filename}")
                            video = await app.send_video(-1002034630043,video=filename,caption=filename.replace(".mp4",""),thumb=filename.replace(".mp4",".png"),supports_streaming=True,progress=progress)
                            up['Total']+=1
                            await app.edit_message_text(-1002034630043,sts.id,f"Uploaded Videos:{up['Total']}\nUploaded {filename}")
                            try:
                                os.remove(filename)
                                os.remove(filename.replace('.mp4','.png'))
                                await app.edit_message_text(-1002034630043,sts.id,f"Uploaded Videos:{up['Total']}\nCleared {filename}")
                            except:
                                pass
                        except Exception as e:
                            print(e)
                    if up["ytdl"] == True:
                        upl = False
print("Bot Started")
app.run(main())
