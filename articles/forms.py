from django import forms


class AddCommentForm(forms.Form):
    comment_text = forms.Textarea()
