<!-- 메인페이지 -->
<html>
  <head>
    <title> Visualization Module </title>
    <!--Meta -->
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <!-- 부트스트랩 사용 -->
    <link rel="stylesheet" href="css/bootstrap.css">
    <!-- 스타일 변경: 왜 부트스트랩에서 안먹힘  -->
    <style>
      
      .img-searchpanel{
        margin-top: 0; margin-left: 2%; margin-right: 2%; margin-bottom: 0; max-width: 100%; height: auto;
      }
      .img-recommend{
        position: relative;
        
        margin-top: 10%; margin-left: 2%; margin-right: 2%; margin-bottom: 10%; max-width: 100%; height: auto;
      }
      .img-recommend .rcmd-text{
        position: absolute;
        top:50%;
        left:50%;
        transform: translate(-50%, -50%);
        text-align: center;
        z-index:1;
        font-size:1.3rem;
        color: white;
        max-width: 100%;
        max-height: 100%;
      }
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

  <body>
    <!-- php -->
    <?
    ini_set("display_errors", 1);
    header("content-type:text/html; charset=UTF-8");
    
    include "lib/db_connect.php";//db연결
    include ("lib/rcmd_random.php");//recommend random

    //db연결
    //$connect = dbconn();
    //rcmd 데이터 랜덤 받기
    $rcmd_data = rand_rcmd_data();

    ?>

    <!-- Nav 별건 없음 -->
    <nav class="navbar navbar-expand-sm navbar-custom">
    </nav>
    <!-- 컨테이너 -->
    <div class="container-fluid">
      <br><br><br><br><br><br>
      <!-- 검색창을 위한 그리드  -->
      <div class="row">
        <div class="col-lg-3 col-md-1">
        </div>
        <div class="col-lg-6 col-md-10">
          <span class= "text-center"><h1><a><i>Product Image<br> Analysis Service<br></h1></i></a></span>
          <img src="resources/Search Panel Resize.svg" class="img-searchpanel center-block">
        </div>
        <div class="col-lg-3 col-md-1">
        </div>
      </div>
      <br><br>
      <hr>
      <!-- 제품 추천을 위한 그리드  -->
      <div class="row">    
        <div class="col-sm-2"></div>
        <div class="col-sm-8">
          <!-- 추천 텍스트  -->
          <span style="font-size:24px">
          RECOMMENDED PRODUCTS
          </span>
          <br><br>
          <div class="row">
            <div class="clearfix visible-sm-block"></div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(0,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(1,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(2,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(3,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(4,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(5,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(6,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(7,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(8,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(9,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(10,$rcmd_data);?></span></div>
              </div>
            </div>
            <div class="col-md-2 col-sm-4 col-xs-6">
              <div class ="img-recommend center-block">
                <img src="<?=$image_string=rand_rcmd_num();?>">
                <div class="rcmd-text"><span><?=get_rcmd_name(11,$rcmd_data);?></span></div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-2"></div>
      </div>
      <br>  
    </div>
    
    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.js"></script>

  </body>
</html>
