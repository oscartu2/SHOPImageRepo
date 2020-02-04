// ----- custom js ----- //

// Hide initial
$("#searching").hide();
$("#results-table").hide();
$("#error").hide();

// Global Variables
var url = 'http://static.pyimagesearch.com.s3-us-west-2.amazonaws.com/vacation-photos/dataset/';
var data = []

$(function() {

	// sanity check
	console.log("Ready!");

	// On Image click
	$(".img").click(function() {

		// Empty/hide results
	    $("#results").empty();
	    $("#results-table").hide();
	    $("#error").hide();

		// Remove active class
		$(".img").removeClass("active")

		// Add active class to clicked picture
		$(this).addClass("active");

		// Grab image url
		var image = $(this).attr("src");
		console.log(image);

	    // Show searching text
	    $("#searching").show();
	    console.log("searching...")

		// Ajax request
		$.ajax({
			type: "POST",
			url: "/search",
			data: {img: image},

			// Handle Success
			success: function(result) {
				console.log(result.results);
				var data = result.results;
				for (i = 0; i < data.length; i++) {
					// $("#results").append('<tr><th><a href="'+url+data[i]["image"]+'">'+data[i]["image"]+'</a></th><th>'+data[i]['score']+'</th></tr>')
					$("#results").append('<tr><th><a href="'+url+data[i]["image"]+'"><img src="'+url+data[i]["image"]+
    '" class="result-img"></a></th><th>'+data[i]['score']+'</th></tr>')
				}
				// Show table
				$("#results-table").show();
			},

			// Handle error
			error: function(error) {
			  console.log(error);
			  // Show error
			  $("#error").append();
			}
		});
	});
});

