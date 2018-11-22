var $ = jQuery.noConflict();

// ====================================== Account reactions =====================================
(function ($) {
    var $image;
    var cropBoxData;
    var canvasData;
    var isInitialized = false;
    var initialAvatar = $("#avatar").attr("src");

    /* CROPPER INITIALISATION & DESRTROY*/
    function initCropper() {
        $image = $("#avatar");
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 224,
            minCropBoxHeight: 224,
            cropBoxResizable: false,
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
    $("#id_avatar").on("change", function () {
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
        else {
            $("#avatar").attr("src", initialAvatar);
        }
    }).fileinput({
        /* SCRIPT TO CONFIG THE BOOTSTRAP FILE-UPLOAD OBJECT */
        mainClass: "input-group-md",
        msgPlaceholder: "Выберите картинку",
        showUpload: true,
        previewFileType: "image",
        browseClass: "btn btn-success",
        browseLabel: "Выбрать",
        browseIcon: "<i class=\"icon-picture\"></i> ",
        removeClass: "btn btn-danger",
        removeLabel: "Удалить",
        removeIcon: "<i class=\"icon-trash\"></i> ",
        removeTitle: "Отменить выбор данного файла",
        uploadClass: "btn btn-info",
        uploadLabel: "Загрузить",
        uploadIcon: "<i class=\"icon-upload\"></i> ",
        uploadTitle: "Обрезать и загрузить данный файл"
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

    /* SCRIPT TO CLEAR LOADED IMAGE */
    $(".fileinput-remove-button").click(function () {
        $("#avatar").attr("src", initialAvatar)
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".fileinput-upload-button").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#formAvatarUpload").submit();
    });

})(jQuery);