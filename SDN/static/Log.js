function getLog(pid,sname)
{
    $.ajax({
        url: "/getLog",
        type: "GET",
        data: {
            "userName":sname
        },
        dataType: "json",
        success: function(data) {
            display(pid,data.x,data.time,data.value,data.name)

            

        }
    })
}
function display(pid,listx,time,value,userName)
{
    
        // 路径配置
        require.config({
            paths: {
                echarts: '/static/dist'
            }
        });
        
        // 使用
        require(
            [
                'echarts',
                'echarts/chart/line'
            ],
            function (ec) {
                // 基于准备好的dom，初始化echarts图表
                var myChart = ec.init(document.getElementById(pid)); 
                
                var option = {
                    title : {
                        text: userName+"游戏服务器连接历史"
                    },
                    tooltip : {
                        trigger: 'axis'
                    },
                    
                    toolbox: {
                        show : false,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : listx
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value'
                        }
                    ],
                    
                    series : [
                        {
                            name:'意向',
                            type:'line',
                            smooth:true,
                            itemStyle: {normal: {areaStyle: {type: 'default'}}},
                            data:value,
                            tooltip: {  
                                trigger: 'item',  
                                formatter: function(a){  
                                        return (time[a["name"]]);  
                                            }  
                                },  
                        }
                    ]
                };
                    
            
        
                // 为echarts对象加载数据 
                myChart.setOption(option); 
            }
        );
}