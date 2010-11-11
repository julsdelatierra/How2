//TODO: Simplificar acciones del How2 en JQuery
function tiny(){
    tinyMCE.init({
            mode : "textareas",
            theme : "advanced",
            skin: "o2k7",
            plugins : "safari,style,advlink,contextmenu,paste,directionality,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
            theme_advanced_buttons1 : "forecolor,backcolor,|,bold,italic,underline,|,bullist,numlist,|,outdent,indent,|,link,unlink,image,|,sub,sup,charmap",
            theme_advanced_buttons2 : "",
            theme_advanced_buttons3 : "",
            theme_advanced_buttons4 : "",
            theme_advanced_toolbar_location : "top",
            theme_advanced_toolbar_align : "left",
            theme_advanced_resizing : false
    });
}
$(document).ready(function(){
    var c=0;
    $("#contribute_category_button").click(function(){
        if (c==0){
            $("#contribute_category").slideDown("slow");
            $("#contribute_category_button").attr({value:'Cancel'});
            $("#contribute_how2_button").attr({disabled:'True'});
            $("#new_how2_button").attr({disabled:'True'});
            c=1;
            $("#title_contribute_category").focus(function(){
                if($("#title_contribute_category").attr('value')=='Category'){
                    $("#title_contribute_category").removeAttr('value');
                }
            });
        }
        else{
            $("#contribute_category").slideUp("slow");
            $("#contribute_category_button").attr({value:'Suggest category'})
            $("#contribute_how2_button").removeAttr('disabled');
            $("#new_how2_button").removeAttr('disabled');
            $("#title_contribute_category").attr({value:'Category'});
            c=0;
        }
    });
    var h = 0;
    $("#contribute_how2_button").click(function(){
        if (h==0){
            $("#contribute_how2").slideDown("slow");
            $("#contribute_how2_button").attr({value:'Cancel'});
            $("#contribute_category_button").attr({disabled:'True'});
            $("#new_how2_button").attr({disabled:'True'});
            h=1;
            $("#title_contribute_how2").focus(function(){
                if ($("#title_contribute_how2").attr('value')=='Title'){
                    $("#title_contribute_how2").removeAttr('value');
                }
            });
        }
        else{
            $("#contribute_how2").slideUp("slow");
            $("#contribute_how2_button").attr({value:'Suggest how2'})
            $("#contribute_category_button").removeAttr('disabled');
            $("#new_how2_button").removeAttr('disabled');
            $("#title_contribute_how2").attr({value:'Title'});
            h=0;
        }
    });
    $("#ch2").submit(function(){
        if(($("#title_contribute_how2").attr('value')=='')||($("#description_contribute_how2").attr('value')=='')){
            $("#error").slideDown("slow").delay(1700).slideUp("slow");
        }
        else{
            $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            complete: function(){
                $("#contribute_how2").slideUp("slow");
                $("#contribute_how2_button").attr({value:'Suggest how2'})
                $("#contribute_category_button").removeAttr('disabled');
                $("#new_how2_button").removeAttr('disabled');
                h=0;
                $("#notice_ch2").slideDown("slow").delay(1700).slideUp("slow");
                $("#title_contribute_how2").attr({value:'Title'});
            }
            });
        }
        return false;
    });
    $("#cc").submit(function(){
        if($("#id_name").attr('value')==''){
            $("#error").slideDown("slow").delay(1700).slideUp("slow");
        }
        else{
            $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: {'name':$("#id_name").attr('value'),'template':$('#id_template').tinymce().getContent()},
            complete: function(){
                $("#contribute_category").slideUp("slow");
                $("#contribute_category_button").attr({value:'Suggest category'})
                $("#contribute_how2_button").removeAttr('disabled');
                $("#new_how2_button").removeAttr('disabled');
                c=0;
                $("#notice_cc").slideDown("slow").delay(1700).slideUp("slow");
                $("#title_contribute_category").attr({value:'Category'});
            }
            });
        }
        return false;
    });
    $("#read_button").click(function(){
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            complete:function(){
                $("#read_button").attr({'value':'Reading'});
                $("#read_button").attr({'disabled':'True'});
            }
        });
    });
    $("#mode_ask").change(function(){
        if($(this).attr('value')=='1'){
            $("#ask_to_hidden").show("slow");
        }
        else{
            $("#ask_to_hidden").hide("slow");
        }
    });
    $(".star_vote").click(function(){
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            complete: function(){
                $("#rating").hide("fast");
            }
        });
    });
    $("#suggest_how2_button").click(function(){
        $("#suggest_how2").show('slow');
    });
    $("#id_category").change(function(){
        $.ajax({
            type:'POST',
            url: '/load_template/',
            data: {'category':$(this).attr('value')},
            success : function(data){
                $('#id_content').tinymce().execCommand('mceSetContent',false,data);
            }
        });
    });
    $("#id_lang").change(function(){
        $.ajax({
            type: 'POST',
            url: '/load_translation/',
            data: {'lang':$(this).attr('value'),'how2':$(this).attr('howto')},
            success: function(data){
                $("#how2_title").text(data['title']);
                $("#how2_content").html(data['content']);
            }
        });
    });
    $("#id_email").focus(function(){
        if($("#id_username").attr('value')==''){
            $('#form_error').show('slow').delay(2000).hide('slow');
            $("#id_username").focus();
        }
        else{
            $.ajax({
                type: 'POST',
                url: '/check_username/',
                data: {'username':$("#id_username").attr('value')},
                success: function(data){
                    if (data == '1'){
                        $("#u_notice").slideDown('slow');
                    }
                    else{
                        $("#u_error").slideDown('slow').delay(2000).slideUp('slow');
                        $("#id_username").focus();
                    }
                }
            });
        }
    });
    $("#id_password").focus(function(){
       if($("#id_email").attr('value')==''){
            $('#form_error').slideDown('slow').delay(2000).slideUp('slow');
            $("#id_email").focus();
        }
        else{
            expr = /^[^@\s]+@[^@\.\s]+(\.[^@\.\s]+)+$/;
            if(!expr.test($("#id_email").attr('value'))){
                $('#email_error').slideDown('slow').delay(2000).slideUp('slow');
                $("#id_email").focus();
            }
            else{
                $.ajax({
                    type: 'POST',
                    url: '/check_email/',
                    data: {'email':$("#id_email").attr('value')},
                    success: function(data){
                        if (data == '1'){
                            $("#e_notice").slideDown('slow');
                        }
                        else{
                            $("#e_error").slideDown('slow').delay(2000).slideUp('slow');
                            $("#id_email").focus();
                        }
                    }
                });
            }
        }
    });
});