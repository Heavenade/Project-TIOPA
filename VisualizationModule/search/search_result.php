<!-- 검색 결과 페이지 -->
<html>
  <head>
    <title> Visualization Module - result </title>
    <!--Meta -->
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <!-- 부트스트랩 사용 -->
    <link rel="stylesheet" href="css/bootstrap.css">
    <!-- 스타일 변경: 왜 부트스트랩에서 안먹힘  -->
    <style>   
      .img-searchpanel{
        position: relative;
        margin-top: 0; margin-left: 2%; margin-right: 2%; margin-bottom: 0; max-width: 100%; height: auto;
      }
      .img-searchpanel .form-searchpanel{
        position: absolute;
        top:50%;
        left:40%;
        transform: translate(-40%, -50%);
        text-align: left;
        z-index:1;
        font-size:1.1rem;
        background-color: transparent;
        border: 0px;
        border-color: transparent;
        box-shadow: transparent;
        max-width: 75%;
        max-height: 100%;
        transition:none;
      }
      .form-control:focus {
        color: #495057;
        background-color: transparent;
        border-color: transparent;
        outline: 0;
        box-shadow: none;
      }
      .img-searchpanel .search-btn{
        position: absolute;
        top:50%;
        left:95%;
        transform: translate(-95%, -50%);
        text-align: center;
        z-index:2;
        font-size:1.1rem;
        color: white;
        max-width: 100%;
        max-height: 100%;
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
      .img-recommend .rcmd-btn{
        position: absolute;
        top:50%;
        left:50%;
        transform: translate(-50%, -50%);
        z-index:2;
        width: 100%;
        height: 100%;
        margin-top: 0%; margin-left: 0%; margin-right: 0%; margin-bottom: 0%;
        padding-top: 0%; padding-left: 0%; padding-right: 0%; padding-bottom: 0%;
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
    
    include_once "lib/db_connect.php";//db연결
    include_once ("lib/rcmd_random.php");//recommend random

    $rcmd_data = rand_rcmd_data();

    ?>

    <!-- Navbar - 로고와 제목 - 메인 페이지로 연결 -->
    <nav class="navbar navbar-expand-sm navbar-custom">
    </nav>
    <!-- 컨테이너 -->
    <div class="container-fluid">
      <!-- 검색창을 위한 그리드 - 검색창은 왼쪽 상단 -->
      <div class="row">
          <div class="col-lg-3 col-md-1"></div>
          <!-- SearchPanel  -->
          <div class="col-lg-6 col-md-10">
            <span class= "text-center"><h1><a><i>Product Image<br> Analysis Service<br></h1></i></a></span>
            <div class="img-searchpanel center-block">
              <img src="resources/Search Panel Resize.svg">
              <input type="search" name="search_text" class="form-control form-searchpanel" value="" placeholder="검색할 제품을 입력하세요.">
              <input type="submit" class="btn btn-primary search-btn" value="검색">
            </div>
          </div>
          <div class="col-lg-3 col-md-1"></div>
        </div>
        <br><br>
        <hr>

      <!--No Result 창 - No result 일 경우 출력 -->
      <div></div> 
      <!-- 제품 추천을 위한 그리드 - No result 일 경우 출력  -->
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
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(0,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(1,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(1,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(2,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(2,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(3,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(3,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(4,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(4,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(5,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(5,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(6,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(6,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(7,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(7,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(8,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(8,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(9,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(9,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(10,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-md-2 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="<?=$image_string=rand_rcmd_num();?>">
                    <div class="rcmd-text"><span><?=get_rcmd_name(11,$rcmd_data);?></span></div>
                    <button type="submit" name="search_text" value="<?=get_rcmd_name(11,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
              </div>
          
          </div>
          <div class="col-sm-2"></div>
        </div>

      <!-- Result가 있을 경우 출력되는 결과 페이지 -->
      <div></div> 

    </div>
    
    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.js"></script>

  </body>
</html>
