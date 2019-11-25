var TextDiv = document.getElementById("TextDiv");
var SuggestDiv = document.getElementById("SuggestDiv");
var pass = document.getElementById("passive");
var act = document.getElementById("active");
var URL = "/send";
TextDiv.addEventListener("keypress", onkeypress);
act.addEventListener("keypress", onactkeypress);
// TextDiv.addEventListener("input", oninput);
// TextDiv.addEventListener("paste", onpaste);

// space = 32, ! = 33, 1 = 49, ? = 63, . = 46
// #id is for list of suggestions
// wid is for span elements
var s_processed = 0;
var g_processed = 0;
var p_processed = 0;
var spell_matrix = [];
var gram_matrix = [];
var g2_matrix = [];
var g3_matrix = [];
var syn_matrix = [];

var punc_matrix = [];
var excl_or_fstop =-1;
var textarr = [];
var n = 0;
// var oldHTML = "";

function onactkeypress(e){
    if(e.keyCode==33 || e.keyCode==63 || e.keyCode==46){
        sendRequest($(this).text(), function(e){}, 9);
    }
}

// $('#active').click(
//     function(e){
//         sendRequest($(this).text(), function(e){}, 9);
//     }
//     )

$('#SuggestDiv').click(function(e){
    var word = document.elementFromPoint(e.clientX, e.clientY);
    console.log(word);
    span_id = word.id.substring(1, word.id.length);
    span_class = document.getElementById("w"+span_id).className;
    var c;
    if(span_class=="SpellClass") c=1;
    else if(span_class=="GramClass") c=2;
    else if(span_class=="PuncClass") c=3;

    if(word.className=="Sugg_li"){
        
        replace(span_id, word.innerHTML, c);

    }
    else if(word.className=="ignore"){
        replace(span_id, "", c);
    }
    console.log(span_class);
    if(span_class=="SpellClass"){
        var finished = true;
        var count=0;
        for(count=0; count<spell_matrix.length; count++){
            if(spell_matrix[count].length!=0){
                finished = false;

                // console.log('error');
                // console.log(count);
                break;
            }
        }
        if(finished){
            console.log('grammar started');
            sendRequest(textarr.slice(g_processed,n), 
                function(){
                    // g_processed=n;
                    gram_complete();
                }, 2)
        }    
    }
    
    if(span_class=="GramClass"){
        gram_complete();
    }

})
var gram_count=1;
function gram_complete(){
    var finished = true;
    var count=0;
    for(count=0; count<gram_matrix.length; count++){
        if(gram_matrix[count].length!=0){
            finished = false;

            // console.log('error');
            // console.log(count);
            break;
        }
    }
    if(finished && gram_count<=3){
        gram_count++;
        gram_matrix.length = 0;
        sendRequest(textarr.slice(0,n), function(){
            gram_complete();
        }, gram_count+1);
    }

    else if(finished){
        sendRequest(textarr.slice(0,n), function(){}, 5);
    }

    // else if(finished){

    //     console.log('punc started');
    //     sendRequest(textarr.slice(p_processed,n), function(){p_processed=n;}, 3);
    //     temp = []
    //     var i;
    //     for( i in textarr){
    //         var j;
    //         for(j in textarr[i].split(" ")){
    //             temp.push((textarr[i].split(" "))[j]);
    //         }
    //     }
    //     textarr = temp.slice();
    //     n = textarr.length;
    //     newHTML = "";
    //     $.each(textarr.slice(), function(index, value){
    //       newHTML += "<span class='SpanClass' id='w"+(index)+"' >" + value + "&nbsp;</span>";
    //       // newHTML += "<span class='other' id='"+index+"''>" + value + "&nbsp;</span>";
    //         if(index==n-1){
    //             newHTML = newHTML.substring(0, newHTML.length-13)+"</span><span class='SpanClass'>&nbsp;</span>";
    //         }
    //     });
                
    //     TextDiv.innerHTML = (newHTML);

        //// Set cursor postion to end of text
        // var child = $(this).children();
        // var range = document.createRange();
        // var sel = window.getSelection();
        // range.setStart(child[child.length - 1], 1);
        // range.collapse(true);
        // sel.removeAllRanges();
        // sel.addRange(range);
        // $(this)[0].focus(); 
    // }       
}

