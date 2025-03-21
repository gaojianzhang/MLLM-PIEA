import json

with open('affection_test_data.json', 'r', encoding='utf-8') as file:
    data_1 = json.load(file)

sum=0
dict_user_outcome={}
with open('persona_test_emotion_10photo.json', 'r') as file:
    dict_user_outcome = json.load(file)


ls_data=[]
num=0
for i in data_1:
    num=0
    for j in data_1[i]["test"]:
        ls_data.append(j)
        num+=1

ls_res=[]
sum=0
for i in range(len(ls_data)):
    one_file = ls_data[i]
    if one_file["emotion"]=="something else":
           continue
    sum+=1
    #print(sum)
    ls_res.append({
    "question_id": sum,
    "image": "/data/sdf1/jianzhang_gao/datasets/"+one_file["img_name"],
    "text": "You are a master of role-playing. I want you to act as a person with personality: "+dict_user_outcome[one_file["user_id"]]+"\n"+"You need to answer according to the following requirements:\nUpon viewing the image provided, identify and articulate the emotion you would most likely feel in a structured two-line format. In the first line, select the emotion from the following list: [excitement, disgust, sadness, contentment, anger, awe, fear, amusement]. In the second line, explain the rationale behind this emotional response."
    })
    #print(one_file["img_name"],dict_user_outcome[i]["img_name"])



with open('question_free_emotion_10photo_3.jsonl', 'w', encoding='utf-8') as file:
    for item in ls_res:
        json.dump(item, file, ensure_ascii=False)
        file.write('\n')

