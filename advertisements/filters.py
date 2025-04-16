import django_filters
from .models import Advertisement


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class AdvertisementFilter(django_filters.FilterSet):
    # Множественная фильтрация
    mark = CharInFilter(field_name='mark', lookup_expr='in')
    model = CharInFilter(field_name='model', lookup_expr='in')
    generation = NumberInFilter(field_name='generation', lookup_expr='in')
    notice = CharInFilter(field_name='notice', lookup_expr='in')
    engine_type = CharInFilter(field_name='engine_type', lookup_expr='in')
    transmission = CharInFilter(field_name='transmission', lookup_expr='in')
    drive = CharInFilter(field_name='drive', lookup_expr='in')
    state = CharInFilter(field_name='state', lookup_expr='in')
    color = CharInFilter(field_name='color', lookup_expr='in')
    availability_in_kyrgyzstan = CharInFilter(field_name='availability_in_kyrgyzstan', lookup_expr='in')
    country_of_registration = CharInFilter(field_name='country_of_registration', lookup_expr='in')
    possibility_of_exchange = CharInFilter(field_name='possibility_of_exchange', lookup_expr='in')

    # Обычная фильтрация
    year_of_manufacture = django_filters.RangeFilter(field_name='year_of_manufacture')
    steering_wheel = django_filters.CharFilter(field_name='steering_wheel')
    mileage = django_filters.RangeFilter(field_name='mileage')  # поддержка от и до
    units_of_mileage = django_filters.CharFilter(field_name='units_of_mileage')
    customs_in_kyrgyzstan = django_filters.BooleanFilter(field_name='customs_in_kyrgyzstan')
    urgently = django_filters.BooleanFilter(field_name='urgently')
    possibility_of_installments = django_filters.BooleanFilter(field_name='possibility_of_installments')
    currency = django_filters.CharFilter(field_name='currency')
    price = django_filters.RangeFilter(field_name='price')  # поддержка от и до
    region = django_filters.CharFilter(field_name='region')
    city = django_filters.CharFilter(field_name='city')

    class Meta:
        model = Advertisement
        fields = []