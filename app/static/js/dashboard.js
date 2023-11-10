(function ($) {
    "use strict";
    /*-----------------------------*/
    var options = {
        labelInterpolationFnc: function (value) {
            return value[0]
        }
    };

    var responsiveOptions = [
  ['screen and (min-width: 640px)', {
            chartPadding: 30,
            labelOffset: 100,
            labelDirection: 'explode',
            labelInterpolationFnc: function (value) {
                return value;
            }
  }],
  ['screen and (min-width: 1024px)', {
            labelOffset: 80,
            chartPadding: 20
  }]
];
})(jQuery);

$(document).ready(function() {
    console.info("Getting data ---- All Contract")

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
            console.info(resData);
            $("#TotalContracts").text(resData['totalContract']);
            $("#ActiveContract").text(resData['activeContract']);
            $("#SignedContract").text(resData['signedContract']);
            $("#OverdueContract").text(resData['overdueContract']);
            console.info("Success ---- All Contract");
        }
    })
})








