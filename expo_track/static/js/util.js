var json_request = function(uri, method, data) {
    // For GET calls can not use json as content type or else
    // magic quotes start being introduced messing up the query
    // Don't JSONify the data sent to $.ajax either
    var content_type;
    var send_data;
    if(method.toLowerCase() == "get") {
        // Default value
        content_type = "application/x-www-form-urlencoded; charset=UTF-8";
        send_data = data;
    } else {
        content_type = "application/json";
        send_data = ko.toJSON(data);
    }
    var request = $.ajax({ url: uri,
                           type: method,
                           contentType: content_type,
                           accepts: "application/json",
                           cache: false,
                           dataType: "json",
                           data: send_data,
                           // Make sure data is urlencoded correctly and not just serialized
                           traditional: true,
                         });
    return request;
}
