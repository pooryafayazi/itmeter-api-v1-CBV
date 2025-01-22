from django import forms
from .models import PostComment,Post
from accounts.models import Profile

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['profile', 'subject', 'message'] 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostCommentForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated: # check if user is authenticated
            try:
                profile = user.profile 
                self.fields['profile'].initial = profile 
                self.fields['profile'].widget.attrs['readonly'] = True 
            except Profile.DoesNotExist:
                pass 

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.cleaned_data.get('profile'):
            comment.user = self.cleaned_data['profile'].user 
        if commit:
            comment.save()
        return comment
    
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'title', 'topic', 'content', 'tags', 'category', 'status', 'login_require', 'published_date']
        widgets = {
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:  # Handle the case where no image is uploaded
            return None
        return image