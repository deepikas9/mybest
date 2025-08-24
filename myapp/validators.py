import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # At least 6 alphabets
        if len(re.findall(r'[A-Za-z]', password)) < 6:
            raise ValidationError(
                _("Password must contain at least 6 alphabets."),
                code='password_no_alpha',
            )

        # At least 1 digit
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Password must contain at least 1 number."),
                code='password_no_number',
            )

        # At least 1 special character
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(
                _("Password must contain at least 1 special character."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 6 alphabets, "
            "1 number, and 1 special character."
        )
