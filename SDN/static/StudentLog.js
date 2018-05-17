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
            var Name=""
            $.each(data.body, function(i, item) {
                str+="<tr>" 
                $.each(item, function(j, element) {
                    if(j==1)
                        uname=element;
                    str+="<td>"+element+"</td>"
                })
                str+="<td><button class=\"btn btn-primary btn-xs\" data-toggle=\"modal\" data-target=\"#showFlow\" onclick=\"getLog('main','"+uname+"')  \">显示流量曲线</button></td>"
                
                str+="</tr>"
            })
            obj.innerHTML=str
        }
    })
}
