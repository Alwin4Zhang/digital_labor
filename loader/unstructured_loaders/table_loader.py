# -*- coding: utf-8 -*-
'''
  @CreateTime	:  2025/03/17 17:24:01
  @Author	:  Alwin Zhang
  @Mail	:  zhangjunfeng@rainbowcn.com
'''

import os

import logging

import math
from io import BytesIO, StringIO
from typing import List, Union, Any, Dict

import pandas as pd
from tqdm import tqdm
from treelib import Tree, Node
from langchain.docstore.document import Document

from loader.unstructured_loaders.loader import FileLoader
from configs.apollo_config import logger
from loader.unstructured_loaders.exc import TextExtractionError
from utils.llm_util import get_num_tokens_from_messages
from configs.model_config import CHUNK_SIZE


class TableLoader(FileLoader):
    DEFAULT_CHUNK_SIZE = 2000
    
    def __init__(self, file_path: str = None, file_stream: BytesIO = None):
        super().__init__(file_path, file_stream)
        self.df = self.read_table()
        self.blocks,self.title = self.table2blocks()
        
    def read_table(self):
        try:
            if self.file_path.lower().endswith(".xlsx") or self.file_path.lower().endswith(
            ".xls"):
                if not self.file_stream:
                    df = pd.read_excel(self.file_path,sheet_name=None)
                else:
                    df = pd.read_excel(self.file_stream,sheet_name=None)
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
            return df
        except Exception as e:
            raise TextExtractionError(f"Failed to extract text from EXCEL/CSV/TSV file: {str(e)}") from e
        
    def table2chilblocks(self, name,df,chunk_size: int = CHUNK_SIZE):
        blocks = []
        
        i,chunk_n = 0,1
        # 缩小chunk size到最小
        while i < len(df):
            i += 1
            chunk_n = len(df) // i
            cur_df = df.iloc[:chunk_n]
            cur_markdown = cur_df.to_markdown(index=False)
            if get_num_tokens_from_messages(content=cur_markdown) <= chunk_size:
                break
            
        for j in range(math.ceil(len(df) / i)):
            cur_df = df.iloc[j*chunk_n:(j+1)*chunk_n]
            if cur_df.empty:
                continue
            block_html = cur_df.to_html(
                index=False, justify="left", classes="mystyle", escape=False
            )

            block_markdown = cur_df.to_markdown(index=False)
            blocks.append({
                "name": name,
                "data": cur_df,
                "style": "table",
                "html": block_html,
                "markdown": block_markdown
            })
        return blocks

    def remove_empty_column_names(self,df):
        columns = df.columns.tolist()
        empty_column_kw = "Unnamed"
        for column in columns:
            if empty_column_kw not in column:
                continue
            df = df.rename(columns={
                column :''
            })
        return df

            
    def table2blocks(self):
        blocks = []
        
        if self.file_path.lower().endswith(".xlsx") or self.file_path.lower().endswith(
            ".xls"):
            for sheet_name,sheet in self.df.items():
                try:
                    sheet = self.df[sheet_name]
                    sheet = sheet.dropna(axis=0,how='all').dropna(axis=1,how='all').fillna("")
                    sheet = self.remove_empty_column_names(df=sheet)
                    sheet_blocks = self.table2chilblocks(
                        name=sheet_name,
                        df=sheet,
                        chunk_size=self.DEFAULT_CHUNK_SIZE
                    )
                    blocks.extend(sheet_blocks)
                    
                except Exception as e:
                    logger.error(f"Failed to extract text from sheet: {str(e)}")
        if self.file_path.lower().endswith(".csv") or self.file_path.lower().endswith(".tsv"):
            df = self.df.dropna(axis=0,how='all').dropna(axis=1,how='all').fillna("")
            df = self.remove_empty_column_names(df=df)
            blocks = self.table2chilblocks(
                name=None,
                df=df,
                chunk_size=self.DEFAULT_CHUNK_SIZE
            )
        return blocks,self._validate_filename()