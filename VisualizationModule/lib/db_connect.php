<?
  function dbconn()
  {
    $host_name= "db.p-cube.kr"; //호스트네임
    $db_user_id = "db_capstone"; //DB userid
    $db_pw = "CapstoneWls.";
    $db_name = "db_capstone";

    $connect = mysqli_connect($host_name,$db_user_id,$db_pw,$db_name);
    mysqli_query($connect,"set names utf8");
    mysqli_select_db($connect, "db_capstone");

    if(!$connect)die("연결에 실패하였습니다." .mysqli_error());

    //echo "MySql 연결에 성공했습니다. <br>";
    return $connect;
  }

  //에러메세지 출력
  function Error($msg)
  {
    echo "
    <script>
    window.alert('$msg');
    history.back(1);
    </script>
    ";
    exit;//위에 에러메세지만 띄운다.
  }
?>