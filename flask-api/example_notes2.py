from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

list = {
        '1':'value1',
}

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        val = request.data.get('key','')
        idx = int(max(list.keys())) + 1
        if val:
            list[idx] = val 
            return list
    return list

if __name__=='__main__':
    app.run(debug=True)
