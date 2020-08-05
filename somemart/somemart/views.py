import json

from django.http import HttpResponse, JsonResponse
from django.views import View
from django import forms
from .models import Item, Review
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            body_data = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse({"error": "Request not valid"}, status=400)
        # print(f"body={body_data}")
        try:
            if isinstance(body_data['title'], int):
                return JsonResponse({"error": "Request not valid"}, status=400)
        except:
            return JsonResponse({"error": "Request not valid"}, status=400)
        try:
            if isinstance(body_data['description'], int):
                return JsonResponse({"error": "Request not valid"}, status=400)
        except:
            return JsonResponse({"error": "Request not valid"}, status=400)
        form = ItemForm(body_data)
        # import pdb; pdb.set_trace()
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
        try:
            body_data = json.loads(request.body.decode('utf-8'))
        except:
            return JsonResponse({"error": "Request not valid"}, status=400)
        try:
            if isinstance(body_data['text'], int):
                return JsonResponse({"error": "Request not valid"}, status=400)
        except:
            return JsonResponse({"error": "Request not valid"}, status=400)
        form = ReviewForm(body_data)
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


# def validate_number(value):
#     print("validator work")
#     print(value)
#     print(type(value))
#     if isinstance(value, int):
#         raise ValidationError("Title is charfield")


class ItemForm(forms.Form):
    """Форма товара."""
    title = forms.CharField(max_length=64)
    # title = forms.CharField(max_length=64, validators=[validate_number])
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    """Форма отзыва о товаре."""
    grade = forms.IntegerField(min_value=1, max_value=10)
    text = forms.CharField(max_length=1024)
