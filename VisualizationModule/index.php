<!-- 메인페이지 -->
<html>
  <head>
    <title> Visualization Module </title>
    <!--Meta -->
    <meta http-equiv="content-type" content = "text/html; charset=UTF-8"/>
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <!-- 부트스트랩 사용 -->
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/capstone-custom.css">
  </head>

  <body>
    <?
    ini_set("display_errors", 1);
    //include_once "lib/db_connect.php";//db연결
    include_once "lib/rcmd_random.php";//recommend random
    $rcmd_data = rand_rcmd_data();//랜덤 추천 제품 데이터 받기
    ?>
    
    <!-- 컨테이너 -->
    <div class="container-fluid container-custom">
      <!-- 검색 입력 폼 -->
      <form action = "search/search_post.php" name = "search" method = "get">
        <!-- 검색창을 위한 그리드  -->
        <div class="row">
          <div class="col-lg-3 col-md-1">  
          </div>
          <div class="col-lg-6 col-md-10">
            <!-- 로고 -->
            <button class="tmp-logo" type="button" id="redirection" name="logo" onClick="location.href='./index.php'">
              <img src="resources/tmp logo.png"></button>
            <!-- 제목 --> 
              <span class= "text-center"><h1><a><i>Product Image<br> Analysis Service</h1></i></a></span>
              <br>
            <!-- SearchPanel  -->
            <div class="img-searchpanel center-block" name="SearchPanel">
              <img src="resources/Search Panel Resize.svg">
              <input type="search" name="search_text" class="form-control form-searchpanel" value="" placeholder="검색할 제품을 입력하세요.">
              <input type="hidden" name="rcmd_name" value="">
              <input type="submit" class="btn btn-primary search-btn" value="검색">
            </div></div>
          <div class="col-lg-3 col-md-1"></div>
        </div>
        <br><br><hr><br>
        
        <!-- 제품 추천을 위한 그리드  -->
        <div class="row">    
          <div class="col-sm-2"></div>
          <div class="col-sm-8">
            <!-- 추천 텍스트  -->
            <span style="font-size:1.3rem">
            RECOMMENDED PRODUCT
            </span><br><br>
              <!-- 하위 6칸 그리드  -->
              <div class="row">
                <div class="clearfix visible-sm-block"></div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(0,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(0,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(1,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(1,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(2,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(2,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(3,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(3,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(4,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(4,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(5,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(5,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(6,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(6,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(7,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(7,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(8,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(8,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(9,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(9,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(10,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(10,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
                <div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
                  <div class ="img-recommend center-block">
                    <img src="resources/Recommend_Rect/<?=$image_string=rand_rcmd_num();?>.svg">
                    <div class="rcmd-text"><span><?=get_rcmd_name(11,$rcmd_data);?></span></div>
                    <button type="submit" name="rcmd_name" value="<?=get_rcmd_name(11,$rcmd_data);?>" class="btn rcmd-btn"></button>
                  </div>
                </div>
              </div>       
          </div>
          <div class="col-sm-2"></div>
        </div>
      <form>  
    </div>
    
    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="js/bootstrap.js"></script>
  </body>
</html>

<!-- <script type="text/javascript">

    /* 페이지 이동 */   
        this.document.getElementById("redirection").submit();

</script> -->
