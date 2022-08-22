FROM hehuabo/wetest:latest

RUN mkdir -p /home/test/OneStep
WORKDIR /home/test/OneStep
ADD . /home/test/OneStep

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x run.sh
CMD ["./run.sh"]

EXPOSE 8080