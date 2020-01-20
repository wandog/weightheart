$("#savebull").click (function (){
    var bulletin_content={
        con_0:$("#bulletin_0")[0].value,
        con_1:$("#bulletin_1")[0].value,
        con_2:$("#bulletin_2")[0].value
    }

    $.ajax({
        type:"POST",
        url:"/saveBulletin",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify(bulletin_content),
        error:function(result){
            // alert(result);
            alert("儲存失敗!");
        },
        success:function(result){
            alert(result);
            
        }

    });
});

// function readBulletinData(){

// }