from django import template
import re

register = template.Library()


@register.filter
def add_link(value):
    content = value.content
    tags = value.tag_set.all()
    for tag in tags:
        content = re.sub(
            r"\#" + tag.name + r"\b",
            '<a href="/post/explore/tags/' + tag.name + '">#' + tag.name + "</a>",
            content,
        )  # re.sub(pattern, repl, string)	string에서 pattern과 매치하는 텍스트를 repl로 치환한다
    return content
