from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MaxLengthValidator, MinLengthValidator

class Feedback(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    suggestions  = models.TextField(validators=[MinLengthValidator(20,"At least 20 characters"),
                                                MaxLengthValidator(1000,"Can't exceed 1000")])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Feedback by {self.user.username}"


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["title"]

    def __str__(self):
        return self.title




class Dish(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,validators=[MaxLengthValidator(1000, "Description cannot exceed 1000 characters."),
                                                          MinLengthValidator(5,"At least 5 characters.")])
    categories = models.ManyToManyField(Category, blank=True)
    
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True,validators=[MaxLengthValidator(1000, "Description cannot exceed 1000 characters.")])
    address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    website = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name


class DishRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    dish = models.ForeignKey(Dish,       on_delete=models.PROTECT)
    local_name = models.CharField(max_length=100,blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["restaurant","dish"],name="combo_dish_res"),
        ]

    def __str__(self):
        name = self.local_name or self.dish.name
        return f"{self.restaurant.name} for {name}"

class DishRestaurantSuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=45)
    local_name = models.CharField(max_length=100, blank=True)
    restaurant_name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.1)],help_text="Suggested price in NOK")
    available = models.BooleanField(default=True,help_text="Currently available?")
    description = models.TextField(blank=True,validators=[MaxLengthValidator(1000, "Description cannot exceed 1000 characters."),
                                                          MinLengthValidator(5,"At least 5 characters.")])
    created_date = models.DateTimeField(auto_now_add=True)
    is_reviewed  = models.BooleanField(default=False,help_text="Set to True when processed")

    class Meta:
        verbose_name_plural = "Dish-Restaurant Suggestions"
        ordering = ['-created_date']

    def __str__(self):
        return f"Suggestion by {self.user.username}: {self.dish_name} @ {self.restaurant_name}"

class Review(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=2,decimal_places=1,validators=[MinValueValidator(0.1), MaxValueValidator(5.0)],help_text="Rating must be between 0.1 and 5.0")
    price_paid = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(0.1)],help_text="Suggested price in NOK")
    description = models.TextField(validators=[MinLengthValidator(5, "Review must be at least 5 characters."),
                                               MaxLengthValidator(1000, "Review cannot exceed 1000 characters.")])
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish_restaurant = models.ForeignKey(
        DishRestaurant, on_delete=models.CASCADE, related_name='reviews'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "dish_restaurant"],
                name="unique_review_per_user_and_dishrest",
            )
        ]

    def __str__(self):
        return f"{self.user.username}'s review of {self.dish_restaurant}"

class Wishlist(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True,validators=[MinLengthValidator(5, "Comments must be at least 5 characters."),
                                               MaxLengthValidator(1000, "Comments cannot exceed 1000 characters.")])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_date"]
        constraints = [models.UniqueConstraint(fields=["user", "dish"],name="unique_user_dish")]

    def __str__(self):
        return f"{self.user.username} wants {self.dish.name}"
    

