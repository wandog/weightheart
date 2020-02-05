# -*- coding: UTF-8 -*-
from __future__ import print_function
from flask import Flask, render_template,request,g, make_response
from accout import account_api
from flask import jsonify
import json
import sqlite3
import sys,random
import base64
import pyqrcode
from datetime import date

reload(sys)
sys.setdefaultencoding('utf-8')
# import make_response

#test

app = Flask(__name__)

# app.register_blueprint(account_api)


def convert_and_save(b64_string,filename):
    with open(filename+'.png', "wb") as fh:
        fh.write(base64.standard_b64decode(b64_string))

# def get_db():
#     # global dbq
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect('test.db')
#         # Enable foreign key check
#         db.execute("PRAGMA foreign_keys = ON")
#     return db

def get_db():
    # global dbq
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect('test.db',timeout=10.0)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
        return db


# @app.teardown_appcontext
# def close_connection(exception):
#     # global db
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()



@app.route("/show_qrcode",methods=['GET'])
def show_qrcode():
    id = request.args.get('id')
    name = request.args.get('name')
    # print("id is %s"%id,file=sys.stderr)
    return render_template('qr_code.html',memberid=id,name=name)



@app.route("/gen_qrcode",methods=['POST'])
def gen_qrcode():
    memberid=request.json['memberID']
    # print(memberid,file=sys.stderr)
    # s=memberid
    # s="test"
    url=pyqrcode.create(memberid)
    result=url.svg('static/qrcode/%s.svg' %memberid,scale=9)
    # result=url.svg('gg.svg',scale=8)
    # print(result,file=sys.stderr)
    if result is None:
        return 'qrcode gen ok'
    else:
        return "qrcode gen fail"
    # return result

@app.route("/id_exist_check", methods = ['POST'])
def id_exist_check():
    memberid=request.json['id'].lower()
    # print(memberid,file=sys.stderr)
    db=get_db()
    with db:
        result=db.execute("select id from members where id=?",(memberid,)).fetchall()
        # print(result,file=sys.stderr)
        if len(result) != 0:
            return "ok"
        else:
            return "fail"


@app.route("/staff_id_exist_check", methods = ['POST'])
def staff_id_exist_check():
    staffid=request.json['id'].lower()
    # print(memberid,file=sys.stderr)
    db=get_db()
    with db:
        result=db.execute("select id from staff where id=?",(staffid,)).fetchall()
        # print(result,file=sys.stderr)
        if len(result) != 0:
            return "ok"
        else:
            return "fail"



