
$(function () {

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


    //bouton principal de deconnexion
    $("a#btn-deconnexion").click(function (event) {
        alerty.confirm("Voulez-vous vraiment vous deconnecter ???", {
            title: "Deconnexion",
            cancelLabel: "Non",
            okLabel: "Oui, me deconnecter !",
        }, function () {
            window.location.href = "/auth/disconnect/";
        })
    });


    //filtre de la barre generale de recherche
    $("#top-search").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("table.table-mise tr:not(.no)").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    //selection des images
    $('body').on("click", "button.btn_image", function(event) {
		$(this).prev("input[type=file]").trigger('click');
	});
	$('body').on("change", ".modal input[type=file]", function(e) {
		var src = URL.createObjectURL(e.target.files[0])
		$(this).prev("img.logo").attr('src', src);
	});

    //selection du mode de payement
    $("div.modepayement_facultatif").hide();
    $("body").on("change", "select[name=modepayement]", function (event) {
        val = $(this).val();
        option = $(this).find("option[value=" + val + "]")
        if (option.attr("id") > 2) {
            $("div.modepayement_facultatif").show()
        } else {
            $("div.modepayement_facultatif").hide()
        }

        if (option.attr("id") != 1) {
            $("div.no_modepayement_facultatif").show()
        } else {
            $("div.no_modepayement_facultatif").hide()
        }
    });


    //selection du livraison
    $("div.tricycle").hide();
    $("body").on("change", "select[name=modelivraison]", function (event) {
        val = $(this).val();
        option = $(this).find("option[value=" + val + "]")
        if (option.attr("id") == 1) {
            $("div.chauffeur").show()
            $("div.tricycle").hide()

        } else if (option.attr("id") == 2) {
            $("div.tricycle").show()
            $("div.chauffeur").hide()

        } else {
            $("div.tricycle").hide()
            $("div.chauffeur").hide()
        }
    });


    //superposition de modals
    $(document).on('show.bs.modal', '.modal', function () {
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function () {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    });
    $(document).on('hidden.bs.modal', '.modal', function () {
        $('.modal:visible').length && $(document.body).addClass('modal-open');
    });



    //Watchdog de deconnexion
    $(document).idleTimer(10 * 60 * 1000);
    $(document).on("idle.idleTimer", function (event, elem, obj) {
        window.location.href = "/auth/locked/";
    });




    // selecteur des onglets item de page
    var section = "<?= $this->getSection() ?>"
    var modul = "<?= $this->getModule() ?>"
    var url = "<?= $this->getPage() ?>"

    if (url == "clients" || url == "client") {
        url = "clients";
    }

    $("nav ul.metismenu li").removeClass('active');
    $("nav ul.metismenu li").each(function (index, el) {
        if ($(this).attr("id") == url) {
            $(this).addClass("active")
            $(this).parent("ul").addClass("in");
            $(this).parent("ul").parent("li.groupe").addClass("active");
        }
    });

    $("a.onglets").each(function () {
        if ($(this).attr("id") == "onglet-" + section) {
            $("a.onglets").removeClass("active btn-warning")
            $("a.onglets").addClass("btn-white");
            $(this).addClass("active btn-warning").removeClass("btn-white");
        }
    })





    if ('matchMedia' in window) {
        // Chrome, Firefox, and IE 10 support mediaMatch listeners
        window.matchMedia('print').addListener(function (media) {
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

});