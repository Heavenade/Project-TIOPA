<?php
	ini_set("display_errors", 1);

	echo "MySql 연결 테스트<br>";
    $host_name= "db.p-cube.kr"; //호스트네임
    $db_user_id = "db_capstone"; //DB userid
    $db_pw = "CapstoneWls.";
    $db_name = "db_capstone";
  
    $db = mysqli_connect($host_name,$db_user_id,$db_pw,$db_name);
    
    if(!$db)
    {
        die("연결에 실패하였습니다." .mysqli_error());
    }
    else
    {
        echo "MySql 연결에 성공했습니다. <br>";
    }
;
?>