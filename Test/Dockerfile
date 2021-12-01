from python:3.8.10-slim
COPY test.py test.py
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt
ENTRYPOINT [ "python3", "-m", "pytest", "test.py" ]