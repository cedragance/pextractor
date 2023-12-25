-----------------------------------------------------
Local run
-----------------------------------------------------
docker system prune --all
docker build -t pextractor .
docker run -t -p 8088:8088 -e PORT=8088 --restart unless-stopped pextractor . > pextractor.log 2>&1 &
-----------------------------------------------------

-----------------------------------------------------
File types
-----------------------------------------------------
.csv
.doc
.docx
.eml
.epub
.gif
.jpg and .jpeg
.json
.html and .htm
.msg
.odt
.pdf
.png
.pptx
.ps
.rtf
.tiff and .tif
.txt
.xlsx
.xls
-----------------------------------------------------

-----------------------------------------------------
Endpoints
-----------------------------------------------------
POST: http://host:port/extract-text
Request:
Content-Length: 21952204
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarywLXApRKMl9UkaGE4
Content-Disposition: form-data; name="upload_file"; filename="Effective Java (Joshua Bloch).pdf"
Content-Type: application/pdf

Response:
Content-Length: 889813
Content-Type: text/plain; charset=utf-8

POST: http://host:port/extract-pdf-images
Request:
Content-Length: 21952204
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarywsoNOJqWqMiB8rm7
Content-Disposition: form-data; name="upload_file"; filename="Effective Java (Joshua Bloch).pdf"
Content-Type: application/pdf

Response:
Content-Type: application/json
Content-Length: 11017
["$tmp$tmpg72kicxg.jpeg","$tmp$tmpev9p71mo.jpeg"]

GET: http://host:port/download-pdf-images?file_location=$tmp$tmpev9p71mo.jpeg
Request:... query parameter file_location= ...

Response:
Content-Disposition: attachment; filename="tmpev9p71mo.jpeg"
Content-Type: application/octet-stream
Content-Length: 2310
-----------------------------------------------------

