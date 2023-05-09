var ytdefer_ic_w = 73;
var ytdefer_ic_h = 52;
var yt_icon =
    '<svg height="100%" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 68 48" width="100%"><path class="ytp-large-play-button-bg" d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#eb3223"></path><path d="M 45,24 27,14 27,34" fill="#fff"></path></svg>';
var yt_dark_icon =
    '<svg height="100%" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 68 48" width="100%"><path class="ytp-large-play-button-bg" d="M66.52,7.74c-0.78-2.93-2.49-5.41-5.42-6.19C55.79,.13,34,0,34,0S12.21,.13,6.9,1.55 C3.97,2.33,2.27,4.81,1.48,7.74C0.06,13.05,0,24,0,24s0.06,10.95,1.48,16.26c0.78,2.93,2.49,5.41,5.42,6.19 C12.21,47.87,34,48,34,48s21.79-0.13,27.1-1.55c2.93-0.78,4.64-3.26,5.42-6.19C67.94,34.95,68,24,68,24S67.94,13.05,66.52,7.74z" fill="#212121" fill-opacity="0.8"></path><path d="M 45,24 27,14 27,34" fill="#fff"></path></svg>';

function ch_ytdefer_setup() {
    var d = document;
    var els = d.getElementsByClassName("ch_ytdefer");
    for (var i = 0; i < els.length; i++) {
        var im = els[i];
        var ds = im.getAttribute("data-src");
        if (!ds) {
            alert("data-src missing for video");
            return;
        }
        // Add ids and clicks		
        im.setAttribute('id', "ch_ytdefer" + i);
        //im.id= ;
        im.onclick = gen_ytdefer_clk(i);
        //e.appendChild(im);

        // Add id to button
        var bt = im.getElementsByClassName("ch_ytdefer_btn")[0];
        bt.setAttribute("id", "ch_ytdefer_icon" + i);

        // Hover button
        im.onmouseover = gen_mouseover(bt);
        im.onmouseout = gen_mouseout(bt);

    }
    if (typeof YT == "undefined") {
        var js = d.createElement("script");
        js.src = "https://www.youtube.com/player_api";
        d.body.appendChild(js);
    }
}

function gen_mouseout(bt) {
    return function() {
        bt.style.backgroundImage = "url(data:image/svg+xml;base64," + window.btoa(yt_dark_icon) + ")";
    };
}

function gen_mouseover(bt) {
    return function() {
        bt.style.backgroundImage = "url(data:image/svg+xml;base64," + window.btoa(yt_icon) + ")";
    };
}

function gen_ytdefer_clk(i) {
    return function() {
        var d = document;
        var im = d.getElementById("ch_ytdefer" + i);
        // Get video id from source
        var vid_id = im.getAttribute("data-src");


        // Create an iframe with the responsive class and append it as a child
        var ifr = d.createElement("div");
        ifr.id = "ch_ytdefer_frame" + i;
        ifr.classList.add("embed-responsive-item");
        ifr.setAttribute("itemprop", "embedUrl");
        im.appendChild(ifr);

        //Remove attributes
        //im.removeAttribute('style');

        // Add player
        var player = new YT.Player(ifr.id, {
            videoId: vid_id,
            events: {
                onReady: function(ev) {
                    ev.target.playVideo();
                },
            },
        });

    };
}

window.addEventListener('load', ch_ytdefer_setup);