@app.route("/save_trans", methods = ['POST'])
def save_trans():
    memberid=request.json['memberid']
    staffid=request.json['staffid']
    startdate=request.json['startdate']
    price=request.json['price']
    membertype=request.json['membertype']
    quotaadded=request.json['quotaadded']
    enddate=request.json['enddate']      
    db=get_db()
    with db:

        if(membertype=="times"):    #自主計次 enddate not needed, quota needed
            db.execute("insert into trans (memberid, staffid, startdate, price, membertype) values(?,?,?,?,?)",(memberid,staffid,startdate,price,membertype))
            db.commit()
            db.execute("update members set quota=quota+? where id=?",(quotaadded,memberid))    
            db.commit()
            result=db.execute('select quota from members where id=?',(memberid,)).fetchone()
            if result:
                return "自主計次加值成功 剩餘次數為"+str(result[0])
            else:
                return "自主次數加值出了問題"

        elif(membertype=="normal"):  #自主年費 enddate neeeded, quota not needed
            # enddate=request.json['enddate']
            db.execute("insert into trans (memberid, staffid, startdate,price,enddate,membertype) values(?,?,?,?,?,?)",(memberid,staffid,startdate,price,enddate,membertype))
            db.commit()
            return "自主年費型合約成立!"

        elif(membertype=="vip"):   #小班月費 enddate needed, quota not needed
            db.execute("insert into trans (memberid, staffid, startdate,price,enddate,membertype) values(?,?,?,?,?,?)",(memberid,staffid,startdate,price,enddate,membertype))
            db.commit()
            return "小班月費合約成立!"
        elif(membertype=="tran_little"):    #小班計次 enddate not needed, quota needed    
            db.execute("insert into trans (memberid, staffid, startdate, price, membertype) values(?,?,?,?,?)",(memberid,staffid,startdate,price,membertype))
            db.commit()
            db.execute("update members set quota_tran_little=quota_tran_little+? where id=?",(quotaadded,memberid))    
            db.commit()
            result=db.execute('select quota_tran_little from members where id=?',(memberid,)).fetchone()
            if result:
                return "小班計次加值成功 剩餘次數為"+str(result[0])
            else:
                return "小班計次加值加值出了問題"


        elif(membertype=="course_limit"):  #enddate and quota both needed
            db.execute("insert into trans (memberid, staffid, startdate, price, membertype, enddate, quota_course_limit) values(?,?,?,?,?,?,?)",(memberid,staffid,startdate,price,membertype,enddate,quotaadded))
            db.commit()
            # db.execute("update members set quota_course_limit=quota_course_limit+? where id=?",(quotaadded,memberid))    
            # db.commit()
            result=db.execute('select quota_course_limit from trans where memberid=? order by startdate desc',(memberid,)).fetchone()
            if result:
                return "有限期教練課加值成功 儲值次數為"+str(result[0])
            else:
                return "有限期教練課加值加值出了問題"
        elif(membertype=="course"): #endate not needed, quota needed
            db.execute("insert into trans (memberid, staffid, startdate, price, membertype) values(?,?,?,?,?)",(memberid,staffid,startdate,price,membertype))
            db.commit()
            db.execute("update members set quota_course=quota_course+? where id=?",(quotaadded,memberid))    
            db.commit()
            result=db.execute('select quota_course from members where id=?',(memberid,)).fetchone()
            if result:
                return "無限期教練課加值成功 剩餘次數為"+str(result[0])
            else:
                return "無限期教練課加值加值出了問題"
        else:
            return "繳費系統錯誤"
        
        # try:    #計次
        #     quotaadded=request.json['quotaadded']      
        # except: #present 年費
        #     enddate=request.json['enddate']
        #     db.execute("insert into trans (memberid, staffid, startdate,price,enddate,membertype) values(?,?,?,?,?,?)",(memberid,staffid,startdate,price,enddate,membertype))
        #     db.commit()

        #     return "年費型合約成立!"
        # else:
        #     db.execute("insert into trans (memberid, staffid, startdate, price,membertype) values(?,?,?,?,?)",(memberid,staffid,startdate,price,membertype))
        #     db.commit()
        #     db.execute("update members set quota=quota+? where id=?",(quotaadded,memberid))    
        #     db.commit()
        #     result=db.execute('select quota from members where id=?',(memberid,)).fetchone()
        #     if result:
        #         return "計次加值成功 剩餘次數為"+str(result[0])
        #     else:
        #         return "次數加值出了問題"
    
    



@app.route("/savecanvas", methods = ['GET', 'POST'])
def savecanvas():
    filename=request.json['filename']
    img=request.json['imgBase64']
    # print(img,sys.stderr)
    img=img.replace("data:image/png;base64,", "")
    convert_and_save(img,'static/photo/%s' %filename)
    return "filesave ok!"

@app.route("/index")
def index():
    return render_template('index.html',topbar="重心健身房管理系統")

@app.route("/bulletin")
def bulletin():
    msg=["","",""]
    count=0
    db=get_db()
    with db:
        result=db.execute("select content from bulletin").fetchall()
        for row in result:
            msg[count]=row[0]
            count=count+1
            
        print("%s %s %s" %(msg[0],msg[1],msg[2]),file=sys.stderr)
        return render_template('bulletin.html',topbar="電子佈告欄系統",b0=msg[0],b1=msg[1],b2=msg[2])

