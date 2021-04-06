import flask
from flask import request
from flask import jsonify
import pickle
import numpy as np

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
		dataset = pickle.load(open('data/dataset.pkl', 'rb'))
		mat = pickle.load(open('data/mat.pkl', 'rb'))
		
		tracks = dataset[0]
		uri_to_index = dataset[1]
		index_to_uri = dataset[2]
		print(len(uri_to_index))


def similar_music(track_uri):
	if not track_uri in uri_to_index: return []

	i0 = uri_to_index[track_uri]

	print(tracks[index_to_uri[i0]]['track_name'])
	top = np.argpartition(mat[i0,:].toarray()[0], -10)[-10:]
	print([tracks[index_to_uri[i]]['track_name']+' - '+tracks[index_to_uri[i]]['artist_name'] for i in top])

	return [index_to_uri[i] for i in top]

@app.route('/', methods=['GET'])
def home():
	load()
	res = similar_music(request.args.get('uri'))
	return jsonify(res)

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80, use_reloader=False)