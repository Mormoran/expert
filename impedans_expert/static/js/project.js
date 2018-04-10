/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
// $('.form-group').removeClass('row');

/*
$(document).ready(function() {

});

$(document).ready(function() {
    $('.chamber-manipulate-button').click(function(el) {
        var cur_url = $(location).attr('href');
        console.log(el.target.id);
        console.log(cur_url);
        var x = cur_url.split("/chamberinfo/")[1];
        console.log(x);
        var thenum = x.replace(/^\D+/g, '');
        var num = parseInt(thenum);
        console.log(num);
        var buttonid = el.target.id;
        $.post("{% url 'chamber' chamber.id %}", {
            csrfmiddlewaretoken: '{{csrf_token}}',
            button: buttonid
        }, function(data) {
            location.reload();
        }).done();
    });
});

var update_id = 0;
var chamber_id = 0;
$(document).ready(function() {
    //if updating an object, gets the obj id
    $('.obj-select-button').click(function(el) {
        var buttonid = el.target.id;
        var thenum = buttonid.replace(/^\D+/g, '');
        var num = parseInt(thenum);
        update_id = num;
        var property_name_id = "name_" + thenum;
        var property_value_id = "value_" + thenum;
        var name = document.getElementById(property_name_id).innerText;
        var value = document.getElementById(property_value_id).innerText;
        console.log(name);
        console.log(value);
        document.getElementById("id_property_name").value = name;
        document.getElementById("id_property_value").value = value;
    });
});

$(document).ready(function() {
    //if creating an object, sets obj id to 0
    $('.new-obj-button').click(function(el) {
        button_id = el.target.id
        var thenum = button_id.replace(/^\D+/g, '');
        chamber_id = parseInt(thenum);
        update_id = 0;
        document.getElementById("id_property_name").value = "";
        document.getElementById("id_property_value").value = "";
    });
});

$(document).ready(function() {
    console.log("HERE B4P");
    //if creating a chamber property, sets obj id to 0
    $('.submit_property').click(function(el) {
        console.log("HERE PROP");
        var property_name = document.getElementById("id_property_name").value;
        var property_value = document.getElementById("id_property_value").value;
        var buttonid = el.target.id;
        $.post("{% url 'chamber' chamber.id %}", {
            csrfmiddlewaretoken: '{{csrf_token}}',
            chamber_id: chamber_id,
            button: buttonid,
            property_id: update_id,
            property_name: property_name,
            property_value: property_value
        }, function(data) {
            location.reload();
        }).done();
    });
});

$(document).ready(function() {
    //if updating a marker, gets the obj id
    $('.obj-select-button').click(function(el) {
        var buttonid = el.target.id;
        var thenum = buttonid.replace(/^\D+/g, '');
        console.log("thenum is: ", thenum);
        var num = parseInt(thenum);
        console.log("num is: ", num);
        update_id = num;
        console.log("update_id is: ", update_id);
        var marker_name_id = "name_" + thenum;
        var marker_string_id = "string_" + thenum;
        var marker_time_id = "time_" + thenum;
        var name = document.getElementById(marker_name_id).innerText;
        var m_string = document.getElementById(marker_string_id).innerText;
        var time = document.getElementById(marker_time_id).innerText;
        console.log(name);
        console.log(value);
        console.log(time);
        document.getElementById("id_marker_name").value = name;
        document.getElementById("id_marker_string").value = m_string;
        // document.getElementById("id_marker_time").value = time;
    });
});

$(document).ready(function() {
    //if creating a marker, sets marker id to 0
    $('.new-obj-button').click(function(el) {
        button_id = el.target.id
        var thenum = button_id.replace(/^\D+/g, '');
        chamber_id = parseInt(thenum);
        update_id = 0;
        document.getElementById("id_marker_name").value = "";
        document.getElementById("id_marker_string").value = "";
        // document.getElementById("id_marker_time").value = "";
    });
});

$(document).ready(function() {
    console.log("HERE B4M");
    //if creating a marker, sets obj id to 0
    $('.submit_marker').click(function(el) {
        console.log("HERE MARKER");
        var marker_name = document.getElementById("id_marker_name").value;
        var marker_string = document.getElementById("id_marker_string").value;
        var marker_time = document.getElementById("id_time_1").value;
        var marker_date = document.getElementById("id_time_0").value;
        var buttonid = el.target.id;
        $.post("{% url 'chamber' chamber.id %}", {
            csrfmiddlewaretoken: '{{csrf_token}}',
            chamber_id: chamber_id,
            button: buttonid,
            marker_id: update_id,
            marker_name: marker_name,
            marker_string: marker_string,
            time_0: marker_date,
            time_1: marker_time
        }, function(data) {
            location.reload();
        }).done();
    });
});


$(document).ready(function() {
    $('.dateinput').datepicker({
        dateFormat: "yy-mm-dd"
    });
});


$(document).ready(function() {
    $('.timeinput').timepicker({
        timeFormat: "hh:mm:ss.sss",
        interval: 5,
        dynamic: true,
        dropdown: true,
        scrollbar: true
    });
});
*/