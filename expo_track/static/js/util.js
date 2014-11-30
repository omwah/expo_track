var json_request = function(uri, method, data) {
    var request = $.ajax({ url: uri,
                           type: method,
                           contentType: "application/json",
                           accepts: "application/json",
                           cache: false,
                           dataType: "json",
                           data: ko.toJSON(data),
                         });
    return request;
}
