var keyworddata = new Map();
$(document).ready(function () {

    $("button#brandbtn,#advlnk").click(function (event)
    {

        var domain_word = $("#domain-input").val();
        $("#companyname").val(domain_word);
        console.log(domain_word);
        // $('#companyname').val(search_word);
        //searchUrl(domain_word );
        search_url(domain_word);
        $('[id^="mentiony-content"][id$="facebooklink"]').each(function (i, el)
        {
            var outerSpan = document.createElement('span');
            outerSpan.contenteditable = 'false';
            outerSpan.className = 'mention-area';
            document.getElementsByTagName('body')[0].appendChild(outerSpan);

            // Now create inner span and append to outer span
            var innerSpan = document.createElement('span');
            innerSpan.className = 'highlight';
            innerSpan.contentEditable="false";
            outerSpan.appendChild(innerSpan);

            //create image and append into inner span
            var fimage = document.createElement("img");
            fimage.src=    $('#image-input').attr('src');
            fimage.id="1";
            fimage.style="border-radius: 40%;background-repeat: no-repeat;background-position: left;margin-bottom:2px;width:13px;height:13px";
            fimage.draggable="false";
            innerSpan.appendChild(fimage);

            //create a tag and insert after image
            var fa = document.createElement("a");
            fa.href="undefined";
            fa.id="2";
            fa.className=("highlight disableselect");
            fa.draggable="false";
            fa.innerHTML=$('#search-input').val();
            fimage.after(fa);

            //create another span for normal text and append in to outer span
            var fspace = document.createElement("span");
            fspace.className="normalText";
            fspace.innerHTML="&nbsp";
            outerSpan.appendChild(fspace);
            el.appendChild(outerSpan);
        });

         $('[id^="mentiony-content"][id$="twitterlink"]').each(function (i, el) {

             var outerSpan = document.createElement('span');
            outerSpan.contenteditable = 'false';
            outerSpan.className = 'mention-area';
            document.getElementsByTagName('body')[0].appendChild(outerSpan);

            // Now create inner span and append to outer span
            var innerSpan = document.createElement('span');
            innerSpan.className = 'highlight';
            innerSpan.contentEditable="false";
            outerSpan.appendChild(innerSpan);

            //create image and append into inner span
            var fimage = document.createElement("img");
            fimage.src= $('#image-input').attr('src');
            fimage.id="1";
            fimage.style="border-radius: 40%;background-repeat: no-repeat;background-position: left;margin-bottom:2px;width:13px;height:13px";
            fimage.draggable="false";
            innerSpan.appendChild(fimage);

            //create a tag and insert after image
            var fa = document.createElement("a");
            fa.href="undefined";
            fa.id="2";
            fa.className=("highlight disableselect");
            fa.draggable="false";
            fa.innerHTML=$('#search-input').val();
            fimage.after(fa);

            //create another span for normal text and append in to outer span
            var fspace = document.createElement("span");
            fspace.className="normalText";
            fspace.innerHTML="&nbsp";
            outerSpan.appendChild(fspace);
            el.appendChild(outerSpan);
        });

          $('[id^="mentiony-content"][id$="linkdinlink"]').each(function (i, el) {

             var outerSpan = document.createElement('span');
            outerSpan.contenteditable = 'false';
            outerSpan.className = 'mention-area';
            document.getElementsByTagName('body')[0].appendChild(outerSpan);

            // Now create inner span and append to outer span
            var innerSpan = document.createElement('span');
            innerSpan.className = 'highlight';
            innerSpan.contentEditable="false";
            outerSpan.appendChild(innerSpan);

            //create image and append into inner span
            var fimage = document.createElement("img");
            fimage.src= $('#image-input').attr('src');
            fimage.id="1";
            fimage.style="border-radius: 40%;background-repeat: no-repeat;background-position: left;margin-bottom:2px;width:13px;height:13px";
            fimage.draggable="false";
            innerSpan.appendChild(fimage);

            //create a tag and insert after image
            var fa = document.createElement("a");
            fa.href="undefined";
            fa.id="2";
            fa.className=("highlight disableselect");
            fa.draggable="false";
            fa.innerHTML=$('#search-input').val();
            fimage.after(fa);

            //create another span for normal text and append in to outer span
            var fspace = document.createElement("span");
            fspace.className="normalText";
            fspace.innerHTML="&nbsp";
            outerSpan.appendChild(fspace);
            el.appendChild(outerSpan);
        });

    });

    $('input#facebooklink,input#twitterlink,input#linkdinlink').mentiony({
        // triggerChar: '@',
        onDataRequest: function (mode, keyword, onDataRequestCompleteCallback) {
            $jQuery_3_1_1.ajax({
                method: "GET",
                url: "https://autocomplete.clearbit.com/v1/companies/suggest?query=:" + keyword,
                dataType: "json",
                success: function (response) {
                    data = "";
                    var data=[];
                    // var lest = response;
                    // console.log(response);
                    var i = 1;
                    $.each(response, function (index, element) {
                        data.push({id: i, name: element.name, 'avatar': element.logo,});
                        i = i + 1;
                    })
                    // NOTE: Assuming this filter process was done on server-side
                    data = jQuery.grep(data, function (item) {

                        return item.name.toLowerCase().indexOf(keyword.toLowerCase()) > -1;
                    });
                    // Call this to populate mention.
                    onDataRequestCompleteCallback.call(this, data);

                }

            });
        }

    });

});

function search_url() {
    $jQuery_3_1_1.ajax({
        url: 'https://company-stream.clearbit.com/v2/companies/find?',
        dataType: 'json',
        data: {
            domain: arguments[0],
        },
        success: function (data, status) {
            $.each(data, function (index, element) {
                //keyworddata.clear();
                if (index == "facebook") {
                    var flike, furl;
                    $.each(element, function (key, value) {
                       if(key.trim() == "handle" )
                            furl = value;
                        else if(key.trim() == "likes" )
                            flike = value;
                    });
                        keyworddata['furl'] = "https://www.facebook.com/"+furl;
                        keyworddata['flike'] = flike;
                }
                if(index== "logo")
                    keyworddata['logo'] = element.trim();
                if (index == "linkedin") {
                    var llike, lurl;
                    $.each(element, function (key, value) {
                        if(key.trim() == "handle" )
                            lurl = value;
                        else if(key.trim() == "likes" )
                            llike = value;
                    });
                    keyworddata['lurl'] = "https://www.linkedin.com/"+lurl;
                    keyworddata['llike'] = llike;
                }

                if (index == "twitter") {
                    var tavatar, tsite, turl, tlike, tid;
                    $.each(element, function (key, value) {
                        if(key.trim() == "handle" )
                            turl = value;
                        else if(key.trim() == "avatar" )
                            tavatar = value;
                        else if(key.trim() == "site" )
                            tsite = value;
                        else if(key.trim() == "id" )
                            tid = value;
                    });
                    keyworddata['turl'] = turl;
                    keyworddata['tavatar'] = tavatar;
                    keyworddata['tsite'] = tsite;
                    keyworddata['tid'] = tid;
                }
            });

        },
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('Authorization', 'Bearer ' + "sk_9b93a0400fa758cb5da0b7b0e4571207");
        }
    });

}
