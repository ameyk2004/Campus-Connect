from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'index.html')

def keep_alive(request):
    return JsonResponse({"status" : "success"})