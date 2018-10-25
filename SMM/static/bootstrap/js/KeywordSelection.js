$jQuery_3_1_1(document).ready(function(){
    $('#anthingModalDiv').on('click', function() {
        $('#optionalword1,#requiredword1,#excludedword1').tagEditor('destroy');
        $('#optionalword1,#requiredword1,#excludedword1').tagEditor();
    });

    $( "a#advlnk" ).click(function()
    {
        $('textarea#optionalword,#requiredword,#excludedword').tagEditor({
         delimiter: ',', /* space and comma */
               maxTags:10,
               onChange: function(field, editor, tags)
         {
             $('#optionalword').html(tags.length ? tags.join(', ') : '----')
         },
        });
        $input = $('#search-input').val();
        $('#optionalword').tagEditor('addTag', $input.trim())
        list = $('#optionalword').tagEditor('getTags')[0].tags;


    // $('#optionalword').tagEditor('removeTag',$('#search-input').val())

});
});
$('#prevanything').on('click', function()
{
    $jQuery_3_1_1('#optionalword').text('');
    $('#optionalword,#requiredword,#excludedword').tagEditor('destroy');


});
$isActive = false;
$jQuery_3_1_1('#priprvbtn').on('click',function () {
    if($("#CompanyModal").is(':visible'))
    {
        $isActive=true;
        $('#anythingModal').modal('show');
    }

});

$jQuery_3_1_1('#sourcebtn').on('click',function ()
{
    $('#optional-input').val($('#optionalword').val()+$('#optionalword1').val());
    $('#required-input').val($('#requiredword').val()+$('#requiredword1').val());
    $('#excluded-input').val($('#excludedword').val()+$('#excludedword1').val());

    // clear

});


$jQuery_3_1_1('#modelclosebtn,#priorModalbtn,#anythingclosebtn,#otherModalbtn').on('click', function()
{
    $('#PriorityModal').modal('hide');
    $("#modelclosebtn,#priorModalbtn,#otherModalbtn,#anythingclosebtn,#srclngModalbtn").trigger("click");
    $('#CompanyModal').modal('hide');
    $('#OtherModal').modal('hide');
    $(".modal").modal('hide');
    $('textarea#optionalword,#requiredword,#excludedword').tagEditor('destroy');

});

