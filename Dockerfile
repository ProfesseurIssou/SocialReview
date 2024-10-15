FROM python:3.11-slim
ADD requirements.txt /home/requirements.txt
COPY src/. /home/
WORKDIR /home
RUN pip install -r requirements.txt
CMD ["/home/SocialReview.py"]
ENTRYPOINT ["python"]