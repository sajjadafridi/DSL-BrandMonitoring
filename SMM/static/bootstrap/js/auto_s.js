var index = 'modal_state';
//  Define friendly data store name
var dataStore = window.sessionStorage;

var app = angular.module('NewAlertSubmitApp', []);
app.controller('NewAlertSubmitAppController', ["$scope", "$http", function ($scope, $http) {

    $scope.keywords = [];

    $scope.preventSubmission = function ($event) {

        var keyword = "";
        if (dataStore.getItem(index) === "company") {
            keyword = $('#search-input').val();
        } else {
            keyword = $('#keyword-input').val();
        }
        if (keyword != "") {
            if ($scope.keywords.includes(keyword)) {
                $event.preventDefault();
                $('#errorMessage').css('display', 'block');
            } else {
                $('#errorMessage').css('display', 'none');
            }
        }
    }

    $scope.get_user_keywords = function () {
        $http.get('get_user_keywords/').then(function (data) {
            angular.forEach(data.data, function (value, key) {
                $scope.keywords.push(value);
            });
        });
    }
    $scope.get_user_keywords();

}]);

$('#advanceopt').hide();

$('#sourcebtn').prop('disabled', true);

//dynamically createted list should be selected using on
$('#rlist').on('click', 'li', function () {
    $('#rlist').hide();
    var searchvalue = $(this).text();
    console.log(searchvalue)
    $('#search-input').val(searchvalue);
    var domainvalue = $(this).children("input").val();
    $('#domain-input').val(domainvalue);
    $('#search_keyword').val(searchvalue);
    var imgUrl = $(this).children('img').attr('src');
    $('#input-image').attr('src', imgUrl);
    $('#image-input').attr('src', imgUrl);
    $('#sourcebtn').prop('disabled', false);
});

$('#rlist').on("keypress", function (e) {

    var code = e.keyCode || e.which;

    if (code == 13) { // 13 = enter key-code        
        var searchvalue = $(this).text();
        console.log(searchvalue)
        $('#search-input').val(searchvalue);
        var domainvalue = $(this).children("input").val();
        $('#domain-input').val(domainvalue);
        $('#search_keyword').val(searchvalue);
        var imgUrl = $(this).children('img').attr('src');
        $('#input-image').attr('src', imgUrl);
        $('#image-input').attr('src', imgUrl);
        $('#sourcebtn').prop('disabled', false);
    }
});


$('#search-input').on('click', function () {
    $('#sourcebtn').prop('disabled', true);
    $('#errorMessage').css('display', 'none');

});

$('#keyword-input').on('click', function () {
    $('#sourcebtn').prop('disabled', true);
    $('#errorMessage').css('display', 'none');

});


$('#ajax-example').on('keydown', function (e) {
    var $listItems = $('#rlist li');
    var key = e.keyCode,
        $selected = $listItems.filter('.selected'),
        $current;

    if (key != 40 && key != 38 && key != 10 && key != 13) return
    $listItems.removeClass('selected');

    if (key == 40) // Down key
    {
        if (!$selected.length || $selected.is(':last-child')) {
            $current = $listItems.eq(0);
        } else {
            $current = $selected.next();
        }
    } else if (key == 38) // Up key
    {
        if (!$selected.length || $selected.is(':first-child')) {
            $current = $listItems.last();
        } else {
            $current = $selected.prev();
        }
    } else if (key == 13 || key == 10) {
        e.preventDefault();
        $('#rlist').hide();
        var $domainvalue = $('#search-input').val();
        $('#search_keyword').val($domainvalue);
        console.log($domainvalue)
        $('#sourcebtn').prop('disabled', false);

    }

    $current.addClass('selected');
    var text_value = $current.text();
    var src = $current.find("img").attr("src");
    $('#search-input').val(text_value);
    $('#input-image').attr('src', src);
})

function showbutton() {
    document.getElementById("myInput").style.backgroundColor = "yellow";
}

$('div#companyDivModal').on('click', function () {
    $('#companyOrcompetitorH').html("Enter the name of Company or Brand you want to search or monitor.");
    $('#CompanyorCompetitorHtop').html("What's the Brand?");
    $('input[name=keyword_input]').val('');
    document.getElementById('search-input').type = 'text';
    document.getElementById('keyword-input').type = 'hidden';

    dataStore.setItem(index, 'company');
    $('#errorMessage').css('display', 'none');
});

$("#keyword-input").on('change keyup paste', function () {
    var key_word_len = $("#keyword-input").val().length;
    if (key_word_len > 0) {
        $('#sourcebtn').prop('disabled', false);
    } else {
        $('#sourcebtn').prop('disabled', true);
    }

});

$('div#anthingModalDiv').on('click', function () {
    $('#companyOrcompetitorH').html("Enter the required keyword in the boxe.");
    $('#CompanyorCompetitorHtop').html("Search keyword");
    $('input[name=search_input]').val('');
    document.getElementById('search-input').type = 'hidden';
    document.getElementById('keyword-input').type = 'text';

    dataStore.setItem(index, 'anything');
    $('#errorMessage').css('display', 'none');
});
$('#image-source,#modelclosebtn').on('click', function () {
    $('#search-input').val("");
    $('#input-image').attr('src', "");
    $('#rlist').hide();
});


var delay = 400,
    input = document.querySelector('#ajax-example input'),
    result = document.querySelector('.result');
var ajax = new XMLHttpRequest(),
    lastKeyUp = 0,
    cb;

input.onkeyup = function (e) {
    var key = e.keyCode
    if (key != 40 && key != 38 && key != 13) {
        lastKeyUp = e.timeStamp;
        if (e.timeStamp - lastKeyUp > delay) {
            doSearch()
        } else {
            cb = setTimeout(doSearch, delay)
        }
    }

};


function doSearch() {
    ajax.open("GET", "https://autocomplete.clearbit.com/v1/companies/suggest?query=:" + input.value.trim(), true);
    ajax.onload = function () {
        var p = 0;
        var sHTML = '';
        JSON.parse(ajax.responseText).map(function (i) {
            sHTML += '<li ';
            if (!i.logo) {
                i.logo = 'http://dummyimage.com/128x128?text=No%20Logo';
            };
            sHTML += 'id="' + p++ + '">' + '<img src="' + i.logo + '" />';
            sHTML += ((i.name) ? i.name : i.domain);
            sHTML += '<input type="hidden" value="' + i.domain + '">' + '</input>';
            // alert(i.domain)
            // sHTML+=' <a href="http://'+i.domain+'">'+i.domain+'</a>';
            sHTML += '</li>';
        });
        if ($('#ajax-example input').val() == null) {
            $('#rlist').hide();
        } else {
            $('#rlist').show();
        }
        result.innerHTML = sHTML;
    };
    ajax.send();
}