import sys

sys.path.append("./")

from db.embedding_utils import embed_texts_api
from utils.cluster_utils import embed_cluster_summarize_texts,recursive_embed_cluster_summarize
from loader.unstructured_loaders.pdf_loader import PDFLoader
from loader.unstructured_loaders.doc_loader import DocLoader
from textsplitter.document_header_splitter import DocumentHeaderTextSplitter


doc_path = "././test/test_files/8.3.1.2.1 柜组及库区设置操作规范.pdf"

doc_loader = PDFLoader(file_path=doc_path, file_stream=None)
document_splitter = DocumentHeaderTextSplitter()
docs = document_splitter.split_text(
    blocks=doc_loader.blocks,
    use_header=False
)

title = "柜组及库区设置操作规范"
texts = [doc.page_content for doc in docs]
# embed_cluster_summarize_texts(texts=texts, 
#                               level=1,
#                               title=title, 
#                               embedding_func=embed_texts_api)


results = recursive_embed_cluster_summarize(
    texts=texts,
    title=title,
    embedding_func=embed_texts_api
)

print(results)
