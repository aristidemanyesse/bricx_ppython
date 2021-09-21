
$(function(){

    voirPrixParZone = function(){    
        Loader.start();    
        var  url = "../../webapp/boutique/elements/templates/traitement.php";
        $.post(url, {action:"voirPrixParZone"}, (data)=>{
            $("body #modal-prixparzone").remove();
            $("body").append(data);
            $("body #modal-prixparzone").modal("show");
            $("select.select2").select2();
            Loader.stop();    
        },"html");
    }



	// Initialisation des plugins
	$("select.select2").select2();


    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });


    $('.footable').footable({
        "paging": {
            "size": 20
        }
    });

    $("#top-search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("table.table-mise tr:not(.no)").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });



    $("input[type=checkbox]").change(function(event) {
        if ($(this).is(":checked")) {
            $(this).parent("label").css("color", "orangered");
        }else{
            $(this).parent("label").css("color", "#888");
        }
    });
    $("input[type=radio]").change(function(event) {
      name = $(this).attr("name")
      $("input[name="+name+"]").parent("label").css("color", "#888");
      $(this).parent("label").css("color", "orangered");
  });

	//
	$('body').on("click", "button.btn_image", function(event) {
		$(this).prev("input[type=file]").trigger('click');
	});
	$('body').on("change", ".modal input[type=file]", function(e) {
		var src = URL.createObjectURL(e.target.files[0])
		$(this).prev("img.logo").attr('src', src);
	});


	$(".btn_modal").click(function(event) {
		$("div.modal form").trigger('reset')
		$("div.modal input[type=hidden][name=id]").val('')
		$("div.modal .unmodified").show();
	});


    modal = function(modal){
        $(modal).modal("show")
    }



    if ('matchMedia' in window) {
        // Chrome, Firefox, and IE 10 support mediaMatch listeners
        window.matchMedia('print').addListener(function(media) {
            if (media.matches) {
                beforePrint();
            } else {
                // Fires immediately, so wait for the first mouse movement
                $(document).one('mouseover', afterPrint);
            }
        });
    } else {
        // IE and Firefox fire before/after events
        $(window).on('beforeprint', beforePrint);
        $(window).on('afterprint', afterPrint);
    }

    function beforePrint() {
        $("i#print").click()
    }

    function afterPrint() {
        $("i#print").click()
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
    	}else{
    		return nom;
    	}
    }

    //Format date
    formatDate = function(ladate){
    	if (ladate == null) {
    		ladate = new Date(ladate);
    	}
    	if (moment(ladate).isValid()) {
    		val = moment(ladate);
    		newdate = val.year()+"-"+concate0(val.month()+1)+"-"+concate0(val.date())+" "+concate0(val.hour())+":"+concate0(val.minute())+":"+concate0(val.second());
    		return newdate;
    	}else{
    		return ladate = new Date();
    	}
    }

    $("input[uppercase]").keyup(function(){
    	$(this).val($(this).val().toUpperCase());
    })

    $("input[required]").prev("label").append(" &nbsp;<span style='color:red'>*</span>")



});