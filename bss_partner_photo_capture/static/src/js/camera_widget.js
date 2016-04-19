openerp.bss_partner_photo_capture = function(instance) {

    instance.bss_partner_photo_capture.FieldBssCamera = instance.web.form.FieldChar.extend({
        template : "FieldBssCamera",

        initialize_content: function() {
            this._super();
        },

        render_value: function() {
            var canvas = $("#canvas"),
                context = canvas[0].getContext("2d"),
                zoneCanvas = $("#zoneCanvas"),
                zoneContext = zoneCanvas[0].getContext("2d"),
                exportCanvas = $("#exportCanvas"),
                exportContext = exportCanvas[0].getContext("2d"),
                video = $("#video"),
                videoObj = { "video": true },
                snapshot_btn = $("#snapshot_btn"),
                video_btn = $("#video_btn"),
                saveButton = $("#saveBtn"),
                moveActive = false,
                resizeActive = false,
                zoneX = 220, 
                zoneY = 140,
                zoneS = 200,
                startX, startY,
                mouseX, mouseY,

                errBack = function(error) {
                    console.log("Video capture error: ", error.code); 
                },

                videoMode = function() {
                    canvas.hide();
                    zoneCanvas.hide();
                    video_btn.hide();
                    video.show();
                    snapshot_btn.show();
                };
                photoMode = function() {
                    video.hide();
                    snapshot_btn.hide();
                    canvas.show();
                    zoneCanvas.show();
                    video_btn.show();
                };

            videoMode();

            // Put video listeners into place
            if(navigator.getUserMedia) { // Standard
                navigator.getUserMedia(videoObj, function(stream) {
                    video[0].src = stream;
                    video[0].play();
                }, errBack);
            } else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
                navigator.webkitGetUserMedia(videoObj, function(stream){
                    video[0].src = window.webkitURL.createObjectURL(stream);
                    video[0].play();
                }, errBack);
            }
            else if(navigator.mozGetUserMedia) { // Firefox-prefixed
                navigator.mozGetUserMedia(videoObj, function(stream){
                    video[0].src = window.URL.createObjectURL(stream);
                    video[0].play();
                }, errBack);
            }
            
            var drawZone = function() {
                zoneContext.clearRect(0, 0, 640, 480);
                zoneContext.beginPath();
                zoneContext.lineWidth="2";
                zoneContext.strokeStyle="blue";
                zoneContext.rect(zoneX,zoneY,zoneS,zoneS);
                zoneContext.stroke();
            };

            snapshot_btn[0].addEventListener("click", function() {
                context.drawImage(video[0], 0, 0, 640, 480);
                drawZone();
                photoMode();
            });

            video_btn[0].addEventListener("click", function() {
                videoMode();
            });

            zoneCanvas.mousedown(function(e) {
                moveActive = true;
                startX = zoneX;
                startY = zoneY;
                mouseX = e.pageX;
                mouseY = e.pageY;
            });

            $(window).mouseup(function(e) {
                if (moveActive) {
                    moveActive = false
                    e.preventDefault();
                }
            });

            $(window).mousemove(function(e) {
                if (moveActive) {
                    zoneX = startX + e.pageX - mouseX;
                    zoneY = startY + e.pageY - mouseY;
                    if (zoneX < 0) {
                        zoneX = 0;
                    }
                    if (zoneX > 640 - zoneS) {
                        zoneX = 640 - zoneS;
                    }
                    if (zoneY < 0) {
                        zoneY = 0;
                    }
                    if (zoneY > 480 - zoneS) {
                        zoneY = 480 - zoneS;
                    }
                    drawZone();
                    e.preventDefault();
                }
            });

            saveButton.click(function() {  
                exportCanvas.prop("width", zoneS);
                exportCanvas.prop("height", zoneS);
                exportContext.drawImage(canvas[0], zoneX, zoneY, zoneS, zoneS, 0, 0, zoneS, zoneS);

                var partner_obj = new instance.web.Model('res.partner');
                partner_obj.call('write', [[5], {'image': exportCanvas[0].toDataURL("image/jpeg", 1.0).split(/,(.+)?/)[1]}]);
            });

        }
        });

    instance.web.form.widgets.add('bss_camera', 'instance.bss_partner_photo_capture.FieldBssCamera');
}
