from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
#from jieba.analyse import  extract_tags
import string
import utils
import gruop_sum_geo
app = Flask(__name__)

u=utils.utils_ertong("care","geoinformation","root","1234")
fumu=utils.utils_fumu("care","geoinformation","root","1234")
lingyanglv=utils.utils_lingyanglv("care","geoinformation","root","1234")
renew_geo_sql=gruop_sum_geo.renew_sql()

@app.route('/')
def hello_world():
    return render_template("main(1).html")

@app.route('/geo_renew')
def get_geo_renw():
    renew_geo_sql.get_geo_sql()
    return render_template("main(1).html")

@app.route('/c2')
def get_c2_data():
    res=[]
    data=u.get_c2_data()
    for key,value in data.items():
        res.append({"name":key,"value":value})
    #for key,value in data_2.items():
     #   res_2.append({"name":key,"value":value})
      #  print(res)
    return jsonify({"data":res})

@app.route('/c2_fumu')
def get_c2_data_fumu():
    res=[]
    data=fumu.get_c2_data_fumu()
    for key,value in data.items():
        res.append({"name":key,"value":value})
    #for key,value in data_2.items():
    #   res_2.append({"name":key,"value":value})
    #  print(res)
    return jsonify({"data":res})

@app.route('/r1')
def get_r1_data():
    data=lingyanglv.get_r1_data()
    keys=list(data.keys())
    values=list(data.values())
    print(jsonify({"keys":keys,"values":values}))
    return jsonify({"keys":keys,"values":values})



if __name__ == '__main__':
    app.run()