$('#TextDiv').click(function(e){
    var wordSpan = document.elementFromPoint(e.clientX, e.clientY);
    console.log(wordSpan);
    if(wordSpan.className=="SpellClass"){
        var spellID = wordSpan.id.substring(1, wordSpan.id.length);
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
    else if(wordSpan.className=="GramClass"){
        var gramID = wordSpan.id.substring(1, wordSpan.id.length);
        var newsuggest;
        var suggest_html = "<ul class='SuggestList'>";
        for(newsuggest in gram_matrix[gramID]){
            console.log(gram_matrix[gramID][newsuggest]);
            suggest_html += "<li class='Sugg_li' id='#" +gramID+"'>"+gram_matrix[gramID][newsuggest]+"</li> ";
        }
        suggest_html +=  "<li class='ignore' id='#" +gramID+"'>IGNORE</li>";
        suggest_html +=  "</ul>";
        SuggestDiv.innerHTML = suggest_html;
    }
    else if(wordSpan.className=="PuncClass"){
        var puncID = wordSpan.id.substring(1, wordSpan.id.length);
        var newsuggest;
        var suggest_html = "<ul class='SuggestList'>";
        for(newsuggest in punc_matrix[puncID]){
            console.log(punc_matrix[puncID][newsuggest]);
            suggest_html += "<li class='Sugg_li' id='#" +puncID+"'>"+punc_matrix[puncID][newsuggest]+"</li> ";
        }
        suggest_html +=  "<li class='ignore' id='#" +puncID+"'>IGNORE</li>";
        suggest_html +=  "</ul>";
        SuggestDiv.innerHTML = suggest_html;
    }
})

function replace(word_id, replacement_string, chk){
    console.log(word_id);
    var old = document.getElementById("w"+word_id);
    oldlastchar = old.innerHTML[old.innerHTML.length-1];
    if(oldlastchar==" ") oldlastchar=old.innerHTML[old.innerHTML.length-2];
    console.log(oldlastchar);

    if(chk==1){
        spell_matrix[word_id].length = 0;
    }
    else if(chk==2){
        gram_matrix[word_id].length = 0;
    }
    else if(chk==3){
        punc_matrix[word_id].length = 0;
        oldlastchar = "";
    }

    
    if(replacement_string!=""){
        textarr[word_id] = replacement_string+oldlastchar;
        old.innerHTML = replacement_string;
        if(oldlastchar=="!" || oldlastchar=="." || oldlastchar=="?" || oldlastchar==","){
            old.innerHTML += oldlastchar+" ";
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
        text += lastchar
        console.log(lastchar);
        textarr = text.replace(/[\s]+/g, " ").trim().split(' ');


        n = textarr.length
        if(s_processed < n){

          if(TextDiv.hasChildNodes()){
            TextDiv.removeChild(TextDiv.lastChild);
          }
          if(TextDiv.hasChildNodes()){
            TextDiv.lastChild.innerHTML += " ";
          }
          newHTML = TextDiv.innerHTML;
          console.log(newHTML);

        $.each(textarr.slice(s_processed, n), function(index, value){
          newHTML += "<span class='SpanClass' id='w"+(s_processed+index)+"' >" + value + "&nbsp;</span>";
          // newHTML += "<span class='other' id='"+index+"''>" + value + "&nbsp;</span>";
            if(s_processed+index==n-1){
                newHTML = newHTML.substring(0, newHTML.length-13)+"</span><span class='SpanClass'>&nbsp;</span>";
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

        sendRequest(textarr.slice(s_processed, n),
         function(){
            // s_processed=n;
            var finished = true;
            var count=0;
            for(count=0; count<spell_matrix.length; count++){
                if(spell_matrix[count].length!=0){
                    finished = false;

                    // console.log('error');
                    // console.log(count);
                    break;
                }
            }
            if(finished){
                console.log('grammar started');
                sendRequest(textarr.slice(g_processed,n), function(){
                    // g_processed=n;
                    gram_complete();
                    }, 2)
            }
        }, 1);   
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

function sendRequest(arr, callback, chk){ // chk = 1--> spell,2--> gram,3-->syn
    if(chk==3) console.log('########################################################');
    var s;
    if(chk!=9) var s = arr.join(" ");
    else s = arr;
    s = s+chk;
    console.log(s);
    // var data_to_send = $.serialize(arr);
    $.ajax({
        type: "GET",
        url: URL,
        dataType: 'json',
        data:{process_arr:s},
        success: function(json){
            console.log(json);
            if(chk==1){
                var i;
                for (i=0; i<json["mat"].length; i++){
                    icol = [];
                    var j;
                    for (j in json["mat"][i]){
                        icol.push(json["mat"][i][j]);
                    }
                    if(icol.length!=0){
                        var id = "w" + (s_processed+i);
                        console.log(id);
                        document.getElementById(id).className = "SpellClass";
                    }
                    spell_matrix.push(icol);
                }
                console.log(spell_matrix);
                callback();
            }
            else if(chk==2 || chk==3 || chk==4){
                var i;
                for (i=0; i<json["mat"].length; i++){
                    icol = [];
                    var j;
                    for (j in json["mat"][i]){
                        icol.push(json["mat"][i][j]);
                    }
                    if(icol.length!=0){
                        var id = "w" + (i);
                        console.log(id);
                        document.getElementById(id).className = "GramClass";
                    }
                    gram_matrix.push(icol);
                }
                console.log(gram_matrix);
                callback();
            }
            else if(chk==5){
                var i;
                for (i=0; i<json["mat"].length; i++){
                    icol = [];
                    var j;
                    for (j in json["mat"][i]){
                        icol.push(json["mat"][i][j]);
                    }
                    if(icol.length!=0){
                        var id = "w" + (p_processed+i);
                        console.log(id);
                        document.getElementById(id).className = "PuncClass";
                    }
                    punc_matrix.push(icol);
                }
                console.log(punc_matrix);
                callback();
            }
            else if(chk==9){
                pass.innerHTML = json["mat"];
            }

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
