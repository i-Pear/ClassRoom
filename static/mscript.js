function getOccupyFunction(date) {
    var str1 = "/getOccupyOperation?" + "date=" + date;
    $.ajax(str1, {
        //请求方式
        type: "POST",
        //请求的媒体类型
        // contentType: "application/json;charset=UTF-8",
        //请求头
        headers: {},
        //数据，json字符串
        // data : JSON.stringify(log),
        //请求成功
        success: function (result) {
            console.log(result);
            let obj = JSON.parse(result);
            let state=obj.state;
            let message=obj.message;
            let data=obj.data;
            console.log(obj);
            console.log(state);
            console.log(message);
            console.log(data);
        },
        //请求失败，包含具体的错误信息
        error: function (e) {
            console.log(e.status);
            console.log(e.responseText);
        }
    });
}