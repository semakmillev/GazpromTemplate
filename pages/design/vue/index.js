String.prototype.replaceAll = function (target, replacement) {
    return this.split(target).join(replacement);
};

var main = this;
var app = new Vue({
    el: '#app',
    data: {
        items: [], //[{id: 1, name: 'semak'}, {id: 2, name: 'ter'}],
        selectedTemplate: "",
        loginEmail: "",
        loginPassword: "",
        registerEmail: "",
        registerPassword: "",
        repeatRegisterPassword: "",
        template_height: 500,
        template_width: 1000,
        template_code: "",
        format: "JPEG",
        verifyCode: "",
        verifyEmail: "",
        verificationCode: "",
        dpi: 96,
        files: {}
    },
    methods: {
        click: function (text) {
            console.log(text);
            this.selectedTemplate = text;
            //model.message = 'New value';
        },
        upload: function () {
            var main = this;
            //var arr = {1:1,2:2};
            var chain = Promise.resolve();
            var steps = -1;
            //console.log(this.files)
            new Promise(function (resolve) {
                for (var x = 0; x < main.files.length; x++) {
                    //var files = main.files;
                    chain = chain.then(function () {
                        return new Promise(function (res) {
                            steps++;
                            var formData = new FormData();
                            formData.append("file", main.files[steps])
                            $.ajax({
                                type: "POST",
                                url: "../../server/upload/" + main.selectedTemplate,
                                //contentType: "text",
                                //dataType: "text",
                                data: formData,
                                processData: false,  // tell jQuery not to process the data
                                contentType: false  // tell jQuery not to set contentType
                            }).done(function () {
                                res("SUCCESS");
                                if (steps == main.files.length - 1) {
                                    resolve("SUCCESS")
                                }
                            }).fail(function (err) {
                                console.error(err);
                                res("ERR");
                            });

                        })

                    });
                }
            }).then(function () {
                main.files = [];
            });
        },

        onFileChange: function (e) {
            this.files = e.target.files || e.dataTransfer.files;
            if (!this.files.length)
                return;
            //this.createImage(files[0]);
        }
        ,
        saveTemplate: function () {
            var code = this.template_code;
            console.log(code);
            $.ajax({
                type: "POST",
                url: "../../server/templatecode/" + this.selectedTemplate,
                contentType: "text",
                dataType: "text",
                data: code
            }).done(function (dt) {
                $('#myModal').modal('hide');
            });


        }
        ,
        editCode: function () {
            var main = this;
            console.log(this.selectedTemplate);
            $.ajax({
                type: "GET",
                url: "../../server/templatecode/" + this.selectedTemplate,
                data: []
            }).done(function (dt) {
                main.template_code = dt;
                console.log(dt);
                $('#myModal').modal('show');
            });


        },

        openLogin: function () {
            $('#loginModal').modal({backdrop: 'static', keyboard: false}); //modal('show',{data-keyboard="false"});
        },

        gotoDB: function () {
            this.$route.push("/admin.html");
            //window.location.href = 'db.html';
        },
        login: function(){
            var main = this;
            var email = main.loginEmail;
            var password = sha256.hex(main.loginPassword);
            console.log(password);
            var regPromise = new Promise(function (resolve, reject) {
                $.ajax({
                    type: "POST",
                    url: "../../login",
                    //contentType: "text",
                    //dataType: "text",
                    data: JSON.stringify({
                        "email": email,
                        "password": password
                    }),
                    contentType: "application/json"
                }).done(function (res) {
                    console.log(res);
                    localStorage.setItem("session_id", res["session_id"]);
                    location.reload();
                }).fail(function () {
                    reject("ERR");
                });

            });
        },
        register: function () {
            var main = this;
            if (this.registerPassword == this.repeatRegisterPassword) {
                var regPromise = new Promise(function (resolve, reject) {
                    $.ajax({
                        type: "POST",
                        url: "../../register",
                        //contentType: "text",
                        //dataType: "text",
                        data: JSON.stringify({
                            "email": main.registerEmail,
                            "password": sha256.hex(main.registerPassword)
                        }),
                        contentType: "application/json"
                    }).done(function (res) {
                        console.log(res);
                        var result = res;
                        if (result["verified"] == "0") {
                            localStorage.setItem("session2verify", result["session_id"]);
                            main.verifyEmail = main.registerEmail;
                            $('[href="#verifyPanel"]').tab('show');

                        }

                    }).fail(function () {
                        reject("ERR");
                    });

                });
                /*
                 var passhash = sha256.hex(this.registerPassword);
                 $('[href="#verifyPanel"]').tab('show');
                 /// this.openVerify();
                 */

            }

        },
        verify: function () {
            var session_id = localStorage.getItem("session2verify");
            console.log(localStorage.getItem("session2verify"));
            var main = this;
            var regPromise = new Promise(function (resolve, reject) {
                $.ajax({
                    type: "POST",
                    url: "../../verify",
                    //contentType: "text",
                    //dataType: "text",
                    data: JSON.stringify({"email": main.verifyEmail, "code": main.verificationCode}),
                    contentType: "application/json"
                }).done(function (res) {
                    //console.log(res);
                    if (res["result"] == "OK") {
                        localStorage.setItem("session_id", session_id);
                        // $('#loginModal').modal("toggle");
                        location.reload();
                    }
                }).fail(function (err) {
                    console.log(err);
                    reject("ERR");
                });

            });
        },
        downloadTemplate: function () {
            var main = this;
            console.log(this.selectedTemplate);
            console.log(this.template_width);
            console.log(this.template_height);
            console.log(this.format);
            var extension = this.format.replace("JPEG", "JPG").toLowerCase();
            var request_data = {
                "width": this.template_width,
                "height": this.template_height,
                "format": this.format,
                "dpi": this.dpi
            };
            var http = new XMLHttpRequest();
            http.open('POST', "../../server/" + this.selectedTemplate, true);
            http.setRequestHeader("Content-type", "application/json; charset=utf-8");
            http.setRequestHeader("Content-length", request_data.length);
            http.setRequestHeader("Connection", "close");
            http.responseType = "blob";
            http.onload = function () {
                if (this.status === 200) {
                    var filename = main.selectedTemplate + "_" + main.template_width + "x" + main.template_height + "." + extension;
                    var disposition = http.getResponseHeader('Content-Disposition');
                    if (disposition && disposition.indexOf('attachment') !== -1) {
                        var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        var matches = filenameRegex.exec(disposition);
                        if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                    }
                    var type = http.getResponseHeader('Content-Type');
                    var blob = typeof File === 'function'
                        ? new File([this.response], filename, {type: type})
                        : new Blob([this.response], {type: type});
                    if (typeof window.navigator.msSaveBlob !== 'undefined') {
                        // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                        window.navigator.msSaveBlob(blob, filename);
                    } else {
                        var URL = window.URL || window.webkitURL;
                        var downloadUrl = URL.createObjectURL(blob);

                        if (filename) {
                            // use HTML5 a[download] attribute to specify filename
                            var a = document.createElement("a");
                            // safari doesn't support this yet
                            if (typeof a.download === 'undefined') {
                                window.location = downloadUrl;
                            } else {
                                a.href = downloadUrl;
                                a.download = filename;
                                document.body.appendChild(a);
                                a.click();
                            }
                        } else {
                            window.location = downloadUrl;
                        }

                        setTimeout(function () {
                            URL.revokeObjectURL(downloadUrl);
                        }, 100); // cleanup
                    }
                }
            };
            //http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            http.onreadystatechange = function () {

            };
            http.send(JSON.stringify(request_data));

            /*
             $.ajax({
             type: "post",
             url: ,
             contentType: "application/json; charset=utf-8",
             dataType: "json",
             data: JSON.stringify(request_data)
             });*/
        },
        get_email_inviation: function(invitation_id){
          return new Promise(function(resolve){
              $.ajax({
                  type: "GET",
                  url: "../../server/invitation/" + invitation_id,
                  data: {}
              }).done(function (dt) {
                  resolve(dt);
              });
          });
        },
        logout: function () {
            localStorage.removeItem("session_id");
            location.reload();
        }
    },

    mounted: function () {

        console.log("session:" + localStorage.getItem("session_id"));

        if (localStorage.getItem("session_id") == null || localStorage.getItem("session_id") == "null") {
            let main = this;
            let uri = window.location.search.substring(1);
            let params = new URLSearchParams(uri);
            let invitation = params.get("invitation");
            if(invitation != null){
                main.get_email_inviation(invitation)
                    .then(function(res) {
                        main.registerEmail = res;
                        main.loginEmail = res;
                        main.openLogin();
                    })
                ;
            }else{
                this.openLogin();
            }
            return;
        }

        var session_id = localStorage.getItem("session_id");
        var main = this;
        $.ajax({
            type: "GET",
            url: "../../server/templatelist/" + session_id,
            data: []
        }).done(function (dt) {
            main.items = dt;
        });

    }
})