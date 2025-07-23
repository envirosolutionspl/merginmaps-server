# Copyright (C) Lutra Consulting Limited
#
# SPDX-License-Identifier: AGPL-3.0-only OR LicenseRef-MerginMaps-Commercial
import re
import safe
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import (
    DataRequired,
    Optional,
    Length,
    ValidationError,
    Email,
    EqualTo,
)

from .models import User
from ..app import UpdateForm, CustomStringField

from ..lang.current import returnTranslation

def username_validation(form, field):
    from ..sync.utils import (
        has_valid_characters,
        has_valid_first_character,
        check_filename,
        is_reserved_word,
    )

    errors = (
        [
            has_valid_characters(field.data),
            has_valid_first_character(field.data),
            is_reserved_word(field.data),
            check_filename(field.data),
        ]
        if field.data
        else []
    )
    for error in errors:
        if error:
            raise ValidationError(error)


class ExtendedEmail(Email):
    """Custom email validation extending WTForms email validation.
    WTForms checks for
    1. spaces,
    2. special characters ,:;()<>[]\"
    3, multiple @ symbols,
    4, leading, trailing, or consecutive dots in the local part
    5, invalid domain part - missing top level domain (user@example), consecutive dots
    Custom check for additional invalid characters disallows |'— because they make our email sending service to fail
    """

    def __call__(self, form, field):
        super().__call__(form, field)

        if re.search(r"[|'—]", field.data):
            EmailAddress = returnTranslation("EmailAddress")
            ContainsAnInvalidCharacter = returnTranslation("ContainsAnInvalidCharacter")
            raise ValidationError(
                f"{EmailAddress} '{field.data}' {ContainsAnInvalidCharacter}"
            )


class PasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def __call__(self, form, field):
        if len(field.data) < self.min_length:
            PasswordsMustBeAtLeast = returnTranslation("PasswordsMustBeAtLeast")
            CharactersLong = returnTranslation("CharactersLong")
            raise ValidationError(
                f"{PasswordsMustBeAtLeast} {self.min_length} {CharactersLong}"
            )

        strength = safe.check(field.data, self.min_length)
        if not bool(strength):
            PasswordIsNotStrongEnough = returnTranslation("PasswordIsNotStrongEnough")
            raise ValidationError(PasswordIsNotStrongEnough)


class LoginForm(FlaskForm):
    """Form with username and password fields for user to sign in."""

    login = CustomStringField(validators=[DataRequired(), Length(max=80)])
    password = PasswordField(validators=[DataRequired()])


class RegisterUserForm(FlaskForm):
    username = CustomStringField(
        "Username",
        validators=[validators.Length(min=4, max=25), username_validation],
    )
    email = CustomStringField(
        "Email Address",
        validators=[DataRequired(), ExtendedEmail()],
    )

    def validate(self):
        if not super().validate():
            return False

        user = User.query.filter(
            (func.lower(User.username) == func.lower(self.username.data.strip()))
            | (func.lower(User.email) == func.lower(self.email.data.strip()))
        ).first()
        if user:
            if user.username.lower() == self.username.data.lower().strip():
                self.username.errors.append(returnTranslation("AlreadyExists"))
            if user.email.lower() == self.email.data.lower().strip():
                self.email.errors.append(returnTranslation("AlreadyExists"))
            return False
        return True


class ResetPasswordForm(FlaskForm):
    email = CustomStringField(
        "Email Address",
        [DataRequired(), ExtendedEmail()],
    )


class UserPasswordForm(FlaskForm):
    PasswordsMustMatch = returnTranslation("PasswordsMustMatch")
    password = PasswordField(
        "Password", [DataRequired(), PasswordValidator(min_length=8)]
    )
    confirm = PasswordField(
        "Confirm password",
        [DataRequired(), EqualTo("password", message=PasswordsMustMatch)],
    )


class UserRegistrationForm(RegisterUserForm, UserPasswordForm):
    pass


class UserChangePasswordForm(UserPasswordForm):
    old_password = StringField("Old Password", [DataRequired()])


class UserForm(UpdateForm):
    """Form to update user private props"""
    Admin = returnTranslation("Admin")
    Active = returnTranslation("Active")

    is_admin = BooleanField(Admin, [Optional()])
    active = BooleanField(Active, [Optional()])


class UserProfileDataForm(UpdateForm):
    """This form is for user profile update"""

    Email = returnTranslation("Email")
    ReceiveNotifications = returnTranslation("ReceiveNotifications")
    FirstName = returnTranslation("FirstName")
    LastName = returnTranslation("LastName")

    receive_notifications = BooleanField(ReceiveNotifications, [Optional()])
    first_name = CustomStringField(FirstName, [Optional()])
    last_name = CustomStringField(LastName, [Optional()])
    email = CustomStringField(Email, [Optional(), ExtendedEmail()])


class ApiLoginForm(LoginForm):
    class Meta:
        csrf = False
        load_instance = True
