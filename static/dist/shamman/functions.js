
$(function(){


    modal = function(modal){
        $(modal).modal("show")
    }



    //mettre en session par ajax
    session = function(name, value){
    	var url = "../../composants/dist/shamman/traitement.php";
    	$.post(url, {action:"session", name:name, value:value}, (data)=>{
            return data;
        });
    }

    //mettre en session par ajax
    unsetSession = function(name){
        var url = "../../composants/dist/shamman/traitement.php";
        $.post(url, {action:"unsetSession", name:name}, (data)=>{
            return data;
        });
    }

    //mettre en session par ajax
    getSession = function(name){
    	var url = "../../composants/dist/shamman/traitement.php";
    	$.post(url, {action:"getSession", name:name}, (data)=>{
            return data;
        });
    }



    //concatener a 0
    concate0 = function(nom){
        if (nom < 10) {
            return "0"+nom;
        }
        return nom;
    }


});