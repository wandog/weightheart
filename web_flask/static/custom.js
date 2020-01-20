
//年費會員打卡
$("#btnGetIn").click (function (){

    if($("#memberID")[0].value==""){
        alert("請輸入會員ID");
        return;
    }
    var memberid={
        id:$("#memberID")[0].value,
        date:$("#presentDate")[0].value
    }
    $.ajax({
        type:"POST",
        url:"/memberGetIn",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(memberid),
        error:function(result){
            // alert(result);
            alert("打卡失敗!");
        },
        success:function(result){
            // alert(result);
            $("#response_1")[0].innerHTML=result;
            loadMemberPhoto();
            $("#showMsg").click();
        }

    });
});

//儲次會員打卡
$("#btnGetInTimes").click (function (){

    if($("#memberID")[0].value==""){
        alert("請輸入會員ID");
        return;
    }

    var r = confirm("確定要扣除次數嗎?");
    if(r==false){
        return;
    }
    var memberid={
        id:$("#memberID")[0].value,
        // date:$("#presentDate")[0].value
    }
    $.ajax({
        type:"POST",
        url:"/memberGetInTimes",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(memberid),
        error:function(result){
            // alert(result);
            alert("儲值次數扣除失敗!");
        },
        success:function(result){
            // alert(result);
            $("#response_1")[0].innerHTML=result;
            loadMemberPhoto();
            $("#showMsg").click();
        }

    });
});


$(document).ready(function(){
    $("#memberQuery").attr("disabled", true);
    $("#memberGetInRec").attr("disabled",true);
    $("#btnGetIn").attr("disabled",true);
    $("#btnGetInTimes").attr("disabled",true);

    MemberIDinput = document.getElementById('memberID');
    MemberIDinput.addEventListener('input', detect_exist);
    
    MemberIDinput = document.getElementById('nationID_add');
    MemberIDinput.addEventListener('input', id_detect_exist);
    
    // MemberIDinput = document.getElementById('staffID');
    // MemberIDinput.addEventListener('input', staff_detect_exist);

    $("#memberID_add")[0].disabled=true;
    var t=setInterval(getTimenDate,1000);

});

function getTimenDate(){
    var today=new Date();
    var date=today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    $("#presentDate")[0].value=date;
    var time= today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    $("#presentTime")[0].value=time;
}


//load the photo of member
function loadMemberPhoto(){
    var canvas = document.getElementById('headPhoto'),
    
    context = canvas.getContext('2d');
    var base_image = new Image();

    // var memberid=$("#h3memberID")[0].innerHTML;
    memberid=$("#memberID")[0].value;

    base_image.onload=function(){
        // context.drawImage(base_image,75,0);
        context.drawImage(this,0,0,this.width,this.height,
            0,0,canvas.width,canvas.height);
        // context.drawImage(this,0,0,640,640*(this.height/this.width));
    };
    
    $.get('/static/photo/'+memberid+'.png')
    .done(function() { 
        // Do something now you know the image exists.
        base_image.src = '/static/photo/'+memberid+'.png';
    }).fail(function() { 
        // Image doesn't exist - do something else.
        base_image.src = '/static/photo/eagle.png';
    })

    
}


//check if staff id exist. if not disable the buttons
function staff_detect_exist(e){
    var id_value={
        id:e.target.value
    }

    console.log(e.target.value);
    //return;
    $.ajax({
        type:"POST",
        url:"/staff_id_exist_check",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(id_value),
        success:function(result){
            // alert(result);
            if(result=="ok"){
                $("#queryStaffData").attr("disabled", false);
                // $("#memberGetInRec").attr("disabled",false);
                // $("#btnGetIn").attr("disabled",false);
                // $("#btnGetInTimes").attr("disabled",false);
                
                
            }else{
                $("#queryStaffData").attr("disabled", true);
                // $("#memberGetInRec").attr("disabled",true);
                // $("#btnGetIn").attr("disabled",true);
                // $("#btnGetInTimes").attr("disabled",true);
            }
        },
        error:function(result){ 
            alert(result);
        }
    });
}




//check if member id exist. if not disable the buttons
function detect_exist(e){
    var id_value={
        id:e.target.value
    }

    console.log(e.target.value);
    //return;
    $.ajax({
        type:"POST",
        url:"/id_exist_check",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(id_value),
        success:function(result){
            if(result=="ok"){
                $("#memberQuery").attr("disabled", false);
                $("#memberGetInRec").attr("disabled",false);
                $("#btnGetIn").attr("disabled",false);
                $("#btnGetInTimes").attr("disabled",false);
                
                
            }else{
                $("#memberQuery").attr("disabled", true);
                $("#memberGetInRec").attr("disabled",true);
                $("#btnGetIn").attr("disabled",true);
                $("#btnGetInTimes").attr("disabled",true);
            }
        },
        error:function(result){ 
            alert(result);
        }
    });
}


