<?php
    function dbconn_sim()
    {
        $host_name= "localhost"; //호스트네임
        $db_user_id = "db_capstone"; //DB userid
        $db_pw = "CapstoneWls.";
        $db_name = "db_capstone_similarity";

        $connect = mysqli_connect($host_name,$db_user_id,$db_pw,$db_name);
        mysqli_query($connect,"set names utf8");
        mysqli_select_db($connect, "db_capstone_similarity");

        if(!$connect)die("연결에 실패하였습니다." .mysqli_error());

        //echo "MySql 연결에 성공했습니다. <br>";
        return $connect;
    }

?>