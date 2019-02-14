$(".dropdown-menu a ").on('click', function () {

    option = $(this).text()
    if ($.trim(option) == 'Positive') {
        $("#dropdownEmotionButton").attr("src", '/static/images/smily.jpg');
    }
    else if ($.trim(option) == 'Negative') {
        $("#dropdownEmotionButton").attr("src", '/static/images/sad.svg');
    }
    else {
        $("#dropdownEmotionButton").attr("src", '/static/images/emotion.jpg');

    }
});