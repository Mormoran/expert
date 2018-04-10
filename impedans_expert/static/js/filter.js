$(document).ready(function() {
    // Setup - add a text input to each footer cell
    // to allow us to filter by column separately
    $('#dataTable tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" class="filterInput"/>' );
    } );
 
    // Define DataTable and additional properties
    var table = $('#dataTable').DataTable({
        "lengthMenu": [ [15, 30, 45, 60, -1], [15, 30, 45, 60, "All"] ],
        "orderMulti": true,
        "stateSave": true,
        "pagingType": "full_numbers",
        "autoWidth": false,
        "pageLength": 15,
        "dom": '<<i><l><p>rt>'
    });
 
    // Apply the search function on search box Input
    // Redraw the table on match
    table.columns().every( function () {
        var that = this;
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that.search( this.value ).draw();
            }
        } );
    } );

	
});