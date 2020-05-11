import re
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET


@require_GET
def index(request):
    return HttpResponse("OK!")


@require_GET
def simple_route(request, suffix):
    if suffix:
        return HttpResponseNotFound()
    return HttpResponse(status=200)


@csrf_exempt
def slug_route(request, suffix):
    # suffix = f"suffix={suffix};len={len(suffix)}"
    # return HttpResponse(content=suffix, status=200)
    match = re.fullmatch(r'^[0-9a-z_-]*$', suffix)
    # return HttpResponse(content=suffix, status=200)
    if match:
        if len(match.group(0)) < 1 or len(match.group(0)) > 16:
            return HttpResponseNotFound()
        else:
            return HttpResponse(content=suffix, status=200)
    else:
        return HttpResponseNotFound()


@csrf_exempt
def sum_route(request, t1, t2):
    summa = str(int(t1) + int(t2))
    return HttpResponse(content=summa, status=200)


@require_GET
def sum_get_method(request):
    try:
        t1 = int(request.GET.get('a'))
        t2 = int(request.GET.get('b'))
    except:
        return HttpResponse(status=400)
    summa = str(t1 + t2)
    return HttpResponse(content=summa, status=200)


@csrf_exempt
@require_POST
def sum_post_method(request):
    try:
        t1 = int(request.POST.get('a'))
        t2 = int(request.POST.get('b'))
    except:
        return HttpResponse(status=400)
    summa = str(t1 + t2)
    return HttpResponse(content=summa, status=200)
