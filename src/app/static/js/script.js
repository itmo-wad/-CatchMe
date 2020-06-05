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


// Token storage
$('.save_token').click(function() {
    token = $('.token_area').val();
    console.log(token);
    if (token.length == 105) {
      $.get("/save_token", { token:token }).done(function(result) {
        if (result=="True"){
          location.reload();
        };
      };
    }
});
