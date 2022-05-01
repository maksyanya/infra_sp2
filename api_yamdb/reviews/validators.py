from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(val):
    current_year = timezone.now().year
    if val > current_year:
        raise ValidationError('Такой год еще не наступил.')
    # Сделал PositiveSmallIntegerField - там мин значение 0.
    # if val < 0:
    #     raise ValidationError('В таком году еще не умели писать.')
