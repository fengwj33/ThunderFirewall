var iplist=new Array();
var editingid=0;
function getlist()
{
    iplist=new Array();
    $.ajax({
        url: "/GetGameServerList",
        type: "GET",
        dataType: "json",
        success: function(data) {
            
            $.each(data.body, function(i, item) {
                var temp=new Array();
                $.each(item, function(j, element) {
                    temp.push(element)
                })
                iplist.push(temp);
            })
            refreshlist();
        
        }
    })
}
function refreshlist()
{
    var obj=document.getElementById("Tlist");
    var str=""
    $.each(iplist, function(i, item) {
        str+="<tr>" 
        $.each(item, function(j, element) {
            str+="<td>"+element+"</td>"
        })
        str+="<td><button class=\"btn btn-primary btn-xs\" data-toggle=\"modal\" data-target=\"#myModal\" onclick=\"edit('"+i+"')  \">编辑</button></td>"
        str+="<td><button class=\"btn btn-primary btn-xs\"  onclick=\"del('"+i+"')  \">删除</button></td>"
        str+="</tr>"
    })
    obj.innerHTML=str
}
function del(id)
{
    iplist.splice(id,1);
    refreshlist()
}
function add()
{
    var inputRuleName=document.getElementById("inputRuleName").value;
    var inputIp=document.getElementById("inputIp").value;
    document.getElementById("inputRuleName").value=""
    document.getElementById("inputIp").value=""
    var temp=new Array(inputRuleName,inputIp)
    iplist.push(temp)
    refreshlist()
}
function edit(id)
{
    var einputRuleName=document.getElementById("einputRuleName");
    var einputIp=document.getElementById("einputIp");
    einputRuleName.value=iplist[id][0];
    einputIp.value=iplist[id][1];
    editingid=id;
}
function confirmedition()
{
    var einputRuleName=document.getElementById("einputRuleName");
    var einputIp=document.getElementById("einputIp");
    iplist[editingid][0]=einputRuleName.value;
    iplist[editingid][1]=einputIp.value;
    refreshlist()
}


function SubmitEdit()
{
    var postval={}
    postval["body"]=iplist
    $.ajax({ 
        type: "post",
        url: "/SetGameServerList",
        data: {
            "iplist": JSON.stringify(postval), 
        },
        dataType: 'text',
        success: function (data) {
            alert("Success");
            //getlist("Tlist");
        },
        error: function () {
            //alert("error");
        }
    })
}