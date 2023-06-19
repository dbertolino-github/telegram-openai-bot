FROM python:3.8

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
EXPOSE 443
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]