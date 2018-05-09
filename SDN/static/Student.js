function getlist()
{
    
    $.ajax({
        url: "/GetStudentList",
        type: "GET",
        dataType: "json",
        success: function(data) {
            var obj=document.getElementById("Tlist");
            var str=""
            var uname=""
            $.each(data.body, function(i, item) {
                str+="<tr>" 
                $.each(item, function(j, element) {
                    if(j==1)
                        uname=element;
                    str+="<td>"+element+"</td>"
                })
                str+="<td><button type=\"button\" class=\"btn btn-danger btn-xs\" onclick=\"dellist('"+uname+"')\"  >删除</button></td></tr>"
            })
            obj.innerHTML=str
        }
    })
}
function addstudent()
{
    var UserName=document.getElementById("inputUser").value;
    var StudentName=document.getElementById("inputSName").value;
    var Password=document.getElementById("inputPassword").value;
    //alert(TeacherName)
    $.ajax({
        type: "post",
        url: "/AddStudent",
        data: {
            "UserName": UserName,
            "StudentName": StudentName,
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
function dellist(id)
{
    $.ajax({
        type: "post",
        url: "/removeStudent",
        data: {
            "UserName": id
        },
        dataType: 'text',
        success: function (data) {
            getlist()
        },
        error: function () {
            alert("error");
        }
    })
    
}