@app.route("/saveBulletin", methods=['POST'])
def saveBulletin():
    print("get in ajax",file=sys.stderr)
    bulletin0=request.json['con_0']
    bulletin1=request.json['con_1']
    bulletin2=request.json['con_2']
    
    db=get_db()
    with db:
        db.execute("UPDATE bulletin SET content=? WHERE b_num=1",(bulletin0,))
        db.execute("UPDATE bulletin SET content=? WHERE b_num=2",(bulletin1,))
        db.execute("UPDATE bulletin SET content=? WHERE b_num=3",(bulletin2,))
        db.commit()

        # print("input is %s" %bulletin0,file=sys.stderr)
        return "ok"



#to get the latest id number
@app.route("/getLastID",methods=["POST"])
def getLastMemID():
    # select * from members order by id desc;
    target_1=request.json["target"]
    # print("target_1 is %s" %target_1,file=sys.stderr) 
    db=get_db()
    with db:
        if target_1=="memberid":
            result=db.execute("select id from members order by id desc limit 1").fetchone()
        elif target_1=="staffid":
            result=db.execute("select id from staff order by id desc limit 1").fetchone()
        else:
            return "something wrong!"
            # result=db.execute("select id from staff order by id desc limit 1").fetchone()
        
        return result[0]


@app.route('/getTransRec', methods = ['GET', 'POST'])
def getTransRec():
    memberid=request.json['id']
    db=get_db()
    with db:
        result=db.execute('select transid, startdate,enddate,price,staffid, name, timestamp, membertype from trans cross join staff where trans.staffid=staff.id and trans.memberid=?',
        (memberid, )).fetchall()
        return jsonify(result)

# show the data of members
@app.route('/member', methods = ['GET', 'POST'])
def member():
    if request.method == 'POST':
        memberid = request.form['memberID'].lower()
        # nationid = request.form['nationID']
        if request.form['submit'] == 'queryPersonData':
            # flash("Successful login", "success")
            db=get_db()
            with db:
                result=db.execute("select name,birth,type,phone,agent_name,agent_phone,agent_relation,address,nationID from members where id=?",(memberid,)).fetchone()
                # result=db.execute("select name from members where id=?",(memberid,)).fetchone()
                result_1=db.execute('select transid, startdate,price,staffid, name, timestamp,enddate,membertype from trans cross join staff where trans.staffid=staff.id and trans.memberid=?',(memberid, )).fetchall()
                result_2=db.execute('select id,name from staff').fetchall()

                # for x in range(len(result_1)):
                #     for y in range(8):
                #         if result_1[x][y]=="normal":
                #             result_1[x][y]="自主月費"

                resp =make_response(render_template('member_data.html',topbar="會員資料",
                memberid=memberid,name=result[0],birth_1=result[1],phone=result[3],
                type_1=result[2],emerName=result[4],emerPhone=result[5],relation=result[6],address=result[7],nationid=result[8],
                trans=result_1,staff=result_2))
                return resp
        elif request.form['submit'] == 'queryGetInLog':
            db=get_db()
            with db:
                result=db.execute("select * from membergetinlog where memberid=? order by timestamp desc",(memberid, )).fetchall()
                if result:
                    return render_template('getinlog.html', topbar="會員入場紀錄", memberid=memberid, result=result)
                else:
                    logexist="此會員沒有入場紀錄"
                    return render_template('getinlog.html', topbar="會員入場紀錄", memberid=memberid, result=result,logexist=logexist)
        else:
            return "錯誤"

