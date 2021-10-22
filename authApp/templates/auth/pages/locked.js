

$(function(){

    $("form#lockedForm").submit(function(event) {
        Loader.start()
        var url = "../ajax/unlocked/";
        var formData = new FormData($(this)[0]);
        $.post({url:url, data:formData, processData:false, contentType:false}, function(data) {
            if (data.status) {
                window.location.href = data.url;
            }else{
                Alerter.error('Erreur !', data.message);
            }
        }, 'json');
        return false;
    });

})