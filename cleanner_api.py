from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# ให้เฟ้นสอนเชื่อมดาต้าเบสให้หน่อย 
# Function 1 :RemoveIrrelevantData
#Route to handle JSON DATA
@app.route('/')
def index():
    print()
@app.route('/removeirrdata/check',methods = ['POST'])
def removeIrrelevantData_check():
    try:
        # Receive JSON data from another host
        read_data = request.get_json()
        # this one read what columns user want to do
        data_match = read_data["data_set"]["columns_match"]
        #retrieve the dataset from database
        data = read_data["data_set"]["rows"]
        # add logic here

        df = pd.DataFrame(data)
        df_left = df.drop(data_match,axis=1)
        df_left.insert(0,"st@tus",True)
      #  print(df_left)
        df_left.replace({'st@tus':{True:"edit", False: "none"}},inplace=True)
        result = df_left.to_json(orient="records",index=False)
        parsed = json.loads(result)
        
        #processed_data = {"received_data":jsonify(parsed), "response": "Processed successfully"} 
        #processed_data = {}

        #Respond with a JSON response
        return jsonify(parsed),200
    except Exception as e:
        #Respond with an error message if something goes wrong
        return jsonify({"error":str(e)}),400


#if user confirm to clean data
@app.route('/removeirrdata/clean',methods = ["POST"])
def removeIrrelevantData_clean():
    try:
        # Receive JSON data from another host
        read_data = request.get_json()
        # this one read what columns user want to do
        data_match = read_data["data_set"]["columns_match"]
        #retrieve the dataset from database
        data = read_data["data_set"]["rows"]
        # add logic here

        df = pd.DataFrame(data)
        df.drop(data_match,axis= 1,inplace=True)
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        
       # processed_data = {"received_data":jsonify(parsed), "response": "Processed successfully"} 
        #processed_data = {}

        #Respond with a JSON response
        return jsonify(parsed), 200
    
    except Exception as e:
        #Respond with an error message if something goes wrong
        return jsonify({"error":str(e)}),400

#function 2 removeduplicatedata
@app.route('/removedupdata/check',methods = ['POST'])
def removeDuplicateData_check():
    try:
        # Receive JSON data from another host
        read_data = request.get_json()
        # this one read what columns user want to do
        #data_match = read_data["data_set"]["columns_match"] # function นี้ไม่ต้องมี 
        #retrieve the dataset from database
        data = read_data["data_set"]["rows"]
        # add logic here

        df = pd.DataFrame(data)
        df.insert(0,"st@tus",df.duplicated())
        df.replace({'st@tus':{True: "delete", False : "none"}},inplace=True)
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)

        #processed_data = {}

        #Respond with a JSON response
        return jsonify(parsed),200

    except Exception as e:
        #Respond with an error message if something goes wrong
        return jsonify({"error":str(e)}),400

# Function 2 RemoveDuplicateData
@app.route('/removedupdata/clean',methods = ['POST'])
def removeDuplicateData_clean():
    try:
        # Receive JSON data from another host
        read_data = request.get_json()
        # this one read what columns user want to do
        #data_match = read_data["data_set"]["columns_match"] # function นี้ไม่ต้องมี 
        #retrieve the dataset from database
        data = read_data["data_set"]["rows"]
        # add logic here

        df = pd.DataFrame(data)
        df.drop_duplicates(inplace=True)
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)

        #Respond with a JSON response
        return jsonify(parsed),200

    except Exception as e:
        #Respond with an error message if something goes wrong
        return jsonify({"error":str(e)}),400

#
if __name__ == "__main__":
    app.run(port=8080)

