requirejs(['ext_editor_io', 'jquery_190'],
    function (extIO, $) {
        var $tryit;
        var io = new extIO({
            multipleArguments: false,
            functions: {
                python: 'rectangles',
                // js: 'rectangles'
            }
        });
        io.start();
    }
);
