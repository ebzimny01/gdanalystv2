$(document).ready(function() {
    $("table#gameresults").Grid({
        sort: true,
        pagination: {
            enabled: true,
            limit: 100, // Default number of rows per page
            summary: true,
        },
        resizable: true,
        fixedHeader: true,
        height: '800px',
        autoWidth: true,
    });
});