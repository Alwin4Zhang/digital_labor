import os

import logging

from io import BytesIO, StringIO
from typing import List, Union, Any, Dict

import pandas as pd
from tqdm import tqdm
from treelib import Tree, Node
from langchain.docstore.document import Document

from loader.unstructured_loaders.loader import FileLoader

from configs.apollo_config import logger



class QALoader(FileLoader):
    QUESTION_TYPE: List = ["类型", "问题类型", "所属类型", "问答类型"]
    QUESTION_NAME: List = ["q", "Q", "Question", "question", "问题", "问", "标准问题"]
    ANSWER_NAME: List = ["a", "A", "Answer", "answer", "答案", "答"]
    MAX_QUESTION_LENGTH = 100

    def __init__(self, file_path: str = None, file_stream: BytesIO = None):
        super().__init__(file_path, file_stream)
        self.df = self.table2df()
        self.docs = []
        # self.qas = self.table2qas()

    def build_tree(self, file_path) -> Tree:
        pass

    def query_content_by_chapter_section(self, query):
        pass

    def table2df(self):
        if self.file_path.lower().endswith(".xlsx") or self.file_path.lower().endswith(
            ".xls"
        ):
            if not self.file_stream:
                df = pd.read_excel(self.file_path)
            else:
                df = pd.read_excel(self.file_stream)
        if self.file_path.lower().endswith(".csv"):
            if not self.file_stream:
                df = pd.read_csv(self.file_path, on_bad_lines="skip")
            else:
                df = pd.read_csv(self.file_stream, on_bad_lines="skip")
        if self.file_path.lower().endswith(".tsv"):
            if not self.file_stream:
                df = pd.read_csv(self.file_path, sep="\t", on_bad_lines="skip")
            else:
                df = pd.read_csv(self.file_stream, sep="\t", on_bad_lines="skip")
        # df.dropna(how="all", inplace=True)
        df = df.fillna("")
        return df

    def table2qas(self):
        qas = []
        column_names = self.df.columns.to_list()
        qt = list(set(column_names) & set(self.QUESTION_TYPE))
        qi = list(set(column_names) & set(self.QUESTION_NAME))
        ai = list(set(column_names) & set(self.ANSWER_NAME))

        if not qi or not ai or not qt:
            return []
        for index, row in self.df[[qt[0], qi[0], ai[0]]].iterrows():
            question = str(row[qi[0]]).strip()
            answer = str(row[ai[0]]).strip()
            question_type = str(row[qt[0]]).strip()
            if not question or not answer:
                logger.info(f"question or answer is empty,will be skip...")
                continue
            if len(question) > self.MAX_QUESTION_LENGTH:
                logger.info(f"question {question} length is too long,will be skip...")
                continue
            self.docs.append(
                Document(
                    page_content=question,
                    metadata={"answer": answer, "question_type": question_type},
                )
            )
            qas.append(
                {"question": question, "answer": answer, "question_type": question_type}
            )
        return qas
