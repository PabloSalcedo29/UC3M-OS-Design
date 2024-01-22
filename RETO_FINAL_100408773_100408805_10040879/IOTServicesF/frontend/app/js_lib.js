/*
 * Javascript file to implement client side usability for 
 * Operating Systems Desing exercises.
 */
var api_server_address = "http://34.159.168.7:5001/"

var get_current_sensor_data = function(){
   $.getJSON(api_server_address + "device_state", function( data ) {
       $.each(data, function(index, item) {
         $("#"+item.room).data(item.type, item.value)
     });
   });
}

var draw_rooms = function(){
   $("#rooms").empty()
   var room_index = 1;
   for (var i = 0; i < 8; i++) {
       $("#rooms").append("<tr id='floor"+i+"'></tr>")
       for (var j = 0; j < 5; j++) {
           $("#floor"+i).append("\
               <td \
               data-bs-toggle='modal' \
               data-bs-target='#room_modal' \
               class='room_cell'\
               id='Room"+room_index+"'\
               > \
               Room "+room_index+"\
               </td>"
               )
           room_index++
       }
   }
}

$("#air_conditioner_mode").change(function(){
   var value = $(this).val()
   $.ajax({
       type: "POST",
       url: api_server_address+"device_command",
       data: JSON.stringify({
           "room":$("#room_id").text(),
           "type":"air-mode",
           "value":value,
       }),
       contentType: 'application/json'
   });
})


$("#in_light_mode").change(function(){
    var value = $(this).val()
    $.ajax({
        type: "POST",
        url: api_server_address+"device_command",
        data: JSON.stringify({
            "room":$("#room_id").text(),
            "type":"in-light-mode",
            "value":value,
        }),
        contentType: 'application/json'
    });
 })

 $("#out_light_mode").change(function(){
    var value = $(this).val()
    $.ajax({
        type: "POST",
        url: api_server_address+"device_command",
        data: JSON.stringify({
            "room":$("#room_id").text(),
            "type":"out-light-mode",
            "value":value,
        }),
        contentType: 'application/json'
    });
 })

 $("#blind_mode").change(function(){
    var value = $(this).val()
    $.ajax({
        type: "POST",
        url: api_server_address+"device_command",
        data: JSON.stringify({
            "room":$("#room_id").text(),
            "type":"blind-mode",
            "value":value,
        }),
        contentType: 'application/json'
    });
 })

$("#rooms").on("click", "td", function() {
   $("#room_id").text($( this ).attr("id") || "");
   $("#temperature_value").text($( this ).data("temperature") || "");
   $("#in_light_value").text($( this ).data("in-light-level") || "");
   $("#in_light_mode").val($( this ).data("in-light-mode"));
   $("#out_light_value").text($( this ).data("out-light-level") || "");
   $("#out_light_mode").val($( this ).data("out-light-mode"));
   $("#blind_value").text($( this ).data("blind-level") || "");
   $("#blind_mode").val($( this ).data("blind-mode"));
   $("#presence_value").text($( this ).data("presence") || "0");
   $("#air_conditioner_value").text($( this ).data("air-level") || "");
   $("#air_conditioner_mode").val($( this ).data("air-mode"));
});

draw_rooms()
setInterval(get_current_sensor_data,2000)