@app.route('/employee', methods = ['GET', 'POST'])
def employee():
    if request.method == 'POST':
        staffid = request.form['staffID'].lower()
        nationid = request.form['nationID'].upper()
        # nationid = request.form['nationID']
        if request.form['submit'] == 'queryStaffData':
            # flash("Successful login", "success")
            db=get_db()
            with db:
                result=db.execute("select name,birth,role,phone,agent_name,agent_phone,agent_relation,address,nationID from staff where id=?",(staffid,)).fetchone()
                if result:
                    pass
                else:
                    result=db.execute("select name,birth,role,phone,agent_name,agent_phone,agent_relation,address,nationID from staff where nationID=?",(nationid,)).fetchone()
                
                    if not result:
                        return "無此員工"    

                resp =make_response(render_template('staff_data.html',topbar="員工資料",
                staffid=staffid,name=result[0],birth_1=result[1],phone=result[3],
                type_1=result[2],emerName=result[4],emerPhone=result[5],relation=result[6],address=result[7],nationid=result[8]))
                return resp
        elif request.form['submit'] == 'queryStaffGetInLog':
            pass
            # db=get_db()
            # result=db.execute("select * from membergetinlog where memberid=? order by timestamp desc",(memberid, )).fetchall()
            # if result:
            #     return render_template('getinlog.html', topbar="會員入場紀錄", memberid=memberid, result=result)
            # else:
            #     logexist="此會員沒有入場紀錄"
            #     return render_template('getinlog.html', topbar="會員入場紀錄", memberid=memberid, result=result,logexist=logexist)
        elif request.form['submit'] == 'queryCourseBooking':   
            pass
        else:
            return "錯誤"

# for 自主計次型入場
@app.route("/memberGetInTimes",methods=['GET','POST'])
def memeberGetInTimes():
    memberid=request.json['id']
    # today=request.json['date']
    print("id is %s"%(memberid),file=sys.stderr)
    
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            quotaminus=checkQuotaNMinus(memberid,db,"times")
            if quotaminus==-1:
                return "此會員自主計次次數為0 須加值"
            else:
                db.execute("insert into membergetinlog (memberid, quota,membertype) values (?,?,?)",(memberid,quotaminus,"times"))
                db.commit()
                return "此會員自主計次儲值次數扣點後為"+str(quotaminus)
            
        else:
            return "沒有此會員"


# for 小班計次型入場
@app.route("/TranLittleGetInTimes",methods=['GET','POST'])
def TranLittleGetInTimes():
    memberid=request.json['id']
    # today=request.json['date']
    print("id is %s"%(memberid),file=sys.stderr)
    
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            quotaminus=checkQuotaNMinus(memberid,db,"tran_little")
            if quotaminus==-1:
                return "此會員小班計次儲值次數為0 須加值"
            else:
                db.execute("insert into membergetinlog (memberid, quota, membertype) values (?,?,?)",(memberid,quotaminus,"tran_little"))
                db.commit()
                return "此會員小班計次儲值次數扣點後為"+str(quotaminus)
            
        else:
            return "沒有此會員"


# for 無限期教練課入場
@app.route("/CourseGetInTimes",methods=['GET','POST'])
def CourseGetInTimes():
    memberid=request.json['id']
    # today=request.json['date']
    print("id is %s"%(memberid),file=sys.stderr)
    
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            quotaminus=checkQuotaNMinus(memberid,db,"course")
            if quotaminus==-1:
                return "此會員無限期教練課計次儲值次數為0 須加值"
            else:
                db.execute("insert into membergetinlog (memberid, quota,membertype) values (?,?,?)",(memberid,quotaminus,"course"))
                db.commit()
                return "此會員無限期教練課計次儲值次數扣點後為"+str(quotaminus)
            
        else:
            return "沒有此會員"


