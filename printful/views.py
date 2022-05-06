from django.shortcuts import render

# Create your views here.
def main_func(request):
    return render(request, 'printful/index.html')
def hoo(request):
    return render(request, 'printful/hoodie.html')
def jack(request):
    return render(request, 'printful/jacket.html')
def tank(request):
    return  render(request, 'printful/tank.html')
def tee(request):
    return render(request, 'printful/tee.html')