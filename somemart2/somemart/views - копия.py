import json
import pprint
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django import forms
from .models import Item, Review
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from base64 import b64decode
from django.contrib.auth import authenticate

pp = pprint.PrettyPrinter(indent=4)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        # print(request.user)
        # print(f"request={dir(request)}")
        # print(f"request.body={request.body}")
        # print(f"content_param={request.content_params}")
        # print(f"METE={pp.pprint(request.META)}")

        raw_login = request.META['HTTP_AUTHORIZATION'].split()[1]
        # print(f"raw_login={raw_login}")
        raw_login2 = b64decode(raw_login.encode('ascii')).decode('ascii')
        # print(f"raw_login2={raw_login2}")
        login = raw_login2.split(":")[0]
        password = raw_login2.split(":")[1]
        print(f"login={login}; password={password}")
        user = authenticate(username=login, password=password)
        print(f"user={user}")
        print(f"user.staff={user.is_staff}")
        if user is not None:
            if user.is_staff:
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
                    print(item.id)
                    data = {"id": item.id}
                    return JsonResponse(data, status=201)
                else:
                    # print("form is not valid")
                    return JsonResponse({"error": "Request not valid"}, status=400)
            else:
                return JsonResponse({}, status=403)
        else:
            return JsonResponse({}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(LoginRequiredMixin, View):
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
class GetItemView(LoginRequiredMixin, View):
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
    # title = forms.CharField(max_length=64, validators=[validate_number])
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    """Форма отзыва о товаре."""
    grade = forms.IntegerField(min_value=1, max_value=10)
    text = forms.CharField(max_length=1024)
