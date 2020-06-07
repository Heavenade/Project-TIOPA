<!-- 텍스트 데이터 받아와서 검색하는 페이지 -->
<!-- 파이썬 검색 모듈과 연동 -->

<?
    ini_set("display_errors", 1);
    header("content-type:text/html; charset=UTF-8");
    
    include_once "../lib/db_connect.php";

    $connect = dbconn();//db연결
    $discription_text = ""; //검색창을 통한 문자열
    $product_name = ""; //버튼 누른 경우의 문자열 == 제품명

    if($_GET['rcmd_name'] == "")
    {
        $discription_text = trim(preg_replace("/\s| /",'',$_GET['search_text']));
    }
    else
    {
        $product_name = $_GET['rcmd_name'];
    }   

   if($discription_text)//검색된 경우
   {
        //제품아이디와 제품명 받아오기
        mysqli_query($connect,"set names utf8");
        $query = "SELECT `product_id` FROM `product_discription` WHERE `discription` = '$discription_text'";
        $result = mysqli_query($connect,$query);

        if(mysqli_num_rows($result)>0)
        {
            $row = $result->fetch_row();
            $product_id = (string)$row[0];
            $query = "SELECT `product_name` FROM `product_dic` WHERE `product_id` = $product_id";
            $result = mysqli_query($connect,$query);
            $row = $result->fetch_row();
            $product_name = (string)$row[0];
        }
        else
        {
            $product_id = "No REsULT";
            $product_name = "No REsULT";
        }     
   }
   else//추천 버튼이 눌린 경우
   {
       //제품명으로 제품아이디 받아오기
        mysqli_query($connect,"set names utf8");
        $query = "SELECT `product_id` FROM `product_dic` WHERE `product_name` = '$product_name'";
        $result = mysqli_query($connect,$query);
        if(mysqli_num_rows($result)>0)
        {
            $row = $result->fetch_row();
            $product_id = (string)$row[0];
        }
        else
        {
            $product_id = "ERROR! Not in DIc!";
            $product_name = "ERRROR! Not in DIc!";
        }  
   }
   echo "추출한 제품 아이디는 " .$product_id ." 이고, 정제된 제품 이름은 ".$product_name." 입니다. ";
?>

<!--search_result로 페이지 이동 -->
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <title>search_post</title>
    </head>
    <body>
        <form id="auto_submit" style="display: hidden" action="./search_result.php" method="POST">
            <!--사용자 검색어 - dbg: 정제된 텍스트 -->
            <input type="hidden" id="search_text" name="search_text" value="<?=$product_name?>">
            <!-- 결과가 있는 지 없는 지 여부 -->
            <!-- 제품 정보 dic -->
        </form>
    </body>
</html>

<script type="text/javascript">
//HTMLPost로 정보 전달이 안된다면 자바스크립트로 작성
    //this.document.getElementById("auto_submit").submit();
</script>



