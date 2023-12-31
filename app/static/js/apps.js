$(document).ready(function() {
    var textarea = $('#customerAddress');
    // textarea.height(textarea[0].scrollHeight - textarea.outerHeight() + textarea.height());
    defaultSelectedOption()

    textarea.on('input', function() {
      this.style.height = 'auto';
      this.style.height = (this.scrollHeight) + 'px';
    });

    $('#selectItems').change(function () {
        var selectedValue = $('option:selected', this).attr('id');
        console.log(selectedValue); // You can use the selectedValue as needed
        if (selectedValue === "contractNumber") {
            $(".items-ContractNumber").show();
            $(".items-SerialNumber").hide();
        } else if (selectedValue === "serialNumber") {
            $(".items-SerialNumber").show();
            $(".items-ContractNumber").hide();
        }
        
    });

    $('#selectItems').trigger('change');
});

function defaultSelectedOption(){
    $(".items-ContractNumber").hide();
}

$('#contractSummary').on('click', function(event) {
    event.preventDefault();
    console.info("Getting data ---- Contract Summary")

    const getValue = $("#billToID").val()
    let billID = getValue.split(" ")

    table = $('#bootstrap-data-table-export').DataTable();
    table.destroy();

    focusDataTable()

    $.ajax({
        url: 'SearchContractSummary', 
        data:JSON.stringify(Number(billID[0])),
        type:'POST',
        contentType: 'application/json',
        beforeSend: function () {
            $('#bootstrap-data-table-export tbody').html('<div id="spinner" class="text-center"><i class="fa fa-spinner fa-spin"></i> Loading...</div>');
        },
        success: function (resData) {
            $('#bootstrap-data-table-export').DataTable({
                dom: 'lBfrtip',
                lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
                buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
                data: resData,
                autoWidth: true,
                columns: [
                    { data:'count'},
                    { data: 'id' },
                    { data: 'name' },
                    { data: 'contractNumber' },
                    {
                        data: 'contractEndDate',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                var datePart = data.split('T')[0];
                                return datePart;
                            }
                            return data;
                        }
                    },
                    {
                        data: null,
                        render: function(data, type, row) {
                            const formattedNumber = data.listPrice.toLocaleString('en-US', {
                                style: 'currency',
                                currency: data.currency
                            });
                            return formattedNumber;
                        }
                    },
                    { data: 'contractStatus'}
                ],
                rowId: 'id',
                initComplete: function () {
                    // This function will be called once the DataTable is fully initialized.
                    console.log('DataTable initialization is complete.');
                    $('#bootstrap-data-table-export tbody spinner').html('');
                }
            });

            let clickHandled = false;
            // Add a click event handler
            $('#bootstrap-data-table-export tbody').on('click', 'tr', function () {
                if (!clickHandled) {
                    const table = $('#bootstrap-data-table-export').DataTable();
                    const data = table.row(this).data(); // Get the row's data
                    const rowId = data.id; // Assuming 'id' is the unique identifier property
            
                    // Do something with the row ID (e.g., display it)
                    console.info('Double-clicked row ID: ' + rowId);
            
                    // Set the flag to prevent further clicks
                    clickHandled = true;
            
                    // Reset the flag after a certain time (e.g., 1 second)
                    setTimeout(function () {
                        clickHandled = false;
                    }, 1500);
                }
            });
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
            console.info("Request Complete ---- Contract Summary");
        }   
    });
});

$('#itemSearch').on('click', function(event){
    let items
    event.preventDefault();
    console.info("Getting data ---- Item Search")

    getSelected = $('option:selected', "#selectItems").attr('id');

    if(getSelected=="serialNumber"){
        const getValue = $("#id-SerialNumber").val()
        items = getValue.split(",")
    }else if(getSelected=="contractNumber"){
        const getValue = $("#id-ContractNumber").val()
        items = getValue.split(",")
    }

    let reqData = {
        "selected":getSelected,
        "items": items
    }
    console.info(reqData)
    table = $('#bootstrap-data-table-export').DataTable();
    table.destroy();

    focusDataTable();
    // console.log(items)

    $.ajax({
        url: 'SearchByItem',
        data:JSON.stringify(reqData),
        type:'POST',
        contentType: 'application/json',
        beforeSend: function () {
            $('#bootstrap-data-table-export tbody').html('<div id="spinner" class="text-center"><i class="fa fa-spinner fa-spin"></i> Loading...</div>');
        },
        success: function (resData) {
            $('#bootstrap-data-table-export').DataTable({
                dom: 'lBfrtip',
                lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
                buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
                data: resData,
                autoWidth: true,
                columns: [
                    {data:'count'},
                    {data:'contractNumbers'},
                    {data:'customerName'},
                    {data:'product'},
                    {data:'productGroup'},
                    {data:'serialNumber'},
                    {data:'serviceSKU'},
                ],
                rowId: 'count',
                initComplete: function () {
                    // This function will be called once the DataTable is fully initialized.
                    console.log('DataTable initialization is complete.');
                    $('#bootstrap-data-table-export tbody spinner').html('');
                }
            });

            let clickHandled = false;
            // Add a click event handler
            $('#bootstrap-data-table-export tbody').on('click', 'tr', function () {
                if (!clickHandled) {
                    const table = $('#bootstrap-data-table-export').DataTable();
                    const data = table.row(this).data(); // Get the row's data
                    const rowId = data.count - 1
                    // Do something with the row ID (e.g., display it)
                    console.info('Click on row: ' + rowId);                   
                    focusDetailsTab();
                    defaultDetailsTab();
                    setDetailsTab(resData,rowId)

                    // Set the flag to prevent further clicks
                    clickHandled = true;
            
                    // Reset the flag after a certain time (e.g., 1 second)
                    setTimeout(function () {
                        clickHandled = false;
                    }, 1500);
                }
            });
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
            console.info("Request Complete --- Item Search");
        }
    })

});

