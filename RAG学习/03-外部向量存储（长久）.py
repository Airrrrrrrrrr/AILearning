# -*- coding: utf-8 -*-
# @Time    : 2026/5/31 16:31
# @Author  : 20962
# @Description  :
import csv
import os
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer


class BGEZhEmbeddings(Embeddings):
    def __init__(self, model_path: str):
        self.model = SentenceTransformer(model_path)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text, normalize_embeddings=True).tolist()


MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "tools", "embedding_model", "BAAI", "bge-small-zh-v1.5")
embedding = BGEZhEmbeddings(model_path=os.path.abspath(MODEL_DIR))
vector_store = Chroma(
    collection_name="movies",
    embedding_function=embedding,
    persist_directory=os.path.join(os.path.dirname(__file__), "chroma_langchain_db"),
)

# 只根据description来进行similarity_search
with open("movie.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    docs = [
        Document(
            page_content=row["description"],
            metadata={
                k: v.split("/") if k == "genre" else v
                for k, v in row.items() if k != "description"
            },
        )
        for row in reader
    ]

for doc in docs[:3]:
    print(doc)
# 将文档向量化
vector_store.add_documents(documents=docs, ids=["id_{}".format(i) for i in range(1, len(docs) + 1)])
# 删除操作
# vector_store.delete(ids=["id_{}".format(i) for i in range(5, 9)])
# 选中“科幻”类型的跟“消灭”有关系的前5个
# filter 需根据实际情况来进行编写
results = vector_store.similarity_search("科技", k=3, filter={"genre": {"$contains": "科幻"}})
# results = vector_store.similarity_search("科技", k=3)
print(len(results))
for result in results:
    print(result)