# for 有限期教練課入場
@app.route("/CourseLimitGetInTimes",methods=['GET','POST'])
def CourseLimitGetInTimes():
    memberid=request.json['id']
    today=request.json['date']
    membertype="course_limit"
    print("id is %s"%(memberid),file=sys.stderr)
    print("get in course limit",file=sys.stderr)
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            value_ret=checkifmemberValid_course_limit(result[0],today,db)
            if(value_ret[0]==0):
                # db.execute("insert into membergetinlog (memberid) values (?)",(memberid,))
                # db.commit()
                startdate=value_ret[1]
                enddate=value_ret[2]
                quotaminus=checkQuotaNMinus_course_limit(memberid,str(startdate),str(enddate),db)
                # return quotaminus
                if quotaminus==-1:
                    return "此會員限期教練課計次儲值次數為0 須加值"
                else:
                    db.execute("insert into membergetinlog (memberid, quota, membertype) values (?,?,?)",(memberid,quotaminus,"course_limit"))
                    db.commit()
                    
                    return "此會員限期教練課計次儲值次數扣點後為"+str(quotaminus)

                # return "此會員有有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            elif(value_ret[0]==-1):    
                return "此會員限期教練課無有效會籍,最近有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            else:
                return "此會員沒有購買限期教練課合約"
        else:
            return "沒有此會員"

def checkifmemberValid_course_limit(id_1, today, db):
    type_1="course_limit"
    result=db.execute('select startdate,enddate from trans where memberid=? and membertype="course_limit" and startdate is not null and quota_course_limit is not 0 order by startdate desc',(id_1,)).fetchall()
    if result:

        today=today.split("-")
        today=date(int(today[0]),int(today[1]),int(today[2]))
        test_result=False
        for row in result:
            startdate=row[0]
            startdate=startdate.split("-")
            startdate=date(int(startdate[0]),int(startdate[1]),int(startdate[2]))

            enddate=row[1]
            enddate=enddate.split("-")
            enddate=date(int(enddate[0]),int(enddate[1]),int(enddate[2]))

            temp_1=(today-startdate)
            temp_2=(enddate-today)
            print("temp_1 is %s temp_2 is %s"%(str(temp_1),str(temp_2)),file=sys.stderr)
            if (str(temp_1).find("-")==-1 and str(temp_2).find("-")==-1):
                test_result=test_result or True
                print("test_result is %s"%test_result,file=sys.stderr)
            if(test_result==True):  #once got the valid time range then break out
                break 
        
        if(test_result==True):
            return [0, startdate, enddate]
        else:
            return [-1, startdate, enddate]
    else:
        return [-2, -1, -1]

def checkQuotaNMinus_course_limit(memberid,startdate,enddate,db):
    print("temp_1 is %s temp_2 is %s"%(startdate,enddate),file=sys.stderr)
    

    result=db.execute("select quota_course_limit from trans where startdate=? and enddate=? and memberid=? and membertype='course_limit'",(startdate,enddate,memberid,)).fetchone()
    
    if result[0]<=0:
        return -1
    else:
        db.execute("update trans set quota_course_limit=? where startdate=? and enddate=? and memberid=? and membertype='course_limit'",(int(result[0])-1,startdate,enddate,memberid))
        db.commit()
        return int(result[0])-1



# def checkQuotaNMinus(id,db,membertype):

#         if(membertype=="times"):
#             point="quota"
#         elif(membertype=="course"):
#             point="quota_course"
#         elif(membertype=="tran_little"):
#             point="quota_tran_little"
#         # elif (membertype=="course_limit"):
#         #     point="quota_course_limit"    
#         # print("today is %s"%(today),file=sys.stderr)
#         result=db.execute("select "+point+" from members where id=? and "+point+">0 ",(id,)).fetchone()
        
#         if result:
#             db.execute("update members set "+point+"=? where id=?",(int(result[0])-1,id))
#             db.commit()
#             return int(result[0])-1
#         else:
#             return -1




# def checkifmemberValid(id_1,today,membertype,db):
    
#     result=db.execute("select startdate,enddate from trans where memberid=? and membertype=? and enddate is not null order by enddate asc",(id_1,membertype,)).fetchall()
    
#     if result:

#         today=today.split("-")
#         today=date(int(today[0]),int(today[1]),int(today[2]))
#         test_result=False
#         for row in result:
#             startdate=row[0]
#             startdate=startdate.split("-")
#             startdate=date(int(startdate[0]),int(startdate[1]),int(startdate[2]))

