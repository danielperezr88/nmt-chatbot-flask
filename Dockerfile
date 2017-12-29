FROM heroku/miniconda:3

RUN apt-get update && apt-get install -y \
        python-dev \
        build-essential

RUN mkdir /opt/webapp

WORKDIR /opt/webapp

# Deploy from local environment
#ADD ./browser /opt/webapp/browser
#ADD ./model /opt/webapp/model
#ADD ./setup /opt/webapp/setup
#ADD ./data /opt/webapp/data
#ADD ./core /opt/webapp/core
#ADD ./nmt /opt/webapp/nmt
#ADD ./requirements.txt /opt/webapp/requirements.txt
#ADD ./scoring.py /opt/webapp/scoring.py
#ADD ./utils.py /opt/webapp/utils.py
#ADD ./model.py /opt/webapp/model.py
#ADD ./web.py /opt/webapp/web.py

# Deploy from anywhere else
RUN git clone https://github.com/danielperezr88/nmt-chatbot-flask.git . && \
    mkdir model && mkdir model/best_bleu && cd model/best_bleu && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/checkpoint && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/hparams && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-16000.meta && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-16000.index && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-16000.data-00000-of-00001 && \
    cd .. && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/checkpoint && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/hparams && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/translate.ckpt-34000.meta && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/translate.ckpt-34000.index && \
    wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/translate.ckpt-34000.data-00000-of-00001

RUN pip install -qr requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT web:app --log-file=gunicorn.log --timeout 120 --worker-class gevent
