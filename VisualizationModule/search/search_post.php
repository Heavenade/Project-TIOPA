<!-- 텍스트 데이터 받아와서 검색하는 페이지 -->
<!-- 파이썬 검색 모듈과 연동 -->

<?
 ini_set("display_errors", 1);
 header("content-type:text/html; charset=UTF-8");
 
 include "../lib/db_connect.php";//db연결

 $connect = dbconn();

 //검색할 문자열 받아옴
 if(!$_GET['search_text']==NULL && !$_GET['search_text']=="" )
 {
    $search_text=$_GET['search_text'];
    echo "검색 입력한 문자열은 ".$search_text;
 }

//  if(!$_GET['rcmd_search_text']==NULL && !$_GET['rcmd_search_text']=="" )
//  {
//     $rcmd_search_text=$_GET['rcmd_search_text'];
//     echo "버튼 클릭한 문자열은 ".$rcmd_search_text;
//  }
 
 
 //검색 모듈에 넘기자 - 형태소 분석 된 단어 리스트 형태

 //이후 제품 정보 dic 반환 받는다.

?>