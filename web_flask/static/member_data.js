//hide the column for 次數
function hideCol() {
    // var membertype = document.getElementsByName("memberType")[0].value;
    var membertype=$("input[name='memberType']:checked").val();
    var col="";
    
    if(membertype=="normal"){
        col="2 3 4 5 6";
    
    }else if(membertype=="times"){
        col="1 3 4 5 6";
    
    }else if(membertype=="vip"){
        col="1 2 4 5 6";
    
    }else if(membertype=="tran_little"){
        col="1 2 3 5 6";
    
    }else if(membertype=="course_limit"){
        col="1 2 3 4 6";
    
    }else if(membertype=="course"){
        col="1 2 3 4 5";
    
    }

    var tbl = document.getElementById("priceTable");
    if (tbl != null) {
        for (var i = 0; i < tbl.rows.length; i++) {
            for (var j = 0; j < tbl.rows[i].cells.length; j++) {

                
                
                if (col.indexOf(j.toString())!=-1){
                    tbl.rows[i].cells[j].style.display = "none";
                }else{
                    tbl.rows[i].cells[j].style.display = "table-cell";
                }
                
                    
            }
        }
    }
}

function calPrice_1(){
    // alert("not yet finished!");
    var membertype=$("input[name='memberType']:checked").val();
    var period=$("input[name='memberTime']:checked").val();
    var times=$("input[name='Times']:checked").val();
    var memberMonths=$("input[name='memberMonths']:checked").val();
    var Times_1=$("input[name='Times_1']:checked").val();
    var CourseTimes=$("input[name='CourseTimes']:checked").val();
    var CourseTimes_infi=$("input[name='CourseTimes_infi']:checked").val();
    var price=0;
    if(membertype=="normal"){
        if(period=="single"){
            price=150;
        }else if(period=="month"){
            price=1300;
        }else if(period=="triple"){
            price=3300;
        }else if(period=="six"){
            price=5400;
        }else{
            price=8400;
        }
    }else if(membertype=="vip"){
        if(memberMonths=="1"){
            price=3200;
        }else if(memberMonths=="3"){
            price=9000;
        }else if(memberMonths=="6"){
            price=16800;
        }else if(memberMonths="12"){
            price=31200;
        }
    }else if(membertype=="times"){
        if(times=="10"){
            price=1200;
        }else if(times=="30"){
            price=3000;
        }else if(times=="50"){
            price=4000;
        }
    }else if(membertype=="tran_little"){
        if(Times_1=="1"){
            price=320;
        }else if(Times_1=="10"){
            price=2800;
        }else if(Times_1=="30"){
            price=7200;
        }else if(Times_1=="50"){
            price=10000;
        }
    }else if(membertype=="course_limit"){
        if(CourseTimes=="5"){
            price=6500;
        }else if(CourseTimes=="10"){
            price=11000;
        }else if(CourseTimes=="20"){
            price=18000;
        }else if(CourseTimes=="40"){
            price=32000;
        }
    }else if(membertype=="course"){
        if(CourseTimes_infi=="5"){
            price=8000;
        }else if(CourseTimes_infi=="10"){
            price=14000;
        }else if(CourseTimes_infi=="20"){
            price=24000;
        }else if(CourseTimes_infi=="40"){
            price=40000;
        }    
    }else{
        console.log("no price");
    }
    price=price.toString();
    $("#priceCharge")[0].innerHTML=price+"<br>新台幣";
}

function calPrice_2(){
    alert("not yet finished!");
}


$(document).ready(function(){
    $( "#start_date" ).datepicker({ dateFormat: 'yy-mm-dd' });
    $( "#end_date").datepicker({ dateFormat: 'yy-mm-dd' });
    loadDefaultHeadPhoto(); //load default img of member
    $("#savepic")[0].style.display="none";
    disableAllData();
    $("#CancelSavePic")[0].style.display="none";
    change_membertype2Chinese();
});

