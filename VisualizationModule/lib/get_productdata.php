<!-- 제품 이미지 가져오는 페이지 -->
<?php
    ini_set("display_errors", 1);
    //header("content-type:text/html; charset=UTF-8");
    include_once "db_connect_sim.php";
    include_once "db_connect.php";

    //db연결
    $connect = dbconn();
    $connect_s = dbconn_sim();


    //제품 대표 특징과 특징별 대표 단어 가져오기
    function get_main_feature_data($product_name)
    {
        $result_data = array(array());

        $connect = dbconn();
        $connect_s = dbconn_sim();

        mysqli_query($connect_s,"set names utf8");
        mysqli_query($connect,"set names utf8");
              
        //대표 특징 단어 가져오기
        $query = "
        SELECT  `Word`
        FROM    `$product_name`
        WHERE   `$product_name`
        ORDER BY `$product_name` DESC
        ";
        $result = mysqli_query($connect_s, $query);

        $i = 0;
        while ($WordData = mysqli_fetch_array($result))
        {
            $targetData = $WordData['Word'];

            // 제품 이름이면 패스
            $query = "SELECT * FROM `product_dic` WHERE `Product_Name` = '$targetData'";
            $data = mysqli_query($connect,$query);
            if(mysqli_num_rows($data)>0)
            {   
                continue;
            }

            // 회사 이름이면 패스
            $query = "SELECT * FROM `carrier_dic` WHERE `Carrier_Alias` = '$targetData'";
            $data = mysqli_query($connect,$query);
            if(mysqli_num_rows($data)>0)
            {   
                continue;
            }

            $result_data[0][0] = $product_name;
            $result_data[0][1] = $targetData;

            $i += 1;

            break;
        }

        //특징별 대표 단어 가져오기
        $query = "
        SELECT  `Feature_Name`
        FROM    `feature_dic`
        JOIN    (
                SELECT  product_dic.category_id
                FROM    `product_dic`
                WHERE   product_dic.Product_Name = '$product_name'
                )PRODUCT ON PRODUCT.category_id = feature_dic.Category_ID
        ";
        $result = mysqli_query($connect, $query);

        $i = 0;
        while ($FeatureData = mysqli_fetch_array($result))
        {
            $targetFeature = (string)$FeatureData['Feature_Name'];
            $query = "
            SELECT  `Word`
            FROM    `$product_name`
            WHERE   `$targetFeature`
            ORDER BY `$targetFeature` DESC
            LIMIT 1";
            $data = mysqli_query($connect_s, $query);
            $WordData = mysqli_fetch_array($data);
            $result_data[$i + 1][0] = $targetFeature;
            $result_data[$i + 1][1] = (string)$WordData['Word'];

            $i += 1;
        }

        return $result_data;
    }


    //product name을 받아서 데이터(단어 string, 단어카테고리 int) 20개 원 문서로 반환
    //마인드맵 전용 함수임
    function get_product_data($product_name, $feature_name)
    {
        $product_data = array(array());//반환할 데이터 :: 이중배열

        //디비에 연결
        $connect = dbconn();
        $connect_s = dbconn_sim();

        mysqli_query($connect_s,"set names utf8");
        mysqli_query($connect,"set names utf8");

        /* 쿼리 날려서 값 받기 */
        $query = "SELECT `Word`, `Sentiment_Value` FROM `$product_name` WHERE `$feature_name` > 0.7 ORDER BY  `$feature_name` DESC LIMIT 20";
        $WordData = mysqli_query($connect_s,$query);// 에러시 false 반환

        if($WordData == False)
        {
            return $product_data;
        }

        $i=0;
        if ($feature_name == $product_name)
        {
            $query = "SELECT `Category` FROM `category_dic` JOIN ( SELECT `category_id` FROM `product_dic` WHERE `Product_Name` = '$product_name')PRODUCT ON PRODUCT.category_id = category_dic.Category_ID";
            $data = mysqli_query($connect, $query);
            $result = mysqli_fetch_array($data);
    
            $product_data[0][$i] = (string)$result['Category'];
            $product_data[1][$i] = "2";

            $i += 1;
        }
       
        while($WordResult = mysqli_fetch_array($WordData))
        {  
            $ipass = 0;
            //0 - Word
            $tmpword = (string)($WordResult['Word']);
            $product_data[0][$i] = "$tmpword";

            $product_data[1][$i] = "4";

            //2. 브랜드 속성 : carrier_dic 활용
            $tmp = $product_data[0][$i];
            $query_2 = "SELECT * FROM `product_dic` WHERE `Product_Name` = '$tmp'";
            $data_2 = mysqli_query($connect,$query_2);
            if(mysqli_num_rows($data_2)>0)
            {
                $product_data[1][$i] = "3";
            }
            //제품명으로 있는가?
            $tmp = $product_data[0][$i];
            $query_3 = "SELECT * FROM `product_dic` WHERE `Product_Name` = '$tmp'";
            $data_3 = mysqli_query($connect,$query_3);
            //회사명으로 있는가?
            $tmp = $product_data[0][$i];
            $query_4 = "SELECT * FROM `carrier_dic` WHERE `Carrier_Alias` = '$tmp'";
            $data_4 = mysqli_query($connect,$query_4);
            if(mysqli_num_rows($data_3)>0 || mysqli_num_rows($data_4)>0)
            {   
                $product_data[1][$i] = "3";    
            }
            if($WordResult['Sentiment_Value'] != null)
            {
                //감정값이 null 아닐때
                if($WordResult['Sentiment_Value'] > 0)
                {
                    $product_data[1][$i] = "5";    
                }
                if($WordResult['Sentiment_Value'] < 0)
                {
                    $product_data[1][$i] = "6";
                }
            }
            
            $i = $i+1;
        }
        
        mysqli_close($connect_s);//db 닫고
        mysqli_close($connect);//db 닫고

        //최종적으로 표시될 단어 데이터를 반환
        return $product_data;
    }
?>