# Copyright 2021 andremmfaria
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.13-alpine

WORKDIR /usr/src/app

COPY . .

RUN apk update \
    && apk upgrade \
    && apk add ffmpeg \
    && apk add --no-cache \
        --virtual .builds \
        ca-certificates \
        build-base \
        linux-headers \
        gcc \
        python3-dev \
        libffi-dev

RUN pip install pdm && pdm install 

CMD ["pdm", "run", "kantharos-bot", "> /dev/stdout"]
