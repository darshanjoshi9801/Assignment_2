import zipfile
from aiohttp import web
import jinja2
import aiohttp_jinja2
import os
import aiohttp

app = web.Application()
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "Templates"))
)

async def index(request):
    response = aiohttp_jinja2.render_template("index.html", request, context={})
    return response


async def extract(request):
    data = await request.post()
    zip_file = data['zip_file'].file

    with zipfile.ZipFile(zip_file,'r') as z:
        extracted_files = z.namelist()
        z.extractall(os.path.join(os.getcwd(), "extracted_files"))

        context = {'file_names' : extracted_files, 'file_path' : os.path.join(os.getcwd(), "extracted_files")}
        response = aiohttp_jinja2.render_template("response.html", request, context=context)
        return response

async def handle_download(request):
    file_name = request.match_info.get('file_name')
    file_path = os.path.join(os.getcwd(), "extracted_files", file_name)
    return web.FileResponse(file_path)

app.add_routes([
    web.get('/', index),
    web.post('/extract', extract),
    web.get('/download/{file_name}',handle_download)
])
if __name__ == '__main__':
    web.run_app(app)