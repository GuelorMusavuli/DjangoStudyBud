# Class based representation of the form
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):

    class Meta():

        model = Room
        fields = '__all__' # create the form based on the fields in the model

        # # Add form widgets to be linked with fields in the PostForm and give
        # # them a different styling by connecting them to CSS styling, for e.g, give a textarea a medium-editor style
        # # from the medium-editor-textarea class as well as applying styles from
        # # our own css classes(in this case : textinputclass and postcontent)
        # widgets = {
        #     'title' : forms.TextInput(attrs={'class':'textinputclass'}),
        #     'body': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        # }

#
# class CommentForm(forms.ModelForm):
#
#     class Meta():
#         model = Comment
#         fields = ('author', 'body')
#
#         #Add form widgets and connect them to CSS styling.
#         widgets = {
#             'author' : forms.TextInput(attrs={'class':'textinputclass'}),
#             'body': forms.Textarea(attrs={'class':'editable medium-editor-textarea '})
#         }
