from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            "content",
            "accuracy",
            "commnucation",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self, *args, **kwargs):

        review = super().save(commit=False)
        return review
