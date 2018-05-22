String.prototype.replaceAll = function (target, replacement) {
    return this.split(target).join(replacement);
};

var main = this;
var app = new Vue({
    el: '#app',
    data: {
        items: [], //[{id: 1, name: 'semak'}, {id: 2, name: 'ter'}],
        // imgs: ["1.jpg","2.jpg","6.jpg","3.jpg","4.jpg","5.jpg",],
        imgs: [],
        templates: [],
        previewImg: "",
        selectedTemplate: "",
        selectedTemplateId : "",
        selectedBrand: "",
        selectedProject: "",
        loginEmail: "",
        loginPassword: "",
        registerEmail: "",
        brands: [],
        projects: [],
        registerPassword: "",
        repeatRegisterPassword: "",
        template_height: 500,
        template_width: 1000,
        template_code: "",
        format: "JPEG",
        verifyCode: "",
        verifyEmail: "",
        verificationCode: "",
        dpi: "",
        files: {}
    },
    methods: {
        showTemplates: function () {

            console.log(this.selectedBrand.ID);
            let session_id = localStorage.getItem("session_id");
            let main = this;
            let brandTemplates = main.templates.filter(template => (template["BRAND_ID"] == main.selectedBrand.ID));
            console.log(brandTemplates);
            main.projects = $.unique(brandTemplates.map(function (t) {
                return t.PROJECT;
            }));
            if (this.selectedProject != "") {
                brandTemplates = brandTemplates.filter(template => (template["PROJECT"] == main.selectedProject));
            }
            this.imgs = brandTemplates.map(function (t) {
                return {ID: t.ID, NAME: t.NAME, PATH: "../../server/preview/" + t.ID + "/" + session_id}
            });

        },
        selectTemplate: function(template){
            console.log(template);
            this.selectedTemplate = template.NAME;
            this.selectedTemplateId = template.ID;
            //this.selectedTemplate.NAME = template.NAME;
            //this.selectedTemplate.ID = template.ID;
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
        preview: function(){
            let main = this;
            let request_data = {
                "width": this.template_width,
                "height": this.template_height,
                "format": this.format,
                "dpi": this.dpi
            };
            main.previewImg = "";
            let modalHeight = this.template_height *(640/this.template_width);
            let modalWidth = 640;

            templateModule.preview(this.selectedTemplateId, request_data)
                .then(function(res){
                    main.previewImg = res;
                    $('#previewModal .modal-content').css('width', modalWidth);
                    $('#previewModal .modal-content').css('height', modalHeight);
                    $('#previewModal').modal('show');
            });
        },
        downloadTemplate: function () {
            let main = this;
            console.log(this.selectedTemplateId);
            console.log(this.template_width);
            console.log(this.template_height);
            console.log(this.format);
            console.log(this.dpi);
            let session_id = localStorage.getItem("session_id");
            let extension = this.format.replace("JPEG", "JPG").toLowerCase();
            let request_data = {
                "width": this.template_width,
                "height": this.template_height,
                "format": this.format,
                "dpi": this.dpi
            };
            let http = new XMLHttpRequest();
            http.open('POST', "../../server/generate/" + this.selectedTemplateId+"/"+session_id, true);
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
        let main = this;
        console.log("session:" + localStorage.getItem("session_id"));
        templateModule.getListOfTemplates()
            .then(function(dt){
                main.templates = dt["templates"];
                main.brands = $.unique(main.templates.map(function (b) {return {'ID': b.BRAND_ID, 'NAME': b.BRAND_NAME};}));
            });
        /*
        brandModule.getListOfBrands("user", false)
            .then(function (dt) {
                main.brands = dt['brands'];
            });
        */
        if (localStorage.getItem("session_id") == null || localStorage.getItem("session_id") == "null") {
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
        $.ajax({
            type: "GET",
            url: "../../server/templatelist/" + session_id,
            data: []
        }).done(function (dt) {
            main.items = dt;
        });

    }
})