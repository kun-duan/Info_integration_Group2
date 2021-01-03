var ec_center_fumu = echarts.init(document.getElementById('c2'), "dark");

var mydata = [{'name': '上海', 'value': 318,'color':'#009fe8'}, {'name': '云南', 'value': 162,'color':'#009fe8'}]
//各省地图颜色数据依赖value
var ec_center_fumu_option = {
    title: {
        text: '',
        subtext: '',
        x: 'left'
    },
    tooltip: {
        trigger: 'item'
    },
    //左侧小导航图标
    visualMap: {
        show: true,
        x: 'left',
        y: 'bottom',
        textStyle: {
            fontSize: 5,
        },
        splitList: [{ start: 1,end: 4999 },
            {start: 5000, end: 9999 },
            {start: 10000, end: 14999 },
            { start: 15000, end: 19999 },
            {  start: 20000, end: 24999 },
            { start: 25000 }],
        color: ['#DC143C', '#FF1493', '#ba55d3', '#45b97c', '#33a3dc','#426ab3']
    },
    //配置属性
    series: [{
        name: '父母数量',
        type: 'map',
        mapType: 'china',
        roam: false, //拖动和缩放
        itemStyle: {
            normal: {
                borderWidth: .5, //区域边框宽度
                borderColor: '#009fe8', //区域边框颜色
                areaColor: "#ffefd5", //区域颜色
            },
            emphasis: { //鼠标滑过地图高亮的相关设置
                borderWidth: .5,
                borderColor: '#4b0082',
                areaColor: "#fff",
            }
        },
        label: {
            normal: {
                show: true, //省份名称
                fontSize: 6,
            },
            emphasis: {
                show: true,
                fontSize: 8,
            }
        },
        data: []  //mydata //数据
    }],

};
ec_center_fumu.setOption(ec_center_fumu_option)