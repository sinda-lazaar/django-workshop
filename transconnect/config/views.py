from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Welcome to home page</h1>")
def homeWithName(request,nom):
    return HttpResponse(f"Welcome to home page {nom}")