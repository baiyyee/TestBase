FROM hehuabo/wetest:latest

RUN mkdir -p /home/test/TestBase
WORKDIR /home/test/TestBase
ADD . /home/test/TestBase

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run.sh
CMD ["./run.sh"]

EXPOSE 8080