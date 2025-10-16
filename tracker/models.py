from django.db import models
import random


class SavingsBox(models.Model):
    """Model representing individual savings boxes"""
    BOX_VALUES = [200, 500, 1000]
    
    value = models.IntegerField()
    is_saved = models.BooleanField(default=False)
    position = models.IntegerField()  # Position in the grid
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Box {self.position}: ₹{self.value} ({'Saved' if self.is_saved else 'Pending'})"
    
    @classmethod
    def initialize_boxes(cls):
        """Initialize boxes to reach approximately ₹1,00,000 total"""
        cls.objects.all().delete()  # Clear existing boxes
        
        target_amount = 100000
        current_total = 0
        position = 1
        
        while current_total < target_amount:
            remaining = target_amount - current_total
            
            # Choose box value based on remaining amount
            if remaining >= 1000:
                available_values = [200, 500, 1000]
            elif remaining >= 500:
                available_values = [200, 500]
            else:
                available_values = [200]
            
            value = random.choice(available_values)
            
            # Adjust if this would exceed target
            if current_total + value > target_amount:
                value = remaining
            
            cls.objects.create(value=value, position=position)
            current_total += value
            position += 1
    
    class Meta:
        ordering = ['position']
