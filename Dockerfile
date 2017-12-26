FROM heroku/miniconda:3

RUN apt-get update

RUN git clone https://github.com/danielperezr88/nmt-chatbot-flask.git && \
    cd nmt-chatbot-flask/model/best_bleu && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/checkpoint && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/hparams && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-16000.meta && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-16000.index && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-16000.data-00000-of-00001 && \
    cd .. && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/checkpoint && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/hparams && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-34000.meta && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-34000.index && \
	wget https://storage.googleapis.com/datasets-hf/reddit-chatbot/2015-05/model/best_bleu/translate.ckpt-34000.data-00000-of-00001

WORKDIR nmt-chatbot-flask

RUN pip install -qr requirements.txt

CMD gunicorn --bind 0.0.0.0:80 nmt-api:app --log-file=gunicorn.log