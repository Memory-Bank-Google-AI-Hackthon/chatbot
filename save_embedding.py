import re

from langchain_core.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from helper_function import get_text_embedding, get_image_embedding

# TODO: 此轉向量過程目前有點久, 需要優化


def save_need_info(need_embedding_content, content_type, api_key):
    """
    可以 call此, 獲得要存檔的物件的embedding, 以及該物件取出五個關鍵字後,
    轉成embedding的兩個tensor, 後續想要方便控管並放在存到db流程的func時,
    可以把這個func拆過去那邊即可

    Parameters:
    need_embedding_content: obj
        要存檔的物件, 目前僅支援圖片(圖片是給gcs的路徑)或是文章本身
    content_type: str
        進來的物件是文字還是圖片, 文字請給 text, 圖片 image
    api_key: str
        建模型要的google api key, main.py那個
    """
    title_tensor = title_embedding(need_embedding_content, content_type, api_key)
    content_tensor = content_embedding(need_embedding_content, content_type)

    return title_tensor, content_tensor


def content_embedding(need_embedding_content, content_type):
    if content_type == "text":
        content_tensor = get_text_embedding(need_embedding_content)
    elif content_type == "image":
        content_tensor = get_image_embedding(need_embedding_content)
    else:
        return ValueError("unknown type in title embedding")

    return content_tensor


def title_embedding(need_embedding_content, content_type, api_key):
    """
    會判斷傳進的物件是文章還是圖片, 目前僅能針對一個去做總結,
    若是給其餘的東西的話會報錯, 但是僅吃content_type的判斷, 所以沒那麼嚴格

    Parameters:
    need_embedding_content: obj
        要存檔的物件, 目前僅支援圖片或是文章本身
    content_type: str
        進來的物件是文字還是圖片, 文字請給 text, 圖片 image
    api_key: str
        建模型要的google api key, main.py那個

    Returns:
    title_tensor: list
        轉出的關鍵字壓成的向量
    """
    base_prompt = {
        "type": "text",
        "text": """
            Your task is to analyze the provided image or article and identify the five most relevant and related keywords.
            Ensure that these keywords accurately capture the essence and main topics of the image or article.
            If you don't get any ariticle but have image. Please provide a detailed description of the image content,
            focusing on visual elements such as the character's appearance, expression, and any accessories.
            please mention this and describe the character's interaction or relation to this text if applicable.
            Highlight key features and the overall mood or theme of the image.
            For each keyword, provide a brief explanation of why you chose it.
            Your final answer should be a list of these five keywords, presented at the end.

            """,
    }
    if content_type == "text":
        base_prompt["text"] = "article: {text_content}. " + base_prompt["text"]
        prompt = [base_prompt]
    elif content_type == "image":
        prompt = [base_prompt, {"type": "image_url", "image_url": "{image_url}"}]
    else:
        return ValueError("unknown type in title embedding")
    prompt_template = HumanMessagePromptTemplate.from_template(template=prompt)

    answer_1 = (
        ChatPromptTemplate.from_messages([prompt_template])
        | ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", temperature=0.5, google_api_key=api_key
        )
        | StrOutputParser()
    )

    answer_2 = (
        ChatPromptTemplate.from_messages([prompt_template])
        | ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", temperature=0.3, google_api_key=api_key
        )
        | StrOutputParser()
    )

    answer_3 = (
        ChatPromptTemplate.from_messages([prompt_template])
        | ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", temperature=0.1, google_api_key=api_key
        )
        | StrOutputParser()
    )

    final_prompt = """
    Result 1: {results_1} \n Result 2:{results_2} \n Result 3: {results_3}
    根據上述回答, 每個Result中, 有前次選擇的五個關鍵字以及選擇的理由。
    你的任務是統整所有的結果, 並從中選出作為最後答案最適合的五個關鍵字,並以中文回答

    回答形式如:
    1. 答案1
    2. 答案2
    總共給我五個答案即可, 不需要額外說明
    """
    summary_generator = (
        PromptTemplate.from_template(final_prompt)
        | ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", temperature=0.1, google_api_key=api_key
        )
        | StrOutputParser()
    )

    # debug用可以print出在chain中的變數的狀況
    def debug_print(data, key):
        print(f"Debug {key}: {data}")
        return data

    input_word = "text_content" if content_type == "text" else "image_url"
    chain = (
        {input_word: RunnablePassthrough()}
        | {
            "results_1": answer_1,  # | (lambda x: debug_print(x, "results_1")),
            "results_2": answer_2,  # | (lambda x: debug_print(x, "results_2")),
            "results_3": answer_3,  # | (lambda x: debug_print(x, "results_3")),
        }
        | summary_generator
    )

    if content_type == "text":
        answers = chain.invoke({"text_content": need_embedding_content})
    elif content_type == "image":
        answers = chain.invoke({"image_url": need_embedding_content})

    # 將結果轉成向量
    items = re.findall(r"\d+\.\s*(.*)", answers.strip())
    title_tensor = get_text_embedding(" ".join(items), 256)

    return title_tensor
