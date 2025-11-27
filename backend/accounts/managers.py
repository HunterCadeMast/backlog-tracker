from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, email):
        return self.get(email = email)

    def create_user(self, email, password = None, **fields):
        if not email:
            raise ValueError(_("Email address needed!"))
        email = self.normalize_email(email).strip()
        fields['username'] = fields.get('username', '').strip()
        user = self.model(email = email, **fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password = None, **fields):
        fields.setdefault("is_staff", True)
        fields.setdefault("is_superuser", True)
        if fields.get("is_staff") is not True:
            raise ValueError(_("Superuser needs to be staff!"))
        if fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser needs to be superuser!"))
        return self.create_user(email, password, **fields)