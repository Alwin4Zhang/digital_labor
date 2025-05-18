import io
import os
import requests
import logging
import base64
import string
import subprocess
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
import sys
import platform
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from tqdm import tqdm

sys.path.append("./")

from db.models.enum import DocumentType
from utils.string_util import broken_lines
from configs.apollo_config import logger,OCR_URL

from utils.minio_util import upload_base64image,get_presiged_url




system_name = sys.platform

CMD = "libreoffice"

if system_name == "darwin":
    CMD = "soffice"




def timeit(method):
    """方法执行时间装饰器"""

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        elapsed = te - ts
        logger.info("%r done at %2.2f ms" % (method.__name__, elapsed * 1000))
        return result

    return timed

def get_file_type(file_name):
    file_type = None
    if file_name.lower().endswith(".docx") or file_name.lower().endswith(".doc"):
        file_type = DocumentType.WORD
    elif file_name.lower().endswith(".pdf"):
        file_type = DocumentType.PDF
    elif file_name.lower().endswith(".pptx"):
        file_type = DocumentType.PPT
    elif (
        file_name.lower().endswith(".xlsx")
        or file_name.lower().endswith(".xls")
        or file_name.lower().endswith(".csv")
        or file_name.lower().endswith(".tsv")
    ):
        file_type = DocumentType.EXCEL
    return file_type


@timeit
def upload_file(
    file_name: str = None,
    base64image = None
):
    try:
        upload_base64image(base64img=base64image,object_name=file_name)
        url = get_presiged_url(
            object_name=file_name
        )
        return url
    except Exception as e:
        logger.error("upload file error:" + e)


def convert_file_to_base64(file_path):
    """将文件转换为base64 data"""
    with open(file_path, "rb") as rf:
        file_buffer = rf.read()
    return base64.b64encode(file_buffer)


def convert_base64_to_buffer(b64_data):
    """将base64 data转换为buffer io"""
    try:
        return base64.b64decode(b64_data)
    except Exception as e:
        print(e)


def convert_bytes_to_file(bytes_data: io.BytesIO = None, file_path: str = None):
    """将bytes保存文件"""
    with open(file_path, "wb") as wf:
        wf.write(bytes_data.getbuffer())


def convert_text_to_multilines(text):
    """将1,2,3,4,5开头的文本换行显示"""
    lines = broken_lines(text)
    return "\n".join([line.lower() for line in lines])


def pt2px(pt):
    """pt转为px"""
    return (96 / 72) * pt


def pt2em(pt):
    "1em = 12pt = 16px = 100%"
    return pt / 12


def convert_file_type(doc_path, target_format, output_directory: str = None):
    """转换数据格式
    如：将doc转为docx,将ppt转为pptx
    依赖于liboffice
    ubuntu: apt-get install libreoffice -y
    apt-get install libreoffice-l10n-zh-cn libreoffice-help-zh-cn

    centos:
    yum install -y libreoffice
    yum install -y libreoffice-headless
    """
    if not output_directory:
        output_directory = os.path.dirname(doc_path)
    subprocess.call(
        [
            CMD,
            "--headless",
            "--convert-to",
            target_format,
            "--outdir",
            output_directory,
            doc_path,
        ]
    )

    doc_abs_path = os.path.abspath(doc_path)
    # 兼容两种形式，一个是传文件名，一个是传文件路径
    doc_path_prefix = doc_abs_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    new_file_path = os.path.join(
        os.path.abspath(output_directory), doc_path_prefix + "." + target_format
    )
    if os.path.exists(new_file_path):
        return new_file_path


def convert_flowchart(wmf_path, target_format, output_directory: str = None):
    """转换数据格式
    如：将wmf visio图转为png
    """
    if not output_directory:
        output_directory = os.path.dirname(wmf_path)
    subprocess.call(
        [
            CMD,
            "--headless",
            "--convert-to",
            target_format,
            wmf_path,
            "--outdir",
            output_directory,
        ]
    )

    path_prefix = wmf_path.rsplit(".", 1)[0]
    new_file_path = os.path.join(
        os.path.abspath(output_directory), path_prefix + "." + target_format
    )
    if os.path.exists(new_file_path):
        return new_file_path


def save_bfile(file_path, stream):
    """保存二进制文件"""
    with open(file_path, "wb") as wf:
        wf.write(stream)
    return os.path.getsize(file_path) > 0


def crop_image(image_path):
    """裁剪图片"""
    image_array = cv2.imread(image_path)

    row, col = image_array.shape[0], image_array.shape[1]
    x_left, x_top, x_right, x_bottom = row, col, 0, 0

    for r in range(row):
        for c in range(col):
            if (
                image_array[r][c][0] < 255 and image_array[r][c][0] != 0
            ):  # 外框有个黑色边框，增加条件判断
                if x_top > r:
                    x_top = r  # 获取最小x_top
                if x_bottom < r:
                    x_bottom = r  # 获取最大x_bottom
                if x_left > c:
                    x_left = c  # 获取最小x_left
                if x_right < c:
                    x_right = c  # 获取最大x_right

    cropped_image = image_array[x_top - 5 : x_bottom + 5, x_left - 5 : x_right + 5]
    return cropped_image


def PIL_image_to_base64(img):
    # img = Image.open(image_path)
    output_buffer = BytesIO()
    img.save(output_buffer, format="PNG")
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    return base64_data


def thread_parallel(func, args_list, max_workers=4):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as exec:
        all_tasks = [exec.submit(func, *args) for args in args_list]
        for future in tqdm(as_completed(all_tasks)):
            results.append(future.result())
    return results


def ocr_api(base64image):
    try:
        body = {
            "value": [
                base64image
            ],
            "key": [
                "image"
            ]
        }
        resp = requests.post(OCR_URL,json=body)
        if resp.status_code == 200:
            err_no = resp.json().get("err_no")
            if err_no == 0:
                value = resp.json()['value']
                if isinstance(value,list):
                    return "\n".join([bbox[0][0] for bbox in eval(value[0])])
    except Exception as e:
        logger.error(e)
    return ""


if __name__ == "__main__":
    f = "/Users/ucdteam/rainbow/test/test.png"
    # crop_image(f)

    # def process_parallel(func, args_list, max_workers=2):
    #     results = []
    #     with ProcessPoolExecutor(max_workers=max_workers) as exec:
    #         all_tasks = [exec.submit(func, *args) for args in args_list]
    #         for future in tqdm(as_completed(all_tasks)):
    #             results.append(future.result())
    #     return results

    def test(a, b):
        return a + b

    # args_list = [(1, 2), (3, 4), (5, 6), (7, 8), (1, 3), (3, 5), (5, 9), (7, 90)]
    # results = thread_parallel(test, args_list)
    # # results = process_parallel(test, args_list)
    # print(results)

    