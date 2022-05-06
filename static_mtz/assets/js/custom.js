//jQuery plugin
(function ($) {
    $.fn.uploader = function (options) {
        console.log("came to uploader")
        var settings = $.extend({
            MessageAreaText: "No files selected.",
            MessageAreaTextWithFiles: "File List:",
            DefaultErrorMessage: "Unable to open this file.",
            BadTypeErrorMessage: "We cannot accept this file type at this time.",
            acceptedFileTypes: ['pdf', 'jpg', 'gif', 'jpeg', 'bmp', 'tif', 'tiff', 'png', 'xps', 'doc', 'docx',
                'fax', 'wmp', 'ico', 'txt', 'cs', 'rtf', 'xls', 'xlsx', 'mp4', 'html', 'csv',
                'mp3', 'avi', 'mov', 'wmv', 'flv', 'zip', 'rar', 'apk', '7z', 'jar', 'py', 'xar',
                'py', 'java', 'js', 'scss', 'exe',
            ]
        }, options);

        var uploadId = 1;
        //update the messaging 
        $('.file-uploader__message-area p').text(options.MessageAreaText || settings.MessageAreaText);

        //create and add the file list and the hidden input list
        var fileList = $('<ul class="file-list"></ul>');
        // var hiddenInputs = $('<div class="hidden-inputs hidden" id="img[]"></div>');
        $('.file-uploader__message-area').after(fileList);
        // $('.file-list').after(hiddenInputs);

        //when choosing a file, add the name to the list and copy the file input into the hidden inputs
        $('.file-chooser__input').on('change', function () {
            var file = $('.file-chooser__input').val();
            var fileName = (file.match(/([^\\\/]+)$/)[0]);

            //clear any error condition
            $('.file-chooser').removeClass('error');
            $('.error-message').remove();

            //validate the file
            var check = checkFile(fileName);
            if (check === "valid") {

                //add the name and a remove button to the file-list
                var x = upload();
                console.log(x);
                if (x) {
                    $('.file-list').append('<li style="display: none;"><span class="file-list__name" style="color:black !important; ">' + fileName + '</span><button class="removal-button pqrst" onclick=deletefile() name="' + fileName + '" id="' + uploadId + '"></button></li>');
                    $('.file-list').find("li:last").show(800);
                }


                //removal button handler
                $('.removal-button').on('click', function (e) {
                    e.preventDefault();

                    //remove the corresponding hidden input
                    $('.hidden-inputs input[data-uploadid="' + $(this).data('uploadid') + '"]').remove();

                    //remove the name from file-list that corresponds to the button clicked
                    $(this).parent().hide("puff").delay(10).queue(function () { $(this).remove(); });

                    //if the list is now empty, change the text back 
                    if ($('.file-list li').length === 0) {
                        $('.file-uploader__message-area').text(options.MessageAreaText || settings.MessageAreaText);
                    }
                });

                //so the event handler works on the new "real" one
                $('.hidden-inputs .file-chooser__input').removeClass('file-chooser__input').attr('data-uploadId', uploadId);

                //update the message area
                $('.file-uploader__message-area').text(options.MessageAreaTextWithFiles || settings.MessageAreaTextWithFiles);

                uploadId++;

            } else {
                //indicate that the file is not ok
                $('.file-chooser').addClass("error");
                var errorText = options.DefaultErrorMessage || settings.DefaultErrorMessage;

                if (check === "badFileName") {
                    errorText = options.BadTypeErrorMessage || settings.BadTypeErrorMessage;
                }

                $('.file-chooser__input').after('<p class="error-message">' + errorText + '</p>');
            }
        });

        var checkFile = function (fileName) {
            var accepted = "invalid",
                acceptedFileTypes = this.acceptedFileTypes || settings.acceptedFileTypes,
                regex;

            for (var i = 0; i < acceptedFileTypes.length; i++) {
                regex = new RegExp("\\." + acceptedFileTypes[i] + "$", "i");

                if (regex.test(fileName)) {
                    accepted = "valid";
                    break;
                } else {
                    accepted = "badFileName";
                }
            }

            return accepted;
        };
    };
}(jQuery));



