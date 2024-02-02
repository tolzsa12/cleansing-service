from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from pandas.api.types import is_object_dtype, is_numeric_dtype, is_bool_dtype
import statistics as stat
import numpy as np

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# ทดลองใช้ SwaggerUI 

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
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
# พอเราคลิกเสร็จให้แสดงคอลัมน์ทุกอัน * เลือกได้แค่คอลัมน์เดียวเท่านั้น
@app.route('/editincdata',methods= ['POST']) 
def getAllUniqueValue():
    try:
        #column = str(request.args.get('column'))
       
        #data_set = {"columns",f'{column}'}
        read_data = request.get_json()
        column = read_data["data_set"]["columns_match"]
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
       
        #data_select, data_change รับมาจาก json ที่แนบมาละกัน
        read_data = request.get_json()
         #column = str(request.args.get('column'))
        # อันนี้รับมาแค่ column เดียวเท่านั้น
        columns = read_data["data_set"]["columns_match"]

        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        #ต้องเพิ่ม 2 Keys ลงไปใน json อีก
        data_select = read_data["data_set"]["data_select"]
        data_change = read_data["data_set"]["data_change"]

        # ลองเปลี่ยนค่า input ที่เข้ามาเป็นตัวเลข
        if (isint(data_change)):
            data_change = int(data_change)
        elif (isfloat(data_change)):
            data_change = float(data_change)

        
        df.insert(0,"st@tus",df[columns] == data_select)
        df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)
        #df[column].replace(data_select,data_change,inplace=True)
        for col in columns:
            df.replace({col : {data_select: data_change}},inplace=True)
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
        #column = str(request.args.get('column'))
        # อันนี้รับมาแค่ column เดียวเท่านั้น
        read_data = request.get_json()
         #column = str(request.args.get('column'))
        # อันนี้รับมาแค่ column เดียวเท่านั้น
        columns = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        #ต้องเพิ่ม 2 Keys ลงไปใน json อีก
        data_select = read_data["data_set"]["data_select"]
        data_change = read_data["data_set"]["data_change"]

         # ลองเปลี่ยนค่า input ที่เข้ามาเป็นตัวเลข
        if (isint(data_change)):
            data_change = int(data_change)
        elif (isfloat(data_change)):
            data_change = float(data_change)
        for col in columns:
            df.replace({col : {data_select: data_change}},inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
#        #Respond with a JSON response
        return json.dumps(parsed,ensure_ascii=False),200
    
    except Exception as e:
        return jsonify({"error":str(e)}),400
# Function ที่ 4 Managing Na Value

# api เส้นที่ 4 manageNaValue
@app.route('/managenavalue/check',methods = ["POST"])
def manageNaValue_check():
    try:
        read_data = request.get_json()
        columns_match = read_data["data_set"]["columns_match"] #เลือกคอลัมน์อะไร
        data = read_data["data_set"]["rows"]
        order_select = read_data["data_set"]["order_select"] #เลือกคำสั่งอะไร


        df = pd.DataFrame(data)
        if order_select == "mean":
        # เราต้องเช็ค NA ตรงนี้
            df.insert(0,"st@tus",df[columns_match].isna().any(axis=1))
            df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)
            for col in columns_match:
                if (is_numeric_dtype(df[col])):
                    mean_value = df[col].mean()
                     #print(mean_value)
                    df[col] = df[col].fillna(mean_value)
                else:
                    mean_value = df[col].mode()[0]
                    df[col] = df[col].fillna(mean_value)

        elif order_select == "median":
        # เราต้องเช็ค NA ตรงนี้
            df.insert(0,"st@tus",df[columns_match].isna().any(axis=1))
            df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)
            for col in columns_match:
                if (is_numeric_dtype(df[col])):
                    median_value = stat.median(df[col])
                     #print(mean_value)
                    df[col] = df[col].fillna(median_value)
                else: #ใช้แบบเดียวกับ mean ไปเลย
                    mean_value = df[col].mode()[0]
                    df[col] = df[col].fillna(mean_value)

        elif order_select == "remove":
             # อันนี้เช็ค NA ยาก
            remove_from_list = []
            for col in columns_match:
                nan_count = df[col].isna().sum() #นับจำนวน nan ทั้งหมดใน dataframe
                print(nan_count)
                print(len(df)) # อันนี้ไว้นับจำนวนทั้งหมด
                #กรองก่อน เหลืออันไหนที่ทำได้ เราทำให้หมดเลย
                if(nan_count / len(df) > 0.1):
                    remove_from_list = remove_from_list + [col]
            for col in remove_from_list:
                columns_match.remove(col)
            df.insert(0,"st@tus",df[columns_match].isna().any(axis=1))
            df.replace({'st@tus':{True: "delete", False : "none"}},inplace=True)
            
        else:
            # check NA ตรงนี้
            df.insert(0,"st@tus",df[columns_match].isna().any(axis=1))
            df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)
            if (isint(order_select)):
                for col in columns_match:
                    df[col] = df[col].fillna(int(order_select))
            elif (isfloat(order_select)):
                for col in columns_match:
                    df[col] = df[col].fillna(float(order_select))
            else:
                for col in columns_match:
                    df[col] = df[col].fillna(order_select)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)

        return json.dumps(parsed,ensure_ascii=False),200


    except Exception as e:
        return jsonify({"error":str(e)}),400
            






