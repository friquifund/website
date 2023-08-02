# docker build -t scraper .
# docker run scraper python entrypoint_bash.py --task_name task_parse_profiles
FROM python:3.10

# Copy source code
COPY . app/

# Create runs directory (Should be an exposed volume)
RUN mkdir runs
ENV LOG=/runs/log

# Install requirements
WORKDIR /app
RUN pip install -e .