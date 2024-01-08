from pyrogram import Client, filters
import requests,os,csv
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from time import time
import time
from datetime import datetime
from pytz import *
import pytz
from pyrogram import enums
from spdatabase import *
from threading import Thread
import subprocess
import json
from datetime import timedelta
import random
from fpdf import FPDF
from PIL import Image
from gofile2 import Gofile


gof = Gofile(token="ktxxFE3Wg487gJJJS0pnAgXmdKCVYgPY")

up = { "ytdl": False,"Total":0}

images = []
def create_combined_pdf(image_files=images):
    #image_files = [img for img in os.listdir() if os.path.isfile(img) and
    #              os.path.splitext(img)[1].lower() in ('.png')]
    pdf = FPDF(format='letter')
    for img in image_files:
        if os.path.exists(img):
            image = Image.open(img)
            img_width, img_height = image.size
            scaling_factor_width = pdf.w / img_width
            scaling_factor_height = pdf.h / img_height
            scaling_factor = min(scaling_factor_width, scaling_factor_height)
            new_width = img_width * scaling_factor
            new_height = img_height * scaling_factor
            x = (pdf.w - new_width) / 2
            y = (pdf.h - new_height) / 2
            pdf.add_page()
            pdf.image(img, x, y, new_width, new_height)
    pdf.output("snaps.pdf")
        
def duration(filename):
        out = subprocess.check_output(["ffprobe", "-v", "quiet", "-show_format", "-print_format", "json", filename])
        ffprobe_data = json.loads(out)
        duration_seconds = float(ffprobe_data["format"]["duration"])
        td = str(timedelta(seconds=duration_seconds)).split(".")[0]
        return duration_seconds,td

def gen_sample(filename):
    dur = duration(filename)
    duration_seconds =  dur[0]
    ran = int(90-duration_seconds)
    sample = random.randint(0,abs(ran))
    #sample = str(timedelta(seconds=float(dur[0])/ran)).split(".")[0]
    total = dur[1]
    output_name = filename.split(".")[0]+f"_sample_."+filename.split(".")[-1]
    out = subprocess.check_output(["ffmpeg","-i",filename,"-ss",str(sample),"-t","90","-c:v","copy","-c:a","copy",output_name,"-y"])
    return output_name


def sample_clip(filename):
    dur = duration(filename)
    total = dur[0]
    count = 1
    output_names =[]
    output = filename.split(".")[0]+f"_sample_."+filename.split(".")[-1]
    for i in range(5,int(total),60):
      output_name = f"sample_{count}."+filename.split(".")[-1]
      output_names.append(output_name)
      sample = str(timedelta(seconds=i))
      out = subprocess.check_output(["ffmpeg","-i",filename,"-ss",sample,"-t","00:00:20","-vf","setpts=0.5*PTS","-an",output_name,"-y"])
      count+=1



    with open("files.txt","w+") as file:
        for i in output_names:
            file.write(f"file {i}\n")
    out = subprocess.check_output(["ffmpeg","-f","concat","-i","files.txt","-c:v","copy","-c:a","copy",output,"-y"])
    for i in output_names:
        os.remove(i)
    return output
        





api_id = 11405252
api_hash = "b1a1fc3dc52ccc91781f33522255a880"
bot_token = "6326333011:AAHHvjzDx7zc8nKXzobh_dNRoS5yH7KTPmw"



app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)













#playlist Links
links=[
     #"https://www.pornhub.com/playlist/275691841",
      # "https://www.pornhub.com/playlist/293168491",
       "https://www.pornhub.com/playlist/263313231"
       
      ]



def internet_speed_test():
    st = speedtest.Speedtest()
    return st.results.share()

       

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")



def chk_siz():
        out = subprocess.check_output(["rclone","--config",'./rclone.conf',"size","Drive:/SiteRip/"])
        x = "".join(out.decode('utf-8').split(":")).split("\n")[1]
        size = x.split(" ")[2]
        return float(size)



def stats(status,link,total,error="No Error"):
    stats = f'<b>├  Status: </b>{status}\n'\
            f'<b>├  Uploaded Videos: </b>{total}\n'\
            f'<b>├  {link.split("/")[-2].capitalize()}: </b>{link.split("/")[-1].capitalize()}\n'\
            f'<b>├  Errors : </b>{error}\n'\
            f'<b>╰  Updated Time: </b>{datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%m/%d %H:%M %p")}\n\n'
    return stats


