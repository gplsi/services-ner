FROM python:3.8-bullseye
WORKDIR /app
RUN apt-get update
RUN apt-get install -y supervisor nginx nano less curl g++ protobuf-compiler libprotobuf-dev
RUN adduser --disabled-password --gecos 'www' www
RUN { \
      echo 'pip-licenses==4.0.1'; \
      echo 'gunicorn==20.1.0'; \
      echo 'flask==2.2.2'; \
	  echo 'Werkzeug==2.3.7'; \
      echo 'mariadb==1.0.6'; \
      echo 'elasticsearch==8.4.1'; \
      echo 'regex'; \
      echo 'pycld3==0.22'; \
      echo 'scikit-learn==1.0.2'; \
      echo 'superlance==2.0.0'; \
      echo 'pyyaml==6.0'; \
      echo 'jsonpatch==1.32'; \
      echo 'requests==2.28.1'; \
      echo 'spacy==3.4.2'; \
      echo 'spacyopentapioca==0.1.6'; \
      echo 'flair==0.11.3'; \
      echo 'transformers==4.22.0'; \
      echo 'cachetools==5.2.0'; \
      echo 'types-cachetools==5.2.1'; \
    } > /app/requirements.txt \
 && pip install pip \
 && pip install -r /app/requirements.txt \
 && rm -rf /app/requirements.txt

# download spacy models
RUN python -m spacy download es_core_news_lg
RUN python -m spacy download es_core_news_md
RUN python -m spacy download es_core_news_sm
RUN python -m spacy download en_core_web_lg

#ENV SERVER_WORKERS=2
#ENV SERVER_THREADS=2
#ENV EMAIL_ACCOUNT=admin@example.com
EXPOSE 9000

#RUN pip install classy-classification==0.4.5
#RUN pip install bertopic[spacy]