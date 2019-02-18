var app = angular.module('ReportsApp', []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller('ReportsAppController', ["$scope", "$http", function ($scope, $http) {

    $scope.drawKeywordPieChart = function (alert_name) {
        $http.get('get_user_sentiment/', {
            params: {
                "alert_name": alert_name,
            }
        }).then(function (data) {
            drawChart(data.data.positive, data.data.negative, data.data.neutral)
        });
    };
    $('#keywords').on('change', (function () {

        //your code here
        alert_name = $(this).val();

        if (alert_name != "_")
            $scope.drawKeywordPieChart(alert_name)

    }));
    $scope.reply_click = function (feed) {
        $scope.Keyword_name = feed.ID;
        $("#display_name").text(feed.DisplayName);
        if (feed.Sentiment == '1') {
            $('#dropdownEmotionButton').attr('src', '/static/images/happy.png');
        } else if (feed.Sentiment == '-1') {
            $('#dropdownEmotionButton').attr('src', '/static/images/emotion.svg');
        } else {

            $('#dropdownEmotionButton').attr('src', '/static/images/sad.svg');
        }

    };
}]);




// Load the Visualization API and the corechart package.

google.charts.load('current', {
    'packages': ['corechart']
});
// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart(pos, neg, net) {
    // console.log(data['positive'])
    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Slices');

    data.addRows([
        ['Positive', pos],
        ['Negative', neg],
        ['Neutral', net]
    ]);
    console.log($('#chart_div').height())
    // Set chart options
    var options = {
        'title': 'Sentimental Analysis',
        'width': 800,
        'height': 800
    };

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}