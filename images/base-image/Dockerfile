FROM ubuntu
ARG AWSCLI_URL=https://awscli.amazonaws.com/awscli-exe-linux-x86_64-2.1.24.zip

RUN apt-get update \
    && apt-get install jq curl wget ruby python3 python3-pip  -y

# Terramform
RUN wget --quiet https://releases.hashicorp.com/terraform/1.2.5/terraform_1.2.5_linux_386.zip \
  && unzip terraform_1.2.5_linux_386.zip \
  && mv terraform /usr/bin \
  && rm terraform_1.2.5_linux_386.zip

# awscli v2
RUN curl -sL ${AWSCLI_URL} -o awscliv2.zip \
    && unzip -q awscliv2.zip \
    && aws/install \
    && rm -rf \
    awscliv2.zip \
    aws \
    /usr/local/aws-cli/v2/*/dist/aws_completer \
    /usr/local/aws-cli/v2/*/dist/awscli/data/ac.index \
    /usr/local/aws-cli/v2/*/dist/awscli/examples

# checkov
RUN pip3 install checkov

# cfn_nag
RUN gem install cfn-nag

# Snyk
RUN curl https://static.snyk.io/cli/latest/snyk-alpine -o snyk \
    && chmod +x ./snyk \
    && mv ./snyk /usr/local/bin/
