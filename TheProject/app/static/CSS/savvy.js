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
            .sidebar('toggle')
        ;
    });

    // Open deactivate account modal
    $('#deactivatebtn').click(function() {
        $('.ui.basic.modal.deactivate')
            .modal('show')
        ;
    })

    // Open activate account modal
    $('#activatebtn').click(function() {
        $('.ui.basic.modal.activate')
            .modal('show')
        ;
    })

    // Open delete account modal
    $('#quitbtn').click(function() {
        $('.ui.basic.modal.destroy')
            .modal('show')
        ;
    })

    // Not sure what this is for anymore. probably nothing
    // Check later
    $('#notibtn').click(function() {
        $('.ui.modal')
            .modal('show')
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

    // Sticky effect
    $('.ui.sticky')
        .sticky({
            context: '#sticky',
            offset       : 20,
            bottomOffset : 20
        })
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
        fields: {
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
            interest: {
                identifier  : 'interest',
                rules: [
                    {
                        type    : 'maxLength[142]',
                        prompt  : 'Keep it 142 characters'
                    }
                ]
            }
        }
    };

    $('#loginForm').form(validationObj, {
        inline: true
    });

    $('#regoForm').form(validationObj, {
        inline: true
    });

    $('#profileForm').form(validationObj, {
        inline: true
    });

    $('#replyForm').form(validationObj, {
        inline: true
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
