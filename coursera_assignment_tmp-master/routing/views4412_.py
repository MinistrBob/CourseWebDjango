from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django import forms


class SumForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()

@require_GET
def simple_route(request, txt):
    if request.method == 'GET' and not txt:
        return HttpResponse("")
    else:
        return HttpResponseNotFound()

@csrf_exempt
def slug_route(request, txt):
    return HttpResponse(txt)

@csrf_exempt
def sum_route(request, a, b):
    return HttpResponse(int(a) + int(b))

@require_GET
def sum_get_method(request):
    try:
        if 'a' in request.GET and request.GET['a'] \
            and 'b' in request.GET and request.GET['b']:
            return HttpResponse(int(request.GET['a']) + int(request.GET['b']))
        else:
            return HttpResponseBadRequest()
    except(KeyError, ValueError):
        return HttpResponseBadRequest()

@require_POST
@csrf_exempt
def sum_post_method(request):
    form = SumForm(request.POST or None)
    if form.is_valid():
        return HttpResponse(form.cleaned_data['a'] + form.cleaned_data['b'])
    else:
        return HttpResponseBadRequest()
