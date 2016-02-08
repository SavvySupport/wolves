$(function () {
    var screenHeight = $(document).height()
    var liftHeight = $('#toTop').height()
    $('#toTopRight').fadeOut();
    $("#toTopRight").css("padding-top", screenHeight + liftHeight * 2);
    $('#toTopRight').fadeIn();

    // Submit form with enter key
    $(function() {
        $("form ui input").keypress(function (e) {
            if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
                $('button[type=submit] .default').click();
                return false;
            } else {
                return true;
            }
        });
    });

    // Open sidebar
    $('#sidebar').click(function() {
        $('.ui.labeled.icon.sidebar')
            .sidebar('setting', 'transition', 'slide along')
            .sidebar('toggle')
        ;
    });

    // Dimmer image on hover
    // Used for displaying fan images
    $('.fanimg.image').dimmer({
        on: 'hover'
    });

    // Automatically shows on init if cookie isnt set
    $('.cookie.nag')
        .nag({
            key      : 'accepts-cookies',
            value    : true
        })
    ;

    // Checkboxes effect
    $('.ui.checkbox')
        .checkbox()
    ;

    // Dropdown list
    $('.ui.dropdown')
        .dropdown()
    ;

    // Sticky effect
    $('.ui.sticky')
        .sticky({
            context: '#stuck',
            pushing: true,
            offset       : 20,
            bottomOffset : 20
        })
    ;

    $('.ui.sticky')
        .sticky('refresh')
    ;

    // Accordion effect
    $('.ui.accordion')
        .accordion()
    ;

    // Dimmer image on hover
    // Used for profile card
    $('.special.cards .image').dimmer({
        on: 'hover'
    });

    // Form validation
    var validationObj = {
        username: {
            identifier  : 'username',
            rules: [
                {
                    type    : 'empty',
                    prompt  : 'username cannot be empty'
                },
                {
                    type    : 'length[5]',
                    prompt  : 'minimum 5 characters required'
                },
                {
                    type    : 'regExp[/^\\w*[^\\[\\]\\^\\$\\.\\|\\?\\*\\+\\(\\)\\\\~\\`\\!\\@\\#\\%\\&\\-\\_\\+\\=\\{\\}\\\'\\"\\"\\<\\>\\:\\;\\, ]+\\w+$/g]',
                    prompt  : 'username cannot contain special characters'
                }
            ]
        },
        password: {
            identifier  : 'password',
            rules: [
                {
                    type    : 'empty',
                    prompt  : 'password cannot be empty'
                },
                {
                    type    : 'length[5]',
                    prompt  : 'minimum 5 characters required'
                }
            ]
        },
        email: {
            identifier  : 'email',
            rules: [
                {
                    type    : 'empty',
                    prompt  : 'email cannot be empty'
                },
                {
                    type    : 'email',
                    prompt  : 'invalid email format?'
                }
            ]
        },
        passwordconfirm: {
            identifier  : 'passwordconfirm',
            rules: [
                {
                    type    : 'match[password]',
                    prompt  : 'your passwords don\'t match.'
                }
            ]
        },
        phone: {
            identifier  : 'phoneNumber',
            rules: [
                {
                    type    : 'regExp[/^[0-9]{8,14}$/]',
                    prompt  : 'Must be all number'
                }
            ]
        },
        termsConditions: {
            identifier  : 'termsConditions',
            rules: [
                {
                    type    : 'checked',
                    prompt  : 'You must agree to the terms first'
                }
            ]
        },
        title: {
            identifier  : 'title',
            rules: [
                {
                    type    : 'empty',
                    prompt  : 'Job title is required'
                },
                {
                    type    : 'minLength[10]',
                    prompt  : 'minimum 10 characters required'
                }
            ]
        },
        description: {
            identifier  : 'description',
            rules: [
                {
                    type    : 'empty',
                    prompt  : 'Job description is required'
                },
                {
                    type    : 'minLength[50]',
                    prompt  : 'minimum 50 characters required'
                },
                {
                    type    : 'maxlength[150]',
                    prompt  : 'maximum 150 characters required'
                }
            ]
        }
    };

    $('#jobForm').form(validationObj, {
        inline: true,
        on: "blur"
    });

    $('#loginForm').form(validationObj, {
        inline: true,
        on: "blur"
    });

    $('#registerForm').form(validationObj, {
        inline: true,
        on: "blur"
    });

    $('#profileForm').form(validationObj, {
        inline: true,
        on: "blur"
    });

    $('#recoverForm').form(validationObj, {
        inline: true,
        on: "blur"
    });

    $('#changepasswordForm').form(validationObj, {
        inline: true,
        on: "blur"
    });

    // Dismiss message
    $('.message .close')
        .on('click', function() {
            $(this)
                .closest('.message')
                .transition('fade')
                ;
            })
        ;

    // Trigger file selector by clicking on the profile
    $('#upload').click(function(){
        $('#attachmentName').click();
    });

    $('#attachmentName').change(function() {
        $('#submit').click();
    });

    $('#submit').click(function() {
        event.preventDefault();
        var form_data = new FormData($('#photoForm')[0]);
        $.ajax({
            type: 'POST',
            url: '/dpupload',
            data: form_data,
            contentType: false,
            processData: false,
            dataType: 'json'
        }).done(function(data, textStatus, jqXHR){
            $("#photoajax").attr('src', data['path']);
            console.log('Success!');
        }).fail(function(data) {
            alert('Failed!');
        }).complete(function(data) {
            console.log('completed');
        });
    });

    $('.deleteJobButton').click(function() {
        event.preventDefault();
        //var form_data = new FormData($('#viewJobForm')[0]);
        var $div = $(this).closest('div')
        var jobId = $div.find('input[name="jobId"]').val();
        var listId = $div.find('input[name="listId"]').val();
        //var jobId = $('#jobId').val();
        //var listId = $('#listId').val();
        data = {
                'test'  : '1234',
                'jobId' : jobId,
                'listId': listId

                }
        $.ajax({
            type: 'POST',
            url: '/deleteJob',
//            data: data,
//            contentType: false,
//            processData: false,
//            dataType: 'json'
            datatype : "json",
            contentType: "application/json; charset=utf-8",
            data : JSON.stringify(data),
        }).done(function(data, textStatus, jqXHR){
            $(data['returnString']).remove();
            console.log('Success!');
        }).fail(function(data) {
            alert('Failed!' + jobId + 'listId' + listId + 'whooo');
        }).complete(function(data) {
            console.log('completed');
        });
    });

    // Restyle and handle file uploads
    var fileExtentionRange = '.png .jpg .jpeg';
    var MAX_SIZE = 3; // MB

    $(document).on('change', '.btn-file :file', function() {
        var input = $(this);

        if (navigator.appVersion.indexOf("MSIE") != -1) { // IE
            var label = input.val();

            input.trigger('fileselect', [ 1, label, 0 ]);
        } else {
            var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
            var numFiles = input.get(0).files ? input.get(0).files.length : 1;
            var size = input.get(0).files[0].size;

            input.trigger('fileselect', [ numFiles, label, size ]);
        }
    });

    $('.btn-file :file').on('fileselect', function(event, numFiles, label, size) {
        $('#attachmentName').attr('name', 'attachmentName'); // allow upload.

        var postfix = label.substr(label.lastIndexOf('.'));
        if (fileExtentionRange.indexOf(postfix.toLowerCase()) > -1) {
            if (size > 1024 * 1024 * MAX_SIZE ) {
                alert('max size：<strong>' + MAX_SIZE + '</strong> MB.');

                $('#attachmentName').removeAttr('name'); // cancel upload file.
            } else {
                $('#_attachmentName').val(label);
            }
        } else {
            alert('Sorry! I\'m not Superman. I can only support these file types ' + fileExtentionRange);
            $('#attachmentName').removeAttr('name'); // cancel upload file.
        }
    });
});
