# -*- coding: utf-8 -*-
from gluon.html import DIV, SCRIPT
from gluon.sqlhtml import SQLFORM

# New widget date
def date_widget(field, value):
    wrapper = DIV()
    input_date = SQLFORM.widgets.date.widget(field, value)
    javascript = SCRIPT("""
        jQuery.datetimepicker.setLocale('es');
            $(function () {
                $("#%s").datetimepicker({
                    format: 'Y-m-d',
                    inline: false,
                    timepicker:false,
                });
            });
    """ % input_date['_id'], _type='text/javascript')
    wrapper.components.extend([input_date,javascript])
    return wrapper

def datetime_widget(field, value):
    wrapper = DIV()
    input_date = SQLFORM.widgets.date.widget(field, value)
    javascript = SCRIPT("""
        jQuery.datetimepicker.setLocale('es');
            $(function () {
                $("#%s").datetimepicker({
                    format: 'd/m/Y H:i',
                    inline: false,
                    timepicker:true,
                });
            });
    """ % input_date['_id'], _type='text/javascript')
    wrapper.components.extend([input_date,javascript])
    return wrapper

# New widget date
def time_widget(field, value):
    wrapper = DIV()
    input_date = SQLFORM.widgets.date.widget(field, value)
    javascript = SCRIPT("""
        jQuery.datetimepicker.setLocale('es');
            $(function () {
                $("#%s").datetimepicker({
                    format: 'H:i',
                    inline: false,
                    timepicker:true,
                    datepicker:false,
                });
            });
    """ % input_date['_id'], _type='text/javascript')
    wrapper.components.extend([input_date,javascript])
    return wrapper
