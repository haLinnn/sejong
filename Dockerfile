FROM python:3.10

WORKDIR /usr/src/app

COPY ./ ./

# ADD requirements.txt .

RUN pip install --upgrade pip

# RUN pip install -r requirements.txt

RUN pip install flask
RUN pip install scikit-learn
RUN pip install matplotlib
RUN pip install pandas
RUN pip install pickle-mixin
RUN pip install numpy
RUN pip install konlpy
RUN pip install yellowbrick
RUN pip install flask_cors

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]