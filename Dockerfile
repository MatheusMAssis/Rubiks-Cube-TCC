FROM python:3.7
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt && rm -rf /root/.cache

# local
#RUN python main.py

# cloud
CMD gunicorn main:app --bind 0.0.0.0:$PORT --timeout 36000 --reload --workers=2 --worker-class=gevent --log-level=warning