$(document).ready(function() {

	///////////////////////////////////////////////////////////////////////////////////////////////
	//								Mini table for Properties									 //
	///////////////////////////////////////////////////////////////////////////////////////////////

	// Setup - add a text input to each footer cell
	// to allow us to filter by column separately
	$('#miniTableProp tfoot th').each( function () {
		var title = $(this).text();
		$(this).html( '<input type="text" class="filterInput"/>' );
	});
 
	// Define DataTable and additional properties
	var propTable = $('#miniTableProp').DataTable({
		"lengthMenu": [ [15, 30, 45, 60, -1], [15, 30, 45, 60, "All"] ],
		"orderMulti": true,
		//"stateSave": true,
		"pagingType": "simple",
		"pageLength": 4,
		"dom": '<rft<p>>',
	});

	propTable.columns().every( function () {
		var that = this;
		$( 'input', this.footer() ).on( 'keyup change', function () {
			if ( that.search() !== this.value ) {
				that.search( this.value ).draw();
			}
		});
	});

	///////////////////////////////////////////////////////////////////////////////////////////////
	//								Mini table for Values										 //
	///////////////////////////////////////////////////////////////////////////////////////////////

	// Setup - add a text input to each footer cell
	// to allow us to filter by column separately
	$('#miniTableVal tfoot th').each( function () {
		var title = $(this).text();
		$(this).html( '<input type="text" class="filterInput"/>' );
	});
 
	// Define DataTable and additional properties
	var valTable = $('#miniTableVal').DataTable({
		"lengthMenu": [ [15, 30, 45, 60, -1], [15, 30, 45, 60, "All"] ],
		"orderMulti": true,
		//"stateSave": true,
		"pagingType": "simple",
		"pageLength": 4,
		"dom": '<rt<p>>',
		"autoWidth": true,
	});
 
	// Apply the search function on search box Input
	// Redraw the table on match
	valTable.columns().every( function () {
		var that = this;
		$( 'input', this.footer() ).on( 'keyup change', function () {
			if ( that.search() !== this.value ) {
				that.search( this.value ).draw();
			}
		});
	});

	///////////////////////////////////////////////////////////////////////////////////////////////
	//								Mini table for Parameters									 //
	///////////////////////////////////////////////////////////////////////////////////////////////

	// Setup - add a text input to each footer cell
	// to allow us to filter by column separately
	$('#miniTableParam tfoot th').each( function () {
	    var title = $(this).text();
		// $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
		$(this).html( '<input type="text" class="filterInput"/>' );
	} );
 
	// Define DataTable and additional properties
	var paramTable = $('#miniTableParam').DataTable({
		"lengthMenu": [ [15, 30, 45, 60, -1], [15, 30, 45, 60, "All"] ],
		"orderMulti": true,
		// "stateSave": true,
		"pagingType": "simple",
		"pageLength": 18,
		"dom": '<rt<p>>',
		"autoWidth": true,
	});

	paramTable.columns().every(function() {
		var that = this;
		$("input", this.footer()).on("keyup change", function() {
			if (that.search() !== this.value) {
				that.search(this.value).draw();
			}
		});
	});
	  
	///////////////////////////////////////////////////////////////////////////////////////////
	//								Mini table for Chambers									 //
	///////////////////////////////////////////////////////////////////////////////////////////

	// Setup - add a text input to each footer cell
	// to allow us to filter by column separately
	$('#miniTableChambers tfoot th').each( function () {
	    var title = $(this).text();
		// $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
		$(this).html( '<input type="text" class="filterInput"/>' );
	} );
 
	// Define DataTable and additional properties
	var chamberTable = $('#miniTableChambers').DataTable({
		//"stateSave": true,
		"pagingType": "simple",
		"pageLength": 6,
		"dom": '<ft<p>>'
	});

	chamberTable.columns().every(function() {
		var that = this;
		$("input", this.footer()).on("keyup change", function() {
			if (that.search() !== this.value) {
				that.search(this.value).draw();
			}
		});
	});
	  
	///////////////////////////////////////////////////////////////////////////////////////////
	//								Mini table for Baselines								 //
	///////////////////////////////////////////////////////////////////////////////////////////

	// Setup - add a text input to each footer cell
	// to allow us to filter by column separately
	$('#miniTableBaselines tfoot th').each( function () {
	    var title = $(this).text();
		// $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
		$(this).html( '<input type="text" class="filterInput"/>' );
	} );
 
	// Define DataTable and additional properties
	var baselinesTable = $('#miniTableBaselines').DataTable({
		//"stateSave": true,
		"pagingType": "simple",
		"pageLength": 6,
		"dom": '<ft<p>>'
	});

	baselinesTable.columns().every(function() {
		var that = this;
		$("input", this.footer()).on("keyup change", function() {
			if (that.search() !== this.value) {
				that.search(this.value).draw();
			}
		});
	});
	  
	///////////////////////////////////////////////////////////////////////////////////
	//								Mini table for Runs								 //
	///////////////////////////////////////////////////////////////////////////////////

	// Setup - add a text input to each footer cell
	// to allow us to filter by column separately
	$('#miniTableRuns tfoot th').each( function () {
	    var title = $(this).text();
		// $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
		$(this).html( '<input type="text" class="filterInput"/>' );
	} );
 
	// Define DataTable and additional properties
	var runsTable = $('#miniTableRuns').DataTable({
		//"stateSave": true,
		"pagingType": "simple",
		"pageLength": 16,
		"dom": '<ft<p>>'
	});

	runsTable.columns().every(function() {
		var that = this;
		$("input", this.footer()).on("keyup change", function() {
			if (that.search() !== this.value) {
				that.search(this.value).draw();
			}
		});
  	});
});