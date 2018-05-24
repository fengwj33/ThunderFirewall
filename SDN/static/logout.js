
function logout()
{
    $.ajax({
        type: "get",
        url: "/logout",
        dataType: 'text',
        success: function (data) {
            alert("已登出")
            parent.location.reload();
                
            
        },
        error: function () {
            //alert("error");
            alert("网络错误！")
        }
    })
}