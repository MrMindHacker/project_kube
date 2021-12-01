from python:3.8.10-slim
COPY hello.py hello.py
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt
ENTRYPOINT [ "python", "hello.py" ]