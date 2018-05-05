function getlist(pid,jsonUrl)
{
    
    $.ajax({
        url: jsonUrl,
        type: "GET",
        dataType: "json",
        success: function(data) {
            var obj=document.getElementById(pid);
            var str="<thead><tr>"
            $.each(data.head, function(i, item) {
                str+="<th>"+item+"</th>"
                
            })
            str+="</tr></thead>"
            str+="<tbody>"
            $.each(data.body, function(i, item) {
                str+="<tr>"
                
                    
                $.each(item, function(j, element) {
                    str+="<td>"+element+"</td>"
                })
                str+="</tr>"
                
            })
            str+="</tbody>"
            obj.innerHTML=str
            

        }
    })
}