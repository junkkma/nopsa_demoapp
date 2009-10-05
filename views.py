#!/usr/bin/python
#!encoding=utf-8

from nopsa.OpenFlashChart import Chart
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.db import connection
from nopsa.demoapp.models import *

graph_dimensions = {'Tuote': 'Product',
                    'Tuoteryhmä': 'Product_group',                    
                    'Asiakas': 'Customer',
                    'Asiakasryhmä': 'Customer_group'}
                      
graph_measures = {'Myynti': 'Net_sales',
                  'Määrä': 'Quantity'}
                    
#----------------
# VIEWS
#----------------

def chart(request): 
  return render_to_response('chart.html', {'x_axis_options': graph_dimensions, 'measures': graph_measures}, context_instance = RequestContext(request))

def chart_data(request):
  if request.is_ajax():
    GET = request.GET
    if GET.has_key(u'x_axis') and GET.has_key(u'measure'):
      return HttpResponse(Get_chart_json_string(GET[u'measure'], GET[u'x_axis']), mimetype='application/json')

#----------------
# OTHER FUNCTIONS
#----------------

def Get_chart_json_string(measure, x_axis):
  
  # Create an sql query and fetch the data
  sql_query = "SELECT "+ x_axis +", SUM("+ measure +") As Measure FROM Sales_data_view GROUP BY "+ x_axis +" ORDER BY "+ measure +" DESC"
  
  cursor = connection.cursor()
  cursor.execute(sql_query)
  data = cursor.fetchall()
  
  graph_values = []
  graph_labels = []
  
  for i in range(len(data)):
    graph_labels.append(data[i][0])
    graph_values.append(data[i][1])
 
  el1 = Chart()
  el1.values = graph_values
  el1.type = 'bar'
  
  el1.width = 4
#  el1.text = measures[measure]
  el1.font_size = 12
  el1.on_show.type = 'grow-up'
  el1.on_show.cascade = 0.5
  el1.on_show.delay = 0
  el1.colour = '#86BBEF'
  
  chart = Chart()
  chart.y_axis.min = min(0,min(graph_values))
  chart.y_axis.max = max(graph_values) 
  chart.x_axis.labels.labels = graph_labels
  chart.x_axis.labels.rotate = 20
  
  chart.title.text = "Myynti"
  chart.bg_colour = '#FFFFFF'
  
  chart.elements = [el1]
  json_string = repr(chart.create())

  return json_string
  
