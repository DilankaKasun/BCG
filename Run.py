from ast import If
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageDraw
import requests
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
import requests
from datetime import date




load_dotenv()

# cloud configure
config = cloudinary.config(secure=True)
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

# Image Upload 
def uploadImage(data):
        cloudinary.uploader.upload(f"cards/{data['Name']}.jpg", public_id=f"{data['Whatsapp Number']}", unique_filename = False, overwrite=True)
        srcURL = cloudinary.CloudinaryImage(f"{data['Name']}").build_url()
        print("****2. Upload an image****\nDelivery URL: ", srcURL, "\n")


# Msg SEND SYSTEM
def SendMSG(data):
        image_info=cloudinary.api.resource(f"{data['Whatsapp Number']}")
        inf_img=json.dumps(image_info,indent=2)
        #url = <API Path>
        inf_img= json.loads(inf_img)
        #API Path Token 
        payload = f"token=xfhlagqg7dpnnsiu&to=94772040343-1636031160@g.us&image={inf_img['url']}&caption=Automatically birthday card generator system&referenceId=&nocache="
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
 
        payload = f"token=xfhlagqg7dpnnsiu&to=%2B{data['Whatsapp Number']}1&image={inf_img['url']}&caption=Automatically birthday card generator system&referenceId=&nocache="
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)

# CSV Read 
df = pd.read_csv("5_6332484065937065819.csv")
records = df.to_dict(orient='record')
#Font Read 
font = ImageFont.truetype("Cookie-Regular.ttf", size=90)

# Birthday Card Generate 
def generate_card(data):
        DownloadURL = 'https://drive.google.com/u/0/uc?id='+data['Your Photo'].split('=')[1]
        print(DownloadURL)
        imgBack = Image.open('temp.png')
        rq =requests.get(DownloadURL, stream=True).raw
        imgPhotos = Image.open(rq).resize((357, 357), Image.ANTIALIAS)
        mask_im = Image.new("L", imgPhotos.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0) + (357,357), fill=255)
        imgFinal = imgBack.copy()
        imgFinal.paste(imgPhotos, (335, 100), mask_im)
        imgPhotos = Image.open("TextBg.jpg").resize((600, 100), Image.ANTIALIAS)
        mask_im = Image.new("L", imgPhotos.size, 0)
        draw2 = ImageDraw.Draw(mask_im)
        draw2.text((300,70), data["Name"] , font=font, anchor="ms", fill='#ffffff')
        print(mask_im)  
        imgFinal.paste(imgPhotos, (200,730), mask_im)
        return imgFinal

# SEND Loop
dayCal = ''
while True:
        today = date.today()
        if today != dayCal :
                dayCal = today
                for record in records:
                        dateTodaya = today.strftime("%m/%d").split('0')[1]
                        birtthDate=record['Birthday'].split('/')[0]+"/"+record['Birthday'].split('/')[1]
                        if dateTodaya == birtthDate:
                                daycal = dateTodaya
                                card = generate_card(record)
                                card.save(f"cards/{record['Name']}.jpg")
                                uploadImage(record)
                                SendMSG(record)
        
                
                