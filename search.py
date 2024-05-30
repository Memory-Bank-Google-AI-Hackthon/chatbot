import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from helper_function import get_text_embedding


def search_similar_item(query_words, db_df, top_k=10):
    """
    目前依consine similarity來作為區分的依據, 後續可以卡更複雜的算法來做區分

    Parameters:
    query_words: str
        直接給使用者提供的prompt
    db_df: pd.DataFrame
        需要將資料庫的內容整理成df放入, 要有image的向量, 跟title組成的向量
    top_k: int
        要篩選前k個可能的物件回傳

    Returns:
    final_index: list
        選擇的前top_k個資料的index
    """
    image_query = np.array(get_text_embedding(query_words)).reshape(1, -1)
    title_query = np.array(get_text_embedding(query_words, 256)).reshape(1, -1)
    image_embs = db_df["image_embeddings"]
    title_embs = db_df["title_embeddings"]
    # TODO: 如果db抓出來的image_embeddings是字串的話, 這邊要換成np.array(eval(image_emb))
    scores1 = np.array(
        [
            cosine_similarity(np.array(image_emb).reshape(1, -1), image_query)[0][0]
            for image_emb in image_embs
        ]
    )
    scores2 = np.array(
        [
            cosine_similarity(np.array(image_emb).reshape(1, -1), title_query)[0][0]
            for image_emb in title_embs
        ]
    )
    db_df["score1"] = scores1
    db_df["score2"] = scores2
    # 目前依title跟使用者要求的內容的相似性高的優先, 再由內容相似的來排
    db_df = db_df.sort_values(by=["score2", "score1"], ascending=False)
    final_index = list(db_df[:top_k].index)

    return final_index
