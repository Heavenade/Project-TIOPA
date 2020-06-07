<!-- 검색 결과 없음 -->
<html>
  <head>
    <title> Visualization Module </title>
    <!--Meta -->
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width; initial-scale=1">
    <!-- 부트스트랩 사용 -->
    <link rel="stylesheet" href="../css/bootstrap.css">
    <!-- 스타일 변경: 왜 부트스트랩에서 안먹힘  -->
    <style>   
      .img-searchpanel{
        position: relative;
        margin-top: 0; margin-left: 2%; margin-right: 2%; margin-bottom: 0; 
        max-width: 100%;
        max-height: 120%;
        width: 100%;
        height: auto;
        font-size: 1.0rem;
      }
      .img-searchpanel .form-searchpanel{
        position: absolute;
        top:50%;
        left:40%;
        transform: translate(-40%, -50%);
        text-align: left;
        z-index:1;
        font-size: 0.95em;
        background-color: transparent;
        border: 0px;
        border-color: transparent;
        box-shadow: transparent;
        max-width: 75%;
        max-height: auto;
        transition:none;
      }
      .img-searchpanel .search-btn{
        position: absolute;
        top:50%;
        left:93%;
        transform: translate(-93%, -50%);
        text-align: center;
        padding-top: 0; padding-left: 0; padding-right: 0; padding-bottom: 0;
        z-index:2;
        font-size: 0.9em;
        color: white;
        max-width: 100%;
        max-height: 75%;
        width: 10%;
        height: 40%;
      }
      .form-control:focus {
        color: #495057;
        background-color: transparent;
        border-color: transparent;
        outline: 0;
        box-shadow: none;
      }
      .img-recommend{
        position: relative;
        font-size:1.0rem;
        margin-top: 0%; margin-left: 0%; margin-right: 0%; margin-bottom: 0%; /* 투명 칸 안 이미지 크기 */
        padding-top: 10%; padding-left:0%; padding-right: 0%; padding-bottom: 10%; /* 이미지 안 텍스트 크기 */
        width: 110%; height: auto;
      }
      .img-recommend .rcmd-text{
        position: absolute;
        top:50%;
        left:50%;
        transform: translate(-50%, -50%); 
        text-align: center;
        z-index:1;
        font-weight: 500;
        font-size:0.9em;
        color: white;
        max-width: 90%; max-height: auto;
        width: auto; height: auto;
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
    
    include_once "../lib/db_connect.php";//db연결
    include_once "../lib/rcmd_random.php";//recommend random

    //rcmd 데이터 랜덤 받기
    $rcmd_data = rand_rcmd_data();
    //이미 검색된 검색어
    $result_text = "";

    //검색한 데이터 받기
    if($_POST['search_text'])
    {
        $result_text=$_POST['search_text'];  
    }
    ?>

    <!-- Nav  - 로고와 메인페이지 리다이렉션 -->
    <nav class="navbar navbar-expand-sm navbar-custom">
    </nav>
    <!-- 컨테이너 -->
    <div class="container-fluid">
      <br><br><br><br><br><br>
      <!-- 검색 입력 폼 -->
      <form action = "../search/search_post.php" name = "search" method = "get">
        <!-- 검색창을 위한 그리드 - 왼쪽으로 붙여야 함 아님 navbar로 옮겨야함 -->
        <div class="row">
          <div class="col-lg-3 col-md-1"></div>
          <!-- SearchPanel  -->
          <div class="col-lg-6 col-md-10">
            <span class= "text-center"><h1><a><i>Product Image<br> Analysis Service<br></h1></i></a></span>
            <div class="img-searchpanel center-block">
              <img src="../resources/Search Panel Resize.svg">
              <input type="search" name="search_text" class="form-control form-searchpanel" value= "<?=$result_text?>" placeholder="검색할 제품을 입력하세요.">
              <input type="hidden" name="rcmd_name" value="">
              <input type="submit" class="btn btn-primary search-btn" value="검색">
            </div>
          </div>
          <div class="col-lg-3 col-md-1"></div>
        </div>
        <br><br>
        <hr>
        <br>
      <form>  
    </div>
    
    <!-- js 사용 -->
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="../js/bootstrap.js"></script>

  </body>
</html>
