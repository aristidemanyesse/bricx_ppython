# coding: utf-8
import json
from django import template
import sqlparse

register = template.Library()



@register.filter('start0')
def start0(number):
    if number is not None:
        if 0 <= int(number) <= 9 :
            return "0"+str(number)
        return number
    return "00"


@register.filter('pretty_json')
def pretty_json(json_text):
    try:
        pretty_json_text = json.dumps(json_text, indent=4)
        return pretty_json_text
    except Exception:
        return json_text


@register.filter('dict_value')
def get_value_from_dict(dict_data, key):
    if key:
        return dict_data.get(str(key))
    return ""



@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def sub(value, arg):
    return value - arg



@register.inclusion_tag('djutils/sort_th.html', takes_context=True)
def sort_th(context, sort_param_name, label):
    return {
        'is_current': context['sort_params'][sort_param_name]['is_current'],
        'is_reversed': context['sort_params'][sort_param_name]['is_reversed'],
        'url': context['sort_params'][sort_param_name]['url'],
        'label': label,
    }