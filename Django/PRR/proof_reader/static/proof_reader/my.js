var TextDiv = document.getElementById("TextDiv");
var SuggestDiv = document.getElementById("SuggestDiv");
var URL = "/send";
TextDiv.addEventListener("keypress", onkeypress);
// TextDiv.addEventListener("input", oninput);
// TextDiv.addEventListener("paste", onpaste);

// space = 32, ! = 33, 1 = 49, ? = 63, . = 46
// #id is for list of suggestions
// wid is for span elements
var processed = 0;
var spell_matrix = [];
var excl_or_fstop =-1;
// var oldHTML = "";

$('#SuggestDiv').click(function(e){
    var word = document.elementFromPoint(e.clientX, e.clientY);
    console.log(word);
    if(word.className=="Sugg_li"){
        // spellID = wordSpan.id.substring(1, wordSpan.id.length);
        // var newsuggest;
        // var suggest_html = "<ul class='SuggestList'>";
        // for(newsuggest in spell_matrix[spellID]){
        //     console.log(spell_matrix[spellID][newsuggest]);
        //     suggest_html += "<li>"+spell_matrix[spellID][newsuggest]+"</li> ";
        // }
        // suggest_html +=  "<li class='ignore'>IGNORE</li>";
        // suggest_html +=  "</ul>";
        // SuggestDiv.innerHTML = suggest_html;
        // console.log(word.id);
        replace(word.id, word.innerHTML);

    }
    else if(word.className=="ignore"){
        replace(word.id, "");
    }

})

$('#TextDiv').click(function(e){
    var wordSpan = document.elementFromPoint(e.clientX, e.clientY);
    console.log(wordSpan);
    if(wordSpan.className=="SpellClass"){
        spellID = wordSpan.id.substring(1, wordSpan.id.length);
        var newsuggest;
        var suggest_html = "<ul class='SuggestList'>";
        for(newsuggest in spell_matrix[spellID]){
            console.log(spell_matrix[spellID][newsuggest]);
            suggest_html += "<li class='Sugg_li' id='#" +spellID+"'>"+spell_matrix[spellID][newsuggest]+"</li> ";
        }
        suggest_html +=  "<li class='ignore' id='#" +spellID+"'>IGNORE</li>";
        suggest_html +=  "</ul>";
        SuggestDiv.innerHTML = suggest_html;
    }

})

function replace(word_id, replacement_string){
    word_id = word_id.substring(1, word_id.length);
    var old = document.getElementById("w"+word_id);
    if(replacement_string!=""){

        var lscid = TextDiv.lastChild.previousSibling.id;
        lscid = lscid.substring(1, lscid.length);
        console.log(lscid);
        old.innerHTML = replacement_string;
        if(excl_or_fstop!=-1 && word_id==lscid){
            old.innerHTML += String.fromCharCode(excl_or_fstop);
            excl_or_fstop = -1;
        }
        else{
            old.innerHTML += " ";
        }
    }
    old.className = "SpanClass";

    SuggestDiv.innerHTML="";

}

function onkeypress(e){
    console.log(e.keyCode);
    // console.log(e.data);

    if(e.keyCode==33 || e.keyCode==63 || e.keyCode==46){
        excl_or_fstop = e.keyCode;
        e.preventDefault();
        var text = $(this).text();
        var lastchar = String.fromCharCode(e.keyCode);

        console.log(lastchar);
        var textarr = text.replace(/[\s]+/g, " ").trim().split(' ');


        var n = textarr.length
        if(processed < n){

          if(TextDiv.hasChildNodes()){
            TextDiv.removeChild(TextDiv.lastChild);
          }
          if(TextDiv.hasChildNodes()){
            TextDiv.lastChild.innerHTML += " ";
          }
          newHTML = TextDiv.innerHTML;
          console.log(newHTML);

        $.each(textarr.slice(processed, n), function(index, value){
          newHTML += "<span class='SpanClass' id='w"+(processed+index)+"' >" + value + "&nbsp;</span>";
          // newHTML += "<span class='other' id='"+index+"''>" + value + "&nbsp;</span>";
            if(processed+index==n-1){
                newHTML = newHTML.substring(0, newHTML.length-13)+lastchar+"</span><span class='SpanClass'>&nbsp;</span>";
            }
        });
                
      	$(this).html(newHTML);

        //// Set cursor postion to end of text
        var child = $(this).children();
        var range = document.createRange();
        var sel = window.getSelection();
        range.setStart(child[child.length - 1], 1);
        range.collapse(true);
        sel.removeAllRanges();
        sel.addRange(range);
        $(this)[0].focus(); 

        sendRequest(textarr.slice(processed, n), function(){processed=n;});   
    }
  }
}




// function onpaste(e){
//     var clipboardData, pastedData;

//     // Stop data actually being pasted into div
//     e.stopPropagation();
//     e.preventDefault();

//     // Get pasted data via clipboard API
//     clipboardData = e.clipboardData || window.clipboardData;
//     pastedData = clipboardData.getData('Text');
//     console.log("heypaste");
//     var text = pastedData.replace(/[\s]+/g, " ").trim();
//     var word = text.split(" ");
//     var newHTML = "";

//     $(this).html(newHTML);
    
//     //// Set cursor postion to end of text
//     var child = $(this).children();
//     var range = document.createRange();
//     var sel = window.getSelection();
//     range.setStart(child[child.length - 1], 1);
//     range.collapse(true);
//     sel.removeAllRanges();
//     sel.addRange(range);
//     $(this)[0].focus(); 
// }

function sendRequest(arr, callback){
    var s = arr.join(" ");
    // var data_to_send = $.serialize(arr);
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data:{process_arr:s},
        success: function(json){
            console.log(json);

            var i;
            for (i=0; i<json["spell"].length; i++){
                icol = [];
                var j;
                for (j in json["spell"][i]){
                    icol.push(json["spell"][i][j]);
                }
                if(icol.length!=0){
                    var id = "w" + (processed+i);
                    console.log(id);
                    document.getElementById(id).className = "SpellClass";
                }
                spell_matrix.push(icol);
            }
            console.log(spell_matrix);
            callback();

            // for (i in json["b"]){
            //   console.log(json["a"][i]) ;
            //   // for (j in i){
            //   //   console.log(j)
            //   // }  
            //   console.log("--------------------------------");     
            // }
            // for (i in json["c"]){
            //   console.log(json["a"][i]) ;
            //   // for (j in i){
            //   //   console.log(j)
            //   // }  
            //   console.log("--------------------------------");     
            // }
          
         
        },
 error: function(e){
     console.log("not recieved" + e.message);
 }
    });
}
