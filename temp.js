function do_pl() {
    console.log("ab:" + hasAdblock);
    if (!oldIE && hasMP4Video) {
      if (hasAdblock) {
        $("#jw").html("<video id=\"flvv\" preload=\"none\" poster=\"//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/main.jpg\" controls style=\"width:100%; height:100%;\" src=\"\"><source src=\"//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/360.mp4\" title=\"360p\" type=\"video/mp4\" /></video>");
      } else {
        $("#jw").html("<video id=\"flvv\" preload=\"none\" poster=\"//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/main.jpg\" controls style=\"width:100%; height:100%;\" src=\"\"><source src=\"//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/360.mp4\" title=\"360p\" type=\"video/mp4\" /><source src=\"//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/720.mp4\" title=\"720p60\" type=\"video/mp4\" /><source src=\"//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/1080.mp4\" title=\"1080p60\" type=\"video/mp4\" /></video>");
      }
      if (hasAdblock) {
        $("#ovrl_ab").show();
        $("#ab_wait").hide();
        $("#ab_close").show();
      } else {
        hide_ov();
      }
      $("#flvv").on("error",
      function() {
        if ($("#flvv").attr("src") != "") {
          $("#ovrl_err").show();
        }
      });
    } else {
      $("#jw").css("background", "#000").html("<span style='color:#fff'>Your browser has not supported. Video can not be played.<br />You can download it: <a href='//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/360.mp4' style='color:#ddd'>360p</a> : <a href='//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/720.mp4' style='color:#ddd'>720p HD 60 FPS</a> : <a href='//s44.bigcdn.cc/pubs/6455b46f37d499.30745525/1080.mp4' style='color:#ddd'>1080p Full HD 60 FPS</a></span>");
    }
  };
  do_pl();