#             enddate=row[1]
#             enddate=enddate.split("-")
#             enddate=date(int(enddate[0]),int(enddate[1]),int(enddate[2]))

#             temp_1=(today-startdate)
#             temp_2=(enddate-today)
#             print("temp_1 is %s temp_2 is %s"%(str(temp_1),str(temp_2)),file=sys.stderr)
#             if (str(temp_1).find("-")==-1 and str(temp_2).find("-")==-1):
#                 test_result=test_result or True
#             if(test_result==True):
#                 break 
#             print("test_result is %s"%test_result,file=sys.stderr)

#         if(test_result==True):
#             return [0, startdate, enddate]
#         else:
#             return [-1, startdate, enddate]
#     else:
#         return [-2, -1, -1]






    
# 用電話查會員號碼
@app.route('/id_querybyPhone', methods =[ 'GET' , 'POST' ])
def id_querybyPhone():
    phone=request.json['phone']
    db=get_db()
    with db:
        result=db.execute("select id from members where phone=?",(phone, )).fetchall()

        if result:
            return jsonify(result)
        else:
            return "查無資料"


# for 自主月費會費型入場
@app.route ( '/memberGetIn' , methods =[ 'GET' , 'POST' ])
def memberGetIn ():
    
    memberid=request.json['id']
    today=request.json['date']
    membertype="normal"
    print("id is %s"%(memberid),file=sys.stderr)
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            value_ret=checkifmemberValid(result[0],today,membertype,db)
            if(value_ret[0]==0):
                db.execute("insert into membergetinlog (memberid,membertype) values (?,?)",(memberid,membertype,))
                db.commit()
                return "此會員有有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            elif(value_ret[0]==-1):    
                return "此會員無有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            else:
                return "此會員沒有購買自主月費合約"
        else:
            return "無此會員"


# for 小班月費會費型入場
@app.route ( '/vipGetIn' , methods =[ 'GET' , 'POST' ])
def vipGetIn ():
    
    memberid=request.json['id']
    today=request.json['date']
    membertype="vip"
    print("id is %s"%(memberid),file=sys.stderr)
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            value_ret=checkifmemberValid(result[0],today,membertype,db)
            if(value_ret[0]==0):
                db.execute("insert into membergetinlog (memberid,membertype) values (?,?)",(memberid,membertype,))
                db.commit()
                return "此會員有有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            elif(value_ret[0]==-1):    
                return "此會員無有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            else:
                return "此會員沒有購買小班月費合約"
        else:
            return "無此會員"



    




#saveNewMember
@app.route('/saveNewMember',methods=['POST'])
def saveNewMember():
    name=request.json['name']
    memberid=request.json['memberID']
    nationid=request.json['nationID']
    birth=request.json['birth']
    phone=request.json['phone']
    emerName=request.json['emerName']
    relation=request.json['relation']
    emerPhone=request.json['emerPhone']
    address=request.json['address']
    savemember=request.json['savemember']
    

    db=get_db()
    with db:
        if savemember==True:    #add new member
            db.execute("insert into members (id,name,birth,type,phone,agent_name,agent_phone,agent_relation,address,nationID) values(?,?,?,'normal',?,?,?,?,?,?)",(memberid,name,birth,phone,emerName,emerPhone,relation,address,nationid))
        elif savemember==False: #add new staff
            db.execute("insert into staff (id,name,birth,phone,role,agent_name,agent_phone,agent_relation,address,nationID) values(?,?,?,?,'業務',?,?,?,?,?)",(memberid,name,birth,phone,emerName,emerPhone,relation,address,nationid))
        else:
            return "abnormal status of savemember variable"
        
        
        db.commit()
        return "ok"

