
function playUrl()
{
    //http://d3sporhxbkob1v.cloudfront.net/bill/vod/sample-video/400k.m3u8
    var url = $("#inputUrlId").val();
    if(!url) {
        return 0;
    }

    parseManifest(url);
    if(manifest) {
        url = manifest[0];
        console.log("This m3u8 is multiple bitrate, default choose first");
    } else {
        console.log("This m3u8 is single bitrate");
    }

    var browserJs = '<script src="lib/hls/browser.js" data-canvas="canvas" data-hls="' + url +'">'
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

var manifest;

function parseManifest(url)
{
    $.ajax({
        url: url,
        type: "GET",
        async: false,
        dataType: "text",
  
        success: function(data) {
            var regExpStr       = new RegExp(/\.ts/);
            var isChildManifest = regExpStr.test(data);
            if(isChildManifest) {
                return '';
            }

            var dataArray = new Array();
            
            manifest  = new Array();
            dataArray = data.split(/\r?\n/);
            
            var i = 0;
            var j = 0;

            for(i = 0; i < dataArray.length; i++) {
                var regStr = new RegExp(/^#/);
                var isNote = regStr.test(dataArray[i]);
                if(isNote == false){
                    if(dataArray[i]){
                        manifest[j] = dataArray[i];
                        j++;
                    } 
                }
            }
        },
        error: function() {
            console.log("error");
        }
    });
}

