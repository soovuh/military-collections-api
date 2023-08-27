from django.core.validators import MinValueValidator
from django.db import models


class MilitaryCollections(models.Model):
    """
    Model representing military collections.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
    )
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contributors(models.Model):
    """
    Model representing contributors to military collections.
    """
    collection_id = models.ForeignKey(to=MilitaryCollections, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
    )
