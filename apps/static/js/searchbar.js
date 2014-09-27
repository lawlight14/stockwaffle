$(document).ready(function(){
	$("#scroll-box").scroll(function(){
    	var sTop = $(this).scrollTop();

	    if(sTop+70 >= $(window).height()*0.7){
	    	var offset = sTop+70 - $(window).height()*0.7
	    	var calcString = sTop <= $("#scroll-box").height() ? "calc(30% - "+offset+"px)" : "10px";

	    	$(".searchbar-container").css("top",calcString);
	    }else{
	    	$(".searchbar-container").css("top","30%");
	    }

	    
	    	var logoBottom = sTop < $("#scroll-box").height() ? sTop : $("#scroll-box").height();
	    	$("#logo").css("bottom",logoBottom);
	    
	});
})
