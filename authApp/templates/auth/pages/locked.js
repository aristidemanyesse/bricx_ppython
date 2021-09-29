

$(function(){
    
        $("form#lockedForm").submit(function(event) {
        var url = "../../webapp/main/modules/access/locked/ajax.php";
        var formData = new FormData($(this)[0]);
        formData.append('action', 'locked');
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