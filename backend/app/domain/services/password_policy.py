"""Password policy enforcement."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.exceptions import ValidationError

_UPPER_RE = re.compile(r"[A-Z]")
_LOWER_RE = re.compile(r"[a-z]")
_DIGIT_RE = re.compile(r"\d")
_SPECIAL_RE = re.compile(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]")


@dataclass(frozen=True)
class PasswordPolicy:
    """Configurable password policy rules."""

    min_length: int = 8
    max_length: int = 128
    require_upper: bool = True
    require_lower: bool = True
    require_digit: bool = True
    require_special: bool = False
    forbid_whitespace: bool = True

    def validate(self, password: str) -> None:
        """Validate a plaintext password. Raises ValidationError when invalid."""
        if not isinstance(password, str):
            raise ValidationError("Password must be a string")
        if len(password) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long"
            )
        if len(password) > self.max_length:
            raise ValidationError(
                f"Password must be at most {self.max_length} characters long"
            )
        if self.forbid_whitespace and any(ch.isspace() for ch in password):
            raise ValidationError("Password must not contain whitespace characters")
        if self.require_upper and not _UPPER_RE.search(password):
            raise ValidationError("Password must contain an uppercase letter")
        if self.require_lower and not _LOWER_RE.search(password):
            raise ValidationError("Password must contain a lowercase letter")
        if self.require_digit and not _DIGIT_RE.search(password):
            raise ValidationError("Password must contain a digit")
        if self.require_special and not _SPECIAL_RE.search(password):
            raise ValidationError("Password must contain a special character")


DEFAULT_PASSWORD_POLICY = PasswordPolicy()