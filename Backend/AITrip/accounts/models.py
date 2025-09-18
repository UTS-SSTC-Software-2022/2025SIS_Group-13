from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    Based on the Users table from DDL:
    - user_id: Handled by Django's default id field
    - email: Already in AbstractUser, will be configured as unique
    - username: Maps to username field (DDL name = Django username)
    - first_name, last_name: Required fields for registration
    - middle_name: Optional field for full name
    - create_time: Custom field to match DDL (auto_now_add=True)
    - update_time: Custom field to match DDL (auto_now=True)
    """
    
    # Override email to make it unique and required
    email = models.EmailField(
        unique=True, 
        verbose_name='Email Address',
        db_index=True
    )
    
    # Time tracking fields to match DDL
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Create Time',
        db_index=True,
        help_text='Time when user was created'
    )

    middle_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Middle Name',
        help_text='Optional middle name'
    )
    
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Update Time',
        db_index=True,
        help_text='Time when user was last updated'
    )  

    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required for admin
    
    class Meta:
        db_table = 'auth_user'  # Keep Django's default table name for compatibility
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['create_time']),
            models.Index(fields=['update_time']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.get_full_name()}"
    
    def get_full_name(self):
        """Return the full name for the user including middle name."""
        name_parts = [self.first_name, self.middle_name, self.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name 
    
