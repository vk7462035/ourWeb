from django.shortcuts import render
from .models import Articles
from django.views.generic import DetailView

def blog_home(request):
    blog = Articles.objects.order_by('-date')
    return render(request, 'main/blog.html', {'blog': blog})

class BlogDetailView(DetailView):
    model = Articles
    template_name = 'main/details_view.html'
    context_object_name = 'article'

def blog_1(request):
    return render(request, 'main/details_view.html')