@app.route('/managenavalue/clean',methods = ["POST"])
def manageNaValue_clean():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"] #เลือกคอลัมน์อะไร
        data = read_data["data_set"]["rows"]
        order_select = read_data["data_set"]["order_select"] #เลือกคำสั่งอะไร

        df = pd.DataFrame(data)
        # order_select มี 4 ตัว mean median remove และอื่นๆ (เติมค่าที่กรอกนั่นละ)
        if order_select == "mean":
            for col in columns_match:
                if (is_numeric_dtype(df[col])):
                    mean_value = df[col].mean()
                     #print(mean_value)
                    df[col] = df[col].fillna(mean_value)
                else:
                    mean_value = df[col].mode()[0]
                    df[col] = df[col].fillna(mean_value)
            
        elif order_select == "median":
            for col in columns_match:
                if (is_numeric_dtype(df[col])):
                    median_value = stat.median(df[col])
                     #print(mean_value)
                    df[col] = df[col].fillna(median_value)
                else: #ใช้แบบเดียวกับ mean ไปเลย
                    mean_value = df[col].mode()[0]
                    df[col] = df[col].fillna(mean_value)
        elif order_select == "remove":
             for col in columns_match:
                 nan_count = df[col].isna().sum() # อันนี้เพื่อนับจำนวน  nan ทั้งหมด ในdataframe
                 print(nan_count)
                 print(len(df)) # อันนี้ไว้นับจำนวนทั้งหมด
                 if (nan_count / len(df) <= 0.1):
                     df = df[df[col].notna()]
        else:
            if (isint(order_select)):
                for col in columns_match:
                    df[col] = df[col].fillna(int(order_select))
            elif (isfloat(order_select)):
                for col in columns_match:
                    df[col] = df[col].fillna(float(order_select))
            else:
                for col in columns_match:
                    df[col] = df[col].fillna(order_select)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200
        

    except Exception as e:
        return jsonify({"error":str(e)}),400

