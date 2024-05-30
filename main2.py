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


# os.environ['GOOGLE_API_KEY'] = ''
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'memory-bank.json'
# client = storage.Client()


# @functions_framework.http
# def chatbot(request):

#     data = request.get_json(silent=True)
#     saveMessage: SaveMessage = SaveMessage(**data)

#     chatbot = ChatBot(api_key=os.getenv('GOOGLE_API_KEY'))
#     chatbot.start_conversation()

#     if saveMessage.images and saveMessage.message:
#         image_path = None
#         bucket = client.get_bucket('chatbot-image')
#         blobs = bucket.list_blobs()
#         for blob in blobs:
#             blob_name_without_extension = re.sub(r'\.[^\.]+$', '', blob.name)
#             if re.search(blob_name_without_extension, saveMessage.images):
#                 image_path = blob.name
#                 blob = bucket.blob(image_path)
#                 image_data = blob.download_as_bytes()
#                 image = Image.open(io.BytesIO(image_data))
#         contents = [image, saveMessage.message]
#     elif saveMessage.message:
#         if '清空' in saveMessage.message:
#             chatbot.clear_conversation()
#         contents = saveMessage.message


#     temperatures = [0, 0.1, 0.7]
#     responses = []
#     for temp in temperatures:
#         text_response = []
#         for chunk in chatbot.send_message(contents, temperature=temp):
#             text_response.append(chunk.text)
#         responses.append("".join(text_response))

#     summary = chatbot.summarize_responses(responses)
#     logger(f'AI回覆:{summary}', level='INFO')

#     return summary
