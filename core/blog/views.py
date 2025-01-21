from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView,DetailView,FormView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.http import HttpResponseNotFound
from .forms import PostCommentForm
from .models import Post,PostComment
from accounts.models import Profile


class ActiveUserRequiredMixin(UserPassesTestMixin):
    def test_func(self, *args, **kwargs):
        return self.request.user.is_active
    

class PostListView(ListView):
    model = Post     
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 4
    pordering = ['-created_date']
    def get_queryset(self):
        queryset = Post.objects.filter(status=True)
        return queryset
    


'''    
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_queryset(self): 
        queryset = Post.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.increment_views()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['previous_post'] = Post.objects.filter(created_date__lt=post.created_date, status=True).order_by('-created_date').first()
        context['next_post'] = Post.objects.filter(created_date__gt=post.created_date, status=True).order_by('created_date').first()
        context['post'] = post
        return context
    
class PostCommentView(FormView):
    # model = PostComment
    form_class = PostCommentForm
    template_name = 'blog/post_detail.html' 
    success_url = '/blog/posts.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user 
        return kwargs

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post is None:
            return HttpResponseNotFound("Post not found.")
        comment = form.save(commit=False)
        comment.post = post 
        comment.save() 
        return super().form_valid(form)
   

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.kwargs['pk']})
    
'''    



from django.views import View

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_queryset(self): 
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.increment_views()
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['previous_post'] = Post.objects.filter(created_date__lt=post.created_date, status=True).order_by('-created_date').first()
        context['next_post'] = Post.objects.filter(created_date__gt=post.created_date, status=True).order_by('created_date').first()
        context['post'] = post
        context['form'] = PostCommentForm(user=self.request.user)  # Include the comment form
        context['current_user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()  # Get the current post
        form = PostCommentForm(request.POST, user=request.user)  # Initialize the form with POST data
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Associate the comment with the post
            comment.user = request.user  # Set the user
            comment.save()  # Save the comment
            return redirect(self.get_success_url())  # Redirect after saving
            
        # If form is not valid, render the same template with errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.kwargs['pk']})
    
    
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_single.html'
    fields = ['title','due_date']
    success_url = '/'
    def form_valid(self, form):
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        form.instance.creator = profile_instance
        return super().form_valid(form)
    
    
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_detail.html'
    fields = ['title','due_date']
    context_object_name = 'post'
    success_url = '/'
    def form_valid(self, form):
        profile_instance = get_object_or_404(Profile, user=self.request.user)
        form.instance.creator = profile_instance
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

