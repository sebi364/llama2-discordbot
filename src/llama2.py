from llama_cpp import Llama
import json
import os

conf = json.load(open("./system/settings.json"))["Llama2"]

model = Llama(
    model_path=conf["Modell-Path"],
    n_ctx=conf["n_ctx"],
    n_gpu_layers=conf["n_gpu_layers"]
)

def generate_response(context):
    response = model.create_chat_completion(
        messages = context["messages"],
        temperature = conf["temperature"],
    )
    return response["choices"][0]["message"]

def retrieve_context(id):
    if os.path.exists(f"./data/{id}.json"):
        return json.load(open(f"./data/{id}.json", "r"))
    else:
        return json.load(open(f"./templates/template.json", "r"))

def delete_context(id):
    if os.path.exists(f"./data/{id}.json"):
        os.remove(f"./data/{id}.json")

def update_context(new_context, id):
    json_string = json.dumps(new_context, indent=3)

    outfile = open(f"./data/{id}.json", "w")
    outfile.write(json_string)
    outfile.close()

def undo(id):
    context = retrieve_context(id)
    context["messages"] = context["messages"][:-2]

    update_context(context, id)

    return context["messages"][-1]["content"]

def respond(message):
    author = message.author.id
    prompt = {
        "role": "user",
        "content": str(message.content)
    }

    context = retrieve_context(author)
    context["messages"].append(prompt)

    response = generate_response(context)
    context["messages"].append(response)

    update_context(context, author)

    return response["content"]