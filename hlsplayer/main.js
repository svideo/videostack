function playUrl()
{
    //http://d3sporhxbkob1v.cloudfront.net/bill/vod/sample-video/400k.m3u8
    var url = $("#inputUrlId").val();
    if(!url) {
        return 0;
    }
   
    $.ajax();
    var browserJs = '<script src="js/hls/browser.js" data-canvas="canvas" data-hls="' + url +'">'
                  //+ "document.body.classList.remove('loading');"
                  + "var converter = this;"
                  + "['play', 'pause'].forEach(function (action) {"
                  + "document.getElementById(action).addEventListener('click', function () {"
                  + "document.body.classList.toggle('paused');"
                  + "converter.currentVideo[action]();"
                  + "});" 
                  + "});"
                  + "</script>";

    $("#browserJsId").html(browserJs);
}
