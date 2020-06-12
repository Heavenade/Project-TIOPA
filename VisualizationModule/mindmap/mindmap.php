<html lang=en>        
    <head>
        <meta charset=UTF-8>
        <title>mindmap</title>
        <style>
        #demo,
        #demo svg {
            width : 700px;
            height : 500px;
            max-width: 100%;
            max-height: auto;
            margin: 0 auto;
            background-color: #f2f2f2;
        }
        </style> 
        <script>window.console = window.console || function(t) {};</script>
    </head>
    <body>
        <? 
            ini_set("display_errors", 1);
            header("content-type:text/html; charset=UTF-8");
        ?>
        <div id="demo"></div>


        <script>
            var root = "<?=$_POST['root']?>";
            var nodenum = "<?=$_POST['nodenum']?>";
            nodenum = (parseInt(nodenum)+1); //갯수보정
            var word_1 = "<?=$_POST['word_1']?>";
            var word_2 = "<?=$_POST['word_2']?>";
            var word_3 = "<?=$_POST['word_3']?>";
            var word_4 = "<?=$_POST['word_4']?>";
            var word_5 = "<?=$_POST['word_5']?>";
            var word_6 = "<?=$_POST['word_6']?>";
            var word_7 = "<?=$_POST['word_7']?>";
            var word_8 = "<?=$_POST['word_8']?>";
            var word_9 = "<?=$_POST['word_9']?>";
            var word_10 = "<?=$_POST['word_10']?>";
            var word_11= "<?=$_POST['word_11']?>";
            var word_12= "<?=$_POST['word_12']?>";
            var word_13= "<?=$_POST['word_13']?>";
            var word_14= "<?=$_POST['word_14']?>";
            var word_15= "<?=$_POST['word_15']?>";
            var word_16= "<?=$_POST['word_16']?>";
            var word_17= "<?=$_POST['word_17']?>";
            var word_18= "<?=$_POST['word_18']?>";
            var word_19= "<?=$_POST['word_19']?>";
            var word_20= "<?=$_POST['word_20']?>";
 
            var type_1 = "<?=$_POST['type1']?>";
            var type_2 = "<?=$_POST['type2']?>";
            var type_3 = "<?=$_POST['type3']?>";
            var type_4 = "<?=$_POST['type4']?>";
            var type_5 = "<?=$_POST['type5']?>";
            var type_6 = "<?=$_POST['type6']?>";
            var type_7 = "<?=$_POST['type7']?>";
            var type_8 = "<?=$_POST['type8']?>";
            var type_9 = "<?=$_POST['type9']?>";
            var type_10= "<?=$_POST['type10']?>";
            var type_11= "<?=$_POST['type11']?>";
            var type_12= "<?=$_POST['type12']?>";
            var type_13= "<?=$_POST['type13']?>";
            var type_14= "<?=$_POST['type14']?>";
            var type_15= "<?=$_POST['type15']?>";
            var type_16= "<?=$_POST['type16']?>";
            var type_17= "<?=$_POST['type17']?>";
            var type_18= "<?=$_POST['type18']?>";
            var type_19= "<?=$_POST['type19']?>";
            var type_20= "<?=$_POST['type20']?>";
        </script>

        <script src="mindmaploop.js"></script>
        <script src="https://d3js.org/d3.v3.min.js"></script>
        <script src="mindmaprender.js"></script>
    </body>      
</html>
    