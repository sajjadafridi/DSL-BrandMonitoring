window.onerror = function () {
    console.log(arguments);
}
//dynamically created list should be selected using on
$('#rlist').on('click', 'li', function(){
    $('#rlist').hide();
    var searchvalue = $(this).text();
    $('#search-input').val(searchvalue);
    var domainvalue=$(this).children("input").val();
    $('#domain-input').val(domainvalue);
    var imgUrl = $(this).children('img').attr('src');
    $('#input-image').attr('src',imgUrl);
    $('#image-input').attr('src',imgUrl);

});

$('#image-source').on('click', function()
{
        $('#search-input').val(" ");
        $('#input-image').attr('src',"");


});


var delay = 400,
    input = document.querySelector('#ajax-example input'),
    result = document.querySelector('.result');
var ajax = new XMLHttpRequest(),
    lastKeyUp = 0,
    cb;

input.onkeyup = function (e) {

    lastKeyUp = e.timeStamp;
    if (e.timeStamp - lastKeyUp > delay) {
        doSearch()
    } else {
        cb = setTimeout(doSearch, delay)
    }
}


function doSearch() {
    ajax.open("GET", "https://autocomplete.clearbit.com/v1/companies/suggest?query=:" + input.value.trim(), true);
    ajax.onload = function () {
        var sHTML = '';
        JSON.parse(ajax.responseText).map(function (i) {
            sHTML += '<li ';
            if (!i.logo) {
                i.logo = 'http://dummyimage.com/128x128?text=No%20Logo';
            };
            sHTML += 'id="' + i.name + '">' + '<img src="' + i.logo + '" />';
            sHTML += ((i.name) ? i.name : i.domain);
            sHTML += '<input type="hidden" value="'+i.domain +'">'+'</input>';
           // alert(i.domain)
            // sHTML+=' <a href="http://'+i.domain+'">'+i.domain+'</a>';
            sHTML += '</li>';
        });
        if (!$('#ajax-example input').val()) {
            $('#rlist').hide();
        }
        else {
            $('#rlist').show();
        }
        result.innerHTML = sHTML;
    };
    ajax.send();
}





doSearch();