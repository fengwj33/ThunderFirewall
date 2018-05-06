function getlist(pid)
{
    
    $.ajax({
        url: "/GetTeacherList",
        type: "GET",
        dataType: "json",
        success: function(data) {
            var obj=document.getElementById(pid);
            var str=""
            var uname=""
            $.each(data.body, function(i, item) {
                str+="<tr>" 
                $.each(item, function(j, element) {
                    if(j==1)
                        uname=element;
                    str+="<td>"+element+"</td>"
                })
                str+="<td><button type=\"button\" class=\"btn btn-danger btn-xs\" onclick=\"dellist('"+pid+"','"+uname+"')\"  >删除</button></td></tr>"
            })
            obj.innerHTML=str
            

        }
    })
}
function addteacher()
{
    var UserName=document.getElementById("inputUser").value;
    var TeacherName=document.getElementById("inputTName").value;
    var Email=document.getElementById("InputEmail").value;
    var Password=document.getElementById("inputPassword").value;
    //alert(TeacherName)
    $.ajax({
        type: "post",
        url: "/AddTeacher",
        data: {
            "UserName": UserName,
            "TeacherName": TeacherName,
            "Email": Email,
            "Password": Password,
        },
        dataType: 'text',
        success: function (data) {
            //alert("Success");
            getlist("Tlist");
        },
        error: function () {
            //alert("error");
        }
    })
    
}
function dellist(pid,id)
{
    
    $.ajax({
        type: "post",
        url: "/removeTeacher",
        data: {
            "UserName": id
        },
        dataType: 'text',
        success: function (data) {
            alert("remove:"+id);
            getlist(pid)
        },
        error: function () {
            alert("error");
        }
    })
    
}