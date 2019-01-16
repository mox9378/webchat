$.ajaxSetup({
            data: {csrfmiddlewaretoken: $.cookie('csrftoken') }
    });
    //submission request event
    function subEvent(method,url,data) {
        $.ajax({
            url:url,
            type:method,
            data:data,
            success:function (response) {
                response = JSON.parse(response);
                if(response){
                    if(response['EventType']=='signin'){
                        signin(response);
                    }else if(response['EventType']=='refresh'){
                        console.log('@',response);
                        refresh(response=response);
                    }else if(response['EventType']=='sendMsg'){
                        sendMsg(response);
                    }else if(response['EventType']=='getMsg'){
                        updateMsgTips(response);
                    }
                }

            },
            error:function (response) {
                console.log('error',response);
            }
        })
    }

function signin(response) {
    if(response['flag']){
        $.cookie('username',response['username']);
        $.cookie('uid',response['uid']);
        $.cookie('is_logind',1);
        console.log('-',response['username'])
        checkLogin()
    }
}

function checkLogin() {
        var flag = $.cookie('is_logind');
        if(flag==1){
            txt = "<li><a href='javascript:void(0);' style='color:red;'>"+$.cookie('username')+"</a></li><li ><a href='javascript:void(0);'>注销</a></li>";
            $("#signs").html(txt);
        }
    }