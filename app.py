import numpy as np
from flask import Flask, request, render_template, send_file
from crowdCalculate import *;
from detectArea import *;

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')

@app.route('/calculate')
def calculate():
	record()
	width = frame_width()
	height = frame_height()
	crowd_density=evaluate_crowd(width,height)
	person_number=(crowd_density).get('person_num')
	person_in=(crowd_density).get('person_count').get('in')
	person_out=(crowd_density).get('person_count').get('out')
	density=crowd_density_algorithm(width,height,person_number,person_in,person_out)
	return str(density)

@app.route('/location')
def location():
    return render_template('location.html')


if __name__ == "__main__":
	app.run()
