FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ ${LAMBDA_TASK_ROOT}/core/
COPY app/ ${LAMBDA_TASK_ROOT}/app/
COPY deploy/lambda/handler.py ${LAMBDA_TASK_ROOT}/handler.py

CMD ["handler.handler"]
