$(function () {
    var $image;
    var cropBoxData;
    var canvasData;
    var isInitialized = false;

    /* CROPPER INITIALISATION*/
    function initCropper() {
        $image = $("#avatar");
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 224,
            minCropBoxHeight: 224,
            dragMode: 'move',
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
        isInitialized = true;
    }

    function destroyCropper() {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    }

    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_avatar").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.readAsDataURL(this.files[0]);
            reader.onload = function (e) {
                $("#avatar").attr("src", e.target.result);
                if (isInitialized = true) {
                    destroyCropper();
                }
                initCropper();
            };
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    $("#modalAvatar").on("shown.bs.modal", function () {
        initCropper()
    }).on("hidden.bs.modal", function () {
        destroyCropper()
    });

    $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#formAvatarUpload").submit();
    });
});