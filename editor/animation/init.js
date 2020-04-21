requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $) {
        function findRectanglesAnimation(tgt_node, data) {

            if (!data || !data.ext) {
                return
            }

            // hide right-answer
            $(tgt_node.parentNode).find(".answer").remove()

            const input = data.in
            const [error_msg, answer] = data.ext.result ? [[], data.out] : data.ext.result_addon

            /*----------------------------------------------*
            *
            * attr
            *
            *----------------------------------------------*/
            const attr = {
                grid: {
                    'stroke-width': '1px',
                    'stroke': '#82D1F5',
                },
                answer_grid: {
                    'stroke-width': '1.5px',
                    'stroke': '#F0801A',
                    'fill': '#FABA00',
                    'opacity': 0.7,
                },
                number: {
                    'font-family': 'sans-serif',
                    'font-weight': 'bold',
                    'stroke-width': 0,
                    'fill': '#294270',

                }
            }

            /*----------------------------------------------*
            *
            * values
            *
            *----------------------------------------------*/
            const grid_size_px = 300
            const os = 10
            const width = input[0].length
            const height = input.length
            const unit = grid_size_px / width

            /*----------------------------------------------*
            *
            * paper
            *
            *----------------------------------------------*/
            const paper = Raphael(tgt_node, grid_size_px+os*2, unit*height+os*2, 0, 0)

            /*----------------------------------------------*
            *
            * draw grid
            *
            *----------------------------------------------*/
            // horizontal
            for (let i = 0; i <= height; i += 1) {
                paper.path(['M', 0+os, i*unit+os, 'h', grid_size_px]).attr(attr.grid)
            }

            // vertical
            for (let i = 0; i <= width; i += 1) {
                paper.path(['M', i*unit+os, 0+os, 'v', unit*height]).attr(attr.grid)
            }

            /*----------------------------------------------*

            *
            * draw answer grid
            *
            *----------------------------------------------*/
            answer.forEach(([y1, x1, y2, x2])=>{
                paper.rect(x1*unit+os, y1*unit+os, (x2-x1+1)*unit, (y2-y1+1)*unit).attr(attr.answer_grid)

            })

            /*----------------------------------------------*

            *
            * draw number
            *
            *----------------------------------------------*/
            for (let i = 0; i < height; i += 1) {
                for (let j = 0; j < width; j += 1) {
                    if (input[i][j] > 0) {
                        paper.text(
                            j*unit+unit/2+os, 
                            i*unit+unit/2+os, 
                            input[i][j]).attr(attr.number).attr(
                                {'font-size': 20*Math.max(0.3, unit/50)})
                    }
                }
            }

            /*----------------------------------------------*
             *
             * message
             *
             *----------------------------------------------*/
            if (!data.ext.result) {
                $(tgt_node).addClass('output').prepend(
                    '<div>' + error_msg+ '</div>').css(
                        {'border': '0','display': 'block',})
            }
        }

        var $tryit;
        var io = new extIO({
            multipleArguments: false,
            functions: {
                python: 'rectangles',
                // js: 'rectangles'
            },
            animation: function($expl, data){
                findRectanglesAnimation(
                    $expl[0],
                    data,
                );
            }
        });
        io.start();
    }
);
