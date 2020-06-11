<!-- 검색 결과 페이지 -->
<html>
  <head>
    <title> Visualization Module </title>
    <meta http-equiv="content-type" content = "text/html; charset = UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <script src="https://d3js.org/d3.v5.min.js"></script>

    <link rel="stylesheet" href="../css/bootstrap.css"> 
    <link rel="stylesheet" href="../css/capstone-custom.css">
  </head>

  <body>
    <?
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

    $product_name = $_POST['product_name'];
    
    /*함수*/ 
    $product_data = get_product_data($product_name);//이중 배열 [0][$i] = 단어 [1][$i] = 속성
    $root_product=$result_text;

     //Main Fearture

     if($product_data[0][0] == "")
     {
      $main_feature_text = "No Result";

     }
     else
     {
      $main_feature_text = $product_data[0][0];

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
      <hr>
      <!-- Main Feature -->
      <div class="row">
        <div class="col-md-2"></div>
        <div class="col-md-8">
          <div class = "main-feature center-block">
            <span class="main-feature-text center-block"><?=$result_text?>의 대표적인 특징은<br>
            <script> document.write("<?=$main_feature_text?>"); </script><br>입니다!</span>
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
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class ="detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
                      </div>
                    </div>
                    <div class="col-md-3 col-sm-4 col-xs-6">
                      <div class = "detailed-filter-card center-block">
                      <img src="../resources/Filter/<?=$image_string=rand_card_num();?>.svg">
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
                        <input type="hidden" name="word_1" value = "<?=$product_data[0][0]?>"/>
                        <input type="hidden" name="word_2" value = "<?=$product_data[0][1]?>"/>
                        <input type="hidden" name="word_3" value = "<?=$product_data[0][2]?>"/>
                        <input type="hidden" name="word_4" value = "<?=$product_data[0][3]?>"/>
                        <input type="hidden" name="word_5" value = "<?=$product_data[0][4]?>"/>
                        <input type="hidden" name="word_6" value = "<?=$product_data[0][5]?>"/>
                        <input type="hidden" name="word_7" value = "<?=$product_data[0][6]?>"/>
                        <input type="hidden" name="word_8" value = "<?=$product_data[0][7]?>"/>
                        <input type="hidden" name="word_9" value = "<?=$product_data[0][8]?>"/>
                        <input type="hidden" name="word_10" value = "<?=$product_data[0][9]?>"/>
                        <input type="hidden" name="word_11" value = "<?=$product_data[0][10]?>"/>
                        <input type="hidden" name="word_12" value = "<?=$product_data[0][11]?>"/>
                        <input type="hidden" name="word_13" value = "<?=$product_data[0][12]?>"/>
                        <input type="hidden" name="word_14" value = "<?=$product_data[0][13]?>"/>
                        <input type="hidden" name="word_15" value = "<?=$product_data[0][14]?>"/>
                        <input type="hidden" name="word_16" value = "<?=$product_data[0][15]?>"/>
                        <input type="hidden" name="word_17" value = "<?=$product_data[0][16]?>"/>
                        <input type="hidden" name="word_18" value = "<?=$product_data[0][17]?>"/>
                        <input type="hidden" name="word_19" value = "<?=$product_data[0][18]?>"/>
                        <input type="hidden" name="word_20" value = "<?=$product_data[0][19]?>"/>

                        <input type="hidden" name="type1" value = "<?=$product_data[1][0]?>"/>
                        <input type="hidden" name="type2" value = "<?=$product_data[1][1]?>"/>
                        <input type="hidden" name="type3" value = "<?=$product_data[1][2]?>"/>
                        <input type="hidden" name="type4" value = "<?=$product_data[1][3]?>"/>
                        <input type="hidden" name="type5" value = "<?=$product_data[1][4]?>"/>
                        <input type="hidden" name="type6" value = "<?=$product_data[1][5]?>"/>
                        <input type="hidden" name="type7" value = "<?=$product_data[1][6]?>"/>
                        <input type="hidden" name="type8" value = "<?=$product_data[1][7]?>"/>
                        <input type="hidden" name="type9" value = "<?=$product_data[1][8]?>"/>
                        <input type="hidden" name="type10" value = "<?=$product_data[1][9]?>"/>
                        <input type="hidden" name="type11" value = "<?=$product_data[1][10]?>"/>
                        <input type="hidden" name="type12" value = "<?=$product_data[1][11]?>"/>
                        <input type="hidden" name="type13" value = "<?=$product_data[1][12]?>"/>
                        <input type="hidden" name="type14" value = "<?=$product_data[1][13]?>"/>
                        <input type="hidden" name="type15" value = "<?=$product_data[1][14]?>"/>
                        <input type="hidden" name="type16" value = "<?=$product_data[1][15]?>"/>
                        <input type="hidden" name="type17" value = "<?=$product_data[1][16]?>"/>
                        <input type="hidden" name="type18" value = "<?=$product_data[1][17]?>"/>
                        <input type="hidden" name="type19" value = "<?=$product_data[1][18]?>"/>
                        <input type="hidden" name="type20" value = "<?=$product_data[1][19]?>"/>
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


    <script>
      document.mindmapform.submit();
    </script>

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script type="text/javascript" src="../js/bootstrap.js"></script>
    <!-- iframe에 값 전달 script -->
    
  </body>
</html>
