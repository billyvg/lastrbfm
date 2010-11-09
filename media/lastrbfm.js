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

        $(this).stopTime("ajax_get");

        // enter pressed 
        if (event.keyCode === 13) {
            event.preventDefault();
            lastFmUserRequest(lastfm_user);
            return false;
        }
        else {
            $(this).oneTime(650, "ajax_get", function() {
                lastFmUserRequest(lastfm_user);
            });
        }
    });


    var lastFmUserRequest = function(user) {
        console.log("user request submitted");
        $.get("getinfo?u="+user, function(data){lastFmUserCallback(data);});
    };

    var lastFmUserCallback = function(data) {
        var track_data, tracks, tracklist_data, tracklist;

        console.log("callback received");
        track_data = [{ 
            artist: 'Test Artist',
            title: 'Test Track Title'
        }, {artist:'test artist 2', title: 'test track title 2'}];

        var track_html = '';
        for (var i = 0; i < track_data.length; i++) {
            tracks = ich.track_template(track_data[i]);
            track_html += tracks.text();
        }
        console.log(tracks);
        tracklist_data = {
            tracklist: track_html
        }
        tracklist = ich.trackList_template(tracklist_data);
        
        $("#body").append(tracklist);
        //console.log(data);
    };

});
