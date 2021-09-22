{% load static %}    
<!DOCTYPE html>
<html lang="fr">
<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="#">
    <meta name="keywords" content="Application de gestion des metiers d'une briqueterie industrielle">
    <meta name="author" content="Aristide Manyessé">
    <link rel="icon" href="{%  static 'dist/images/logo.png' %}" type="image/x-icon">
    
    
    <link href="{% static 'dist/css/bootstrap.min.css' %}" rel="stylesheet">
    <link href="{% static 'dist/font-awesome/css/font-awesome.css' %}" rel="stylesheet">
    
    
    <!-- Text spinners style -->
    <link href="{% static 'dist/css/plugins/textSpinners/spinners.css' %}" rel="stylesheet">

    <link href="{% static 'dist/css/plugins/chartist/chartist.min.css' %}" rel="stylesheet">

    <link href="{% static 'dist/css/animate.css' %}" rel="stylesheet">
    <link href="{% static 'dist/css/style.css' %}" rel="stylesheet">

    <link href="{% static 'dist/css/plugins/toastr/toastr.min.css' %}" rel="stylesheet">
    
    <link href="{% static 'dist/css/plugins/iCheck/custom.css' %}" rel="stylesheet">
    <link href="{% static 'dist/css/plugins/chosen/bootstrap-chosen.css' %}" rel="stylesheet">
    <link href="{% static 'dist/js/plugins/select2/dist/css/select2.css' %}" rel="stylesheet">
    <link href="{% static 'dist/js/plugins/alerty/dist/css/alerty.min.css' %}" rel="stylesheet">
    <link href="{% static 'dist/css/plugins/awesome-bootstrap-checkbox/awesome-bootstrap-checkbox.css' %}" rel="stylesheet">
    <link href="{% static 'dist/css/plugins/ionRangeSlider/ion.rangeSlider.css' %}" rel="stylesheet">
    <link href="{% static 'dist/css/plugins/ionRangeSlider/ion.rangeSlider.skinFlat.css' %}" rel="stylesheet">
    <link href="{% static 'dist/css/plugins/datapicker/datepicker3.css' %}" rel="stylesheet">
    
    <!-- FooTable -->
    <link href="{% static 'dist/css/plugins/footable/footable.core.css' %}" rel="stylesheet">

    <!-- FooTable -->
    <link href="{% static 'dist/css/plugins/chosen/bootstrap-chosen.css' %}" rel="stylesheet">

    <!-- feuille de style de Shamman -->
    <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">


    {% block title %}
    <title>BRICX</title>    
    {% endblock title %}
</head>


<body>
    <body class="top-navigation">

      <div id="wrapper">
          <div id="page-wrapper" class="gray-bg">
              <div class="row border-bottom white-bg">
                  <nav class="navbar navbar-expand-lg navbar-static-top" role="navigation">
                      <!--<div class="navbar-header">-->
                          <!--<button aria-controls="navbar" aria-expanded="false" data-target="#navbar" data-toggle="collapse" class="navbar-toggle collapsed" type="button">-->
                              <!--<i class="fa fa-reorder"></i>-->
                              <!--</button>-->

                              <a href="#" class="navbar-brand " style="padding: 3px 15px;"><h1 class="mp0 gras" style="font-size: 45px">BRICX</h1></a>
                              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-label="Toggle navigation">
                                  <i class="fa fa-reorder"></i>
                              </button>

                              <!--</div>-->
                              <div class="navbar-collapse collapse" id="navbar">
                                  <ul class="nav navbar-nav mr-auto">
                                      <li class="gras <?= (isJourFerie(dateAjoute(1)))?"text-red":"text-muted" ?>">
                                          <span class="m-r-sm welcome-message text-uppercase" id="date_actu"></span> 
                                          <span class="m-r-sm welcome-message gras" id="heure_actu"></span> 
                                      </li>

                                  </ul>
                                  <ul class="nav navbar-top-links navbar-right">
                                      <li class=""><a class="dropdown-item text-red" href="#" id="btn-deconnexion" ><i class="fa fa-sign-out"></i> Déconnexion</a></li>
                                  </ul>
                              </div>
                          </nav>
                      </div>

                      <div class="wrapper-content">
                          {% block main%}
                          <h1>Hello world</h1>
                          {% endblock main%}
                      </div>

                      <?php include($this->rootPath("webapp/master/elements/templates/footer.php")); ?>


                  </div>
              </div>


              <?php include($this->rootPath("webapp/master/elements/templates/script.php")); ?>

          </body>

      </body>

      {% include "./script.html" %}


      </html>




      {% block style %}
      <s>

      </style>
      {% endblock style %}


      {% block script %}
      <script>

      </script>
      {% endblock script %}
