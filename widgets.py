from django import forms

class jQCalendarWidget(forms.DateInput):
  # A widget that replaces the admin calendar widget, can also be used for other calendar stuff as well.
  
  class Media:
    js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js",
          "http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js",
          "/static/js/dateinput_init.js",)
    css = {
      'screen': ("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/redmond/jquery-ui.css",)}
  
  def __init__(self, attrs={}):
    super(jQCalendarWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'})