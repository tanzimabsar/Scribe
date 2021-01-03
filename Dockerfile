FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ScribeService /ScribeService/ScribeService

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

CMD ["ls"]

CMD ["uvicorn", "ScribeService.main:app", "--host", "0.0.0.0", "--port", "8000"]