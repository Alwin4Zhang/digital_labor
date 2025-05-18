import os
import sys

sys.path.append('././')

import pandas as pd
from tqdm import tqdm
from fuzzywuzzy import fuzz

import models.shared as shared
from models.loader import LoaderCheckPoint
from models.loader.args import parser, DEFAULT_ARGS
from configs.model_config import *
from chains.local_doc_qa import LocalDocQA

tqdm.pandas(desc='testset precision bar')


def init_local_doc_qa():
    args = None
    args = parser.parse_args(
        args=['--model', 'chatglm2-6b-int4', '--no-remote-model'])
    args_dict = vars(args)
    shared.loaderCheckPoint = LoaderCheckPoint(args_dict)
    llm_model_ins = shared.loaderLLM()
    llm_model_ins.set_history_len(LLM_HISTORY_LEN)
    local_doc_qa = LocalDocQA()
    local_doc_qa.init_cfg(llm_model=llm_model_ins)
    return local_doc_qa


def sim_by_edit_dist(a, b, thres=90):
    return 1 if fuzz.ratio(a, b) >= thres else 0


def test_func_faiss_precision(data_path,
                              qa_model=None,
                              model_name='m3e-base',
                              use_keywords=False,
                              use_rank=False):
    dir_path = os.path.dirname(data_path)
    df_testset = pd.read_csv(data_path)

    def inner_func(row):
        q = row['问题收集']
        a = row['正确答案']
        if not use_rank:
            recalls = qa_model.get_relevant_documents_by_faiss(
                q, use_keywords=use_keywords)
        else:
            recalls, query_keywords = qa_model.get_relevant_documents_custom(q)
            recalls = qa_model.rerank(q, query_keywords, recalls)
        if not recalls:
            row[model_name] = 0
            return row
        best_answer = recalls[0]['content']
        row[model_name] = sim_by_edit_dist(a, best_answer)
        return row

    df_testset = df_testset.progress_apply(func=inner_func, axis=1)
    print("precision percentage:\t ",
          len(df_testset[df_testset[model_name] == 1]) / len(df_testset) * 100,
          "%")
    print(
        "hr percision precentage:\t",
        len(df_testset[(df_testset[model_name] == 1)
                       & (df_testset['类别'] == '人事')]) /
        len(df_testset[df_testset['类别'] == '人事']) * 100, "%")
    df_testset.to_csv(f"{dir_path}/testset_result_{model_name}.csv",
                      index=False)


if __name__ == '__main__':

    local_doc_qa = init_local_doc_qa()
    # query = "工伤假扣钱吗?"

    # recalls,query_keywords = local_doc_qa.get_relevant_documents_custom(query)
    # sorted_recalls = local_doc_qa.rerank(query,query_keywords,recalls)
    # print(query,sorted_recalls[0])

    testset_path = "/rainbow/zhangjunfeng/langchain-ChatGLM/test/testset_test/testset.csv"
    # df_testset = pd.read_csv(testset_path)
    # print(df_testset)
    # model_name = "text2vec"
    model_name = "text2vec-kw"
    # model_name = "m3e-base"
    # model_name = "m3e-base-kw"
    # model_name = "m3e-large-kw"
    # model_name = "bge-large-kw"
    # model_name = "bge-ranker-large"
    import time
    start = time.time()
    test_func_faiss_precision(testset_path,
                              qa_model=local_doc_qa,
                              model_name=model_name,
                              use_keywords=True,
                              use_rank=False)
    print((time.time() - start) / 100)
    # print(df_testset[df_testset['问题收集'].str.contains('R3')])
