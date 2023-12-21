FROM python:3.12-alpine

RUN apk add --no-cache ffmpeg

ENV DLHDHR_HOST=0.0.0.0
ENV DLHDHR_PORT=8000

WORKDIR /app/
COPY . /app/
RUN pip install .

EXPOSE 8000
CMD ["python", "-m", "dlhdhr"]
