from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForms
import sys
import os
from subprocess import run,PIPE
from time import gmtime, strftime
import pathlib
from django.template import loader
from django import template
import shutil

def contact(request):

    if request.method == 'POST':
        form = ContactForms(request.POST,request.FILES)
        if form.is_valid():
            return render(request, {'name': form.cleaned_data})

    form = ContactForms()
    return render(request, 'form.html', {'form': form})

def handle_uploaded_file(f):
    temp_path = "".join([os.getcwd(), "/upload/media/"]) + "".join([strftime("%Y%m%d%S", gmtime()), "/"])
    with open(temp_path + str(f).replace(" ", "_"), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def button(request):
    return render(request, 'home.html')



params=None

def Upload(request):
    if request.method == 'POST':
        form = ContactForms(request.POST, request.FILES)
        if form.is_valid():
            temp_path = "".join([os.getcwd(), "/upload/media/"]) + "".join([strftime("%Y%m%d%S",
                                                                                     gmtime()),
                                                                            "/"])
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)
        infofile = []
        markerfile = []
        csvfiles = []
        num_files = 0
        for count, x in enumerate(request.FILES.getlist("files")):
            def process(f):
                with open(temp_path + str(f).replace(" ", "_"), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            process(x)
            num_files += 1
            if pathlib.Path(str(x)).suffix == ".csv":
                csvfiles.append(str(x))
            elif pathlib.Path(str(x)).suffix == ".txt":
                markerfile.append(str(x))
            elif pathlib.Path(str(x)).suffix == ".xlsx":
                infofile.append(str(x))
        global params
        params = {}
        params['inputpath'] = temp_path
        if os.path.exists("".join([temp_path, "".join([form.cleaned_data['clusteringtype'], "_output"])])):
            shutil.rmtree("".join([temp_path, "".join([form.cleaned_data['clusteringtype'], "_output"])]))
        os.mkdir("".join([temp_path, "".join([form.cleaned_data['clusteringtype'], "_output"])]))
        params['outputpath'] = "".join([temp_path, "".join([form.cleaned_data['clusteringtype'], "_output"])])
        params['kvalue'] = form.cleaned_data['kvalue']
        params['markerfile'] = markerfile
        params['analysisname'] = form.cleaned_data['AnalysisName']
        params['thread'] = 2
        params['pheno'] = infofile
        params['clustering'] = form.cleaned_data['clusteringtype']
    return render(request, 'valid.html', {'name': form.cleaned_data,
                                          'infofile': infofile,
                                          'markerfile': markerfile,
                                          'csvfiles': csvfiles,
                                          'num_files': num_files})

def external(request):
    if request.method == 'POST':
        out = run([sys.executable,
                   "/".join([os.getcwd(),
                             "scripts",
                             "cytophenograph.v2_0.py"]),
                   "-i", params["inputpath"],
                   "-o", params["outputpath"],
                   "-k", str(params["kvalue"]),
                   "-m", "".join([params["inputpath"], params["markerfile"][0]]),
                   "-n", params["analysisname"],
                   "-t", str(params["thread"]),
                   "-p", "".join([params["inputpath"], params["pheno"][0]]),
                   "-c", params["clustering"]], shell=False, stdout=PIPE)
        # print(params.get("inputpath"))
    return render(request, 'scriptout.html', {'name': out.stdout,
                                              'cognome': params})


def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('../templates/')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('../templates/page-500.html')
        return HttpResponse(html_template.render(context, request))