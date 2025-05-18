#!/bin/bash
docker run -itd -v /rainbow/zhangjunfeng/digital_labor:/app -p 7860:7860 --name digital_labor_test digital_labor:v2.2 /usr/bin/python3 api.py