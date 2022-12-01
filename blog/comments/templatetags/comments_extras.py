from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, essay, user, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'essay': essay,
        'user': user,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, essay):
    comment_list = essay.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
