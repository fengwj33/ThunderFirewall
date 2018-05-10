function getlist()
{
    
    $.ajax({
        url: "/GetStudentListWP",
        type: "GET",
        dataType: "json",
        success: function(data) {
            var obj=document.getElementById("Tlist");
            var str=""
            var uname=""
            var Name=""
            $.each(data.body, function(i, item) {
                str+="<tr>" 
                $.each(item, function(j, element) {
                    if(j==1)
                        uname=element;
                    if(j==2)
                        Name=element;
                    if(j==3){
                        if(element=="NONE")
                            str+="<td><button class=\"btn btn-primary btn-xs\" data-toggle=\"modal\" data-target=\"#mAddParent\" onclick=\"setUName2('"+uname+"','"+Name+"')  \">添加家长</button></td>"
                        else
                            str+="<td>"+element+"</td>"
                    }
                    else
                        str+="<td>"+element+"</td>"
                })
                str+="<td><button class=\"btn btn-primary btn-xs\" data-toggle=\"modal\" data-target=\"#mEditName\" onclick=\"setUName('"+uname+"','"+Name+"')  \">编辑</button></td>"
                
                str+="</tr>"
            })
            obj.innerHTML=str
        }
    })
}
function setUName(userName,Name)
{
    var inpUName=document.getElementById("inputUser");
    var inpName=document.getElementById("inputName");
    inpUName.value=userName;
    inpName.value=Name;
}
function setUName2(userName,Name)
{
    var stuUName=document.getElementById("StuuserName");
    var stuName=document.getElementById("StuName");
    stuUName.value=userName;
    stuName.value=Name;
}
function SubmitEdit()
{
    var inpUName=document.getElementById("inputUser");
    var inpName=document.getElementById("inputName");
    var UserName=inpUName.value;
    var StudentName=inpName.value;
    $.ajax({
        type: "post",
        url: "/editStudent",
        data: {
            "UserName": UserName,
            "StudentName": StudentName,
        },
        dataType: 'text',
        success: function (data) {
            //alert("Success");
            getlist();
        },
        error: function () {
            //alert("error");
        }
    })
}
function AddTeacher()
{
    var inpstuUName=document.getElementById("StuuserName");
    var inppUserName=document.getElementById("pUserName");
    var inppPassword=document.getElementById("pPassword");
    var inppEmail=document.getElementById("pEmail");
    var inppName=document.getElementById("pName");
    var stuUName=inpstuUName.value;
    var pUserName=inppUserName.value;
    var pPassword=inppPassword.value;
    var pEmail=inppEmail.value;
    var pName=inppName.value;
    inppUserName.value=""
    inppPassword.value=""
    inppEmail.value=""
    inppName.value=""

    $.ajax({
        type: "post",
        url: "/AddParent",
        data: {
            "UserName": pUserName,
            "ParentName":pName,     
            "StudentUName": stuUName,
            "Email":pEmail,
            "Password":pPassword,
        },
        dataType: 'text',
        success: function (data) {
            //alert("Success");
            getlist();
        },
        error: function () {
            //alert("error");
        }
    })
    

}