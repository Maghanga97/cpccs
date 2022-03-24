$(document).ready(function(){
    $("#text_swa").hide();
    $("#button_eng").hide();

    $("#button_swa").click(function(){
        $("#text_eng").hide();
        $("#text_swa").show();
        $("#button_swa").hide();
        $("#button_eng").show();
        $("#head").text("Karibu");
    });
    $("#button_eng").click(function(){
        $("#text_eng").show();
        $("#button_eng").hide();
        $("#head").text("Welcome");

        $("#text_swa").hide();
        $("#button_swa").show();
    });
    $("#go").click(function(){
        $("#popup").fadeOut(1000);
    });
    $("textarea").keypress(function(){
        var chrs = $("textarea").val().length;
        var str = document.getElementById("limit");
        str.innerHTML=chrs;
        if(chrs==160){
            str.innerHTML=chrs+" "+"Maximum characters reached.";
        }else{
            str.innerHTML= "Max = 160 chars"+" "+ "("+chrs+")";
        }
    });
    $("textarea").keyup(function(){
        var chrs = $("textarea").val().length;
        var str = document.getElementById("limit");
        str.innerHTML=chrs;
        if(chrs==160){
            str.innerHTML=chrs+" "+"Maximum characters reached.";
        }else{
            str.innerHTML= "(Max = 160 chars)"+" "+ "("+chrs+")";
        }
    })
    $(".reporter_details").hide();
    $(".report_details").hide();

    // Welcome Message Modal
        $("#Message_Modal").css("display","block"); 

    $(".close").click(function(){
        $("#Message_Modal").css("display","none");
    });
    $("#go").click(function(){
        $("#Message_Modal").css("display","none");
    });


    // User selection Modal
    $(".startbtn").click(function(){
        $("#Welcome_Modal").css("display","block"); 
    })

    $(".close").click(function(){
        $("#Welcome_Modal").css("display","none");
    });

    $("#onymous").click(function(){
        $(".controller").fadeOut(1000,function(){
                $(".reporter_details").fadeIn(1000);
        });
        $(".prev2").click(function(){
            $(".reporter_details").fadeOut(1000,function(){
                $(".controller").fadeIn(1000); 
            });
        });
        $(".next").click(1000,function(){
            $("#newprev").hide(function(){
                $("#prev3").show();
            });
            $(".reporter_details").fadeOut(1000,function(){
                $(".report_details").fadeIn(1000);
            });
            $(".prev3").click(function(){
                $(".report_details").fadeOut(1000,function(){
                    $(".reporter_details").fadeIn(1000); 
                });
            });
        });
    });
    $("#anonymous").click(function(){
        $("#prev3").hide();
        $("#newprev").show();
        $(".controller").fadeOut(1000,function(){
                $(".report_details").fadeIn(1000);     
        });
        $("#newprev").click(function(){
            $(".report_details").fadeOut(1000,function(){
                $(".controller").fadeIn(1000); 
            });
        });
    });

});