from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Feedback, Review, DishRestaurant, Dish, Restaurant, Wishlist,DishRestaurantSuggestion,Category


# 1
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['suggestions']
        widgets = {'suggestions': forms.Textarea(attrs={'rows': 5,'maxlength':1000,"minlength": 20,'required':True,'placeholder': 'Share any insights for this web?'}),
        }


    def clean_suggestions(self):
        text = self.cleaned_data['suggestions'].strip()
        if not text:
            raise ValidationError("Feedback cannot be blank or only whitespace.")
        for bad in ('shit', 'fuck', 'asshole', 'dickhead'):
            if bad in text.lower():
                raise ValidationError("Please help us build a friendly community :)")
        return text


# 2
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'price_paid', 'description', 'photo']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0.1,'max': 5.0,'step': 0.1,'required': True}),
            'price_paid': forms.NumberInput(attrs={'min': 0.1,'step': 0.01,'required': True}),
            'description': forms.Textarea(attrs={'rows': 4,'required': True,'maxlength':1000,"minlength": 5,'placeholder': 'How was it? 5-1000 characters...'})},
        labels = {
            'rating': 'Rating',
            'price_paid': 'Price Paid',
            'description': 'Review',
            'photo': 'Photo (optional)'}
          
    def __init__(self, user, dish_restaurant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.dish_restaurant = dish_restaurant

    def clean(self):
        super().clean()
        exists = (Review.objects.filter(user=self.user, dish_restaurant=self.dish_restaurant).exclude(pk=self.instance.pk)
            .exists()
        )
        if exists:
            raise ValidationError(
                "You have already submitted a review for this dish."
            )
        return self.cleaned_data
    
    def clean_description(self):
        text = self.cleaned_data['description'].strip()
        if not text:
            raise ValidationError("Review cannot be blank or only whitespace.")
        for bad in ('shit', 'fuck', 'asshole', 'dickhead'):
            if bad in text.lower():
                raise ValidationError("Please help us build a friendly community :)")
        return text

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            return photo
        max_size = 1 * 1024 * 1024
        if photo.size > max_size:
            raise ValidationError("Image size must be under 1 MB.")
        if photo.content_type not in ('image/jpeg', 'image/png'):
            raise ValidationError("Only JPEG or PNG images are allowed.")
        return photo

# 3
class DishRestaurantSuggestionForm(forms.ModelForm):
    class Meta:
        model = DishRestaurantSuggestion
        fields = ['dish_name','local_name','restaurant_name','price','available','description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3,'maxlength':1000,"minlength": 5,'placeholder': 'How about give us some details'})}

# 4
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['comments']
        widgets = {'comments': forms.Textarea(attrs={'rows': 3,'maxlength':1000,"minlength": 5,'placeholder': 'Any notes?'})}
        labels = {'comments': 'Notes (optional)'}



# 5
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean_password1(self):
        pwd = self.cleaned_data.get("password1") or ""
        validate_password(pwd)
        return pwd
    
    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username', '')
        email = cleaned.get('email', '')
        if username and email:
            local_part = email.split('@')[0].lower()
            if username.lower() == local_part:
                raise ValidationError("Username should not match the part of your email before '@'.")
        return cleaned
