// Load image and preview
$(function (){
    "use strict";
    $("#up_recycling").change(function(){
        console.log(this.files[0]);
        let objUrl = getObjectURL(this.files[0]) ; // 获取文件信息
        console.log("objUrl = "+objUrl);
        if (objUrl) {
            $("#img_loaded01").attr("src", objUrl);
        }
    });
});


function getObjectURL(file) {
    "use strict";
    let url = null;
    if(Window.createObjectURL !== undefined) {
        url = window.createObjectURL(file) ;
    }else if (window.URL !== undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file) ;
    }else if (window.webkitURL !== undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file) ;
    }
    return url ;
}


// Detect image
function recycling_up() {
    "use strict";
    let fileObj = $("#up_recycling")[0].files[0];
    console.log("asdfasdf",fileObj);
    let form = new FormData();
    let img_src;
    // 获取<select>元素
    var name = document.getElementById("name").value;
    var classification = document.getElementById("classification").value;
    // 获取选定的值
    var name_value = name;
    console.log(name)
    if (fileObj) {
        form.append("file", fileObj);
    }
    form.append("name",name_value)
    form.append("classification",classification)
    $.ajax({
        type: 'POST',
        url: "recycling_add",
        data: form,
        async: false,
        processData: false,
        contentType: false,
        success: function (res){
            alert("添加成功!");
            console.log(res);
            window.location.href = "recycling";
        },
        error: function (){
            alert("添加失败!");
            console.log("后台处理错误");
        }
    });}