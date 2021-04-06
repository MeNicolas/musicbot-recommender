FROM python:3.8
RUN pip install flask numpy scipy wget
#ADD https://nicod.s3.fr-par.scw.cloud/dataset.pkl ./data/dataset.pkl
#ADD https://nicod.s3.fr-par.scw.cloud/mat.pkl ./data/mat.pkl
COPY main.py ./app/main.py
RUN mkdir -p ./data
EXPOSE 80
CMD python ./app/main.py
