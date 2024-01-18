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
    print("hello, this is first page")
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
        return json.dumps(parsed,ensure_ascii=False),200
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
        return json.dumps(parsed,ensure_ascii=False), 200
    
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
        print(df.columns.values)
        df.insert(0,"st@tus",df.duplicated())
        df.replace({'st@tus':{True: "delete", False : "none"}},inplace=True)
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)

        #processed_data = {}

        #Respond with a JSON response
        return json.dumps(parsed,ensure_ascii=False),200

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
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        #Respond with an error message if something goes wrong
        return jsonify({"error":str(e)}),400

# Function ที่ 3 Edit Inconsistant Data มีทั้งหมด 3 เส้น
# พอเราคลิกเสร็จให้แสดงคอลัมน์ทุกอัน * เลือกได้แค่คอลัมน์เดียวเท่านั้น
@app.route('/editincdata/',methods= ['GET'])
def getAllUniqueValue():
    try:
        column = str(request.args.get('column'))
        #data_set = {"columns",f'{column}'}
        read_data = request.get_json()
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        df_unique = df[column].unique()
        data_set = {"column" : df_unique.tolist()}
        return json.dumps(data_set,ensure_ascii=False),200
    
    except Exception as e:
        return jsonify({"error":str(e)}),400
# อันนี้คือเป็นหน้าให้ผู้ใช้ยืนยัน
@app.route('/editincdata/check',methods = ["POST"]) #ถามเฟ้นว่าทำแบบไหนง่ายกว่ากัน
def editInconsistantData_check():
    try:
        column = str(request.args.get('column'))
        #data_select, data_change รับมาจาก json ที่แนบมาละกัน
        read_data = request.get_json()
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        #ต้องเพิ่ม 2 Keys ลงไปใน json อีก
        data_select = read_data["data_set"]["data_select"]
        data_change = read_data["data_set"]["data_change"]
        df.insert(0,"st@tus",df[column] == data_select)
        df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)
        df[column].replace(data_select,data_change,inplace=True)
        
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
#        #Respond with a JSON response
        return json.dumps(parsed,ensure_ascii=False),200
#อันนี้เป็นหน้าที่หลังจากยืนยันแล้ว
#
    except Exception as e:
        return jsonify({"error":str(e)}),400
#        
@app.route('/editincdata/clean',methods = ["POST"])
def editInconsistantData_clean():
    try:
        column = str(request.args.get('column'))
        read_data = request.get_json()
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        #ต้องเพิ่ม 2 Keys ลงไปใน json อีก
        data_select = read_data["data_set"]["data_select"]
        data_change = read_data["data_set"]["data_change"]
        df[column].replace(data_select,data_change,inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
#        #Respond with a JSON response
        return json.dumps(parsed,ensure_ascii=False),200
    
    except Exception as e:
        return jsonify({"error":str(e)}),400
if __name__ == "__main__":
    app.run(debug=True,port=8080)

