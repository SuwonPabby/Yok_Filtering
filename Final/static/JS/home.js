$(document).ready(function(){
    $("#loading").hide();
    $('form input').change(function () {
        $('form p').text(this.files.length + " file(s) selected");
    });
});


    

