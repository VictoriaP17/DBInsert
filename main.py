from flask import Flask,render_template,request,jsonify
from taosrest import RestClient
from flask_basicauth import BasicAuth

app=Flask(__name__)
basic_auth = BasicAuth(app)
#app.template_folder = ''   #CHANGE TO TEMPLATES FOLDER IF NEEDED

app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = ''
app.config['BASIC_AUTH_FORCE'] = True

servicesHeader={"Content-Type":"application/json"}

@app.route('/webservices/db/insert/', methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')

    if request.method=='POST':

        if not request.form['txtId'] or not request.form['txtMacAddress'] or not request.form['txtDescription'] or not request.form['txtType']:
            error_response = {"error": "One or more field(s) were null, please provide all required information"}
            return  jsonify(error_response),400,servicesHeader
        product_id=request.form['txtId']
        product_mac_address=request.form['txtMacAddress']
        product_description=request.form['txtDescription']
        product_type=request.form['txtType']


        db_host=''  #CHANGE TO SERVER IP/DOMAIN, INCLUDING PORT
        db_user=''                    #CHANGE TO ACTUAL DESIRED VALUES
        db_password=''
        db_name=''
        db_table=''

        try:
            client = RestClient(db_host, user=db_user, password=db_password)
            res: dict = client.sql(f"insert into {db_name}.{db_table} values(now(),{product_id},'{product_mac_address}','{product_description}','{product_type}')")
            status_code=res["code"]
            
            if status_code!=0:
                error_response = {"error": "DB returned error with next code: " + str(status_code)}
                return  jsonify(error_response),400,servicesHeader
            
            return "Success",200,servicesHeader

        except Exception as e:
            error_response = {"error": e}
            return jsonify(error_response),400,servicesHeader


if __name__ == "__main__":
    app.run()