import flask
import pickle
import pdb


app = flask.Flask(__name__)
@app.route('/', methods = ['Get'])
def say_hello():
	return flask.redirect(flask.url_for('static', filename = 'landing.html'))

@app.route('/slicedf', methods = ['Get', 'Post'])
def slice_df():
	x = flask.request.form
	print x
	condition1 = flask.request.form['condition1']
	#pdb.set_trace()
	try:
		condition1 = int(flask.request.form['condition1'])
	except:
		return str(condition1) +  ' was not an integer'
	final_df = pickle.load(file('final_df.pkl'))
	#pdb.set_trace()
	sliced = final_df[final_df['playcount'] > condition1]
	output1 = zip(list(sliced['playcount']), list(sliced.index))
	return flask.render_template('list.html', output1 = output1)





if __name__ == '__main__':
	app.run(debug = True)