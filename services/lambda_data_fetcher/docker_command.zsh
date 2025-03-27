#!/bin/zsh

# build
docker build --platform linux/amd64 -t backtest-data-fetcher:lambda .

# run
docker run --platform linux/amd64 -p 9000:8080 backtest-data-fetcher:lambda

# リポジトリ作成 (初回のみ)
aws ecr create-repository --repository-name backtest-data-fetcher-repo --region ap-northeast-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

# login
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin 779846785267.dkr.ecr.ap-northeast-1.amazonaws.com

# tag
docker tag backtest-data-fetcher:lambda 779846785267.dkr.ecr.ap-northeast-1.amazonaws.com/backtest-data-fetcher-repo:latest

# push
docker push 779846785267.dkr.ecr.ap-northeast-1.amazonaws.com/backtest-data-fetcher-repo:latest
