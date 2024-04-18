function switchCamera(camera) {
    // Send an AJAX request to switch camera
    $.ajax({
        type: 'GET',
        url: '/switch_camera',
        data: { camera: camera },
        success: function(response) {
            // Optionally, handle success response
            console.log(response);
        },
        error: function(xhr, status, error) {
            // Handle error
            console.error(xhr.responseText);
        }
    });
}


$(document).ready(function(){
   $('#open-report-tab').click(function(){
       $('#overlay').addClass('active');
       $('#report-tab').addClass('active');
   });

   $('#close-report-tab').click(function(){
       $('#overlay').removeClass('active');
       $('#report-tab').removeClass('active');
   });
});