function genID(id){
    // console.log($(this).html());
    // var newid=$("#memberID_add")[0].value;
    if(id=="addNewStaff"){
        $("#title_add_guys")[0].innerHTML="新增員工";
        var input={
            target:"staffid"
        };
    }else if(id=="addNewMember"){
        $("#title_add_guys")[0].innerHTML="新增會員";
        var input={
            target:"memberid"
        };
    }
    

    var checklist=["name_add","memberID_add","birth_add","phone_add","emerName","relation",
"emerPhone","address_add","nationID_add"];
    //clear the data at first
    for(var i=0;i<checklist.length;i++){
        $("#"+checklist[i])[0].value="";
    }

    $("#idmsg")[0].innerHTML="";

    // var input={
    //     target:"memberid"
    // };
    $.ajax({
        type:"POST",
        url:"/getLastID",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(input),
        success:function(result){
            if(id=="addNewMember"){
                var n1=$("#memberID_add")[0].value=result.replace("m","");
                n1=parseInt(n1); n1="000"+(n1+1);
                n1=n1.slice(-4);
                $("#memberID_add")[0].value="m"+n1;
            }else if(id=="addNewStaff"){
                var n1=$("#memberID_add")[0].value=result.replace("s","");
                n1=parseInt(n1); n1="000"+(n1+1);
                n1=n1.slice(-4);
                $("#memberID_add")[0].value="s"+n1;

            }else{
                console.log("id is wrong!!");
            }
        },
        error:function(result){ 
            console.dir(result);
        }
    });
}



function saveMemberData(){
    var savemember_1=($("#title_add_guys")[0].innerHTML=="新增會員")?true:false;

    var checklist=["name_add","memberID_add","birth_add","phone_add","emerName","relation",
"emerPhone","address_add"]

    if(savemember_1==false){
        checklist.push("nationID_add");
    }

    for(var i=0;i<checklist.length;i++){
        if($("#"+checklist[i])[0].value==""){
            if(savemember_1==true){
                alert("身份證字號以外有欄位為空白!!");
            }else{
                alert("不可以有欄位為空白!!");
            }
            return;
        }
    }
    
    // var savemember_1=($("#title_add_guys")[0].innerHTML=="新增會員")?true:false;

    var data_1={
        name:$("#name_add")[0].value,
        memberID:$("#memberID_add")[0].value,
        nationID:$("#nationID_add")[0].value.toUpperCase(),
        birth:$("#birth_add")[0].value,
        phone:$("#phone_add")[0].value,
        emerName:$("#emerName")[0].value,
        relation:$("#relation")[0].value,
        emerPhone:$("#emerPhone")[0].value,
        address:$("#address_add")[0].value,
        savemember:savemember_1
    }

    $.ajax({
        type:"POST",
        url:"/saveNewMember",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(data_1),
        success:function(result){
            // $("#savepic")[0].style.display="none";
            alert(result);
        },
        error:function(result){ 
            // $("#savepic")[0].style.display="none";
            console.dir(result);
        }
    });
}

$("#birth_add").datepicker({
    changeYear: true,
    yearRange: "1910:2099",
    controlType: 'select',
    oneLine: true,
    timeFormat: 'hh:mm tt',
    dateFormat: 'yy-mm-dd'
}).css({"z-index":9999});


//for nation id check
function id_detect_exist(e){
    // var id_value={
    //     id:e.target.value
    // }

    console.log(e.target.value);
    var ret=checkid(e.target.value)
    if(ret==false){
        $("#idmsg")[0].innerHTML="格式錯誤";    
    }else if(ret==true){
        $("#idmsg")[0].innerHTML="格式正確";    
    }
    //return;
}  

$("#BtnQuerybyPhone").click(function(){

    var data={
        phone:$("#phoneNumber")[0].value
    };

    $.ajax({
    type:"POST",
    url:"/id_querybyPhone",
    contentType: 'application/json;charset=UTF-8',
    data:JSON.stringify(data),
    success:function(result){
        // alert(result);
        // console.dir(result);
        $("#response_memberid")[0].innerHTML=result;
    },
    error:function(result){ 
        alert(result);
        
        // response_memberid
    }
    });
})






//check nation id number
function checkid(id){
//建立字母分數陣列(A~Z)
var city = new Array(1,10,19,28,37,46,55,64,39,73,82, 2,11,20,48,29,38,47,56,65,74,83,21, 3,12,30)
id = id.toUpperCase();
//使用「正規表達式」檢驗格式
if (id.search(/^[A-Z](1|2)\d{8}$/i) == -1) {
    return false;
} else {
    //將字串分割為陣列(IE必需這麼做才不會出錯)
    id = id.split('');
    //計算總分
    var total = city[id[0].charCodeAt(0)-65];
    for(var i=1; i<=8; i++){
        total += eval(id[i]) * (9 - i);
    }
    //補上檢查碼(最後一碼)
    total += eval(id[9]);
    //檢查比對碼(餘數應為0);
    return ((total%10 == 0 ));
}  
}
  
