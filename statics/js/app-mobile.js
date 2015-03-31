// Configuration Size Windows
var windowResizeHandler = function() {
    window_height = $(window).height();
    columns_view = $('#columns-view').height();
    $('#down').height(window_height - columns_view - 50);
}

// Resize maps where resize window.
window.onload = windowResizeHandler;
$(window).on('resize', windowResizeHandler);