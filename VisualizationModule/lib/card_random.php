<?php
    ini_set("display_errors", 1);
    //header("content-type:text/html; charset=UTF-8");
    include_once ("db_connect.php");
    include_once ("db_connect_sim.php");

    //랜덤 리소스 적용을  위한 랜덤 수 추출
    function rand_card_num()
    {
        $random_result = mt_rand (1, 6);
        return $random_result;
    }
    //전체 텍스트 불러오기
    function get_card_data($product_name)
    {
        $card_data = array();//이중배열로 받아오네욤
         //디비에 연결
         $connect = dbconn();
         $connect_s = dbconn_sim();
         mysqli_query($connect_s,"set names utf8");
         mysqli_query($connect,"set names utf8");
 

        //feature 12개 순서대로 받아오기
        $query_1 = "SELECT `Feature_Name` FROM `feature_dic` JOIN 
        ( SELECT `Category_ID` FROM `product_dic` WHERE `Product_Name` = '$product_name')ProductINFO ON  ProductINFO.`Category_ID` = `feature_dic`.`Category_ID`";

        $data = mysqli_query($connect,$query_1);

        $i=0;
        while($result = mysqli_fetch_array($data))
        {  
            $card_data[$i] = $result['Feature_Name'];
            $i += 1;
        }
        mysqli_close($connect_s);//db 닫고
        mysqli_close($connect);//db 닫고

        //최종적으로 표시될 단어 데이터를 반환
        return $card_data;
    }
?>