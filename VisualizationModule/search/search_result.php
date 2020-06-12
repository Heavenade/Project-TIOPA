<!-- 검색 결과 페이지 -->
<html>
  <head>
    <title> Visualization Module </title>
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script src="https://d3js.org/d3.v5.min.js"></script>

    <link rel="stylesheet" href="../css/bootstrap.css?after"> 
    <link rel="stylesheet" href="../css/capstone-custom.css?after">
  </head>

  <body>
    <?php
    ini_set("display_errors", 1);
    header("content-type:text/html; charset=UTF-8");

    include_once "../lib/db_connect.php";//db연결
    include_once "../lib/db_connect_sim.php";//db연결
    include_once "../lib/get_productdata.php";
    include_once "../lib/card_random.php";


    //검색한 문자열 받기
    $result_text = "";
    if($_POST['search_text']){ $result_text=$_POST['search_text'];  }
    
    /*변수*/
   

    $nodenum= 10;

    //제품 공식명칭 받기
    $product_name = $_POST['product_name'];
    //마인드맵 표시할 특징 받기
    //메인일때는 제품이름임
    $feature_name = $_POST['feature_name'];
    
    /*함수*/ 

    //제품의 대표 특징단어와 특징별 대표단어 가져오기
    $feature_data = get_main_feature_data($product_name);

    //대표 특징단어는 [0][1]
    $main_feature = $feature_data[0][1];

    //특징 이름은 [1~][0]
    //특징별 대표단어는 [1~][1]
    $htmlList = '';
    $i = 1;
    while ($i < count($feature_data))
    {
      $targetFeatureName = $feature_data[$i][0];
      $image_string=rand_card_num();
      if (count($feature_data[$i]) > 0)
        $targetWord = $feature_data[$i][1];
      else
        $targetWord = "(없음)";

      //html 코드 생성
      //form submit feature_name 의 value에 마인드맵으로 로드할 특징 이름 입력
      $htmlList = $htmlList."
      <div class='col-md-3 col-sm-4 col-xs-6'>
        <div class ='detailed-filter-card center-block'>
          <img src='../resources/Filter/$image_string.svg'>
          <div class='detailed-filter-text'><span>$targetFeatureName: $targetWord</span></div>
          <button type='submit' name='feature_name' value='$targetFeatureName' class='btn detailed-filter-btn'></button>
        </div>
      </div>
      ";

      $i += 1;
    }
    
    $root_product=$result_text;

    $product_data = get_product_data($product_name, $feature_name);
     
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
            <span class="main-feature-text center-block"><?=$product_name?>의 대표적인 특징은<br>
            <script> document.write("<?=$main_feature?>"); </script><br>입니다!</span>
          </div>
        </div>
        <div class="col-md-2"></div>
      </div>
      <hr>


      <!-- Detailed Filter -->
      <div class="detailed-filter row">
        <div class="col-md-12"><span class="detailed-filter">DETAILED FILTER</span>
          <div class="row">
              <div class="col-sm-2">
              </div>
              <div class="col-sm-8">
                <br><br>
                <form id="search_result_submit" style="display: hidden" action="./search_result.php" method="POST">
                    <!--사용자 검색어 -->
                    <input type="hidden" name="search_text" value="<?=$product_name?>">
                    <!-- 제품 정보 -->
                    <input type="hidden" name="product_name" value="<?=$product_name?>">
                    <!-- card grid  -->
                    <div class="row">
                      <div class="clearfix visible-sm-block"></div>
                      <!-- php로 html 코드 출력 -->
                      <?php
                      echo $htmlList;
                      ?>
                    </div>
                </form>
              </div>
              <div class="col-sm-2"></div>
          </div>
        </div>
      </div>
      <hr>
      
      <!-- Visualization -->
      <div class="visualization row">
          <div class="col-md-12"><span class="visualization-text"><br>VISUALIZATION</span><br><br><br><br><br><br>
            <div class="row">
                <div class="clearfix visible-sm-block"></div>
                <div class="col-sm-4">
                    <div class ="visualization-cate center-block">
                      <img src="../resources/Category Resize.svg">
                    </div>
                </div>
                <div class="col-sm-6">
                    <!-- 마인드 맵 -->
                    <div class ="visualization-mindmap center-block">
                      <!-- 전달될 값 받는 hidden 폼 -->
                      <iframe name='map'  class ="mindmap-iframe" 
                      style = "display:block; border:none; width:70vw; height: 70vh"
                      frameborder="0" cellspacing="0">
                      </iframe>
                      <form name="mindmapform" method="POST" target="map" action="../mindmap/mindmap.php">
                        <input type="hidden" name="nodenum" value ="<?=$nodenum?>"/>
                        <input type="hidden" name="root" value ="<?=$root_product?>"/>
                        <?php
                        $list = '';
                        $i = 0;
                        while ($i < 20)
                        {
                          if ($i < count($product_data[0]))
                          {
                            $targetData = $product_data[0][$i];
                          }
                          else
                          {
                            $targetData = null;
                          }
                          $targetIndex = $i + 1;
                          $list = $list."
                          <input type='hidden' name='word_{$targetIndex}' value = '{$targetData}'/>
                          ";
                          $i += 1;
                        }

                        $i = 0;
                        while ($i < 20)
                        {
                          
                          if ($i < count($product_data[1]))
                          {
                            $targetData = $product_data[1][$i];
                          }
                          else
                          {
                            $targetData = null;
                          }
                          $targetIndex = $i + 1;
                          $list = $list."
                          <input type='hidden' name='type{$targetIndex}' value = '{$targetData}'/>
                          ";
                          $i += 1;
                        }

                        echo $list;
                        ?>

                      </form>
                      <script>
                        document.mindmapform.target = 'map';
                        document.mindmapform.submit();
                      </script>
                      <div class="slidecontainer mindmap-slide center-block">
                        <input type="range" min="1" max="20" value="10" class="slider" id="myRange">
                        <p class = "slidervalue" id="slidervalue">10</p>
                        <script> var slider = document.getElementById("myRange");
                                  var output = document.getElementById("slidervalue");
                                  output.innerHTML = slider.value; // Display the default slider value
                                  $nodenum = slider.value;
                                  slider.oninput = function() {
                                    output.innerHTML = this.value;
                                    $nodenum = this.value;
                                    document.mindmapform.nodenum.value =  $nodenum ;
                                    document.mindmapform.submit();
                                  }
                        </script>
                      </div>
                    </div>
                </div>
                <div class="col-sm-2">
                </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics -->
      <!-- <div class="visualization row">
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
                        
                      </div>
                  </div>
            </div>
          </div>
        </div>
        <hr>
      </div> -->

    <!-- js 사용 -->


    <script>
      document.mindmapform.submit();
    </script>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="../js/bootstrap.js"></script>
    
  </body>
</html>
