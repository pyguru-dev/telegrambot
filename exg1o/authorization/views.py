from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

# Create your views here.
def authorization(request):
	return render(request, 'authorization.html')

@csrf_exempt
def authorize_in_account(request):
	data = json.loads(request.body)
	print(data)