def cap(title,pid,vid,svid,gf):
    text =  f'├  Title : {title}\n'\
            f'├  [Screenshots](https://t.me/c/2034630043/{pid})\n'\
            f'├  [Sample Video](https://t.me/c/2034630043/{svid})\n'\
            f'├  [Video](https://t.me/c/2034630043/{vid})\n'\
            f'├  [GoFile]({gf})\n'\
            f'╰  Updated Time: {datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%m/%d %H:%M %p")}\n\n'
    return text




def file():
     files = [file for file in os.listdir() if file.endswith(".mp4") and ("temp" not in file and "sample" not in file)]
     return files,len(files)



def ytdlpp(link):
     time.sleep(2)
     os.system("""yt-dlp --downloader aria2c --match-filter "duration>180"  -N 4 --max-download 167  --download-archive dled.txt --lazy-playlist  -o '%(title)s.%(ext)s' -f '(mp4)[height=?720]' --write-thumbnail --embed-metadata """ + link)
     print("Download Completed")
     time.sleep(20)
     up["ytdl"] = True
            
    
folder = gof.create_folder(parentFolderId="e470784e-1dad-4712-865a-abf2befcb592",folderName="Playlist")
clip_folder = gof.create_folder(parentFolderId=folder["id"],folderName="Pictures")
sample_folder = gof.create_folder(parentFolderId=folder["id"],folderName="Clips")

