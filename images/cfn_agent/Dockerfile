FROM docker:dind

ARG AWSCLI_URL=https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.1.24.zip

RUN apk add --no-cache gcompat curl jq  && rm -rf /var/cache/apk/* 

RUN curl -sL ${AWSCLI_URL} -o awscliv2.zip \
    && unzip -q awscliv2.zip \
    && aws/install \
    && rm -rf \
    awscliv2.zip \
    aws \
    /usr/local/aws-cli/v2/*/dist/aws_completer \
    /usr/local/aws-cli/v2/*/dist/awscli/data/ac.index \
    /usr/local/aws-cli/v2/*/dist/awscli/examples

