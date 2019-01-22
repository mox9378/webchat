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
                    }else if(response['EventType']=='signup'){
                        signup(response);
                    }else if(response['EventType']=='refresh'){
                        refresh(response=response);
                    }else if(response['EventType']=='sendMsg'){
                        sendMsg(response);
                    }else if(response['EventType']=='getMsg'){
                        getMsg(response);
                    }
                }
            },
            error:function (response) {
            }
        })
    }


function signup(response){
    if(response['flag']){
        $('#id_signup .input-group').addClass('has-success');
        $('#signup_noties').addClass('alert-success').text('reg success!');
        checkLogin();
        setTimeout(clsDialog,1500);
    }else{
        //for login fail.
        $('#id_signup .input-group').addClass('has-error');
        $('#signup_noties').addClass('alert-danger').text('reg error!');
    }
}

function signin(response) {
    if(response['flag']){
        $.cookie('username',response['username']);
        $.cookie('uid',response['uid']);
        $.cookie('is_logind',1);
        $.cookie('user',escape(response['user']))
        $('#id_signin .input-group').addClass('has-success');
        $('#signin_noties').addClass('alert-success').text('sign in success!');
        checkLogin();
        setTimeout(function () {
            location.reload();
        },1500);
        //clsDialog()
    }else{
        //for login fail.
        $('#id_signin .input-group').addClass('has-error');
        $('#signin_noties').addClass('alert-danger').text('sign in error!');
    }
}

function logout(){
        $.cookie('is_logind','')
        $.cookie('uid','')
        $.cookie('username','');
        $.cookie('user','');
        location.reload();
}
function checkLogin() {
        var flag = $.cookie('is_logind');
        if(flag==1){
            txt = "<li><a href='javascript:void(0);' style='color:red;'>"+unescape($.cookie('user'))+"</a></li><li ><a href='javascript:void(0);' onclick='logout();'>注销</a></li>";
            $("#signs").html(txt);
        }
    }