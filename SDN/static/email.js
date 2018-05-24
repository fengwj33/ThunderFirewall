
function SubmitEdit()
{
    var emailaddr=document.getElementById("EmailAddr").value;
    $.ajax({
        type: "post",
        url: "/setEmail",
        data: {
            "EmailAddr": emailaddr,
        },
        dataType: 'text',
        success: function (data) {
            alert("修改成功！")
                
            
        },
        error: function () {
            //alert("error");
            alert("网络错误！")
        }
    })
}