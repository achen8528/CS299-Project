from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from .models import Input, InputForm
from .compute import compute
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
def input(request):
    result = None
          
    if ( request.method == 'POST' ):
        form = InputForm(request.POST, request.FILES)
        form2 = form.save()
        if ( len(request.FILES) > 0 and form.is_valid() ) :
            cfile = request.FILES['csvfile']
            cfilehandle = open(settings.MEDIA_ROOT + "/" + str(form2.csvfile), "r")
            csvstr = ""
            for line in cfilehandle:
                csvstr += (line + "\n")
            cfilehandle.close()
            result = compute(csvstr)
        
        elif ( form2.csvstr != "" and form.is_valid() ):
            result = compute(form2.csvstr)
        else:
            form = InputForm()

    else:
        form = InputForm()
    return render(request, 'predict.html', 
        {'form':form, 
         'result': result,
        })

