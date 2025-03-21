FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# ローカル開発環境の./srcディレクトリをコンテナ上の/appディレクトリにコピー
COPY ./src ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]
