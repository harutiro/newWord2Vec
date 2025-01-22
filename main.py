# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # CORSをインポート

from gensim.models import word2vec
from numpy import negative

MODEL_FILENAME_WIN = "models\wiki2.vec.pt"
MODEL_FILENAME = "models/wiki2.vec.pt"
try:
    w2v = word2vec.KeyedVectors.load_word2vec_format(MODEL_FILENAME, binary=True)
except:
    w2v = word2vec.KeyedVectors.load_word2vec_format(MODEL_FILENAME_WIN, binary=True)

app = Flask(__name__)
CORS(app)  # CORSを全てのエンドポイントに対して有効にする
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま

@app.route('/near' ,methods=["GET"])
def near():
    try:
        req = request.args
        get_number = req.get("get_number")
        str = req.get("str")
    except:
        return jsonify({
            'status':'NO',
            'error':'error'
        })

    
    # default 表示
    if get_number is None:
        get_number = 5

    if str is None:
        return jsonify({
            'status':'NO',
            'error':'default設定の"strが設定されていません"'
        })


    try:
        w2v.most_similar(str, topn=int(get_number))
    except:
        return jsonify({
            'status':'NO',
            'error':'対応していない単語が使用されました'
        })

    print(get_number)
    
    data = w2v.most_similar(str, topn=int(get_number))

    return jsonify({
            'status':'OK',
            'mode':"near",
            'moji':str,
            'num0':get_number,
            'data':list(map(lambda x: x[0], data)),
            
        })


@app.route('/calculation' ,methods=["GET"])
def calc():
    try:
        req = request.args
        get_number = req.get("get_number")
        positiveStr = req.getlist("positive")
        negativeStr = req.getlist("negative")

    except:
        return jsonify({
            'status':'NO',
            'error':'error'
        })

    
    # default 表示
    if get_number is None:
        get_number = 5

    if positiveStr is None:
        return jsonify({
            'status':'NO',
            'error':'default設定の"strが設定されていません"'
        })

    if negativeStr is None:
        return jsonify({
            'status':'NO',
            'error':'default設定の"strが設定されていません"'
        })

    try:
        w2v.most_similar(positive=positiveStr,negative=negativeStr, topn=int(get_number))
    except:
        return jsonify({
            'status':'NO',
            'error':'対応していない単語が使用されました'
        })

    print(get_number)
    
    data = w2v.most_similar(positive=positiveStr,negative=negativeStr, topn=int(get_number))

    return jsonify({
            'status':'OK',
            'mode':"calculation",
            'positive':positiveStr,
            "negative":negativeStr,
            'get_number':get_number,
            "data":list(map(lambda x: x[0], data))
            
        })

@app.route('/')
def index():
    return 'hello, world'

## おまじない
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
