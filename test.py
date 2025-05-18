import os
import fitz
import logging
from io import BytesIO
from pdf2docx import Converter
from pdf2docx.page.Pages import Pages
from time import perf_counter
from multiprocessing import Pool, cpu_count

from typing import AnyStr, IO, Union

# logging
logging.basicConfig(
    level=logging.INFO, 
    format="[%(levelname)s] %(message)s")

class ConversionException(Exception): 
    pass

class MakedocxException(ConversionException): 
    pass


class CustomConverter(Converter):
    def __init__(
        self, pdf_file: str = None, file_stream: BytesIO = None, password: str = None
    ):
        self.filename_pdf = pdf_file
        self.password = str(password or "")
        self._fitz_doc = None
        if pdf_file is not None and os.path.exists(pdf_file):
            self._fitz_doc = fitz.Document(pdf_file)
        if file_stream is not None:
            self._fitz_doc = fitz.Document(stream=file_stream, filetype="pdf")
        # initialize empty pages container
        self._pages = Pages()

    def convert(self, docx_filename: Union[str, IO[AnyStr]] = None, start: int = 0, end: int = None, pages: list = None,
                **kwargs):
        """Convert specified PDF pages
        """
        t0 = perf_counter()
        logging.info('Start to convert %s', self.filename_pdf)
        settings = self.default_settings
        settings.update(kwargs)
        if pages and settings['multi_processing']:
            raise ConversionException('Multi-processing works for continuous pages '
                                    'specified by "start" and "end" only.')
        # convert page by page
        if settings['multi_processing']:
            self._convert_with_multi_processing(docx_filename,start, end, **settings)
        else:
            self.parse(start, end, pages, **settings)

        logging.info('Terminated in %.2fs.', perf_counter()-t0)    

    def _convert_with_multi_processing(self, docx_filename,start: int, end: int, **kwargs):
        '''Parse and create pages based on page indexes with multi-processing
        Reference:

            https://pymupdf.readthedocs.io/en/latest/faq.html#multiprocessing
        '''
        # make vectors of arguments for the processes
        cpu = min(kwargs['cpu_count'], cpu_count()) if kwargs['cpu_count'] else cpu_count()  
        prefix = 'pages' 
        vectors = [(i, cpu, start, end, self.filename_pdf, self.password, 
                            kwargs, f'{prefix}-{i}.json') for i in range(cpu)]
        # start parsing processes
        pool = Pool()
        pool.map(self._parse_pages_per_cpu, vectors, 1)

        # restore parsed page data
        for i in range(cpu):
            filename = f'{prefix}-{i}.json'
            if not os.path.exists(filename): continue            
            self.deserialize(filename)
            os.remove(filename)


    @staticmethod
    def _parse_pages_per_cpu(vector):
        '''Render a page range of a document.
        
        Args:
            vector (list): A list containing required parameters.
                * 0  : segment number for current process                
                * 1  : count of CPUs
                * 2,3: whole pages range to process
                * 4  : pdf filename
                * 5  : password for encrypted pdf
                * 6  : configuration parameters
                * 7  : json filename storing parsed results
        '''
        # recreate the arguments
        idx, cpu, s, e, pdf_filename, password, kwargs, json_filename = vector

        # open pdf to get page count: all pages are marked to parse temporarily 
        # since don't know which pages to parse for this moment
        cv = Converter(pdf_filename, password)
        cv.load_pages()

        # the specified pages to process
        e = e or len(cv.fitz_doc)
        all_indexes = range(s, e)
        num_pages = len(all_indexes)

        # page segment processed by this cpu
        m = int(num_pages/cpu)
        n = num_pages % cpu
        seg_size = m + int(idx<n)
        seg_from = (m+1)*idx + min(n-idx, 0)
        seg_to = min(seg_from + seg_size, num_pages)
        page_indexes = [all_indexes[i] for i in range(seg_from, seg_to)]

        # now, mark the right pages
        for page in cv.pages: page.skip_parsing = True
        for i in page_indexes: 
            cv.pages[i].skip_parsing = False
        
        # parse pages and serialize data for further processing
        cv.parse_document(**kwargs).parse_pages(**kwargs).serialize(json_filename)
        cv.close()

if __name__ == "__main__":
    file_path =  "/Users/ucdteam/Downloads/解析失败文件/THSY-2024-02天虹股份在营商业项目EHS评估综合报告-吉安天虹.pdf"
    import time
    start = time.time()
    convertor = CustomConverter(
        pdf_file=file_path, file_stream=None
    )
    default_settings = convertor.default_settings
    # convertor.parse(**default_settings)

    convertor.convert(
        file_path,multi_processing=True
    )
    print(time.time() - start)
    blocks = []
    for page in convertor._pages:
        for section in page.sections:
            # section_store = section.store()
            blks = section.store()["columns"][0]["blocks"]
            # 添加page页面的section属性 方便计算每个block在页面的位置
            x0, x1, y0, y1 = (
                section.bbox.x0,
                section.bbox.x1,
                section.bbox.y0,
                section.bbox.y1,
            )
            for blk in blks:
                blk.setdefault("section_bbox", (x0, y0, x1, y1))
            blocks.extend(blks)
    for blk in blocks:
        print(blk)
    print(time.time() - start)