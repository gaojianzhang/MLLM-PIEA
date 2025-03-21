import json

with open('affection_trainset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

sum=0
dict_user_outcome={}
with open('persona_train_random_7photo.json', 'r') as file:
   dict_user_outcome = json.load(file)



ls_res = []
for i in data:
    
    person_file = data[i]
    for one_file in person_file["train"]:
        if one_file["emotion"]=="something else":
           continue
        sum+=1
        ls_res.append({
    "question_id": sum,
    "image": "/data/sdf1/jianzhang_gao/datasets/"+one_file["img_name"],
    "conversations": [
      {
        "from": "human",
        "value": "<image>\nYou are a master of role-playing. I want you to act as a person with personality: "+dict_user_outcome[i]+"\n"+"You need to answer according to the following requirements:\nUpon viewing the image provided, identify and articulate the emotion you would most likely feel in a structured two-line format. In the first line, select the emotion from the following list: [excitement, disgust, sadness, contentment, anger, awe, fear, amusement]. In the second line, explain the rationale behind this emotional response."
      },
      {
        "from": "gpt",
        "value": one_file["emotion"]+"\n"+one_file["utterance"]
      }
    ]
    })


with open('train_data_free_random_7photo.json', 'w', encoding='utf-8') as f:
    json.dump(ls_res, f, ensure_ascii=False, indent=4)

