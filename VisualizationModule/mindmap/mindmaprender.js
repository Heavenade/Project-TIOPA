+function (d3) {

    var swatches = function (el) {

        console.log("루트를 포함한 노드 개수 : "+(parseInt(nodenum)));

        var w = 700;
        var h = 500;
    
        //사용할 색상 코드
        var palette = {
        "lightgray": "#c2c2c2",
        "gray": "#708284",
        "mediumgray": "#536870",
        "darkgray": "#475B62",
        "darkblue": "#0A2933",
        "darkerblue": "#042029",
        "paleryellow": "#FCF4DC",
        "paleyellow": "#EAE3CB",
        "yellow": "#A57706",
        "orange": "#BD3613",
        "red": "#D11C24",
        "pink": "#C61C6F",
        "purple": "#595AB7",
        "blue": "#2176C7",
        "green": "#259286",
        "white": "#fefefe",
        "yellowgreen": "#738A05",
        /*for capstone*/
        "capbg":"#F2F2F2",
        "proudct":"#6454f0",//0
        "mainfeature":"#6454f0",//1
        "higherfeature":"#37c6cd",//2
        "brandfeature":"#c165dd",//3
        "positivefeature":"#95c674",//4
        "negativefeature":"#f2a16a",//5
        "productetcfeature":"#fc76b3",//6
        "etcfeature":"#facd68"//7
        };
    
        var nodes = 
        [
            { name: root},
            {
                //노드 이름이자 텍스트
                name: word_1,
                //노드의 속성 -어떤 색상 사용할지
                attr: type_1,
                //선을 연결할 타겟
                target: [0] 
            },
            {
                name: word_2,
                attr: type_2,
                target: [0] 
            },
            {
                name: word_3,
                attr: type_3,
                target: [0] 
            },
            {
                name: word_4,
                attr: type_4,
                target: [0] 
            },
            {
                name: word_5,
                attr: type_5,
                target: [0] 
            },
            {
                name: word_6,
                attr: type_6,
                target: [0] 
            },
            {
                name: word_7,
                attr: type_7,
                target: [0] 
            },
            {
                name: word_8,
                attr: type_8,
                target: [0] 
            },
            {
                name: word_9,
                attr: type_9,
                target: [0] 
            },
            {
                name: word_10,
                attr: type_10,
                target: [0] 
            },
            {
                name: word_11,
                attr: type_11,
                target: [0] 
            },
            {
                name: word_12,
                attr: type_12,
                target: [0] 
            },
            {
                name: word_13,
                attr: type_13,
                target: [0] 
            },
            {
                name: word_14,
                attr: type_14,
                target: [0] 
            },
            {
                name: word_15,
                attr: type_15,
                target: [0] 
            },
            {
                name: word_16,
                attr: type_16,
                target: [0] 
            },
            {
                name: word_17,
                attr: type_17,
                target: [0] 
            },
            {
                name: word_18,
                attr: type_18,
                target: [0] 
            },
            {
                name: word_19,
                attr: type_19,
                target: [0] 
            },
            {
                name: word_20,
                attr: type_20,
                target: [0] 
            }
        ];   
        
        var nodes2 = nodes.splice(0, nodenum);
        //노드와 링크 세팅
        var links = [];
        for (var i = 0; i < nodes2.length; i++) 
        {
            if (window.CP.shouldStopExecution(0)) break;
            if (nodes2[i].target !== undefined) 
            {
                for (var x = 0; x < nodes2[i].target.length; x++) 
                {
                    if (window.CP.shouldStopExecution(1)) break;
                links.push( { source: nodes2[i],target: nodes2[nodes2[i].target[x]] });
                }window.CP.exitedLoop(1);
            }
        }window.CP.exitedLoop(0);
    
        var myChart = d3.select(el).
        append('svg').
        attr('width', w).
        attr('height', h);
    
        //물리 적용
        var force = d3.layout.force().
        nodes(nodes2).
        links([]).
        gravity(0.1).
        charge(-400).//이게 분포 범위
        size([w, h]);//최대 분포 범위
        
        //연결선의 세팅
        var link = myChart.selectAll('line').
        data(links).enter().append('line').
        attr('stroke', palette.lightgray);
    
        //노드의 세팅
        var node = myChart.selectAll('rect').
        data(nodes2).enter().
        append('g').
        call(force.drag);
    
        node.append('rect'). //사각형 노드
        attr('rx', 10). //완만도
        attr('ry', 10).
        attr("width", function (d,i)//글씨 넓이 만큼
        {
            if (i > 0) //leaf
            {
                return 100;
            } 
            else //root
            {
                return 200;     
            }
        }). //크기
        attr("height",function (d,i)//글씨 폭 만큼
        {
            if (i > 0) //leaf
            {
                return 25;
            } 
            else //root
            {
                return 45;     
            }
        }).
        attr("x", function (d,i)//글씨 폭 만큼//노드 위치 //글씨 폭 받아와서 조정하도록
        {
            if (i > 0) //leaf
            {
                return -50;
            } 
            else //root
            {
                return -160;     
            }
        }).
        attr("y", function (d,i)//글씨 폭 만큼//노드 위치 //글씨 폭 받아와서 조정하도록
        {
            if (i > 0) //leaf
            {
                return -15;
            } 
            else //root
            {
                return -25;     
            }
        }).

        attr('stroke', function (d, i)//테두리
        {
            if (i > 0) //leaf
            {
                if(nodes2[i].attr == 1)
                {
                    return palette.mainfeature;
                }
                else if(nodes2[i].attr == 2)
                {
                    return palette.higherfeature;
                }
                else if(nodes2[i].attr == 3)
                {
                    return palette.brandfeature;
                }
                else if(nodes2[i].attr == 4)
                {
                    return palette.productetcfeature;
                }
                else if(nodes2[i].attr == 5)
                {
                    return palette.positivefeature;
                }
                else if(nodes2[i].attr == 6)
                {
                    return palette.negativefeature;
                }
                else(nodes2[i].attr == 7)
                {
                    return palette.etcfeature;
                }  
            } 
            else //root
            {
                return palette.product;
            }
        }).
        attr('stroke-width', 5).

        attr('fill', function (d, i) //색상 채우기 //색상 받아오도록 //i값으로 각 노드 접근해 attr별로
        {
            if (i > 0) //leaf
            {
                if(nodes2[i].attr == 1)
                {
                    return palette.mainfeature;
                }
                else if(nodes2[i].attr == 2)
                {
                    return palette.higherfeature;
                }
                else if(nodes2[i].attr == 3)
                {
                    return palette.brandfeature;
                }
                else if(nodes2[i].attr == 4)
                {
                    return palette.productetcfeature;
                }
                else if(nodes2[i].attr == 5)
                {
                    return palette.positivefeature;
                }
                else if(nodes2[i].attr == 6)
                {
                    return palette.negativefeature;
                }
                else if(nodes2[i].attr == 7)
                {
                    return palette.etcfeature;
                }  
            } 
            else //root
            {
                return palette.product;
            }
        }
        );
        node.append('text').
        text(function (d) 
        {
            return d.name;
        }).
        attr('font-family', 'Roboto Slab'). //폰트
        attr('fill', function (d, i) //폰트 색상
        {
        if (i > 0) { //leaf
            return palette.white;
        } else { //root
            return palette.white;
        }
        }).
        attr('x', function (d, i) { //라인 말단과 단어의 거리 x
        if (i > 0) //leaf
        {    
            return -30;
        } 
        else //root
        {    
            return 20;
        }
        }).
        attr('y', function (d, i) { //라인 말단과 단어의 거리 y
        if (i > 0) //Leaf
        {
            return 5;
        } 
        else //root
        {
            return 5;
        }
        }).
        attr('text-anchor', function (d, i) { //앵커
        if (i > 0) //Leaf
        { 
            return 'beginning';
        } 
        else //root
        { 
            return 'end';
        }
        }).
        attr('font-size', function (d, i) { //폰트 크기
        if (i > 0) 
        { //Leaf 
            //return this.getComputedTextLength();
            return '0.8rem';
        } else 
        {//root 
            return '1rem';
        }
        });
    
        force.on('tick', function (e) {
        node.attr('transform', function (d, i) {
            return 'translate(' + d.x + ', ' + d.y + ')';
        });
    
        link.
        attr('x1', function (d) {
            return d.source.x;
        }).
        attr('y1', function (d) {
            return d.source.y;
        }).
        attr('x2', function (d) {
            return d.target.x;
        }).
        attr('y2', function (d) {
            return d.target.y;
        });
        });       
        force.start();        
    }('#demo');        
    }(window.d3);