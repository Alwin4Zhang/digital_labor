import os
import copy
import numpy as np
from typing import Any, Callable, List, Dict, Optional

from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore
# from langchain.vectorstores.faiss import dependable_faiss_import
from langchain_community.vectorstores.faiss import dependable_faiss_import
from langchain.docstore.base import Docstore
from langchain.docstore.document import Document
from langchain_community.vectorstores.utils import (
    DistanceStrategy,
    maximal_marginal_relevance,
)

from configs.model_config import *


class MyCustomFAISS(FAISS, VectorStore):

    def __init__(self,
                 embedding_function: Callable,
                 index: Any,
                 docstore: Docstore,
                 index_to_docstore_id: Dict[int, str],
                 normalize_L2: bool = False,
                 distance_strategy: DistanceStrategy = DistanceStrategy.
                 EUCLIDEAN_DISTANCE):
        super().__init__(embedding_function=embedding_function,
                         index=index,
                         docstore=docstore,
                         index_to_docstore_id=index_to_docstore_id,
                         normalize_L2=normalize_L2,
                         distance_strategy=distance_strategy)
        self.score_threshold = VECTOR_SEARCH_SCORE_THRESHOLD
        self.chunk_size = CHUNK_SIZE
        self.chunk_conent = False

    def seperate_list(self, ls: List[int]) -> List[List[int]]:
        # TODO: 增加是否属于同一文档的判断
        lists = []
        ls1 = [ls[0]]
        for i in range(1, len(ls)):
            if ls[i - 1] + 1 == ls[i]:
                ls1.append(ls[i])
            else:
                lists.append(ls1)
                ls1 = [ls[i]]
        lists.append(ls1)
        return lists

    def similarity_compare_with_score_by_diff_query(self, q1, q2, k=1) -> int:
        """根据传入的q1,q2判断哪个q更接近知识库"""
        faiss = dependable_faiss_import()
        e1 = self.embedding_function(q1)
        e2 = self.embedding_function(q2)
        vec1 = np.array([e1], dtype=np.float32)
        vec2 = np.array([e2], dtype=np.float32)
        if self._normalize_L2:
            faiss.normalize_L2(vec1)
            faiss.normalize_L2(vec2)
        scores1, indices1 = self.index.search(vec1, k)
        scores2, indices2 = self.index.search(vec2, k)
        score1_f, docs1 = [], []
        for j, i in enumerate(indices1[0]):
            if i == -1 or 0 < self.score_threshold < scores1[0][j]:
                continue
            score1_f.append(scores1[0][j])
            if i in self.index_to_docstore_id:
                _id = self.index_to_docstore_id[i]
                doc = self.docstore.search(_id)
                docs1.append((i, doc))
            # break
        score2_f, docs2 = [], []
        for j, i in enumerate(indices2[0]):
            if i == -1 or 0 < self.score_threshold < scores2[0][j]:
                continue
            score2_f.append(scores2[0][j])
            if i in self.index_to_docstore_id:
                _id = self.index_to_docstore_id[i]
                doc = self.docstore.search(_id)
                docs2.append((i, doc))
            # break
        # print('compare....',score1_f,score2_f)
        if not score1_f and not score2_f:  # q1,q2都没有相似
            return 2, []
        if not score1_f and score2_f:  # q1没有相似，q2相似
            return 0, docs2
        if not score2_f and score1_f:  # q1相似，q2没有相似
            return 1, docs1
        if score1_f[0] <= score2_f[0]:  # q1,q2都有相似
            return 1, docs1
        return 0, docs2

    def similarity_search_with_score_by_vector(
        self,
        embedding,
        k=1,
        filter: Optional[Dict[
            str, Any]] = None,  # Filter by metadata. Defaults to None.
        fetch_k:
        int = 20,  # (Optional[int]) Number of Documents to fetch before filtering.Defaults to 20.
        **kwargs
    ) -> List[Document]:
        faiss = dependable_faiss_import()
        vector = np.array([embedding], dtype=np.float32)
        if self._normalize_L2:
            faiss.normalize_L2(vector)
        scores, indices = self.index.search(vector, k)  # 分数是从小到大排序，越小越相似
        docs = []
        for j, i in enumerate(indices[0]):
            if i == -1 or 0 < self.score_threshold < scores[0][j]:
                # This happens when not enough docs are returned.
                continue
            if i in self.index_to_docstore_id:
                _id = self.index_to_docstore_id[i]
                doc = self.docstore.search(_id)
                docs.append((i, doc))
        return docs

    def delete_doc(self, source: str or List[str]):
        try:
            if isinstance(source, str):
                ids = [
                    k for k, v in self.docstore._dict.items()
                    if v.metadata["source"] == source
                ]
                vs_path = os.path.join(
                    os.path.split(os.path.split(source)[0])[0], "vector_store")
            else:
                ids = [
                    k for k, v in self.docstore._dict.items()
                    if v.metadata["source"] in source
                ]
                vs_path = os.path.join(
                    os.path.split(os.path.split(source[0])[0])[0],
                    "vector_store")
            if len(ids) == 0:
                return f"docs delete fail"
            else:
                for id in ids:
                    index = list(self.index_to_docstore_id.keys())[list(
                        self.index_to_docstore_id.values()).index(id)]
                    self.index_to_docstore_id.pop(index)
                    self.docstore._dict.pop(id)
                # TODO: 从 self.index 中删除对应id
                # self.index.reset()
                self.save_local(vs_path)
                return f"docs delete success"
        except Exception as e:
            print(e)
            return f"docs delete fail"

    def update_doc(self, source, new_docs):
        try:
            delete_len = self.delete_doc(source)
            ls = self.add_documents(new_docs)
            return f"docs update success"
        except Exception as e:
            print(e)
            return f"docs update fail"

    def list_docs(self):
        return list(
            set(v.metadata["source"] for v in self.docstore._dict.values()))
