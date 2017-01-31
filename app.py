import os, sys
import json
import numpy as np
np.random.seed(10)
import pandas as pd

from flask import Flask, request, redirect, render_template



ENTER_POINT = '/embed'
app = Flask(__name__, static_url_path=ENTER_POINT, static_folder=os.getcwd())
app.debug = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 6

@app.before_first_request
def load_globals():
	global meta_df, N_SIGS
	meta_df = pd.read_csv('log/CD_lm978_978dims/metadata.tsv', sep='\t')
	print meta_df.shape
	N_SIGS = meta_df.shape[0]
	return


@app.route(ENTER_POINT + '/')
def index_page():
	return app.send_static_file('index.html')

@app.route('/lib/textures/sprites/disc.png')
def send_file():
	return app.send_static_file('lib/textures/sprites/disc.png')

@app.route(ENTER_POINT + '/toy', methods=['GET'])
def toy_data():
	if request.method == 'GET':
		n = request.args.get('n', 10)
		rand_idx = np.random.choice(range(N_SIGS), n, replace=False)

		rand_coords = np.random.randn(n, 3)
		df = meta_df.iloc[rand_idx]
		df = df.assign(x=rand_coords[:,0], y=rand_coords[:,1], z=rand_coords[:,2])

		return df.to_json(orient='records')


@app.route(ENTER_POINT + '/pca', methods=['GET'])
def load_pca_coords():
	if request.method == 'GET':
		coords = np.load('data/pca_coords.npy')
		df = meta_df.assign(x=coords[:,0], y=coords[:,1], z=coords[:,2])

	return df.to_json(orient='records')


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)

