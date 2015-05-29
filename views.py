from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
#def hello(request):
#    return HttpResponse("Hello world")

def search_form(request):
    return render(request, 'search_form.html')


#TEST VIEWS
def test(request):
    return render(request, 'test.html')


def test_function(request):

    dataset = ManualiResources().export()
    print(dataset.csv)

    return render(request, 'test.html', {'error': True})