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
    db=get_db()
    with db:
        try:    #計次
            quotaadded=request.json['quotaadded']      
        except: #present 年費
            enddate=request.json['enddate']
            db.execute("insert into trans (memberid, staffid, startdate,price,enddate) values(?,?,?,?,?)",(memberid,staffid,startdate,price,enddate))
            db.commit()

            return "年費型合約成立!"
        else:
            db.execute("insert into trans (memberid, staffid, startdate, price) values(?,?,?,?)",(memberid,staffid,startdate,price))
            db.commit()
            db.execute("update members set quota=quota+? where id=?",(quotaadded,memberid))    
            db.commit()
            result=db.execute('select quota from members where id=?',(memberid,)).fetchone()
            if result:
                return "計次加值成功 剩餘次數為"+str(result[0])
            else:
                return "次數加值出了問題"
    
    # members_1=[]
    # for row in c:
    #     members_1.append({
    #         'id':row[0],
    #         'name':row[1]
    #     })
    
    # print(members_1,file=sys.stderr)    
    # return render_template('db_test.html',members=members_1)


# @app.route("/")
# def hello():
#     return render_template('base.html')    




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
        result=db.execute('select transid, startdate,enddate,price,staffid, name, timestamp from trans cross join staff where trans.staffid=staff.id and trans.memberid=?',
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
                result_1=db.execute('select transid, startdate,price,staffid, name, timestamp,enddate from trans cross join staff where trans.staffid=staff.id and trans.memberid=?',(memberid, )).fetchall()
                result_2=db.execute('select id,name from staff').fetchall()

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

# for 儲次型入場
@app.route("/memberGetInTimes",methods=['GET','POST'])
def memeberGetInTimes():
    memberid=request.json['id']
    # today=request.json['date']
    print("id is %s"%(memberid),file=sys.stderr)
    # db=get_db()
    # result=db.execute("select * from members where id=?",(memberid, )).fetchone()
    # if result:
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            quotaminus=checkQuotaNMinus(memberid,db)
            if quotaminus==-1:
                return "此會員儲值次數為0 須加值"
            else:
                db.execute("insert into membergetinlog (memberid, quota) values (?,?)",(memberid,quotaminus))
                db.commit()
                return "此會員儲值次數扣點後為"+str(quotaminus)
            
        else:
            return "沒有此會員"
    
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


# for 會費型入場
@app.route ( '/memberGetIn' , methods =[ 'GET' , 'POST' ])
def memberGetIn ():
    
    memberid=request.json['id']
    today=request.json['date']
    print("id is %s"%(memberid),file=sys.stderr)
    db=get_db()
    with db:
        result=db.execute("select * from members where id=?",(memberid, )).fetchone()
        if result:
            value_ret=checkifmemberValid(result[0],today)
            if(value_ret[0]==0):
                db.execute("insert into membergetinlog (memberid) values (?)",(memberid,))
                db.commit()
                return "此會員有有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            elif(value_ret[0]==-1):    
                return "此會員無有效會籍,有效日為"+str(value_ret[1])+'~'+str(value_ret[2])
            else:
                return "此會員沒有購買年費合約"
        else:
            return "無此會員"
    
# def writeGetInLog(id_1, quota):
#     db=get_db()
#     # print("today is %s"%(today),file=sys.stderr)
#     db.execute("insert into membergetinlog (memberid,quota) values (?,?)",(id_1,quota,))
#     db.commit()
#     return 0



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







def checkQuotaNMinus(id,db):
    
    
        # print("today is %s"%(today),file=sys.stderr)
        result=db.execute("select quota from members where id=? and quota>0 ",(id,)).fetchone()
        
        if result:
            db.execute("update members set quota=? where id=?",(int(result[0])-1,id))
            db.commit()
            return int(result[0])-1
        else:
            return -1

def checkifmemberValid(id,today):
    db=get_db()
    with db:
        # print("today is %s"%(today),file=sys.stderr)
        result=db.execute("select startdate,enddate from trans where memberid=? and enddate is not null order by enddate asc",(id,)).fetchall()
        
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
                    test_result=test_result or True; 
                print("test_result is %s"%test_result,file=sys.stderr)

            if(test_result==True):
                return [0, startdate, enddate]
            else:
                return [-1, startdate, enddate]
        else:
            return [-2, -1, -1]



# @app.route('/draw', methods=['POST','GET'])
# def draw ():
#     # global db
#     db=get_db()
#     group_name = request.form.get('group_name')
#     valid_members_sql = 'SELECT id FROM members '
#     cursor=db.cursor()
#     if group_name == 'ALL':
#         cursor.execute(valid_members_sql)
#     else:
#         valid_members_sql += 'WHERE group_name = ?'
#         cursor.execute(valid_members_sql, (group_name, ))
    
#     gg=cursor.fetchall()
#     # print(row, file=sys.stderr)
#     # for row in gg:
#     #     print(row[0],file=sys.stderr)
#     # return str(row[0])


#     valid_member_ids = [
#         row[0] for row in gg
#     ]

#     # print(valid_member_ids,file=sys.stderr)

#     if not valid_member_ids:
#         err_msg = "<p>No members in group '%s'</p>" % group_name
#         return err_msg, 404
    
#     lucky_member_id = random.choice(valid_member_ids)


#     member_name, member_group_name = db.execute(
#         'SELECT name, group_name FROM members WHERE id = ?',
#         (lucky_member_id, )
#     ).fetchone()

#     with db:
#         db.execute('INSERT INTO draw_histories (memberid) VALUES (?)',(lucky_member_id, ))

    
    
    
#     return '<p>%s（團體：%s）</p>' % (member_name.encode("utf-8"), member_group_name.encode("utf-8"))
    # return "pp"

# @app.route('/history')
# def history():
#     db = get_db()
#     recent_histories = db.execute(
#         'SELECT m.name, m.group_name, d.time '
#         'FROM draw_histories AS d, members as m '
#         'WHERE m.id == d.memberid '
#         'ORDER BY d.time DESC '
#         'LIMIT 10'
#     ).fetchall()
#     return render_template(
#         'history.html',
#         recent_histories=recent_histories
#     )


if __name__ == "__main__":
    # app.run(host='0.0.0.0',debug=True,ssl_context='adhoc')
    app.run(host='0.0.0.0',debug=True)



