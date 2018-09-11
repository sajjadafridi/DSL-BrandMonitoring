$('input#facebooklink').mentiony({
    	  // triggerChar: '@',

  onDataRequest: function (mode, keyword, onDataRequestCompleteCallback) {

    $.ajax({

      method: "GET",

      url: "https://autocomplete.clearbit.com/v1/companies/suggest?query=:"+keyword,

      dataType: "json",

      success: function (response) {
      	data=""
      	// var lest = response;
      	// console.log(response);
      	var data=[];
      	var i=1;
        $.each(response, function (index, element)
        {

        data.push({ id:i, name:element.name, 'avatar':element.logo,});
        i=i+1;
})
        // NOTE: Assuming this filter process was done on server-side

        data = jQuery.grep(data, function( item ) {

            return item.name.toLowerCase().indexOf(keyword.toLowerCase()) > -1;

        });



          // Call this to populate mention.

        onDataRequestCompleteCallback.call(this, data);


      }

    });


  }

});


$('input#facebooklink').mentiony({
    	  // triggerChar: '@',

  onDataRequest: function (mode, keyword, onDataRequestCompleteCallback) {

    $.ajax({

      method: "GET",

      url: "https://autocomplete.clearbit.com/v1/companies/suggest?query=:"+keyword,

      dataType: "json",

      success: function (response) {
      	data=""
      	// var lest = response;
      	// console.log(response);
      	var data=[];
      	var i=1;
        $.each(response, function (index, element)
        {

        data.push({ id:i, name:element.name, 'avatar':element.logo,});
        i=i+1;
})

        // NOTE: Assuming this filter process was done on server-side

        data = jQuery.grep(data, function( item ) {

            return item.name.toLowerCase().indexOf(keyword.toLowerCase()) > -1;

        });


          // Call this to populate mention.

        onDataRequestCompleteCallback.call(this, data);


      }

    });


  }

});