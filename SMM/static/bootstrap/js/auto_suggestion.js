
// $jQuery_3_1_1('div#advanceopt').hide();
//dynamically crea  ted list should be selected using on
$jQuery_3_1_1('#rlist').on('click', 'li', function(){
    $('#rlist').hide();
    var searchvalue = $(this).text();
    $('#search-input').val(searchvalue);
    var domainvalue=$(this).children("input").val();
    $('#domain-input').val(domainvalue);
    $('#search_keyword').val(searchvalue);
    var imgUrl = $(this).children('img').attr('src');
    $('#input-image').attr('src',imgUrl);
    $('#image-input').attr('src',imgUrl);
    if(!$('div#advanceopt').is(":visible"))
    {
        $('div#advanceopt').show();
    }


});

$jQuery_3_1_1('#companyModalDiv').on('click', function()
{
    $('#companyOrcompetitorH').html("Enter the name of Company or Brand you want to search or monitor.");
     $('#CompanyorCompetitorHtop').html("What's the Brand?");
});
$jQuery_3_1_1('#competitorModalDiv').on('click', function()
{
        $('#companyOrcompetitorH').html("Enter the name of Competitor you want to search or monitor.");
         $('#CompanyorCompetitorHtop').html("What's the Name?");
});
$jQuery_3_1_1('#image-source,#modelclosebtn').on('click', function()
{
        $('#search-input').val("");
        $('div#advanceopt').hide();
        $('#input-image').attr('src',"");
        $('#rlist').hide();


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
        if ($('#ajax-example input').val() == null) {
            $('#rlist').hide();
        }
        else {
            $('#rlist').show();
        }
        result.innerHTML = sHTML;
    };
    ajax.send();
}


//cancel button click action

// $jQuery_3_1_1(function () {
//      alert("iam clicked");
//      $("#CompanyModal .close").click()
//    $('#CompanyModal').modal('toggle');
// });


$jQuery_3_1_1('#modelclosebtn,#priorModalbtn,#srclngModalbtn').on('click', function()
{
    $('#PriorityModal').modal('hide');
    $("#modelclosebtn,#priorModalbtn,#otherModalbtn").trigger("click");
    $('#CompanyModal').modal('hide');
    $('#OtherModal').modal('hide');

     $(".modal").modal('hide');
});
// $("#CompanyModal .close").click(

// $jQuery_3_1_1("#modelclosebtn").on(function(){
//     alert("iam clicked");
//        $('#CompanyModal').modal('hide');
// });



doSearch();