$(document).ready(function() {
    // Function to handle window resize
    $('#resize-card').css('width', '33.333%');
    $(window).resize(function() {
        // Get the viewport width
        var viewportWidth = $(window).width();
        console.log("Viewport width:", viewportWidth);
        if (viewportWidth >= 800 && viewportWidth <= 1200) {
            console.log("Viewport width is between 800 and 1000 pixels");
            $("#resize-card").addClass("w-75");
            $("#resize-card").removeClass("w-100");
        } else if(viewportWidth < 800) {
            console.log("Viewport width is not between 800 and 1000 pixels");
            $("#resize-card").removeClass("w-75");
            $("#resize-card").addClass("w-100");
        }else if(viewportWidth > 1200){
            $("#resize-card").removeClass("w-100");
            $("#resize-card").removeClass("w-75");

            $('#resize-card').css('width', '33.333%');
        }
    });
    
    // Trigger the resize event on page load to get the initial viewport width
    $(window).resize();
});