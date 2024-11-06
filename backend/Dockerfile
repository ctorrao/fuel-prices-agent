FROM langchain/langgraph-api:3.11

ADD requirements.txt /deps/__outer_fuel-prices-agent/src/requirements.txt
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -r /deps/__outer_fuel-prices-agent/src/requirements.txt

ADD . /deps/__outer_fuel-prices-agent/src
RUN set -ex && \
    for line in '[project]' \
                'name = "fuel-prices-agent"' \
                'version = "0.1"' \
                '[tool.setuptools.package-data]' \
                '"*" = ["**/*"]'; do \
        echo "$line" >> /deps/__outer_fuel-prices-agent/pyproject.toml; \
    done

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

ENV LANGSERVE_GRAPHS='{"agent": "/deps/__outer_fuel-prices-agent/src/agent.py:graph"}'

WORKDIR /deps/__outer_fuel-prices-agent/src