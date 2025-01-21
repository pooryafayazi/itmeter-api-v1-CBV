from django import forms
from .models import PostComment
from accounts.models import Profile

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['profile', 'subject', 'message'] 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostCommentForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
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