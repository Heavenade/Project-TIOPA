<!-- 검색 결과 페이지 -->
<html>
  <head>
    <title> Visualization Module </title>
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <link rel="stylesheet" href="../css/bootstrap.css">
    <link rel="stylesheet" href="../css/capstone-custom.css">
  </head>

  <body>
    <?
    ini_set("display_errors", 1);
    header("content-type:text/html; charset=UTF-8");   
    include_once "../lib/db_connect.php";//db연결
    //검색한 문자열 받기
    $result_text = "";
    if($_POST['search_text']){ $result_text=$_POST['search_text'];  }
    
    /*변수*/
    //Main Fearture
    $positive_feature_text="카메라 인덕션";
    $negative_feature_text="배터리 폭발";
    
    //Detailed Filter
    
    /*함수*/
    //get_productdata.php 참고
    ?>
   
    <!-- 컨테이너 -->
    <div class="container-fluid">
      <!-- logo and Subject-->
      <div class="row">
          <div class="col-lg-1 col-md-2 col-sm-2 col-xs-2">
              <!-- logo button-->
              <div class ="nav-logo center-block">
                <img src="../resources/Recommend_Square/1.svg">  
                <button class="btn nav-logo-btn" type="button" onClick="location.href='../index.php'"></button>      
              </div>
          </div>
            <div class="col-lg-6 col-md-8 col-sm-8 col-xs-8">
              <!-- subject -->
              <p class ="nav-subject-text">Product Image Analysis Service</p>
            </div>
          <div class="col-lg-5 col-md-2 col-sm-2 col-xs-2">
          </div>
      </div>
      <!-- SearchPanel-->
      <div class="row">
        <div class="col-lg-6 col-md-8 col-sm-8 col-xs-8">
          <div class="nav-searchpanel center-block">
              <img src="../resources/Search Panel Resize.svg">
              <form action = "../search/search_post.php" name = "search" method = "get"> 
              <input type="search" name="search_text" class="form-control form-searchpanel" value= "<?=$result_text?>" placeholder="검색할 제품을 입력하세요.">
              <input type="hidden" name="rcmd_name" value="">
              <input type="submit" class="btn btn-primary search-btn" value="검색">
              </form>
          </div>
        </div>
      </div>
      <hr>
      <!-- Main Feature -->
      <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8">
          <div class = "main-feature center-block">
            <span class="main-feature-text center-block"><?=$result_text?>의 대표적인 특징은<br>
            <?="     $positive_feature_text     |     $negative_feature_text    "?><br>입니다!</span>
          </div>
        </div>
        <div class="col-md-2"></div>
      </div>
      <hr>


      <!-- Detailed Filter -->
      <div class="detailed-filter row">
        <div class="col-md-12"><span class="detailed-filter-text">DETAILED FILTER</span>
          <div class="row">
              <div class="col-sm-2">
              </div>
              <div class="col-sm-8">
              <br><br>
                  <!-- card grid  -->
                  <div class="row">
                    <div class="clearfix visible-sm-block"></div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/1.svg">
                      </div>
                    </div>
                  </div>       
              </div>
              <div class="col-sm-2"></div>
          </div>
        </div>
      </div>
      <hr>
      
      <!-- Visualization -->
      <div class="visualization row">
          <div class="col-md-12"><span class="visualization-text"><br>VISUALIZATION</span>
          <br><br><br><br><br><br>
            <div class="row">
                  <div class="clearfix visible-sm-block"></div>
                  <div class="col-sm-4">
                      <div class ="visualization-cate center-block">
                      <img src="../resources/Category Resize.svg">
                      </div>
                  </div>
                  <div class="col-sm-8">
                      <div class ="visualization-mindmap center-block">
                        <!-- 마인드 맵 -->
                      </div>
                  </div>
            </div>
          </div>
        </div>
      </div>
      <hr>

      <!-- Statistics -->
      <div class="visualization row">
          <div class="col-md-12"><span class="visualization-text"><br>STATISTICS</span>
          <br><br><br><br><br><br>
            <div class="row">
                  <div class="clearfix visible-sm-block"></div>
                  <div class="col-sm-4">
                      <div class ="visualization-cate center-block">
                      <img src="../resources/Category Resize.svg">
                      </div>
                  </div>
                  <div class="col-sm-8">
                      <div class ="visualization-mindmap center-block">
                        <!-- 마인드 맵 -->
                      </div>
                  </div>
            </div>
          </div>
        </div>
        <hr>






      </div>
    




    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="../js/bootstrap.js"></script>

  </body>
</html>