## Function ที่ 5 Split Columns แยกคอลัมน์
@app.route('/splitcolumn/check',methods = ["POST"])
def splitColumn_check():
    try:
        # อาจจะมีการแบ่งเป็น String อย่างเดียวหรือว่าจะให้สามารถแบ่งจุดทศนิยมออกด้วยดีไหมนะ
        
        read_data = request.get_json()

        column_match = read_data["data_set"]["columns_match"] #เลือกคอลัมน์อะไร
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        column_1 = read_data["data_set"]["column_1"]
        column_2 = read_data["data_set"]["column_2"]
        delimiter = read_data["data_set"]["delimiter"]

        df.insert(0,"st@tus",False)
        if (not is_numeric_dtype(df[column_match])):
            df[[column_1,column_2]] = df[column_match].str.split(delimiter,expand = True, n = 1) #กำหนด n = 1 เพื่อให้แบ่งแค่ทีละ 2 อัน
            col_index = df.columns.tolist().index(column_match)
            df.insert(col_index+1,column_1,df.pop(column_1))
            df.insert(col_index+2,column_2,df.pop(column_2))
            df["st@tus"] = True
        df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)

        
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

        
    except Exception as e:
        return jsonify({"error":str(e)}),400
    

@app.route('/splitcolumn/clean',methods = ["POST"])
def splitColumn_clean():

    try:
        read_data = request.get_json()

        column_match = read_data["data_set"]["columns_match"] #เลือกคอลัมน์อะไร
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        column_1 = read_data["data_set"]["column_1"]
        column_2 = read_data["data_set"]["column_2"]
        delimiter = read_data["data_set"]["delimiter"]

        if (not is_numeric_dtype(df[column_match])):
            df[[column_1,column_2]] = df[column_match].str.split(delimiter,expand = True, n = 1) #กำหนด n = 1 เพื่อให้แบ่งแค่ทีละ 2 อัน
            col_index = df.columns.tolist().index(column_match)
            df.insert(col_index+1,column_1,df.pop(column_1))
            df.insert(col_index+2,column_2,df.pop(column_2))
        
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

        
    except Exception as e:
        return jsonify({"error":str(e)}),400



## Function ที่ 6 Replace Excess Categories with “Other”) 
@app.route('/replaceexcdata/check',methods = ["POST"])
def replaceExcData_check():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"] #เลือกคอลัมน์อะไร
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        
        #เก็บค่า index เอาไว้มั้ย แล้วเราค่อยเอามาเพิ่ม + แปลงให้เป็น set ก่อน เพื่อตัดตัวซ้ำทิ้ง
        #indices = [0,1,3,6,10,15]
        #df.loc[indices,'A'] = 16
        status_index = []
        for col in columns_match:
            if not (is_numeric_dtype(df[col])):
                values, counts = np.unique(list(df[col].dropna()),return_counts= True)
                count_sort_ind = np.argsort(-counts)

                list_unique = values[count_sort_ind] 
                list_keep = list_unique[0:5]  # จะเอากี่อันก็เปลี่ยนเลข 5 เป็นเลขอื่นเอา
             
                status_index = status_index + np.flatnonzero(~df[col].isin(list_keep)).tolist()
                df.loc[~df[col].isin(list_keep),col] = "อื่น ๆ" 
                #df.insert(0,"st@tus",~df[col].isin(list_keep))
                #  เก็บเป็นเซ็ตมั้ย ว่า index ไหนต้องเปลี่ยน
        
        status_index = list(set(status_index))
        df.loc[df.index.isin(status_index), 'st@tus'] = True
        df.loc[~df.index.isin(status_index), 'st@tus'] = False
        df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error":str(e)}),400


@app.route('/replaceexcdata/clean',methods = ["POST"])
def replaceExcData_clean():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"] #เลือกคอลัมน์อะไร
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        
        #ถ้าสมมุติสร้าง column มาเก็บ true กับ false แล้วสุดท้ายแล้วเอาทุกตัวมา .any() ได้มั้ยอ่ะ
        for col in columns_match:
            if not (is_numeric_dtype(df[col])):
                values, counts = np.unique(list(df[col].dropna()),return_counts= True)
                count_sort_ind = np.argsort(-counts)
                list_unique = values[count_sort_ind] 
                list_keep = list_unique[0:5]  
                df.loc[~df[col].isin(list_keep),col] = "อื่น ๆ" 
               
        
        
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error":str(e)}),400
    
