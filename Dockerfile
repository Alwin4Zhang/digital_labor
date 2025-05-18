FROM rec-docker-hub.tianhong.cn/aigc/python:3.8.20-slim-libreoffice24

#定义时区参数
ENV TZ=Asia/Shanghai
#设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone

MAINTAINER "lingzhi"

WORKDIR /usr/src/app

COPY . .

# RUN apt-get install -y git

RUN pip install --user --no-cache-dir -r requirements.txt -i http://nexus.tianhong.cn/repository/pypi/simple --trusted-host nexus.tianhong.cn
RUN pip install pdf2docx-0.5.7a2-py3-none-any.whl -i http://nexus.tianhong.cn/repository/pypi/simple --trusted-host nexus.tianhong.cn --force-reinstall
# RUN pip install git+http://code.lingzhi.com/bifrost/ai/llm/pdf2docx.git

CMD ["python3", "api.py"]