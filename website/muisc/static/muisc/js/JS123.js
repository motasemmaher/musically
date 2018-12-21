

var url ='http://127.0.0.1:8000/Album/';
$.ajax({
    method:'GET',
    url :url,
    success:function(data){
        console.log(data[0].artlist);
        console.log("asdd");
    }
});

$(document).ready(function(){
    
        

    $('.m').click(function(){

        $(".v").removeClass("btn-info");
        $(".m").addClass("btn-info");
    });
    $('.v').click(function(){
        $(".m").removeClass("btn-info");
        $(".v").addClass("btn-info");   
    }); 
    $('.play').click(function(){
            song = document.getElementsByClassName("play");
            Audio = document.getElementById("Audio");
            Audio.src=this.value;
    });
    $('#serach').click(function(){
        g = document.getElementsByTagName('input');
        console.log(g[0].value);
        
    })

});




      