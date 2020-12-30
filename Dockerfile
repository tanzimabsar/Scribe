FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ScribeService /ScribeService

CMD ["uvicorn", "ScribeService.main:app", "--host", "0.0.0.0", "--port", "80"]