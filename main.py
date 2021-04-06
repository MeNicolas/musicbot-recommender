import flask
from flask import request
from flask import jsonify
import pickle
import numpy as np
from pathlib import Path
import wget

app = flask.Flask(__name__)
app.config["DEBUG"] = True

tracks = []
uri_to_index = {}
index_to_uri = {}
mat = None

def load():
	print('b')
	global tracks, uri_to_index, index_to_uri, mat
	if mat == None:
		if not Path("data/dataset.pkl").is_file():
			wget.download('https://nicod.s3.fr-par.scw.cloud/dataset.pkl', 'data/dataset.pkl')
		if not Path("data/mat.pkl").is_file():
			wget.download('https://nicod.s3.fr-par.scw.cloud/mat.pkl', 'data/mat.pkl')
		
		dataset = pickle.load(open('data/dataset.pkl', 'rb'))
		mat = pickle.load(open('data/mat.pkl', 'rb'))
		
		tracks = dataset[0]
		uri_to_index = dataset[1]
		index_to_uri = dataset[2]
		print(len(uri_to_index))

load()

def similar_music(track_uri, n=10):
	if not track_uri in uri_to_index: return []

	i0 = uri_to_index[track_uri]

	print(tracks[index_to_uri[i0]]['track_name'])
	
	col = np.array(list(map(lambda x: x[0], mat[:i0,i0].toarray())))
	row = mat[i0,i0:].toarray()[0]

	counts = np.concatenate((col, row), axis=0)
	top = np.argpartition(counts, -n)[-n:]
	
	
	print([tracks[index_to_uri[i]]['track_name']+' - '+tracks[index_to_uri[i]]['artist_name'] for i in top])

	return [index_to_uri[i] for i in top]

@app.route('/', methods=['GET'])
def home():
	load()
	uri = request.args.get('uri')
	n = request.args.get('n')

	res = similar_music(uri, n)
	return jsonify(res)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80, use_reloader=False)