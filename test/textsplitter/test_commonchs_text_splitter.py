# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2025/04/17 14:51:35
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''
import sys
sys.path.append("./")

from loader.unstructured_loaders.pdf_loader import PDFLoader

from textsplitter.commonchs_text_splitter import commonchs_doc_splitter


if __name__ == '__main__':
    abs_path = "./test/test_files/6.1.2.1.1 超市DM选品规范.pdf"
    abs_path = "./test/test_files/6、超市门店员工岗位操作手册（花艺助理）1.pdf"
    pdf_loader = PDFLoader(
        file_path=abs_path
    )
    
    blocks = pdf_loader.blocks
    
    documents = commonchs_doc_splitter.split_text(blocks=blocks)
    print(documents)