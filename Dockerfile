FROM heroku/miniconda:3

RUN apt-get update && apt-get install -y \
        python-dev \
        build-essential

RUN git clone https://github.com/danielperezr88/nmt-chatbot-flask.git && \
    mkdir nmt-chatbot-flask/model && mkdir nmt-chatbot-flask/model/best_bleu && cd nmt-chatbot-flask/model/best_bleu && \
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

ADD ./nmt-chatbot-flask /opt/webapp
WORKDIR /opt/webapp

RUN pip install -qr requirements.txt

CMD gunicorn --bind 0.0.0.0:80 web:app --log-file=gunicorn.log