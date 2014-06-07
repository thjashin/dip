from flask import Flask, request, Response
import base64
from cStringIO import StringIO
import os

app = Flask(__name__)

def main_func(run_id, query, image):
    """
    This is the part that you should implement
    parameter:
        run_id: unicode string
        query: unicode string
        image: file-like object, contain a jpeg image
    you should use query and image to calculate a score
    """
    return 0.3

@app.route('/', methods=['POST'])
def interface():
    form = request.form
    run_id = form['runID'].decode('utf-8')
    query = form['query'].decode('utf-8')
    image = form['image']
    img_string = base64.decodestring(image)
    with open('dumps/%s.jpg', 'wb') as f:
        f.write(img_string)

    img = StringIO(img_string)

    try:
        ret = main_func(run_id, query, img)
    except:
        ret = 'error'
    with open('dumps/log.tsv', 'a') as f:
        f.write('\t'.join(run_id, query, str(ret)) + '\n')
    return Response(str(ret), mimetype='text/plain')

if __name__ == '__main__':
    if not os.path.isdir('dumps'):
        os.makedirs('dumps')
    app.run(host='0.0.0.0', port=8003, debug=True)
