$(function(){

    $("input.maj").change(function(){
        var url = "/administration/organisation/ajax/mise_a_jour/";
        var id = $(this).attr("id")
        var model = $(this).attr("model")
        var name = $(this).attr("name")
        var val = $(this).val()
        $.post(url, {model:model, name:name, id:id, val:val}, (data)=>{
            if (data.status) {
                Alerter.success('Reussite !', "Modification prise en compte avec succès !");
            }else{
                Alerter.error('Erreur !', data.message);
            }
        },"json");
    })

})