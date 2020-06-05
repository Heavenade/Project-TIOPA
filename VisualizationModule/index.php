<!-- 메인페이지 -->
<html>
  <head>
    <title> 시각화모듈 어쩌구 </title>
    <!--Meta -->
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <!-- 부트스트랩 사용 -->
    <link rel="stylesheet" href="css/bootstrap.css">
    <!-- 스타일 변경: 왜 부트스트랩에서 안먹힘  -->
    <style>
      img { max-width: 100%; height: auto; }
      body{
        background-color: #f2f2f2;
      }
      .container, .container-fluid {
        background: #f2f2f2;
      }
      .navbar-custom {
          background-color: #f2f2f2;
      }
      /* change the brand and text color */
      .navbar-custom .navbar-brand,
      .navbar-custom .navbar-text {
          color: rgba(255,255,255,.8);
      }
      /* change the link color */
      .navbar-custom .navbar-nav .nav-link {
          color: rgba(255,255,255,.5);
      }
      /* change the color of active or hovered links */
      .navbar-custom .nav-item.active .nav-link,
      .navbar-custom .nav-item:hover .nav-link {
          color: #ffffff;
      }   
    </style>

  </head>

  <body class= "text-center">
    <!-- Nav 별건 없음 -->
    <nav class="navbar navbar-expand-sm navbar-custom">
    </nav>
    <!-- 컨테이너 -->
    <div class="container-fluid">
    

      <!-- 검색창을 위한 그리드  -->
      <div class="row justify-content-md-center">
        <div class="col-sm-4">
        </div>
        <div class="col-sm-4">
          <p class="text-center">로고 및 검색창</p>
          <br><br><br><br>
          <h1> 로고와 제목<br><br></h1>
          <h1> 검색창<br><br><br></h1>
        </div>
        <div class="col-sm-4">
        </div>
      </div>

      

      <!-- 추천 텍스트  -->
      <p class="text-left">RECOMMENDED PRODUCTS<br></p>
      <!-- 제품 추천을 위한 그리드  -->

      <div class="row">
        <!-- <div class="clearfix visible-sm-block"></div> -->
        <div class="col-sm-2">blank</div>
        <div class="col-sm-8">product lists
          <br><br>
          <div class="row">
            <div class="col-sm-2">contents</div>
            <div class="col-sm-2">contents</div>
            <div class="col-sm-2">contents</div>
            <div class="col-sm-2">contents</div>
            <div class="col-sm-2">contents</div>
            <div class="col-sm-2">contents</div>
          </div>
        </div>
        <div class="col-sm-2">blank</div>
        <!-- <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div>
        <div class="col-lg-2 col-md-3 col-sm-4">contents</div> -->
      </div>

      
    </div>
    <!-- 데이터 베이스 연결 php -->
    <?
    ini_set("display_errors", 1);

    include "lib/db_connect.php";
    $connect = dbconn();
    ?>

    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.js"></script>

  </body>
</html>
