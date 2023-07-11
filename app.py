from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import requests
from datetime import datetime
import json

app = Flask(__name__, static_url_path='/static')

lotto_name = '1'


@app.route('/select-lotto', methods=['POST'])
def select_lotto():
  selected_lotto = request.form['lotto_name']
  #load_lotto_data(selected_lotto)
  print(f"selected_lotto = {selected_lotto}")
  return load_lotto_data(selected_lotto)


def sort_numbers(lists, p1, p2):
  for sub_list in lists:
    sub_list.sort(key=lambda x: (x[p1], x[p2]))

  return lists


def load_lotto_data(lotto_name):
  url = f'http://api.lottotry.com/api/lottotypes?lottoName={lotto_name}'

  # Make a GET request
  response = requests.get(url)
  if response.status_code == 200:
    global data
    data = response.json()  # Parse the response as JSON
    #print(data)
  else:
    print('Request failed with status code:', response.status_code)

  #return data
  #print(data[0])
  number_range = data[0]['numberRange']
  print(f"number_range = {number_range}")

  draw_numbers = []
  draw_date = []
  numbers = []
  values_list = []

  for da in data:
    draw_numbers.append(int(da['drawNumber']))
    #draw_date.append(datetime(['drawDate']).strftime('%Y-%m-%d'))
    #draw_date.append(da['drawDate'].strftime('%Y-%m-%d'))
    draw_date.append(da['drawDate'].split('T')[0])
    numbers.append(da['numbers'])

  # Access the first element in the array

  for row in numbers:
    values = []
    for va in row:
      values.append(va['value'])

    values_list.append(values)

  #sorted_list = sort_numbers(numbers, 'distance', 'value')
  sorted_list = sort_numbers(numbers, 'value', 'value')
  #print(sorted_list)

  draw_numbers_count = len(draw_numbers)
  lotto = {
    'number_range': number_range,
    'draw_numbers': draw_numbers,
    'draw_numbers_count': draw_numbers_count,
    'draw_date': draw_date,
    'numbers': sorted_list,
    'values_list': values_list,
  }

  return lotto


lotto = load_lotto_data(lotto_name)


@app.route('/', methods=['GET', 'POST'])
def home():

  #print(lotto)
  return render_template('home.html', lotto=lotto)


@app.route('/update-content', methods=['GET', 'POST'])
def update_content():
  if request.method == "POST":
    lotto_name = request.form['lotto_name']
    print(lotto_name)
    global lotto
    lotto = load_lotto_data(lotto_name)

  return home()
  


@app.route('/static/css/<path:filename>')
def serve_css(filename):
  return send_from_directory(app.static_folder + '/css', filename)


app.run(host='0.0.0.0', port=8001, debug=True)