#updateMember
@app.route('/updateMember',methods=['POST'])
def updateMember():

    name=request.json['name']
    memberid=request.json['memberID']
    nationid=request.json['nationID']
    birth=request.json['birth']
    phone=request.json['phone']
    emerName=request.json['emerName']
    relation=request.json['relation']
    emerPhone=request.json['emerPhone']
    address=request.json['address']

    # print("json inputs are %s %s %s %s %s %s %s %s %s"%(name, memberid, nationid
    # ,birth ,phone ,emerName ,relation ,emerPhone ,address),file=sys.stderr)
    # print("json inputs are %s %s"%(name,memberid) ,file=sys.stderr)
    # print(memberid,file=sys.stderr)
    db=get_db()
    with db:
        # result=db.execute("select id from members where id=?",(memberid,)).fetchall()    
        db.execute("update members set name=?,birth=?,phone=?,agent_name=?,agent_phone=?,agent_relation=?,address=?,nationID=? where id=?",
        (name,birth,phone,emerName,emerPhone,relation,address,nationid,memberid))
        db.commit()
        return "ok"


#updateMember
@app.route('/updateStaff',methods=['POST'])
def updateStaff():

    name=request.json['name']
    memberid=request.json['memberID']
    nationid=request.json['nationID']
    birth=request.json['birth']
    phone=request.json['phone']
    emerName=request.json['emerName']
    relation=request.json['relation']
    emerPhone=request.json['emerPhone']
    address=request.json['address']

    # print("json inputs are %s %s %s %s %s %s %s %s %s"%(name, memberid, nationid
    # ,birth ,phone ,emerName ,relation ,emerPhone ,address),file=sys.stderr)
    # print("json inputs are %s %s"%(name,memberid) ,file=sys.stderr)
    # print(memberid,file=sys.stderr)
    db=get_db()
    with db:
        # result=db.execute("select id from members where id=?",(memberid,)).fetchall()    
        db.execute("update staff set name=?,birth=?,phone=?,agent_name=?,agent_phone=?,agent_relation=?,address=?,nationID=? where id=?",
        (name,birth,phone,emerName,emerPhone,relation,address,nationid,memberid))
        db.commit()
        return "ok"







def checkQuotaNMinus(id,db,membertype):

        if(membertype=="times"):
            point="quota"
        elif(membertype=="course"):
            point="quota_course"
        elif(membertype=="tran_little"):
            point="quota_tran_little"
        # elif (membertype=="course_limit"):
        #     point="quota_course_limit"    
        # print("today is %s"%(today),file=sys.stderr)
        result=db.execute("select "+point+" from members where id=? and "+point+">0 ",(id,)).fetchone()
        
        if result:
            db.execute("update members set "+point+"=? where id=?",(int(result[0])-1,id))
            db.commit()
            return int(result[0])-1
        else:
            return -1

def checkifmemberValid(id_1,today,membertype,db):
    
    result=db.execute("select startdate,enddate from trans where memberid=? and membertype=? and enddate is not null order by enddate asc",(id_1,membertype,)).fetchall()
    
    if result:

        today=today.split("-")
        today=date(int(today[0]),int(today[1]),int(today[2]))
        test_result=False
        for row in result:
            startdate=row[0]
            startdate=startdate.split("-")
            startdate=date(int(startdate[0]),int(startdate[1]),int(startdate[2]))

            enddate=row[1]
            enddate=enddate.split("-")
            enddate=date(int(enddate[0]),int(enddate[1]),int(enddate[2]))

            temp_1=(today-startdate)
            temp_2=(enddate-today)
            print("temp_1 is %s temp_2 is %s"%(str(temp_1),str(temp_2)),file=sys.stderr)
            if (str(temp_1).find("-")==-1 and str(temp_2).find("-")==-1):
                test_result=test_result or True
            if(test_result==True):
                break 
            print("test_result is %s"%test_result,file=sys.stderr)

        if(test_result==True):
            return [0, startdate, enddate]
        else:
            return [-1, startdate, enddate]
    else:
        return [-2, -1, -1]




if __name__ == "__main__":
    # app.run(host='0.0.0.0',debug=True,ssl_context='adhoc')
    app.run(host='0.0.0.0',debug=True)



