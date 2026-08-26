import sys
import ast
from flask import Flask,request,jsonify
from flask_cors import CORS

fname=sys.argv[1]

f=open(f'./data/{fname}.csv','w')
columns=['ts','videoBitrate', 'videoIndex', 'videoPendingIndex', 'videoPendingMaxIndex', 'videoMaxIndex', 'videoBufferLength', 'videoDroppedFrames', 'videoLatencyCount', 'videoLatency', 'videoDownloadCount', 'videoDownload', 'videoRatioCount', 'videoRatio', 'videoMtp', 'videoEtp', 'videoLiveLatency', 'videoPlaybackRate', 'audioBitrate', 'audioIndex', 'audioPendingIndex', 'audioPendingMaxIndex', 'audioMaxIndex', 'audioBufferLength', 'audioDroppedFrames', 'audioLatencyCount', 'audioLatency', 'audioDownloadCount', 'audioDownload', 'audioRatioCount', 'audioRatio', 'audioMtp', 'audioEtp','Throughput', 'audioLiveLatency', 'audioPlaybackRate']
f.write(','.join(columns)+'\n')


app=Flask(__name__)
CORS(app)


@app.route("/data",methods=['POST'])
def data():
    app.logger.info(request.data)
    dict_log= eval(request.data.decode('utf-8'))
    f.write(','.join([str(e) for e in list(dict_log.values())])+'\n')
    f.flush()
    return jsonify("Logged"),200


app.run(port=13000)
