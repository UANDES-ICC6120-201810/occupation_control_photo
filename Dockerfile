# For ARM architectures use
FROM arm32v7/ubuntu:latest

# For x86 architectures use
# FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
# Important to keep the '-y' to say 'yes' to the prompt or will raise non-zero error.

RUN apt-get update \
    && apt-get install -y python2.7 \
                          python-pip \
                          nano \
                          python-opencv \
    && pip install requests \
                   boto3

CMD python /root/main.py
