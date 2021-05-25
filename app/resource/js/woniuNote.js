//显示模态框中的登陆面板
function showLogin() {
    $("#login").addClass("active");
    $("#reg").removeClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").addClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").removeClass("active");
    $("#mymodal").modal("show");
}
//显示模态框中的注册面板
function showReg() {
    $("#login").removeClass("active");
    $("#reg").addClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").addClass("active");
    $("#findpanel").removeClass("active");
    $("#mymodal").modal("show");
}
//显示模态框中的找回密码面板
function showReset() {
    $("#login").removeClass("active");
    $("#reg").removeClass("active");
    $("#find").addClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").addClass("active");
    $("#mymodal").modal("show");
}

function doSendMail(obj) {
    var email = $.trim($("#regname").val());
    //对邮箱地址进行校验
    if(!email.match(/.+@.+\..+/)) {
        bootbox.alert({title:"错误提示",message:"邮箱地址格式不正确."});
        $("#regname").focus();
        return false;
    }
    //如果邮件格式正确，则让发邮件按钮变成不可用，避免二次操作

    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'email-invalid'){
            bootbox.alert({title:"错误提示",message: "邮箱地址格式不正确。"});
            $("#regname").focus();
            return false;
        }
        if (data == 'send-pass'){
            bootbox.alert({title:"信息提示",message: "邮箱验证码已成功发送，请查收。"});
            $("#regname").attr('disabled',true);
            $(obj).attr('disabled',true);
            return false;
        }
        else {
            bootbox.alert({title:"错误提示",message: "邮箱验证码未发送成功。"});
            return false;
        }

    });

}

function doReg(e) {
    if (e != null && e.keyCode != 13){
        return false;
    }


    var regname = $.trim($("#regname").val());
    var regpass = $.trim($("#regpass").val());
    var regcode = $.trim($("#regcode").val());

    if (!regname.match(/.+@.+\..+/) || regpass.length < 5) {

        bootbox.alert({title:"错误提示",message:"注册邮箱不正确或密码少于5位。"});
        return false;
    }
    else {
        param = "username="+regname;
        param +="&password="+ regpass;
        param +="&ecode="+regcode;
        $.post('/user',param,function(data){
            if (data == "ecode-error"){
                bootbox.alert({title:"错误提示",message:"验证码无效。"});
                $("#regcode").val('');
                $("#regcode").focus();
            }
            else if(data =="up-invalid"){
                bootbox.alert({title:"错误提示",message:"注册邮箱不正确或密码不能少于5位。"});

            }
            else if(data == "user-repeated"){
                bootbox.alert({title:"错误提示",message:"该用户名已经被注册。"});
                $("#regname").focus();
            }
            else if (data =="reg-pass"){
                bootbox.alert({title:"信息提示",message:"恭喜你，注册成功。"});
                setTimeout('location.reload();',1000);
            }
            else if (data =="reg-fail"){
                 bootbox.alert({title:"错误提示",message:"注册失败，请联系管理员"});

            }
        });
    }
}


function doLogin(e) {
     if (e != null && e.keyCode != 13){
        return false;
    }


    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());

    // if (!loginname.match(/.+@.+\..+/) || loginpass.length < 5) {
    //
    //     bootbox.alert({title:"错误提示",message:"用户名错误或密码少于5位。"});
    //     return false;
    // }
    // else {
        var  param = "username="+loginname;
        param +="&password="+ loginpass;
        param +="&vcode="+logincode;
        $.post('/login',param,function(data){
            if (data == "vcode-error"){
                bootbox.alert({title:"错误提示",message:"验证码无效。"});
                $("#logincode").val('');
                $("#logincode").focus();
            }

            else if (data =="login-pass"){
                bootbox.alert({title:"信息提示",message:"恭喜你，登录成功。"});
                setTimeout('location.reload();',1000);
            }
            else if (data =="login-fail"){
                 bootbox.alert({title:"错误提示",message:"登录失败，请联系管理员"});

            }
        });
    // }

}
