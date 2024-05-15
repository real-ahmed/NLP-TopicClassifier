    $(document).ready(function() {
        $('#predictBtn').click(function() {
            var textInput = $('#textInput').val();
            var modelType = $('#modelType').val();

            $.ajax({
                url: '/predict',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    text: textInput,
                    modelType: modelType
                }),
                success: function(data) {
                    $('#predictedTopic').text(data.prediction);
                    $('#predictionModal').modal('show');                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        });

        $('.close').click(function() {
            $('#predictionModal').hide();
        });
    });