(function ($) {

    $.fn.uploader2 = function (options) {
        console.log("cambodia")
        var settings = $.extend({
            MessageAreaText: "No files selected.",
            MessageAreaTextWithFiles: "File List:",
            DefaultErrorMessage: "Unable to open this file.",
            BadTypeErrorMessage: "We cannot accept this file type at this time.",
            acceptedFileTypes: ['pdf', 'jpg', 'gif', 'jpeg', 'bmp', 'tif', 'tiff', 'png', 'xps', 'doc', 'docx',
                'fax', 'wmp', 'ico', 'txt', 'cs', 'rtf', 'xls', 'xlsx', 'mp4', 'html', 'csv',
                'mp3', 'avi', 'mov', 'wmv', 'flv', 'zip', 'rar', 'apk', '7z', 'jar', 'py', 'xar',
                'py', 'java', 'js', 'scss', 'exe',
            ]
        }, options);
        2
        var uploadId2 = 1;
        //update the messaging 
        $('.file-uploader2__message-area p').text(options.MessageAreaText || settings.MessageAreaText);

        //create and add the file list and the hidden input list
        var fileList = $('<ul class="file-list2"></ul>');
        // var hiddenInputs = $('<div class="hidden-inputs hidden" id="img[]"></div>');
        $('.file-uploader2__message-area').after(fileList);
        // $('.file-list').after(hiddenInputs);

        //when choosing a file, add the name to the list and copy the file input into the hidden inputs
        $('.file-chooser2__input').on('change', function () {
            var file = $('.file-chooser2__input').val();
            var fileName = (file.match(/([^\\\/]+)$/)[0]);

            //clear any error condition
            $('.file-chooser2').removeClass('error');
            $('.error-message2').remove();

            //validate the file
            var check = checkFile(fileName);
            if (check === "valid") {

                //add the name and a remove button to the file-list
                var x = upload2();
                console.log(x);
                if (x) {
                    $('.file-list2').append('<li style="display: none;"><span class="file-list2__name" style="color:black !important;">' + fileName + '</span><button class="removal-button2 pqrs" onclick=deletefile2() name="' + fileName + '" id="' + uploadId2 + '"></button></li>');
                    $('.file-list2').find("li:last").show(800);
                }


                //removal button handler
                $('.removal-button2').on('click', function (e) {
                    e.preventDefault();

                    //remove the corresponding hidden input
                    $('.hidden-inputs input[data-uploadid="' + $(this).data('uploadid') + '"]').remove();

                    //remove the name from file-list that corresponds to the button clicked
                    $(this).parent().hide("puff").delay(10).queue(function () { $(this).remove(); });

                    //if the list is now empty, change the text back 
                    if ($('.file-list2 li').length === 0) {
                        $('.file-uploader2__message-area').text(options.MessageAreaText || settings.MessageAreaText);
                    }
                });

                //so the event handler works on the new "real" one
                $('.hidden-inputs .file-chooser2__input').removeClass('file-chooser2__input').attr('data-uploadId', uploadId2);

                //update the message area
                $('.file-uploader2__message-area').text(options.MessageAreaTextWithFiles || settings.MessageAreaTextWithFiles);

                uploadId2++;

            } else {
                //indicate that the file is not ok
                $('.file-chooser2').addClass("error");
                var errorText = options.DefaultErrorMessage || settings.DefaultErrorMessage;

                if (check === "badFileName") {
                    errorText = options.BadTypeErrorMessage || settings.BadTypeErrorMessage;
                }

                $('.file-chooser2__input').after('<p class="error-message2">' + errorText + '</p>');
            }
        });

        var checkFile = function (fileName) {
            var accepted = "invalid",
                acceptedFileTypes = this.acceptedFileTypes || settings.acceptedFileTypes,
                regex;

            for (var i = 0; i < acceptedFileTypes.length; i++) {
                regex = new RegExp("\\." + acceptedFileTypes[i] + "$", "i");

                if (regex.test(fileName)) {
                    accepted = "valid";
                    break;
                } else {
                    accepted = "badFileName";
                }
            }

            return accepted;
        };
    };
}(jQuery));
//init 


$(document).ready(function () {
    $('.fileUploader').uploader({
        MessageAreaText: "No files selected. Please select a file."
    });
});

$(document).ready(function () {
    $('.fileUploader').uploader2({
        MessageAreaText: "No files selected. Please select a file."
    });
});