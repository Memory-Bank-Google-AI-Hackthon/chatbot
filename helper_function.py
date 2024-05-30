import os


def build_embedding_model():
    from vertexai.vision_models import MultiModalEmbeddingModel

    mm_embedding_model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    return mm_embedding_model


def get_text_embedding(
    text: str = "",
    dimension=1408,
):
    """
    使用場景:
    當使用者想要存取網頁時, 將網頁內容爬下來(目前先以文字占多數的網頁為主),
    將所有文字內容轉成向量, 之後交由db儲存, 並以此判斷取用時要抓哪筆資料交還給使用者

    text:
        爬取過後的網頁的文字內容
    dimension: int
        要存取的向量的維度
    """
    mm_embedding_model = build_embedding_model()
    embedding = mm_embedding_model.get_embeddings(
        contextual_text=text,
        dimension=dimension,
    )
    return embedding.text_embedding


def get_image_embedding(
    image_path: str = None,
    dimension=1408,
):
    """
    使用場景:
    當使用者想要存取圖片時, 預期會先交由資料庫將圖片存到gcs上,
    之後再透過這個func, 將該圖片轉成向量後存到bigquery中

    image_path:
        圖片在gcs上的位置
    dimension: int
        要存取的向量的維度
    """
    from vertexai.vision_models import Image as VMImage

    mm_embedding_model = build_embedding_model()
    image = VMImage.load_from_file(image_path)
    embedding = mm_embedding_model.get_embeddings(
        image=image,
        dimension=dimension,
    )
    return embedding.image_embedding


def convert_file_to_jpg(file_path, output_folder):
    """
    將沒辦法embedding的圖檔轉成jpg
    目前測下來可轉的: jpg, png, jfif
    不可轉的: webp

    Parameters:
    file_path: str
        需要轉檔的圖片的位置
    output_folder: str
        輸出JPEG文件的資料夾位置

    Returns: str
        轉換後JPEG的位置
    """
    from PIL import Image

    # 讀檔
    with Image.open(file_path) as img:
        # 找出檔名
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # 換成jpg的路徑名稱
        jpg_file_path = os.path.join(output_folder, f"{file_name}.jpg")
        # 圖像轉換成RGB模式（JPEG不支持透明度）
        rgb_image = img.convert("RGB")
        rgb_image.save(jpg_file_path, "JPEG")
        # print(f"文件已轉換並存於: {jpg_file_path}")

    return jpg_file_path
