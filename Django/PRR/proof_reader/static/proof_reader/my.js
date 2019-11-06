var TextDiv = document.getElementById("TextDiv");
var SuggestDiv = document.getElementById("SuggestDiv");
var TextArea = document.getElementById("TextArea");
var URL = "/send";
TextDiv.addEventListener("keypress", onkeypress);
// TextDiv.addEventListener("input", oninput);
// TextDiv.addEventListener("paste", onpaste);

// space = 32, ! = 33, 1 = 49, ? = 63, . = 46
var processed = 0;
var spell_matrix = [];
var oldHTML = "";
function onkeypress(e){
    console.log(e.keyCode);
    // console.log(e.data);

    if(e.keyCode==33 || e.keyCode==63 || e.keyCode==46){
        e.preventDefault();
        var text = $(this).text();
        var lastchar = String.fromCharCode(e.keyCode);

        console.log(lastchar);
        var textarr = text.replace(/[\s]+/g, " ").trim().split(' ');


        var n = textarr.length
        if(processed < n){

          var newHTML=oldHTML;
          console.log(newHTML);

        $.each(textarr.slice(processed, n), function(index, value){
          newHTML += "<span class='SpanClass' id='w"+(processed+index)+"' >" + value + "&nbsp;</span>";
          // newHTML += "<span class='other' id='"+index+"''>" + value + "&nbsp;</span>";
            if(processed+index==n-1){
                newHTML = newHTML.substring(0, newHTML.length-13)+lastchar+" </span>";
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

        sendRequest(textarr.slice(processed, n), function(){processed=n; oldHTML=TextDiv.innerHTML;});   
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
                    icol.push(j);
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
