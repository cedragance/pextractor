FROM python:3.11.4-slim-buster

RUN apt-get update && apt-get install -y libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

RUN pip install flask python-multipart textract python-pptx xlrd docx2txt PyMuPDF Pillow pydub wave regex

WORKDIR /workdir 
COPY app /workdir/

EXPOSE $PORT

ENTRYPOINT ["python", "-u", "server.py", "serve"]