// Attila Csala
// MAM04 - Kidnify

var kidnify_main = function() {

		//make Kidnify fancy and animated
    $('.logo').animate({
            left: '0px'
        }, 3000)
    $('.on_logo_text').animate({
            right: '0px'
        }, 3000)
    $('.under_logo_login').animate({
            top:"50%"
        }, 3000, "swing")
    $('.back_to_main').animate({
    					left: '-42%'
    			}, 3000)
    			
    	$('.log_out').animate({
    					left: '-38%'
    			}, 3000)
    			
    	$('.matching_effect').animate({
    					left: '38%'
    			}, 3000)
    			
    $('.google_map').animate({
    					top: '15%'
    			}, 3000)			
    			
    			
//    	$(".google_map").click(function(){
//			$(".google_map").hide();
//		});
		
//		$(".toggle_map").click(function(){
//			$(".google_map").hide();
//		});
};
  
$(document).ready(kidnify_main)
  
