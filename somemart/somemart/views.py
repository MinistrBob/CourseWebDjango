import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django import forms
from .models import Item, Review
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        # print(request.body)
        form = ItemForm(request.POST)
        # print(request.body)
        if form.is_valid():
            # print("form valid")
            data = form.cleaned_data
            # print(data)
            item = Item(title=data['title'], description=data['description'], price=data['price'])
            item.save()
            # print(item.id)
            data = {"id": item.id}
            return JsonResponse(data, status=201)
        else:
            # print("form is not valid")
            return JsonResponse({"error": "Request not valid"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        # print(item_id)
        # print(request.body)
        form = ReviewForm(request.POST)
        if form.is_valid():
            # print("form valid")
            data = form.cleaned_data
            try:
                item = Item.objects.get(id=item_id)
            except:
                return JsonResponse({"error": "item does not exist"}, status=404)
            review = Review(grade=data['grade'], text=data['text'], item=item)
            review.save()
            # print(item.id)
            data = {"id": review.id}
            return JsonResponse(data, status=201)
        else:
            # print("form is not valid")
            return JsonResponse({"error": "Request not valid"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # print(item_id)
        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "item does not exist"}, status=404)
        reviews_list = []
        try:
            # print(dir(item))
            reviews = item.review_set.all().order_by('-id')[0:5]
            # print(reviews)
            if reviews:
                for rev in reviews:
                    rev_dict = model_to_dict(rev)
                    reviews_list.append(rev_dict)
        except ObjectDoesNotExist:
            pass
        # data = json.dumps(item)
        data = model_to_dict(item)
        data["reviews"] = reviews_list
        return JsonResponse(data, status=200)


class ItemForm(forms.Form):
    """Форма товара."""
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    """Форма отзыва о товаре."""
    grade = forms.IntegerField(min_value=1, max_value=10)
    text = forms.CharField(max_length=1024)
