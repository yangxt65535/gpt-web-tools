import openai
from flask import Flask, render_template, request, jsonify

import os, re, json

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

@app.route("/")
def route_chat():
    return render_template("index.html")

@app.route("/update-api-key", methods=["POST"])
def route_update_api_key():
    data = json.loads(request.data.decode("utf-8"))
    print(data)
    new_api_key = data["api_key"].strip()
    response = {"update_status": "fail"}
    print("receive key", new_api_key)
    if (re.match(r"sk-[0-9a-zA-Z]*", new_api_key)):
        response = {"update_status": "succeed"}
        openai.api_key = new_api_key
    print(response)
    return jsonify(response)

@app.route("/retrieve-api-key", methods=["GET"])
def route_retrieve_api_key():
    response = {"api_key": openai.api_key}
    return jsonify(response)

@app.route("/chat", methods=["POST"])
def route_chat_work():
    data = json.loads(request.data.decode("utf-8"))
    print(data)

    body = {
        "model": "gpt-3.5-turbo",
        "messages": data["messages"],
        "stream": True,  # 启用流式API
    }

    for chunk in client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "Generate 10 names for a chinese cuisine cooking book",
            },
        ],
        stream=True
    ):
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="")

    return "1"
    # cstr = res.content.decode("utf-8")
    # res = re.findall(r'\{"content":"(.*?)"\}', cstr)
    # response["message"] = {
    #     "role": "assistant",
    #     "content": "".join(res)
    # }
    # print(response)
   
    # return jsonify(response)


