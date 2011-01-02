$(function() {
    
    /**
     * Events related to the text input box
     */
    var defaultLoginText = "Your Last.FM Username";
    var blurClass = "blur";

    $("#lastfmUser").val(defaultLoginText);
    $("#lastfmUser").addClass(blurClass);

    $("#lastfmUser").focus(function() {
        if ($(this).val() === defaultLoginText) {
            $(this).toggleClass(blurClass);
        }
        $(this).val("");
    });

    $("#lastfmUser").blur(function() {
        if ($(this).val() == "") {
            $("#lastfmUser").val(defaultLoginText);
            $("#lastfmUser").toggleClass(blurClass);
        }
    });
            
    var keypress_delay = 2;
    var lastfm_user = "";

    $("#lastfmUser").keypress(function(event) {
        lastfm_user = $(this).val();

        //$(this).stopTime("ajax_get");

        // enter pressed 
        if (event.keyCode === 13) {
            event.preventDefault();
            try {
              lastFmUserRequest(lastfm_user);
            }
            catch (err) {
              console.log(err);
            }
            return false;
        }
		/*
        else {
            $(this).oneTime(650, "ajax_get", function() {
                lastFmUserRequest(lastfm_user);
            });
        }
		*/
    });


    var lastFmUserRequest = function(user) {
        console.log("user request submitted");
        try {
        $.get("/getinfo?lfmusername="+user, function(data){
          lastFmUserCallback(data);
        });
        } catch(err) {console.log(err)}
    };

    var lastFmUserCallback = function(data) {
      $('#containertest').html(data);
    /*
        var track_data, tracks, tracklist_data, tracklist, progress;

        console.log("callback received");
        var track_dom = $("#trackList");
        if (!track_dom.length) {
			track_data = JSON.parse(data);
			console.log(track_data);

            tracklist_data = {
                tracks: track_data
            }
            tracklist = ich.trackList_template(track_data);
            progress = track_data['progress'];
            $("#body").append(progress);
            $("#body").append(tracklist);
        }*/
    };

});
