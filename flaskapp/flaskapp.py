import flask
import pickle

final_df = pickle.load(file('final_df.pkl'))

app = flask.Flask(__name__)
@app.route('/', methods = ['Get'])
def say_hello():
	return flask.redirect(flask.url_for('static', filename = 'landing.html'))

if __name__ == '__main__':
	app.run(debug = True)