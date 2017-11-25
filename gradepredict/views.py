from django.shortcuts import render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from .models import Input, InputForm
from .compute import compute
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
import numpy as np

# Create your views here.
def input(request):
    result = None
          
    if ( request.method == 'POST' ):
        form = InputForm(request.POST, request.FILES)
        form2 = form.save()
        training_X = [0,0]
        training_y = [0]
        userTestVals = []

        if ( len(request.FILES) > 0 and form.is_valid() ) :
            # pull data from csv file

            with open(settings.MEDIA_ROOT + "/" + str(form2.csvfile), 'r') as grades:
                reader = csv.reader(grades)
                for row in reader:
                    if row[2] == '':
                        userTestVals = [float(row[0]), float(row[1])]
                    else:   
                        newrow = [float(row[0]), float(row[1])]
                        training_X = np.vstack([training_X, newrow])
                        training_y = np.vstack([training_y, float(row[2])])
                
            training_X = np.delete(training_X, 0, 0)
            training_y = np.delete(training_y, 0, 0)

            result = compute(training_X, training_y, userTestVals)
        
        elif ( form2.csvstr != "" and form.is_valid() ):
            lines = form2.csvstr.split("\n")
            for line in lines:
                row = line.split(',')
                if row[2] == '':
                    userTestVals = [float(row[0]), float(row[1])]
                else:   
                    newrow = [float(row[0]), float(row[1])]
                    training_X = np.vstack([training_X, newrow])
                    training_y = np.vstack([training_y, float(row[2])])
            training_X = np.delete(training_X, 0, 0)
            training_y = np.delete(training_y, 0, 0)
            result = compute(training_X, training_y, userTestVals)

        else:
            form = InputForm()

    else:
        form = InputForm()
    return render(request, 'predict.html', 
        {'form':form, 
         'result': result,
        })

