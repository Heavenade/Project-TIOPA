<!-- 텍스트 데이터 받아와서 검색하는 페이지 -->
<?
    ini_set("display_errors", 1);
    header("content-type:text/html; charset=UTF-8");
    include_once "../lib/db_connect.php";

    $connect = dbconn();//db연결

    $discription_text = NULL; //검색창을 통한 문자열
    $product_name = NULL; //버튼 누른 경우의 문자열 == 제품명
    $product_id = NULL;
    $category_name = NULL;

    $hold_text = NULL;//discription_text를 정제한 텍스트

    if($_GET['rcmd_name'] == "" && $_GET['search_text'] != "")
    {
        $discription_text = strtoupper(trim(preg_replace("/\s| /",'',$_GET['search_text'])));//가공

        $hold_text = $_GET['search_text'];
    }
    else
    {
        $product_name = $_GET['rcmd_name'];
        $hold_text = $_GET['rcmd_name'];
    }   

   if($discription_text)//검색된 경우
   {
        mysqli_query($connect,"set names utf8");

        //제품아이디와 제품명 받아오기
        $query = "SELECT `product_id` FROM `product_discription` WHERE `discription` = '$discription_text'";
        $result = mysqli_query($connect,$query);

        //카테고리명 받아오기
        $query = "SELECT `Category` FROM `category_dic` WHERE `Category` = '$discription_text'";
        $category_result = mysqli_query($connect,$query);

        if(mysqli_num_rows($result)>0)//제품이 존재할 경우
        {
            $row = $result->fetch_row();
            $product_id = (string)$row[0];
            $query = "SELECT `product_name` FROM `product_dic` WHERE `product_id` = $product_id";
            $result = mysqli_query($connect,$query);
            $row = $result->fetch_row();
            $product_name = (string)$row[0];
        }
        else if(mysqli_num_rows($category_result)> 0)//대분류 카테고리로 존재할 경우
        {
            $row = $category_result->fetch_row();
            $category_name = (string)$row[0]; 
        }
        else//결과가 존재하지 않을 경우
        {
            $product_id = NULL;
            $product_name = NULL;
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
        else//"ERROR! Not in DIc!" DB 오류;
        {
            $product_id = NULL;
            $product_name = NULL;
        }
   }
?>

<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    </head>
    <body>
        <!--search_result로 페이지 이동 시 POST -->
        <form id="search_result_submit" style="display: hidden" action="./search_result.php" method="POST">
            <!--사용자 검색어 -->
            <input type="hidden" name="search_text" value="<?=$hold_text?>">
            <!-- 제품 정보 -->
            <input type="hidden" name="product_name" value="<?=$product_name?>">
            <input type="hidden" name="product_id" value="<?=$hproduct_idt?>">
        </form>
        <!-- Category_result로 페이지 이동 시 POST -->
        <form id="category_result_submit" style="display: hidden" action="./category_result.php" method="POST">
            <!--사용자 검색어 -->
            <input type="hidden" id="search_text" name="search_text" value="<?=$hold_text?>">
            <!-- 카테고리 정보 -->
            <input type="hidden" name="category_name" value="<?=$category_name?>">
        </form>

        <!-- No_result로 페이지 이동 시 POST -->
        <form id="no_result_submit" style="display: hidden" action="./no_result.php" method="POST">
            <!--사용자 검색어 -->
            <input type="hidden" id="search_text" name="search_text" value="<?=$hold_text?>">
        </form>
    </body>
</html>

<script type="text/javascript">

    var product_id = "<?=$product_id ?>";
    var product_name = "<?=$product_name ?>"
    var category_name = "<?=$category_name ?>"

    /* 페이지 이동 */
    if(product_id && product_name)
    {   
        this.document.getElementById("search_result_submit").submit();
    }
    else if(category_name)
    {
        this.document.getElementById("category_result_submit").submit();
    }
    else
    {
        this.document.getElementById("no_result_submit").submit();
    }   
</script>



