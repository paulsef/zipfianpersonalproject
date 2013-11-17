import flask
import pickle
import pdb
import userinfo

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
	output= []
	for i in range(10):
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