from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug')
    category = filters.CharFilter(field_name='category__slug')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    # Тут не понял, name чувствителен к регистру,
    # icontains - без учета регистра.
    # exact, iexact - то же с NONE.
    # И вообще SQLite - не чувствителен к регистру, как оказалось).

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
