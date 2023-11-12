(function ($) {
    //    "use strict";


    /*  Data Table
    -------------*/

 	// $('#bootstrap-data-table').DataTable();

    $('#bootstrap-data-table-export').DataTable({
        dom: 'lBfrtip',
        lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
        buttons: []
    });

    // $('#bootstrap-data-table-6month').DataTable();
    $('#bootstrap-data-table-6month').DataTable({
        dom: 'lBfrtip',
        lengthMenu: [[5, 10], [5, 10]],
        buttons: []
    })

    $('#bootstrap-data-table-between1y6m').DataTable({
        dom: 'lBfrtip',
        lengthMenu: [[5, 10], [5, 10]],
        buttons: []
    })

    $('#bootstrap-data-table-more1y').DataTable({
        dom: 'lBfrtip',
        lengthMenu: [[5, 10], [5, 10]],
        buttons: []
    })

})(jQuery);