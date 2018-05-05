var panelpart1= "<div class=\"panel panel-default\" style=\"margin-bottom:0px;margin-top:0px\"  >"+
                "<div class=\"panel-heading\">"+
                "   <h5 class=\"panel-title\" >"+
                "        <a data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#%id%\">"+
                "        %head%"+
                "        </a>"+
                "   </h5>"+
                "</div>"+
                "<div id=\"%id%\" class=\"panel-collapse collapse %open%\">"+
                "   <div class=\"panel-body\" style=\"padding:0px\">"+
                "       <table class=\"table table-responsive table-bordered table-hover\" style=\"margin-bottom:0px\">"+
                "           <tbody>";
var panelpart2= "           </tbody>"+
                "       </table>"+
                "   </div>"+
                "</div>"
                "</div>"
var listElement="<tr><th onclick=\"jmp('%url%')\">%title%</th></tr>"
var badge="<span class=\"badge pull-right\">%count%</span>"
function addpanel(pid,head,id,isopen,inner){
    var obj=document.getElementById(pid);
    var p1=panelpart1.replace(/%head%/g,head);
    p1=p1.replace(/%id%/g,id);
    if(isopen){
        p1=p1.replace(/%open%/g,"in");
    }
    else{
        p1=p1.replace(/%open%/g,"");
    }
    var p2=panelpart2.replace(/%id%/g,id);
    p2=p2.replace(/%head%/g,head);
    obj.innerHTML+=p1+inner+p2;
}
function getNav(pid,jsonUrl)
{
    
    $.ajax({
        url: jsonUrl,
        type: "GET",
        dataType: "json",
        success: function(data) {
            var head="";
            var content="";
            $.each(data.head, function(i, item) {
                content="";
                head=item.title;
                if(item.count!="0")
                    head+=badge.replace(/%count%/g,item.count)

                $.each(item.content, function(j, element) {
                    if(element.count!="0")
                        content+=listElement.replace(/%url%/g,element.url).replace(/%title%/g,element.title+badge.replace(/%count%/g,element.count));
                    else
                        content+=listElement.replace(/%url%/g,element.url).replace(/%title%/g,element.title);

                })
                addpanel(pid,head,"id"+i.toString(),i==0,content);
            })


        }
    })
}
function jmp(url){
    var obj=document.getElementById("iframe");
    obj.setAttribute("src",url);
}