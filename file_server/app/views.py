from datetime import datetime
import os
from pathlib import Path
from django.shortcuts import render_to_response
from django.views.generic import TemplateView

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = os.path.join(dir, 'files')


class FileList(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, date: "Date as string" = None, **kwargs) -> "context for template":
        context = super().get_context_data(**kwargs)
        server_files = []
        for file in os.listdir(files):
            file_stats = os.stat(os.path.join(files, file))
            file_info = {
                'name': file,
                'ctime': datetime.fromtimestamp(file_stats.st_ctime),
                'mtime': datetime.fromtimestamp(file_stats.st_mtime),
            }

            if date == None or date[:10] == datetime.fromtimestamp(file_stats.st_ctime).strftime("%Y-%m-%d") \
                    or date[:10] == datetime.fromtimestamp(file_stats.st_mtime).strftime("%Y-%m-%d"):
                server_files.append(file_info)

        context.update({
            'files': server_files,
            'date': date
        })
        return context


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    if name in os.listdir(files):
        content = Path(os.path.join(files, name)).read_text()
        return render_to_response('file_content.html', context={'file_name': name, 'file_content': content})

    else:
        return render_to_response('index.html')