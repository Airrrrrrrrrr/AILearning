# -*- coding: utf-8 -*-
# @Time    : 2026/5/31 16:31
# @Author  : 20962
# @Description  :
import csv
import os
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
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
vector = InMemoryVectorStore(embedding=embedding)

# 只根据description来进行similarity_search
with open("movie.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    docs = [
        Document(
            page_content=row["description"],
            metadata={k: v for k, v in row.items() if k != "description"},
        )
        for row in reader
    ]

for doc in docs[:3]:
    print(doc)
# 将文档向量化
vector.add_documents(documents=docs, ids=["id_{}".format(i) for i in range(1, len(docs) + 1)])
# 删除操作
vector.delete(ids=["id_{}".format(i) for i in range(5, 9)])
# 选中“科幻”类型的跟“消灭”有关系的前5个
results = vector.similarity_search("消灭", k=5, filter=lambda doc: doc.metadata.get("genre","").find("科幻") != -1 )

for result in results:
    print(result)