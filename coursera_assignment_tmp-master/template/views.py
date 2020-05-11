from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def echo(request):
    return render(request, 'echo.html', context={
        'st': request.META.get('HTTP_X_PRINT_STATEMENT'),
        'get_dict': request.GET,
        'post_dict': request.POST,
        'meta_dict': request.META
    }, status=200)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })

# def echo(request):
#     return render(request, 'echo.html', context={
#         'name': request.GET.get('name', 1),
#         'test': "Check out www.djangoproject.com",
#         'get': request.GET,
#         'post': request.POST,
#         'meta': request.META
#     })