## Function ที่ 7 ลบข้อมูลที่ไม่ใช่ตัวเลขออก Remove Unreadable Numbers
@app.route('/removeunrnumber/check', methods = ["POST"])
def removeUnreadableNumbers_check():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)

        #
        df.insert(0,"st@tus",False)
        for col in columns_match:
            if (is_object_dtype(df[col])):
                df.loc[:,col] = df[col].apply(lambda x: float(x) if isfloat(x) else x) # หน้าเท่ากับคือบอกว่าให้มาแทนค่าตัวเดิม
                df["st@tus"] = df["st@tus"] | df[col].apply(lambda x: not isinstance(x,(int,float,bool)))
                #print(col)
        df.replace({'st@tus':{True: "delete", False : "none"}},inplace=True)
                
        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error" : str(e)}),400


@app.route('/removeunrnumber/clean',methods = ["POST"])
def removeUnreadableNumbers_clean():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)

        for col in columns_match:
            if (is_object_dtype(df[col])):
                
                df.loc[:,col] = df[col].apply(lambda x: float(x) if isfloat(x) else x) # หน้าเท่ากับคือบอกว่าให้มาแทนค่าตัวเดิม
                index_delete = df[~df[col].apply(lambda x: isinstance(x,(int,float,bool)))].index
                df.drop(index_delete,inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200
                
        
    
    except Exception as e:
        return jsonify({"error": str(e) }),400

# Function ที่ 8 Flag Outlier ระบุค่าผิดปกติทางสถิติ
@app.route('/flagoutlier/check',methods = ["POST"])
def flagOutliers_check():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)

        df.insert(0,"st@tus","none")

        for col in columns_match:
            if(is_numeric_dtype(df[col])):
                
                col_isoutlier = col + '_isoutlier'
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                # ไปหาเพิ่มเติมว่า ddof คืออะไร ส่งผลต่อการคำนวณมั้ย
                #เพื่อทดสอบว่ามันทำงานได้มั้ย เรา จะ set treshold ไว้ที่ 1 ก่อน แต่โดยปกติแล้วเรามักจะใช้ 3 นะ
                df[col_isoutlier] = df[col].apply(lambda x: (x < (Q1 - 1.5* IQR)) | (x > (Q3 + 1.5 *IQR)))
                #outlier_indices = np.where(df[col_zscore] > z_treshold)[0]
                df.replace({col_isoutlier:{True: 1, False : 0}},inplace=True)
                #no_outliers = df.drop(outlier_indices)
                col_index = df.columns.tolist().index(col)
                df.insert(col_index+1, col_isoutlier, df.pop(col_isoutlier))
                df["st@tus"] = "edit"

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error": str(e)}),400


@app.route('/flagoutlier/clean',methods = ["POST"])
def flagOutliers_clean():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)

        
        for col in columns_match:
            if(is_numeric_dtype(df[col])):
                
                col_isoutlier = col + '_isoutlier'
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                #เพื่อทดสอบว่ามันทำงานได้มั้ย เรา จะ set treshold ไว้ที่ 1 ก่อน แต่โดยปกติแล้วเรามักจะใช้ 3 นะ
                df[col_isoutlier] = df[col].apply(lambda x: (x < (Q1 - 1.5* IQR)) | (x > (Q3 + 1.5 *IQR)))
                df.replace({col_isoutlier:{True: 1, False : 0}},inplace=True)
                
                col_index = df.columns.tolist().index(col)
                df.insert(col_index+1, col_isoutlier, df.pop(col_isoutlier))

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error": str(e)}),400
    
