
function SubmitEdit()
{
    var oldPassword=document.getElementById("oldPassword").value;
    var newPassword=document.getElementById("newPassword").value;
    var newPassword2=document.getElementById("newPassword2").value;
    if(newPassword!=newPassword2){
        alert("两次输入不一致，请检查")
        return;
    }
    $.ajax({
        type: "post",
        url: "/setPassword",
        data: {
            "oldPassword": oldPassword,
            "newPassword": newPassword,
        },
        dataType: 'text',
        success: function (data) {
            if(data=="Success")
                alert("密码修改成功！")
            else
            {
                alert("原密码错误，即将下线！")
                parent.location.reload();
            }
                
            
        },
        error: function () {
            //alert("error");
            alert("网络错误！")
        }
    })
}