from flask import render_template, jsonify,request,Flask,send_from_directory
from openpyxl import load_workbook
import os
import requests, json
import pandas as pd
app=Flask(__name__)
@app.route('/',methods=["GET","POST"])
def index():
    url = 'http://65.2.11.36:32344/graphql'
    
    params={"query":"{\n  twitterUserTweets {\n    id\n    id_str\n    text\n    truncated\n    source\n    in_reply_to_status_id\n    in_reply_to_status_id_str\n    in_reply_to_user_id\n    in_reply_to_user_id_str\n    in_reply_to_screen_name\n    geo\n    coordinates\n    place\n    is_quote_status\n    retweet_count\n    favorite_count\n    favorited\n    retweeted\n    possibly_sensitive\n    lang\n    created_at\n    screen_name\n    contributors\n    retweeted_status_text\n    retweeted_status_id\n    retweeted_status_id_str\n    reply_count\n    like_count\n    quote_count\n    name\n    sentiment {\n      query\n      query_result\n      score\n    }\n  } \n}","variables":{}}
    df=[]
    response=requests.get(url,params)
    response=json.loads(response.text)
    f=response["data"]
    for i in f["twitterUserTweets"]:
        df.append([i["id"],i["text"]])
    df=pd.DataFrame(df,columns=["id","text"])
    sdf=df["text"]
    m=[]
    mm=[]
    m1=[]
    for i in sdf:
        i=i.split("\n")
        w=""
        for s in i:
            w=w+s
        i=w
        w=i.split(" ")
        w1=[]
        for q in w:
            try:
                if q[0]=="@":
                    w1.append(q)
            except IndexError:
                pass
        w=i
        for name in w1:
            w=w.replace(name,"")
            w=w.replace(w.split(" ")[-1],"")
        res=requests.post("http://localhost:5000/predict",json={"query":w})
        
        m.append(json.loads(res.text)["score"])
        mm.append(json.loads(res.text)["query_result"])
        m1.append(w)
    df.insert(2,"score",m)
    df.insert(3,"query_result",mm)
    df.insert(4,"message1",m1)
    df.to_excel("vishal.xlsx")
    return send_from_directory(directory="../..",path="vishal.xlsx",as_attachment=bool(1))
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1001))
    app.run(debug=True, host='0.0.0.0', port=port)