#Function ที่ 9 Remove Outlier เอาที่ผิดปกติออก
@app.route('/removeoutlier/check',methods = ["POST"])
def removeOutlier_check():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)

        df.insert(0,"st@tus",False)
        for col in columns_match:
            if (is_numeric_dtype(df[col])):
                #col_zscore = col + ''
                #col_isoutlier = col + '_isoutlier'
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1

                df["st@tus"] = df["st@tus"] | df[col].apply(lambda x: (x <= (Q1 - 1.5* IQR)) | (x >= (Q3 + 1.5 *IQR)))
        
        df.replace({'st@tus':{True: "delete", False : "none"}},inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error": str(e)}),400
    
@app.route('/removeoutlier/clean',methods = ["POST"])
def removeOutlier_clean():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data) 
        
        df.insert(0,"st@tus",False)
        for col in columns_match:
            if (is_numeric_dtype(df[col])):
                #col_zscore = col + ''
                #col_isoutlier = col + '_isoutlier'
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1

                df["st@tus"] = df["st@tus"] | df[col].apply(lambda x: (x <= (Q1 - 1.5* IQR)) | (x >= (Q3 + 1.5 *IQR)))

        df = df[~df["st@tus"]]
        df.drop("st@tus",axis= 1,inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200
    
    except Exception as e:
        return jsonify({"error": str(e)}),400

#Function ที่ 10 Clamp Outlier ตัดค่าผิดปกติไปอยู่ตรง
@app.route('/changeoutlier/check',methods = ["POST"])
def changeOutlier_check():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data)
        order_select = read_data["data_set"]["order_select"] #เลือกคำสั่งอะไร

        df.insert(0,"st@tus",False)
        if order_select == "clamp":
        
            for col in columns_match:
                if (is_numeric_dtype(df[col])):
               
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1

                    df["st@tus"] = df["st@tus"] | df[col].apply(lambda x: (x <= (Q1 - 1.5* IQR)) | (x >= (Q3 + 1.5 *IQR)))
                    df.loc[df[col] < (Q1 - 1.5* IQR),col] = Q1 - 1.5 * IQR
                    df.loc[df[col] > (Q3 + 1.5* IQR),col] = Q3 + 1.5 * IQR

        else:
            if (isint(order_select)):
                order_select = int(order_select)
            elif (isfloat(order_select)):
                order_select = float(order_select)

            for col in columns_match:
                 if (is_numeric_dtype(df[col])):

                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1

                    df["st@tus"] = df["st@tus"] | df[col].apply(lambda x: (x <= (Q1 - 1.5* IQR)) | (x >= (Q3 + 1.5 *IQR)))
                    df.loc[df[col] < (Q1 - 1.5* IQR),col] = order_select
                    df.loc[df[col] > (Q3 + 1.5* IQR),col] = order_select                  

        df.replace({'st@tus':{True: "edit", False : "none"}},inplace=True)

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200
    
    except Exception as e:
        return jsonify({"error": str(e)}),400
    

@app.route('/changeoutlier/clean',methods = ["POST"])
def changeOutlier_clean():
    try:
        read_data = request.get_json()

        columns_match = read_data["data_set"]["columns_match"]
        data = read_data["data_set"]["rows"]
        df = pd.DataFrame(data) 
        order_select = read_data["data_set"]["order_select"] #เลือกคำสั่งอะไร

        if order_select == "clamp":
        
            for col in columns_match:
                if (is_numeric_dtype(df[col])):
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1

                    df.loc[df[col] < (Q1 - 1.5* IQR),col] = Q1 - 1.5 * IQR
                    df.loc[df[col] > (Q3 + 1.5* IQR),col] = Q3 + 1.5 * IQR         

        else:
            if (isint(order_select)):
                order_select = int(order_select)
            elif (isfloat(order_select)):
                order_select = float(order_select)

            for col in columns_match:
                 if (is_numeric_dtype(df[col])):

                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1


                    df.loc[df[col] < (Q1 - 1.5* IQR),col] = order_select
                    df.loc[df[col] > (Q3 + 1.5* IQR),col] = order_select    

        result = df.to_json(orient="records",index=False)
        parsed = json.loads(result)
        return json.dumps(parsed,ensure_ascii=False),200

    except Exception as e:
        return jsonify({"error":str(e)}),400

if __name__ == "__main__":
    app.run(debug=True,port=8080)

