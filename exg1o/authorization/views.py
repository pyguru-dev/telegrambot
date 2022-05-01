from django.shortcuts import render

# Create your views here.
def authorization(request):
	return render(request, 'authorization.html')