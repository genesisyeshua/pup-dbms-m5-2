function onFormSubmit(event){
	var data = $(event.target).serializeArray();
	var thesis={};

	for (var i=0;i<data.length;i++){
		thesis[data[i].name] = data[i].value;
	}

	var list_element=$('<li id="item"' +'class="' + thesis.year + thesis.title1 + '">');
	var item = list_element.html(thesis.year + ' ' + thesis.title1);

	var thesis_create_api = '/api/thesis';
	$.post(thesis_create_api, thesis, function(response){
		if(response.status = 'OK') {
			var full_thesis = response.data.year + ' ' + response.data.title1 + ' by: ' + response.data.thesis_author;
			$('.thesis-list').append('<li>' + full_thesis)
		}
		else {
			// prompt("Error.")
		}
	});
	return false;
}

function FetchAllThesis() {
  var thesis_list_api = '/api/thesis';
  $.get(thesis_list_api, {}, function(response) {
    response.data.forEach(function(thesis_list) {
      var thesis_item = thesis_list.year + ' ' + thesis_list.title1;
      thesis_list.author.forEach(function(e) {
        var thesis_auth = e.first_name + ' ' + e.last_name;
        $('.thesis-list').append('<li>' + thesis_item + ' by: ' + thesis_auth + '</li>');
      });
    });
  });
}

function onRegFormSubmit(event)
{
  var data = $(event.target).serializeArray();

  var user = {};
  for (var i = 0; i < data.length; i++) {
    user[data[i].name] = data[i].value;
  }

  var user_api = '/register';
  $.post(user_api, user, function(response) {
    console.log('data', response)
    if (response.status = 'OK') {
       alert('Registration successful!');
       window.location.replace("/home");
     } else {
       prompt("Error.");
     }
  });
  return false;
}

$('.RegForm').submit(onRegFormSubmit);
$('.create-form').submit(onFormSubmit);
FetchAllThesis();

// function loadAllThesis(){
// 	var thesis_list_api = '/api/thesis';
// 	$.get(thesis_list_api, {}, function(response){
// 		console.log('thesis list', response)
// 		response.data.forEach(function(thesis) {
// 			var full_thesis = thesis.year + ' ' + thesis.title1;	
// 			$('.thesis-list').append('<li>' + full_thesis + '</li>' )
// 		});
// 	});
// }

// $('.create-form').submit(onFormSubmit);
// loadAllThesis();
