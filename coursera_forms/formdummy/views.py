from django.shortcuts import render
from django.views import View


# Create your views here.
class FormDummyView(View):

    def get(self, request):
        # from pdb import set_trace
        # set_trace()
        hello = request.GET.get('hello')
        print(hello)
        return render(request, 'form.html', {'hello': hello})

    def post(self, request):
        text = request.POST.get('text')
        grade = request.POST.get('grade')
        image = request.FILES.get('image')
        content = image.read()
        context = {
            'text': text,
            'grade': grade,
            'content': content
        }
        print(context)
        return render(request, 'form.html', context)
