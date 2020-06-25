<?php
    //header("content-type:text/html; charset=UTF-8");
    include_once ("db_connect.php");

    //랜덤 리소스 적용을  위한 랜덤 수 추출
    function rand_rcmd_num()
    {
        $random_result = mt_rand (1, 8);
        return $random_result;
    }
    //전체 중 추천 제품 데이터 불러오기
    function rand_rcmd_data()
    {
        $rcmd_data = array(array());//이중배열로 받아오네욤
        $connect = dbconn();
        mysqli_query($connect,"set names utf8");

        //랜덤 제품명과 제품 카테고리 받아오기
        $query = "SELECT `Product_Name`,`Category_ID` FROM `product_dic` ORDER BY Count DESC LIMIT 12";
        $data = mysqli_query($connect,$query);
        $i=0;
        while($result = mysqli_fetch_array($data))
        {  
            //0 - 이름
            $rcmd_data[0][$i] = $result['Product_Name'];
            //1 - 카테고리 넘버 
            $rcmd_data[1][$i] = $result['Category_ID'];
            $i = $i+1;
        }
        mysqli_close($connect);
        return $rcmd_data;
    }
    //랜덤 제품명 받아오기
    function get_rcmd_name($num,$data)
    {
        $i = 0;
        while($i<$num)
        {  
            $i = $i+1;
        }
        return $data[0][$i]; 
    }
    //카테고리 이미지는 나중에 적용합시다 (이미지를 번호로 구분해서)
    function get_rcmd_cate($num)
    {
        //랜덤 제품의 카테고리 받아오기
        $i = 0;
        while($i<$num)
        {  
            $i = $i+1;
        }
        return $data[1][$i]; 
    }

    //특정 카테고리의 추천 제품 데이터 불러오기
    function rand_cate_rcmd_data($category_name)
    {
        $rcmd_cate_data = array(array());
        $connect = dbconn();
        mysqli_query($connect,"set names utf8");

        //카테고리 dic에서 카테고리 ID 받아오기
        $query = "SELECT `Category_ID` FROM `category_dic` WHERE `Category` = '$category_name'";
        $result = mysqli_query($connect,$query);
        $row = $result->fetch_row();
        $category_ID = (string)$row[0];
    
        //카테고리 내의 랜덤 제품명 받아오기
        $query = "SELECT `Product_Name` FROM `product_dic` WHERE `Category_ID` = '$category_ID' ORDER BY `Count` DESC LIMIT 12";

        $data = mysqli_query($connect,$query);
        
        $i=0;

        while($result = mysqli_fetch_array($data))
        {  
            //0 - 이름
            $rcmd_cate_data[0][$i] = $result['Product_Name'];
            //1 - 카테고리 넘버 
            $rcmd_cate_data[1][$i] = $category_ID;
            $i = $i+1;
        }
        mysqli_close($connect);

        return $rcmd_cate_data;
    }
?>