$('#sendEmail').on('click', function(event){
    event.preventDefault();
    console.log("-- Processing Send an Email --")

    const emailRecipient = $("#emailRecipient").val()
    const emailCC = $("#emailCC").val()
    const emailSubject = $("#emailSubject").val()
    const mailMessage = $("#mailMessage").val()

    dataEmail = {
        "emailRecipient": emailRecipient,
        "emailCC":emailCC,
        "emailSubject":emailSubject,
        "mailMessage":mailMessage
    }

    $.ajax({
        url: 'sendMail',
        data:JSON.stringify(dataEmail),
        type:'POST',
        contentType: 'application/json',
        success: function (resData) {
            $(function () {
                $('#composeEmail').modal('toggle');
            });
            console.log(resData)
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
            console.info("Request Complete ---- Sent Email");
        }
    });
});

function focusDataTable(){
    console.info("initiate focus on table tab")
    $("#tabItemSearch a[href='#details']").attr("hidden","true");
    $("#tabItemSearch a[href='#details']").removeClass("active");
    $("#tabItemSearch a[href='#table']").addClass("active");
    $("#tabItemSearch a[href='#table']").trigger('click');
}

function focusDetailsTab(){
    console.info("initiate focus on details tab")
    $("#tabItemSearch a[href='#details']").removeAttr("hidden");
    $("#tabItemSearch a[href='#table']").removeClass("active");
    $("#tabItemSearch a[href='#details']").addClass("active");
    $("#tabItemSearch a[href='#details']").trigger('click');
}

function setDetailsTab(data,row){
    // console.log(data[row]['contractNumbers'])
    $('#customerID').val(data[row]['customerID']);
    $('#customerName').val(data[row]['customerName']);
    $('#customerAddress').val(data[row]['customerAddress']);
    $('#detailsContractNumber').val(data[row]['contractNumbers']);
    $('#serviceSKU').val(data[row]['serviceSKU']);
    $('#billTo').val(data[row]['billTo']);
    $('#salesOrder').val(data[row]['salesOrder']);
    $('#purchaseOrder').val(data[row]['purchaseOrder']);
    $('#MsalesOrder').val(data[row]['MsalesOrder']);
    $('#MpurchaseOrder').val(data[row]['MpurchaseOrder']);

    startDateContractFormated =data[row]['startDateContract'].split("T");
    $('#startDateContract').val(startDateContractFormated[0]);

    endtDateContractFormated =data[row]['endDateContract'].split("T");
    $('#endDateContract').val(endtDateContractFormated[0]);

    dateFormat = data[row]['ldod'].split("T");
    $('#ldod').val(dateFormat[0]);

    $('#contractStatus').val(data[row]['contractStatus']);
    $('#productName').val(data[row]['product']);

    editedDescription = data[row]['description'];
    $('#productDescription').val(editedDescription.replace(/\^\^/g, ''));

    $('#group').val(data[row]['productGroup']);
    $('#detailsSerialNumber').val(data[row]['serialNumber']);
    
    $('#warrantyType').val(data[row]['warrantyType']);
    $('#warrantyStatus').val(data[row]['warrantyStatus']);

    dateWarrantyFormated = data[row]['warrantyEndDate'].split("T");
    $('#warrantyEndDate').val(dateWarrantyFormated[0]);
}

function defaultDetailsTab(){
    $('#customerID').val("");
    $('#customerName').val("");
    $('#customerAddress').val("");
    $('#detailsContractNumber').val("");
    $('#serviceSKU').val("");
    $('#billTo').val("");
    $('#salesOrder').val("");
    $('#purchaseOrder').val("");
    $('#MsalesOrder').val("");
    $('#MpurchaseOrder').val("");
    $('#startDateContract').val("");
    $('#endDateContract').val("");
    $('#ldod').val("");
    $('#contractStatus').val("");
    $('#productName').val("");
    $('#productDescription').val("");
    $('#group').val("");
    $('#detailsSerialNumber').val("");
    $('#warrantyType').val("");
    $('#warrantyEndDate').val("");
}