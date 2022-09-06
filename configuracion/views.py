from django.shortcuts import render,redirect
import sweetify
from configuracion.forms import ConfigEmailForm
from configuracion.models import ConfigEmail
from django.contrib.auth.decorators import login_required

# Create your views here.




@login_required
def add_confemail(request,id=0):
    
    if request.method == "GET":
            if id == 0 :
                form = ConfigEmailForm()
            else:
                email = ConfigEmail.objects.get(pk=id)

                form = ConfigEmailForm(instance=email)
            return render(request, 'configuracion/confi_email.html', {'form': form})
    else:
            if id == 0:
                form = ConfigEmailForm(request.POST)
            else:
                email = ConfigEmail.objects.get(pk=id)
                form = ConfigEmailForm(request.POST,instance= email)
            if form.is_valid():
                    form.save()
                    sweetify.success(request, 'Exito', text='Apagado Correctamente', persistent='Aceptar')
            return redirect('/home/')
        
        
        