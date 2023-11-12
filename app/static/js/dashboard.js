$(document).ready(function() {
    console.info("Getting data ---- All Contract for Dashboard")
    table6Month = $('#bootstrap-data-table-6month').DataTable();
    table6Month.destroy();

    tableBetween = $('#bootstrap-data-table-between1y6m').DataTable();
    tableBetween.destroy();

    tableMore1Y = $('#bootstrap-data-table-more1y').DataTable();
    tableMore1Y.destroy();

    $.ajax({
        url: 'Dashboard', 
        type:'GET',
        contentType: 'application/json',
        beforeSend: function () {
            $('#TotalContracts').html('<i class="fa fa-spinner fa-spin"></i>');
            $('#ActiveContract').html('<i class="fa fa-spinner fa-spin"></i>');
            $('#SignedContract').html('<i class="fa fa-spinner fa-spin"></i>');
            $('#OverdueContract').html('<i class="fa fa-spinner fa-spin"></i>');
        },
        success: function (resData) {
            // console.info(resData);
            $("#TotalContracts").text(resData['totalContract']);
            $("#ActiveContract").text(resData['activeContract']);
            $("#SignedContract").text(resData['signedContract']);
            $("#OverdueContract").text(resData['overdueContract']);

            var dataArray = Object.values(resData['top5PriceList']);
            var chartData = [];

            // console.log(chartData)

            dataArray.forEach(function (item) {
                // console.log("customerName:", item.endCustomers[0].name);
                // console.log("listPrice:", item.listPrice);
    
                chartData.push({
                    customerName: item.endCustomers[0].name,
                    listPrice: item.listPrice,
                });
            });

            Morris.Bar( {
                element: 'Top5Pricelist',
                data: chartData,
                xkey: 'customerName',
                ykeys: ['listPrice'],
                labels: ['List Price ($)'],
                barColors: [ '#343957'],
                hideHover: 'auto',
                gridLineColor: '#eef0f2',
                resize: true
            } );

            $('#bootstrap-data-table-6month').DataTable({
                dom: 'lBfrtip',
                lengthMenu: [[5, 10], [5, 10]],
                buttons: ['copy','excel', 'pdf'],
                data: resData['6MonthfromNow'],
                autoWidth: true,
                order: [[1, 'asc']],
                columns: [
                    {data:'contractNumber'},
                    {data:'dayLeft'},
                    {
                        data: 'contractEndDate',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                var datePart = data.split('T')[0];
                                return datePart;
                            }
                            return data;
                        }
                    }
                ]
            })

            $('#bootstrap-data-table-between1y6m').DataTable({
                dom: 'lBfrtip',
                lengthMenu: [[5, 10], [5, 10]],
                buttons: ['copy','excel', 'pdf'],
                data: resData['6MonthLessThan1YearfromNow'],
                autoWidth: true,
                order: [[1, 'asc']],
                columns: [
                    {data:'contractNumber'},
                    {data:'dayLeft'},
                    {
                        data: 'contractEndDate',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                var datePart = data.split('T')[0];
                                return datePart;
                            }
                            return data;
                        }
                    }
                ]
            })
            
            $('#bootstrap-data-table-more1y').DataTable({
                dom: 'lBfrtip',
                lengthMenu: [[5, 10], [5, 10]],
                buttons: ['copy','excel', 'pdf'],
                data: resData['1yearfromNow'],
                autoWidth: true,
                order: [[1, 'asc']],
                columns: [
                    {data:'contractNumber'},
                    {data:'dayLeft'},
                    {
                        data: 'contractEndDate',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                var datePart = data.split('T')[0];
                                return datePart;
                            }
                            return data;
                        }
                    }
                ]
            })
        },
        error: function (xhr, status, error) {
            // Handle error response
            console.error('Error:', status, error);
    
            // Check if it's a network-related error
            if (status === 'error' && xhr.status === 0) {
                console.error('Network error: The request was aborted or the network connection was lost.');
                // Implement retry logic or show an appropriate message to the user.
            }
        },
        complete: function () {
            // This callback will be called regardless of success or failure
            console.info("Request Complete ---- All Contract");
        }
    })
})