//load the photo of member
function loadDefaultHeadPhoto(){
    var canvas = document.getElementById('canvas'),
    // if(canvas.getContext){
    context = canvas.getContext('2d');
    var base_image = new Image();

    var memberid=$("#h3memberID")[0].innerHTML;
    memberid=memberid.split('&nbsp;&nbsp;&nbsp;&nbsp;')[1];

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

// function checkifPhotoExist(id){
//     $.get("/static/photo/"+id)
//     .done(function() { 
//         // Do something now you know the image exists.
//         alert("file exist");
//     }).fail(function() { 
//         // Image doesn't exist - do something else.
//         alert("file not exist");
//     })

// }



// get the data of cookie
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

$("#CancelSavePic").click(function(){
    // stop the webcam
    try{
        video.srcObject.stop();
    }catch(e){
        video.srcObject.getVideoTracks()[0].stop();
    }

    $(this)[0].style.display="none";
    $("#video")[0].style.display="none";
    $("#savepic")[0].style.display="none";
    $("#takepic")[0].style.display="inline";
    // $("#savepic")[0].style.display="inline";
});

var video=document.getElementById("video");
var canvas=document.getElementById("canvas");
var context=canvas.getContext('2d');

function startVideoStream(){
    $("#savepic")[0].style.display="inline";
    $("#video")[0].style.display="inline";
    $("#takepic")[0].style.display="none";
    $("#CancelSavePic")[0].style.display="inline";
    navigator.getMedia=navigator.getUserMedia||navigator.webkitGetUserMedia||
                        navigator.mozGetUserMedia||navigator.msGetUserMedia;
    
    navigator.getUserMedia({
        video:true,
        audio:false
    },function(stream){
        _streamcopy=stream;
        video.srcObject=stream;
        video.play();
    },function(error){
        console.log("webcam video error",error.code);
    }
    );
}

//register click event handler for 拍照
$("#savepic").click(function(){
    
    //show the video photo to canvas
    canvas.width=video.videoWidth;
    canvas.height=video.videoHeight;
    context.drawImage(video,0,0,video.videoWidth,video.videoHeight);
    //canvas.width=320;
    //canvas.height=240;
    //context.drawImage(video,0,0,320,240);


    $("#video")[0].style.display="none";
    $("#CancelSavePic")[0].style.display="none";
    $("#takepic")[0].style.display="inline";
    


    // stop the webcam
    try{
        video.srcObject.stop();
    }catch(e){
        video.srcObject.getVideoTracks()[0].stop();
    }
    

    // var canvas=document.getElementById("fami_chart");
    var dataURL=canvas.toDataURL('image/png',1);
    // var org=getCookie("OIDX");
        
    var line=$("#h3memberID")[0].innerHTML;
    var data=line.split('&nbsp;&nbsp;&nbsp;&nbsp;');
    var id=data[1];

    var img={
        imgBase64: dataURL,
        filename:id
    };

    //save canvas to server image file
    $.ajax({
        type:"POST",
        url:"/savecanvas",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(img),
        success:function(result){
            $("#savepic")[0].style.display="none";
            // alert(result);
        },
        error:function(result){ 
            $("#savepic")[0].style.display="none";
            console.dir(result);
        }
    });
});

$("#h3memberID").click(function(){
    var line=$("#h3memberID")[0].innerHTML;
    var data=line.split('&nbsp;&nbsp;&nbsp;&nbsp;');
    var id=data[1];
    var jj={
            memberID:id,
            // name:$("#name")[0].value
        };
    // var host;
    $.ajax({
        type:"POST",
        url:"/gen_qrcode",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(jj),
        success:function(result){
            // alert(result);
            var host=window.location.host;
            // alert(host);
            window.open('http://'+host+'/show_qrcode?id='+jj.memberID+"&name="+$("#name")[0].value,'會員QRCODE',
            'height=250,width=600,top=700,left=300,scrollbars=yes,resizable'
            );
        },
        error:function(err){
            alert("gen qr code fail!");
        }
    });
});

$("#confirmTrans").click(function(){
    var type=$('input[name ="memberType"]:checked').val();
    var times=$('input[name ="Times"]:checked').val()   //for 自主計次       
    var tranlittle_times=$('input[name ="Times_1"]:checked').val()   //for 小班訓練    
    var course_times=$('input[name ="CourseTimes"]:checked').val()   //for 限期教練    
    var courseinfini_times=$('input[name ="CourseTimes_infi"]:checked').val()   //for 無限期教練    
    var price_1=parseInt($("#priceCharge")[0].innerHTML.split("<br>")[0]);

    if($("#start_date")[0].value==""){
        alert("起始日不可為空!");
        return;
    }
    if(type=="normal"||type=="vip"||type=="course_limit"){
        if($("#end_date")[0].value==""){
            alert("到期日不可為空!");
            return;
        }
    }


    
    if(type=="times"){  //計次會員
        var data={
            memberid:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1],
            staffid:$("#staffID").val(),
            startdate:$("#start_date")[0].value,
            enddate:null,
            quotaadded:times,
            price:price_1,
            membertype:"times"
        }
        $.ajax({
            type:"POST",
            url:"/save_trans",
            contentType: 'application/json;charset=UTF-8',
            data:JSON.stringify(data),
            success:function(result){
                alert(result);
            },
            error:function(err){
                console.log(err);
            }
        });
    }else if(type=="normal"){  //年費會員
        var data={
            memberid:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1],
            staffid:$("#staffID").val(),
            startdate:$("#start_date")[0].value,
            enddate:$("#end_date")[0].value,
            quotaadded:null,
            price:price_1,
            membertype:"normal"
        }
        $.ajax({
            type:"POST",
            url:"/save_trans",
            contentType: 'application/json;charset=UTF-8',
            data:JSON.stringify(data),
            success:function(result){
                // console.log(result);
                alert(result);
            },
            error:function(err){
                console.log(err);
            }
        });
    }else if(type=="vip"){  //小班月費
        var data={
            memberid:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1],
            staffid:$("#staffID").val(),
            startdate:$("#start_date")[0].value,
            enddate:$("#end_date")[0].value,
            quotaadded:null,
            price:price_1,
            membertype:"vip"
        }
        $.ajax({
            type:"POST",
            url:"/save_trans",
            contentType: 'application/json;charset=UTF-8',
            data:JSON.stringify(data),
            success:function(result){
                // console.log(result);
                alert(result);
            },
            error:function(err){
                console.log(err);
            }
        });
    }else if(type=="tran_little"){  //小班訓練
        var data={
            memberid:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1],
            staffid:$("#staffID").val(),
            startdate:$("#start_date")[0].value,
            enddate:null,
            quotaadded:tranlittle_times,
            price:price_1,
            membertype:"tran_little"
        }
        $.ajax({
            type:"POST",
            url:"/save_trans",
            contentType: 'application/json;charset=UTF-8',
            data:JSON.stringify(data),
            success:function(result){
                // console.log(result);
                alert(result);
            },
            error:function(err){
                console.log(err);
            }
        });
    }else if(type=="course_limit"){  //限期教練
        var data={
            memberid:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1],
            staffid:$("#staffID").val(),
            startdate:$("#start_date")[0].value,
            enddate:$("#end_date")[0].value,
            quotaadded:course_times,
            price:price_1,
            membertype:"course_limit"
        }
        $.ajax({
            type:"POST",
            url:"/save_trans",
            contentType: 'application/json;charset=UTF-8',
            data:JSON.stringify(data),
            success:function(result){
                // console.log(result);
                alert(result);
            },
            error:function(err){
                console.log(err);
            }
        });
    }else if(type=="course"){  //無限期教練
        var data={
            memberid:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1],
            staffid:$("#staffID").val(),
            startdate:$("#start_date")[0].value,
            enddate:null,
            quotaadded:courseinfini_times,
            price:price_1,
            membertype:"course"
        }
        $.ajax({
            type:"POST",
            url:"/save_trans",
            contentType: 'application/json;charset=UTF-8',
            data:JSON.stringify(data),
            success:function(result){
                // console.log(result);
                alert(result);
            },
            error:function(err){
                console.log(err);
            }
        });
    }

    
    //clear all records
    //暫時comment 方便開發
    $("#transRec").find("tr:gt(0)").remove();  
    
    var input={
        id:$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1]
    };

    $.ajax({
        type:"POST",
        url:"/getTransRec",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(input),
        success:function(result){
            console.log(result);
            // var gg=result;    
            show_trans_rec(result,'transRec');
            change_membertype2Chinese();
        },
        error:function(err){
            console.log(err);
        }
    });
});

