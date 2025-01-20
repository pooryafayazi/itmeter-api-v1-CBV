from django.shortcuts import redirect, get_object_or_404

from django.views.generic import ListView, CreateView,UpdateView,DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from .models import Post

from django.views.generic import ListView

from accounts.models import Profile


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self, *args, **kwargs):
        return self.request.user.is_active

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 4
    

    def get_queryset(self):        
        # queryset = Task.objects.all()  
        # profile_instance = get_object_or_404(Profile, user=self.request.user)
        # queryset = Task.objects.filter(user=self.request.user)  
        queryset = Post.objects.filter(status=True)
        # filter_value = self.request.GET.get('filter')
        # sort_value = self.request.GET.get('sort')
        # filter_value = self.request.GET.get('filter')
        # sort_value = self.request.GET.get('sort')
        # if filter_value == '1':
        #      queryset = queryset.filter(title__isnull=False)
        # elif filter_value == '2':
        #     queryset = queryset.filter(complete=True)
        # elif filter_value == '3':
        #     queryset = queryset.filter(active=True)
        # elif filter_value == '4':
        #     queryset = queryset.filter(due_date__isnull=False)


        # if sort_value == '2':  
        #     queryset = queryset.order_by('due_date')
        # else: 
            # queryset = queryset.order_by('-created_date')

        return queryset
    
   
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_list.html'
    fields = ['title','due_date']
    success_url = '/'
    def form_valid(self, form):
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        form.instance.creator = profile_instance
        # form.instance.user = self.request.user
        return super().form_valid(form)
    
    
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_detail.html'
    fields = ['title','due_date']
    context_object_name = 'post'
    # form_class = TaskForm i didnt create TaskForm
    success_url = '/'
    def form_valid(self, form):
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        form.instance.creator = profile_instance
        # form.instance.user = self.request.user
        return super().form_valid(form)


class PostCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Post, pk=pk)
        task.complete = not task.complete
        task.active = not task.active
        task.save()
        return redirect('blog:list_view')
    
    
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    context_object_name = "post"
    success_url = '/'

