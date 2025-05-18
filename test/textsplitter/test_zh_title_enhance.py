import sys

sys.path.append("././")

from configs.model_config import *
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import nltk
from vectorstores import MyFAISS, MyCustomFAISS
from chains.local_doc_qa import load_file, tree

import torch
from transformers import AutoModel, AutoTokenizer

nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path

model_path = "/rainbow/zhangjunfeng/bert_models/pytorch/text2vec-large-chinese"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)
device = "cuda:0" if torch.cuda.is_available() else 'cpu'


def get_embeddings(text_list):
    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[
            0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(
            token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded,
                         1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    encoded_input = tokenizer(text_list,
                              padding=True,
                              truncation=True,
                              return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    return mean_pooling(model_output, encoded_input['attention_mask'])


if __name__ == "__main__":
    filepath = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "knowledge_base", "test_kb", "content", "test_55779840fck.rb")

    filepath = '/rainbow/zhangjunfeng/langchain-ChatGLM/knowledge_base/test_rb/content/test_95q76x1nio.rb'
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model_dict[EMBEDDING_MODEL],
        model_kwargs={'device': EMBEDDING_DEVICE})

    # docs = load_file(filepath, using_zh_title_enhance=True)
    docs, answers = load_file(filepath,
                              using_zh_title_enhance=False,
                              qa_split=True)
    vector_store = MyCustomFAISS.from_documents(docs, embeddings)
    # TODO:对答案做向量索引
    # answer_vector_stores = MyCustomFAISS.from_documents(answers,embeddings)
    # answer_vector_stores.index_to_docstore_id = vector_store.index_to_docstore_id
    # query = "指令提示技术有什么示例"
    # search_result = vector_store.similarity_search(query)
    # print(search_result)
    # query = "新店开业前，销售过机说明"
    # query = "折扣码预定期终止维护作业（crtt018）终止日期修改说明内容是什么？"
    query = "手机自助买单取消订单，款项退货说明"
    vec = get_embeddings([query]).cpu().numpy()
    docs = vector_store.similarity_search_with_score_by_vector(
        embedding=vec[0])
    print(docs)
    if docs:
        print(answers[docs[0]])
    # pass
