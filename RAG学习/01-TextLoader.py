# -*- coding: utf-8 -*-
# @Time    : 2026/5/31 16:11
# @Author  : 20962
# @Description  : 文档加载器

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
loader = TextLoader(file_path="../LangChain学习/todo/LangChain学习Todo清单.md",encoding="utf-8")

docs = loader.load()
print(docs)
print(type(docs))
print(len(docs))



spliter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=50,
    separators=['\n\n','\n','。'],
    length_function=len,
)

split_docs = spliter.split_documents(docs)
print(split_docs)
print(type(split_docs))
print(len(split_docs))