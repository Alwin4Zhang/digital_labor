# !/bin/bash
ab -c50 -n1000 -p test_milvus.txt -T 'application/json' http://192.168.148.148:7860/api/local_doc_qa/search_docs_from_vector_db