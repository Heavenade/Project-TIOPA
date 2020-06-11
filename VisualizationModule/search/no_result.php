<!-- 검색 결과 없음 -->
<html>
  <head>
    <title> Visualization Module </title>
    <!--Meta -->
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <!-- 부트스트랩 사용 -->
    <link rel="stylesheet" href="../css/bootstrap.css">
    <link rel="stylesheet" href="../css/capstone-custom.css">
  </head>

  <body>
    <!-- php -->
    <?
    ini_set("display_errors", 1);
    //header("content-type:text/html; charset=UTF-8");
    
    include_once "../lib/db_connect.php";//db연결
    include_once "../lib/rcmd_random.php";//recommend random

    //이미 검색된 검색어
    $result_text = "";

    //검색한 데이터 받기
    if($_POST['search_text'])
    {
        $result_text=$_POST['search_text'];  
    }
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
      <hr><br><br>

      <!-- Result-->
      <span class="noresult-text"><i>No Result</i> </span>

    </div>
      
    
    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="../js/bootstrap.js"></script>

  </body>
</html>
