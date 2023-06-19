FROM python:3.8

# INSTALL HEAVY LIBS
RUN pip install torch==1.10.2 transformers==4.16.2
RUN python -c 'from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment"); AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")'


# COPY SOURCE CODE AND SET WORKDIR
COPY . /home
WORKDIR /home

# INSTALL LIB
ADD requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ARG RAILWAY_ENVIRONMENT
ENV RAILWAY_ENVIRONMENT=production

# RUN
EXPOSE 80
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]