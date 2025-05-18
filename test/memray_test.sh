#!/bin/bash
# 1.生成bin 文件
python3 -m memray run my_script.py

# 查看图
memray flamegraph test/test_parser/memray-test_parser.py.16469.bin

# 实时查看内存使用图
python3 -m memray run --live my_script.py