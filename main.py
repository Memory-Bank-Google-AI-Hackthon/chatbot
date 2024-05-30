# import os
# import re
# import io
# from PIL import Image
# import functions_framework
# from google.cloud import storage
# from dataclasses import dataclass, field
# from ChatBot import ChatBot
# from schema import SaveMessage
# from cloud_logger import logger
# from big_query import saveInfo
# from save_embedding import save_need_info
from fastapi import FastAPI
from schema import SaveMessage
app = FastAPI()


# os.environ["GOOGLE_API_KEY"] = ""
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "memory-bank.json"
# client = storage.Client()


# @functions_framework.http
# def chatbot(request):
#     data = request.get_json(silent=True)
#     saveMessage: SaveMessage = SaveMessage(**data)

#     chatbot = ChatBot(api_key=os.getenv("GOOGLE_API_KEY"))
#     chatbot.start_conversation()

#     if saveMessage.message == "save":
#         if saveMessage.images:
#             image_path = None
#             bucket = client.get_bucket("chatbot-image")
#             blobs = bucket.list_blobs()
#             for blob in blobs:
#                 blob_name_without_extension = re.sub(r"\.[^\.]+$", "", blob.name)
#                 if re.search(blob_name_without_extension, saveMessage.images):
#                     image_path = blob.name
#                     blob = bucket.blob(image_path)
#                     image_data = blob.download_as_bytes()
#                     image = Image.open(io.BytesIO(image_data))
#             contents = [image, saveMessage.message]
#             # info = save_need_info(image, "image", os.environ['GOOGLE_API_KEY'])
#             saveInfo(image_path, "x", "y")
#         elif saveMessage.url:
#             a = 1
#             # info = save_need_info(url, "text", os.environ['GOOGLE_API_KEY'])
#             # saveInfo(url, info[0], info[1])
#         return "save"
#     elif saveMessage.message == "take":
#         return "take"
#     elif saveMessage.message == "summary":
#         temperatures = [0, 0.1, 0.7]
#         responses = []
#         for temp in temperatures:
#             text_response = []
#             for chunk in chatbot.send_message(contents, temperature=temp):
#                 text_response.append(chunk.text)
#             responses.append("".join(text_response))

#         summary = chatbot.summarize_responses(responses)
#         logger(f"AI回覆:{summary}", level="INFO")
#         return summary
#     elif saveMessage.message:
#         if "清空" in saveMessage.message:
#             chatbot.clear_conversation()
#         contents = saveMessage.message

#     return "hihi"


@app.get("/healthz")
def healthz():
    return {"message": "Ok"}


@app.post("/save_messages")
async def save_messages(msg: SaveMessage):

    return {"message": "save_messages"}


@app.post("/get_message")
async def get_message():
    return {"message": "get_message"}
