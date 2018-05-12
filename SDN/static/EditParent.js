function getlist()
{
    
    $.ajax({
        url: "/GetParentList",
        type: "GET",
        dataType: "json",
        success: function(data) {
            var obj=document.getElementById("Tlist");
            var str=""
            var uname=""
            var Email=""
            var Name=""
            $.each(data.body, function(i, item) {
                str+="<tr>" 
                $.each(item, function(j, element) {
                    if(j==1)
                        uname=element;
                    if(j==2)
                        Name=element;
                    if(j==3)
                        Email=element;
                    str+="<td>"+element+"</td>"
                })
                str+="<td><button class=\"btn btn-primary btn-xs\" data-toggle=\"modal\" data-target=\"#myModal\" onclick=\"setUName('"+uname+"','"+Email+"','"+Name+"')  \">编辑</button></td></tr>"
            })
            obj.innerHTML=str
            

        }
    })
}
function setUName(userName,Email,Name)
{
    var inpUName=document.getElementById("inputUser");
    var inpEmail=document.getElementById("InputEmail");
    var inpName=document.getElementById("inputName");
    inpUName.value=userName;
    inpEmail.value=Email;
    inpName.value=Name;
}
function SubmitEdit()
{
    var inpUName=document.getElementById("inputUser");
    var inpEmail=document.getElementById("InputEmail");
    var inpName=document.getElementById("inputName");
    var UserName=inpUName.value;
    var ParentName=inpName.value;
    var Email=inpEmail.value;
    $.ajax({
        type: "post",
        url: "/editParent",
        data: {
            "UserName": UserName,
            "ParentName": ParentName,
            "Email": Email,
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