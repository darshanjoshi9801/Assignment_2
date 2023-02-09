import zipfile
from aiohttp import web


async def index():
    return web.Response(text=
    """
    <!DOCTYPE html>
    <head>
    <title>Web app for extracting zip files</title>
    </head>
    <body>
    <form action="/extract" enctype="multipart/form-data" method="post">
    <input type="file" name="zip_file">
    <input type="submit">
    </form>
    </body>
    </html>
    """, content_type='text/html')


async def extract(request):
    data = await request.post()
    zip_file = data['zip_file'].file
    with zipfile.ZipFile(zip_file,'r') as z:
        extracted_files = z.namelist()
        html = "<ul>"
        for file in extracted_files:
            html += f"<li><a href='/{file}' download>{file}</a></li>"
        html += "</ul>"
        return web.Response(text=html, content_type="text/html")


app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/extract', extract)
])
if __name__ == '__main__':
    web.run_app(app)