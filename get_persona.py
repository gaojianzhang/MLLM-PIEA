import http.client
import json
import requests
import time
import math
from bs4 import BeautifulSoup
import csv
import random




conn = http.client.HTTPSConnection("YOUR_API_URL")
sum=0

data = {}
with open('affection_trainset.json', 'r', encoding="utf-8") as file:
   file_content = json.load(file)
data = file_content
with open('image_feature.json', 'r', encoding="utf-8") as file:
   file_content = json.load(file)
data_fea=file_content
dict_id_to_img={}
ls_now=[]
ls_have_user=[]
for i in data:
    ls_have_user.append(i)
dict_emo_to_cat={"excitement":1,"disgust":2,"sadness":2,"contentment":1,"anger":2,"awe":1,"fear":2,"amusement":1,"something else":3}
for i in ls_have_user:#emotion polarty diversity
    id_to_emo = []
    dict_hcat = {1: 0, 2: 0, 3: 0}
    target_count = {1: 5, 2: 5, 3: 0}#change the number of photos here
    selected = []
    
    for j in data[i]["exp"]:
        emo_cat = dict_emo_to_cat[j["emotion"]]
        if len(selected) >= 10:#here
            break
        if dict_hcat[emo_cat] < target_count[emo_cat] and j["emotion"] not in id_to_emo:
            selected.append(j)
            id_to_emo.append(j["emotion"])
            dict_hcat[emo_cat] += 1

    for j in data[i]["exp"]:
        if len(selected) >= 10:#here
            break
        if j not in selected:
            selected.append(j)
            id_to_emo.append(j["emotion"])

    if dict_id_to_img.get(data[i]["exp"][0]["user_id"], -1) == -1:
        dict_id_to_img[data[i]["exp"][0]["user_id"]] = []
    dict_id_to_img[data[i]["exp"][0]["user_id"]].extend(selected[:10])#here

    if len(dict_id_to_img[data[i]["exp"][0]["user_id"]]) < 10:#here
        print(f"User {i} has fewer than 10 entries available.")
'''
for i in ls_have_user:#image semantic diversity
    if dict_id_to_img.get(data[i]["exp"][0]["user_id"], -1) == -1:
        dict_id_to_img[data[i]["exp"][0]["user_id"]] = []
    
    inserted_points = []
    inserted_points.append(data[i]["exp"][0])
    dict_id_to_img[data[i]["exp"][0]["user_id"]].append(data[i]["exp"][0])

    while len(inserted_points) < 10:#change the number of photos here
        max_distance_sum = 0
        next_point = None

        for candidate in data[i]["exp"]:
            if candidate in inserted_points:
                continue
            
            distance_sum = 0
            for inserted in inserted_points:
                summ = 0
                for k in range(512):
                    summ += (data_fea[inserted["img_name"]][k] - data_fea[candidate["img_name"]][k]) ** 2
                distance_sum += math.sqrt(summ)
            
            if distance_sum > max_distance_sum:
                max_distance_sum = distance_sum
                next_point = candidate
        
        if next_point:
            inserted_points.append(next_point)
            dict_id_to_img[data[i]["exp"][0]["user_id"]].append(next_point)
'''
'''
for i in ls_have_user:#random
    random.seed(2024)
    dict_id_to_img[i] = random.sample(data[i]["exp"], 10)#change the number of photos here
'''
sum=0
ls_user=[]

headers = {
   'Accept': 'application/json',
   'Authorization': 'YOUR_TOKEN_HERE',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}
dict_res={}

sum=0

print(len(ls_have_user))
for j in ls_have_user:
    i=dict_id_to_img[j]
    sum += 1
    print(sum)
    #print(i[0]["emotion"],i[1]["emotion"],i[2]["emotion"],i[3]["emotion"],i[4]["emotion"],i[5]["emotion"],i[6]["emotion"],i[7]["emotion"],i[8]["emotion"],i[9]["emotion"])
    if sum<=0:
        continue
    try_num=0
    while True:
        if try_num>=10:
            break
        try:
            payload = json.dumps({
            "model": "gpt-4o-2024-08-06",
            "messages": [
                    {"role": "user", "content": [
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[0]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[1]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[2]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[3]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[4]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[5]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[6]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[7]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[8]["img_name"]}},
                        {"type": "image_url", "image_url": {"url": "http://1.13.255.9:5907/" + i[9]["img_name"]}},
                        {"type": "text", "text": "You are a master of sentiment analysis. In the input, there are ten images. You have seen the first ten images and have already provided corresponding emotional reactions and explanations. Below are your emotional reactions and explanations for the first three images:\n"
                        +"**[Image One]**\n"
                        +"Emotional reaction to the image:"+i[0]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[0]["utterance"]+'\n'
                                + "**[Image Two]**\n"
                                + "Emotional reaction to the image:" + i[1]["emotion"] + "\n"
                                + "Explanation for this emotional reaction:" + i[1]["utterance"] + '\n'
                                + "**[Image Three]**\n"
                                + "Emotional reaction to the image:" + i[2]["emotion"] + "\n"
                                + "Explanation for this emotional reaction:" + i[2]["utterance"] + '\n'
                        +"**[Image Four]**\n"
                        +"Emotional reaction to the image:"+i[3]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[3]["utterance"]+'\n'
                        +"**[Image Five]**\n"
                        +"Emotional reaction to the image:"+i[4]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[4]["utterance"]+'\n'
                        +"**[Image Six]**\n"
                        +"Emotional reaction to the image:"+i[5]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[5]["utterance"]+'\n'
                        +"**[Image Seven]**\n"
                        +"Emotional reaction to the image:"+i[6]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[6]["utterance"]+'\n'
                        +"**[Image Eight]**\n"
                        +"Emotional reaction to the image:"+i[7]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[7]["utterance"]+'\n'
                        +"**[Image Nine]**\n"
                        +"Emotional reaction to the image:"+i[8]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[8]["utterance"]+'\n'
                        +"**[Image Ten]**\n"
                        +"Emotional reaction to the image:"+i[9]["emotion"]+"\n"
                        +"Explanation for this emotional reaction:"+i[9]["utterance"]+'\n'
                       +"Now, based on this user's emotional response, you need to analyze their personality. Please consider what kind of personality traits this user might have based on emotional reaction to the picture.Please note that you only need to output your one paragraph of analysis, and no other content is needed. Your answer should be around 200 words."
                        }
                    ]}
                ]
            })
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            dict_data = json.loads(data)
            print(dict_data["choices"][0]["message"]["content"])
            with open('persona_train_emotion_10photo.json', 'r') as file:
                dict_res=json.load(file)
            dict_res[j]=dict_data["choices"][0]["message"]["content"]
            with open('persona_train_emotion_10photo.json', 'w') as file:
                json.dump(dict_res, file, indent = 4)
            break
        except:
            print("ERROR",sum)
            try_num+=1
            time.sleep(5)
    if try_num==10:
        raise ValueError("NO!!!!")


