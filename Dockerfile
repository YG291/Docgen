FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY lambda_handler.py .
COPY doc_gen.py .
COPY genfunctions.py .
COPY conversion_script.py .
COPY templates/ templates/

CMD [ "lambda_handler.handler" ]