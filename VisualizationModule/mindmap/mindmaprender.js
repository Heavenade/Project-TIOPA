+function (d3) {
        
    var swatches = function (el) {
        var w = screen.width,
        h = screen.height;
    
        var circleWidth = 10;
    
        var palette = {
        "lightgray": "#819090",
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
        "yellowgreen": "#738A05" };
    
    
        var nodes = 
        [
            {
            name: "갤럭시노트" },
            {
            name: "단어 1",
            target: [0] },
            {
            name: "단어 2",
            target: [0] },
            {
            name: "단어 3",
            target: [0] },
            {
            name: "단어 4",
            target: [0] },
            {
            name: "단어 5",
            target: [0] },
            {
            name: "단어 6",
            target: [0] },
            {
            name: "단어 7",
            target: [0] },
            {
            name: "단어 8",
            target: [0] 
            }
        ];   
    
        var links = [];
        for (var i = 0; i < nodes.length; i++) 
        {
            if (window.CP.shouldStopExecution(0)) break;
            if (nodes[i].target !== undefined) 
            {
                for (var x = 0; x < nodes[i].target.length; x++) 
                {
                    if (window.CP.shouldStopExecution(1)) break;
                links.push( { source: nodes[i],target: nodes[nodes[i].target[x]] });
                }window.CP.exitedLoop(1);
            }
        }window.CP.exitedLoop(0);
    
        var myChart = d3.select(el).
        append('svg').
        attr('width', w).
        attr('height', h);
    
        var force = d3.layout.force().
        nodes(nodes).
        links([]).
        gravity(0.1).
        charge(-1000).
        size([w, h]);
    
        var link = myChart.selectAll('line').
        data(links).enter().append('line').
        attr('stroke', palette.white);
    
        var node = myChart.selectAll('circle').
        data(nodes).enter().
        append('g').
        call(force.drag);
    
        node.append('circle').
        attr('cx', function (d) {
        return d.x;
        }).
        attr('cy', function (d) {
        return d.y;
        }).
        attr('r', circleWidth).
        attr('stroke', function (d, i)
        {
            if (i > 0)
            {
                return palette.paleyellow;
            } 
            else 
            {
                return "transparent";
            }
        }).
        attr('stroke-width', 2).
        attr('fill', function (d, i) {
        if (i > 0) {
            return palette.white;
        } else {
            return "transparent";
        }
        });
    
        node.append('text').
        text(function (d) {
        return d.name;
        }).
        attr('font-family', 'Roboto Slab').
        attr('fill', function (d, i) {
        if (i > 0) {
            return palette.mediumgray;
        } else {
            return palette.white;
        }
        }).
        attr('x', function (d, i) {
        if (i > 0) {
            return circleWidth + 20;
        } else {
            return circleWidth - 15;
        }
        }).
        attr('y', function (d, i) {
        if (i > 0) {
            return circleWidth;
        } else {
            return 8;
        }
        }).
        attr('text-anchor', function (d, i) {
        if (i > 0) {
            return 'beginning';
        } else {
            return 'end';
        }
        }).
        attr('font-size', function (d, i) {
        if (i > 0) {
            return '2em';
        } else {
            return '3.4em';
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