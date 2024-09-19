// Load image and preview
$(function (){
    "use strict";
    $("#load_img01").change(function(){
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
function detect() {
    "use strict";
    let fileObj = $("#load_img01")[0].files[0];
    console.log(fileObj);
    let form = new FormData();

    form.append("file", fileObj);

    $.ajax({
        type: 'POST',
        url: "imageDetect",
        data: form,
        async: false,
        processData: false,
        contentType: false,
        success: function (res){
            alert("检测完成!");
            console.log(res);
            // img_src = "data:image/png;base64,"+res;
            // console.log(img_src);
            // $("#img_detected").attr("src",res);
            window.location.href = "disposal/"+res;
        },
        error: function (){
            alert("检测失败!");
            console.log("后台处理错误");
        }
    });

}