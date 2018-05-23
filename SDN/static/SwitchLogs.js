function getlist(pid)
{
    
    $.ajax({
        url: "/getSwitchLog",
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
                        str+="<td style=\"word-break:break-all; \"><pre>"+element+"</pre></td>"
                    else
                        str+="<td style=\"word-break:break-all; \">"+element+"</td>"

                })
                str+="</tr>"
            })
            obj.innerHTML=str
            

        }
    })
}
