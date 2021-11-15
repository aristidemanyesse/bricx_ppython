
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

    $('input[name="daterange"]').daterangepicker();
    $('#reportrange').daterangepicker({
        format: 'DD-MM-YYYY',
        minDate: '01-11-2021',
        maxDate: moment(),
        dateLimit: { days: 60 },
        showDropdowns: true,
        showWeekNumbers: true,
        timePicker: false,
        timePickerIncrement: 1,
        timePicker12Hour: true,
        ranges: {
            "Aujourd'hui": [moment(), moment()],
            'Hier': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Les 7 derniers jours': [moment().subtract(6, 'days'), moment()],
            'Les 30 derniers jours': [moment().subtract(29, 'days'), moment()],
            'Ce mois': [moment().startOf('month'), moment().endOf('month')],
            'Le mois passé': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
        },
        opens: 'left',
        drops: 'down',
        buttonClasses: ['btn', 'btn-sm'],
        applyClass: 'btn-primary',
        cancelClass: 'btn-default',
        separator: ' au ',
        locale: {
            applyLabel: 'Submit',
            cancelLabel: 'Cancel',
            fromLabel: 'From',
            toLabel: 'To',
            customRangeLabel: 'Modifier',
            daysOfWeek: ['Di', 'Lu', 'Ma', 'Me', 'Je', 'Ve','Sa'],
            monthNames: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre'],
            firstDay: 1
        }
    }, function(start, end, label) {
        filter_date(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'))
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
        $("table.table-mise tr:not(.no), .item").filter(function () {
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

        if (option.attr("id") != 2) {
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