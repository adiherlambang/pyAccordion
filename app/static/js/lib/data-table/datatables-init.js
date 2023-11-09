(function ($) {
    //    "use strict";


    /*  Data Table
    -------------*/

 	$('#bootstrap-data-table').DataTable();


    // $('#bootstrap-data-table').DataTable({
    //     lengthMenu: [[10, 20, 50, -1], [10, 20, 50, "All"]],
    // });

	// $('#bootstrap-data-table-export').DataTable({
    //     paging: true,
    //     pageLength: 10 // Show 10 records per page
    // });

    $('#bootstrap-data-table-export').DataTable({
        dom: 'lBfrtip',
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        buttons: []
    });
})(jQuery);