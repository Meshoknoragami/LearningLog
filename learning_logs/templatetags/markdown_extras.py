import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def markdownify(text):
    """Преобразует Markdown в безопасный HTML"""
    return mark_safe(
        markdown.markdown(
            text,
            extensions=[
                'fenced_code',
                'nl2br',
                'extra',  # включает ссылки, таблицы, сокращения и т.д.
            ],
            output_format='html5'
        )
    )
