$( document ).ready(function() {
    var ajax = function(uri, method, data) {
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

    function LoginViewModel() {
        var self = this;
        self.username = ko.observable();
        self.password = ko.observable();

        self.login = function(data) {
            var login_uri = $("#login-view form")[0].action;
            ajax(login_uri, "POST", data).done(function(ret_data) {
                console.log(ret_data);
            });
        }
    }
    var loginViewModel = new LoginViewModel();
    ko.applyBindings(loginViewModel, $('#login-view')[0]);
});
