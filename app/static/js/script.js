// Token renderer
$('.gen_token').click(function() {
    console.log('Inside');
    $.get("/gen_token").done(function(token) {
        try{
            $('.token_area').val(token);
        }
        catch(error){
            console.error(error);
        }
    });
});