function show_trans_rec(result, tableid){
    table=$("#"+tableid);
    result.forEach(function(item,index,array){
        
        var os='<tr style="border:solid 2px">';
        for(var i=0;i<item.length;i++){
            // os='<tr><td>'+item[i]+'</td>';
            os+='<td>'+item[i]+'</td>';
        }
        os+='</tr>';
        table.append(os);
    });
}


$("#editenable").click(function(){
    disableAllData();
})

$("#saveNdisableEdit").click(function(){
    if(saveMemberData()!=-1){
        disableAllData();
    }
    
});

function change_membertype2Chinese(){
    $('#transRec td').html(function(i, html){
        return html.replace(/normal/g, '自主月費'); 
      });
    $('#transRec td').html(function(i, html){
        return html.replace(/times/g, '自主計次'); 
    });
    $('#transRec td').html(function(i, html){
        return html.replace(/vip/g, '小班月費'); 
    });
    $('#transRec td').html(function(i, html){
        return html.replace(/tran_little/g, '小班計次'); 
    });
    $('#transRec td').html(function(i, html){
        return html.replace(/course_limit/g, '限期教練課'); 
    });
    $('#transRec td').html(function(i, html){
        return html.replace(/course/g, '無限期教練課'); 
    });
}


function disableAllData(){

    if(typeof(this.disable)=='undefined'){
        // disableAllData.disable=true;
        this.disable=true;
    }
    

    var array=['name','birth','phone','memberType','emerName'
    ,'relation', 'emerPhone','mem_address','saveNdisableEdit','nationID']
    array.forEach(function(item,index,array){
        $("#"+item)[0].disabled=this.disable;
    })

    this.disable=!this.disable;
}


function saveMemberData(){
    var array=['name','birth','phone','memberType','emerName'
    ,'relation', 'emerPhone','mem_address'];
    
    for(var i=0;i<array.length;i++){
        if($("#"+array[i])[0].value==""){
            alert("身份證字號以外有欄位為空白!!");
            return -1;
        }
    }
    
    var mID=$("#h3memberID")[0].innerHTML.split("&nbsp;&nbsp;&nbsp;&nbsp;")[1];

    var data_1={
        name:$("#name")[0].value,
        memberID:mID,
        nationID:$("#nationID")[0].value.toUpperCase(),
        birth:$("#birth")[0].value,
        phone:$("#phone")[0].value,
        emerName:$("#emerName")[0].value,
        relation:$("#relation")[0].value,
        emerPhone:$("#emerPhone")[0].value,
        address:$("#mem_address")[0].value,

    }

    $.ajax({
        type:"POST",
        url:"/updateMember",
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
