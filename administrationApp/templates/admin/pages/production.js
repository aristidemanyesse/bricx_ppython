

$(function(){

    $(".formExigence").submit(function(event) {
        Loader.start();
        var url = "/administration/organisation/ajax/exigence/";
        var formdata = new FormData($(this)[0]);
        $.post({url:url, data:formdata, contentType:false, processData:false}, function(data){
            if (data.status) {
                window.location.reload();
            }else{
                Alerter.error('Erreur !', data.message);
            }
        }, 'json')
        return false;
    });


    change_production_auto = function(){
        var url = "/administration/organisation/ajax/change_production_auto/";
        $.post(url, {}, (data)=>{
            if (data.status) {
                Alerter.success('Mise à jour !', "Modification effectuée avec succès !");
            }else{
                Alerter.error('Erreur !', data.message);
            }
        },"json");
    }

})