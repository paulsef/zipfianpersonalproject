import flask
import pickle
import pdb
import userinfo

app = flask.Flask(__name__)
@app.route('/', methods = ['Get'])
def say_hello():
	return flask.redirect(flask.url_for('static', filename = 'landing.html'))

@app.route('/slicedf', methods = ['Post'])
def slice_df():
	playcount, top_count = flask.request.form['playcount'], flask.request.form['top_count']
	avg_diff_hours, age = flask.request.form['avg_diff_hours'], flask.request.form['age']
	hour_registered, genre = flask.request.form['hour_registered'], flask.request.form['genre']
	final_df = pickle.load(file('final_df.pkl'))
	sliced, errors = userinfo.slice_all(final_df, playcount, top_count, avg_diff_hours, age, hour_registered, genre)
	if sliced.shape[0] == 0:
		return 'no user met the search critera' + str(errors)
	elif sliced.shape[0] < 5:
		x = sliced.shape[0]
	else:
		x = 5
	output= []
	for i in range(x):
		user_dict = {}
		index = sliced.index[i]
		user_dict['playcount'] = sliced['playcount'][index]
		user_dict['name'] = sliced['names'][index]
		user_dict['probability'] = sliced['probs'][index]
		user_dict['image_ref'] = None#userinfo.get_image(user_dict['name'])
		output.append(user_dict)
	#zip(list(sliced['playcount']), list(sliced['names']), list(sliced['user_id']))
	return flask.render_template('list.html', output1 = output)





if __name__ == '__main__':
	app.run(debug = True)