async def main():
   async with app: 
     filenames = []
     for link in links:

            up[link.split("/")[-1]] = 0
            
            crtda = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%m/%d %H:%M %p")
            if up["ytdl"]:
                time.sleep(2)
                await app.edit_message_text(-1002034630043,3,text='Starting Bot')
                up["ytdl"] = False
                time.sleep(2)
            #result = internet_speed_test()
            #await app.send_photo(-1002034630043,result,caption=stats("Active",link,"Uploading..")
            await app.edit_message_text(-1002034630043,3,text=stats("Active",link,"Uploading.."))

            dl = Thread(target=ytdlpp, args=(link,))
            dl.start()

            
            while ( not up["ytdl"] ) or ( file()[1] > 0 ):
                    files = file()
                    #print(up["ytdl"],files)
                    if files[1]>0:
                        for  filename in files[0]:
                            if filename not in filenames:
                                try:
                                        sample_filename = filename.split(".")[0]+f"_sample_."+filename.split(".")[-1]

                                        if not  os.path.exists(filename.replace('.mp4','.png')):
                                              os.system(f'''vcsi """{filename}""" -g 2x2 --metadata-position hidden -o """{filename.replace('.mp4','.png')}""" ''')
                                        gof.upload(filename.replace('.mp4','.png'),clip_folder["id"])

                                        if not  os.path.exists(sample_filename):
                                              sample_filename = gen_sample(filename)
                                        gof.upload(sample_filename,sample_folder["id"])

                                        if not  os.path.exists(sample_filename.replace('.mp4','.png')):
                                            os.system(f'''vcsi """{sample_filename}""" -g 1x1 --metadata-position hidden -o """{sample_filename.replace('.mp4','.png')}""" ''')
                                        gof.upload(sample_filename.replace('.mp4','.png'),clip_folder["id"])
                                        #images.append(filename.replace(".mp4",".png"))

                                        ssn = 10
                                        imgs =[]
                                        ssimgs = []
                                        dur = duration(filename)[0]
                                        interval = duration(filename)[0] // ssn
                                        print(interval)
                                        im = [img for img in os.listdir() if filename.replace(".mp4","-") in img]
                                        print(im)
                                        if len(im) != ssn:
                                            cmd = f'''ffmpeg -i """{filename}""" -vf fps=1/{interval} "{filename.replace(".mp4","-")}"%3d.png'''
                                            os.system(cmd)
                                            for i in range(1,11):
                                                    if i <10:
                                                        ss = f'{filename.replace(".mp4","-")}00{i}.png'
                                                    elif i==10:
                                                        ss = f'{filename.replace(".mp4","-")}0{i}.png'
                                                    if os.path.exists(ss):
                                                        ssimgs.append(ss)
                                                        gof.upload(ss,clip_folder["id"])
                                                        imgs.append(InputMediaPhoto(media=ss,caption=ss))
                                        else:
                                             for i in im:
                                                  if os.path.exists(i):
                                                        ssimgs.append(i)
                                                        gof.upload(i,clip_folder["id"])
                                                        imgs.append(InputMediaPhoto(media=i,caption=i))
                                                  
                                             
                                                #os.system(f'''rclone --config './rclone.conf' copy """{ss}"""  'PH_Pics:/Phvdl/Pictures/New/{filename.replace(os.path.splitext(filename)[1],'')}/'  ''')
                                        #os.system(f'''ffmpeg -i """{filename}""" -ss {cap_time} -q:v 1 -frames:v 1  "{ss}" -y''')
                                            
                                            
                                        

                                        if not  os.path.exists(filename.replace(".mp4",".jpg")):
                                             os.system(f'''vcsi """{filename}""" -g 1x1 --metadata-position hidden -o """{filename.replace('.mp4','.jpg')}""" ''')
                                        gof.upload(filename.replace('.mp4','.jpg'),clip_folder["id"])

                                        if len(imgs) >0:
                                          pic = await app.send_media_group(-1002034630043,imgs)
                                          time.sleep(2)
                                          pic = pic[0]
                                        else:
                                           os.system(f'''vcsi """{filename}""" -g 3x3--metadata-position hidden -o """{filename.replace('.mp4','.jpeg')}""" ''')
                                           pic = await app.send_photo(-1002034630043,photo=filename.replace('.mp4','.jpeg'))
                                           gof.upload(filename.replace('.mp4','.jpeg'),clip_folder["id"])


                                        sample = await app.send_video(-1002034630043,video=sample_filename,caption=sample_filename.replace(".mp4",""),thumb=sample_filename.replace("mp4","png"),supports_streaming=True,duration=int(duration(sample_filename)[0]),progress=progress)
                                        time.sleep(2)
                                        video = await app.send_video(-1002034630043,video=filename,caption=filename.replace(".mp4",""),thumb=filename.replace(".mp4",".jpg"),supports_streaming=True,duration=int(duration(filename)[0]),progress=progress)
                                        gf = gof.upload(filename,folder["id"])
                                        
                
                                        await app.send_photo(-1002034630043,photo=filename.replace('.mp4','.png'),caption=cap(filename,pic.id,video.id,sample.id,gf['downloadPage']),parse_mode=enums.ParseMode.MARKDOWN,progress=progress)
                                        


                                        #await app.send_photo(-1001848025191, photo=filename.replace(".mp4",".png"))
                                        #sample_video = await app.send_video(-1001945634929, video=sample_filename,caption=sample_filename.replace(".mp4",""),thumb=filename.replace("mp4","jpg"))
                                        #video = await app.send_video(-1002034630043,video=filename,caption=filename.replace(".mp4",""),thumb=filename.replace(".mp4",".jpg"))


                                        
                                        os.system(f'''rclone --config './rclone.conf' copy """{filename.replace(os.path.splitext(filename)[1],'.jpg')}"""  'PH_Pics:/Phvdl/Pictures/'  ''')                
                                        os.system(f'''rclone --config './rclone.conf' copy """{filename.replace(os.path.splitext(filename)[1],'.png')}"""  'PH_Pics:/Phvdl/Pictures/Snap/'  ''')
                                        os.system(f'''rclone --config './rclone.conf' copy """{sample_filename.replace(os.path.splitext(filename)[1],'.png')}"""  'PH_Pics:/Phvdl/Pictures/Snap/samples/'  ''')
                                        os.system(f'''rclone --config './rclone.conf' copy """{sample_filename}"""  'PH_Pics:/Phvdl/Samples/'  ''')
                                       
                                        

                                        filenames.append(filename)
                                        try:
                                             rmfiles = [filename,sample_filename,filename.replace(".mp4",".jpg"),filename.replace(".mp4",".png"),sample_filename.replace(".mp4",".png")]
                                             for i in rmfiles:
                                                  os.remove(i)
                                             for i in ssimgs:
                                                   os.remove(i)
                                        except Exception as e:
                                             print(e)
                                        up[link.split("/")[-1]]  += 1
                                        up["Total"]+=1

                                        txt = stats("Uploading",link,up[link.split("/")[-1]])
                                        oldtxt = " "
                                        if txt != oldtxt:
                                            await app.edit_message_text(-1002034630043,3,text=txt)
                                            oldtxt = txt


                                except Exception as e:
                                        print(e)
                                        await app.edit_message_text(-1002034630043,3,text=stats("Completed",link,up[link.split("/")[-1]],e))
                                 
                            
            #create_combined_pdf()
            #await app.send_document(-1001945634929, document="snaps.pdf")
            #os.system(f'''rclone --config './rclone.conf' move   'PH_Pics:/Pictures/Caps/new/'  ''')
            await app.edit_message_text(-1002034630043,3,text=stats("Offline",link,up["Total"]))
                    
print("bot up")
app.run(main())
  
