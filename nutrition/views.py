from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Nutrient, Nutrition_table
from .forms import NutritionData

def AllProduct(request):
    number_available = len(Nutrition_table.objects.all())
    counter = 1
    id = []
    product_name = []
    while counter <= number_available:
        nt_object = Nutrition_table.objects.get(id=counter)
        id.append(nt_object.id)
        product_name.append(nt_object.Product)
        counter += 1
        output = zip(id, product_name)
    form = NutritionData
    return render(request, 'all_product.html', {'output': output, 'form': form})

def product(request):
    if 'txtSearch' and 'searchBy' in request.GET:
        txtSearch = request.GET.get('txtSearch')
        searchBy = request.GET.get('searchBy')
        if txtSearch == "":
            return HttpResponse('Please enter a product name', status=404)
        product_id = Nutrition_table.objects.get(Product=txtSearch).id
        product_name = Nutrition_table.objects.get(id=product_id)
        nt_object = Nutrition_table.objects.filter(id=product_id).values()
        for i in nt_object:
            nt_object_dict = i

            return render(request, 'product_nutrient.html', {'nt_object': nt_object_dict.items(), 'product_name': product_name})

    else:
        if 'txt' in request.GET:
            txt = request.GET.get('txt')
            product_id = Nutrition_table.objects.get(Product=txt).id
            product_name = Nutrition_table.objects.get(id=product_id)
            nt_object = Nutrition_table.objects.filter(id=product_id).values()
            for i in nt_object:
                nt_object_dict = i
                return render(request, 'product_nutrient.html',
                              {'nt_object': nt_object_dict.items(), 'product_name': product_name})

        return HttpResponse('Product Not Found', status=404)
def livesearch(request):
    if 'term' and 'searchBy' in request.GET:
        searchBy = request.GET.get('searchBy')
        q = request.GET.get('term')
        results = []
        if searchBy == 'product':
            search_qs = Nutrition_table.objects.filter(Product__startswith=q)
            for r in search_qs:
                results.append(r.Product)
        elif searchBy == 'nutrient':
            search_qs = Nutrient.objects.filter(NutrientName__startswith=q)
            for r in search_qs:
                results.append(r.NutrientName)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def nutrient(request):
    return render(request, 'abc.html')
