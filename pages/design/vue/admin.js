String.prototype.replaceAll = function (target, replacement) {
    return this.split(target).join(replacement);
};

var app = new Vue({
    el: '#app',
    data: {
        companies: [],
        brands: [],
        templates: [],
        companyBrands: [],
        showArchiveBrands: false,
        brandTemplates: [],
        selectedCompany: "",
        selectedBrand: "",
        selectedTemplate: "",
        newBrandName: "",
        newTemplateName: "",
        template_code: "\n\n",
        templateFiles: [],
        confirmation: {title: "", text: "", result: false},
        updloadingFiles: []
    },
    methods: {
        yesNoConfirm: function (title, text) {
            var main = this;
            this.confirmation.title = title;
            this.confirmation.text = text;
            $("#confirmationModal").modal();
            return new Promise(function (resolve) {
                $("#confirmationModal").on("hidden.bs.modal", function () {
                    console.log(main.confirmation.result);
                    resolve(main.confirmation.result);
                });
            })


        },

        confirmationResult: function (res) {
            this.confirmation.result = res;
            $("#confirmationModal").modal("hide");
        },
        test: function () {
            this.yesNoConfirm("test", "test")
                .then(function (res) {
                    alert(res);
                });
        },
        refreshCompanyBrands: function () {
            var main = this;
            main.companyBrands = main.brands.filter(brand => (brand["COMPANY_ID"] == main.selectedCompany.ID)
            )
            ;
            //return main.brands.filter(main.brand => (brand['COMPANY_ID'] == main.selectedCompany.ID)
            //);
        },
        refreshBrandTemplates: function () {
            var main = this;
            this.brandTemplates = this.templates.filter(template => (template["BRAND_ID"] == main.selectedBrand.ID)
            )
            ;
        },
        companyInfo: function (company) {
            this.selectedCompany = company;
            this.refreshCompanyBrands();
            $("#companyInfoModal").modal('show');
        },

        brandInfo: function (brand) {
            this.selectedBrand = brand;
            this.refreshBrandTemplates();
            $("#brandInfoModal").modal('show');
        },
        addBrand: function () {
            var session_id = localStorage.getItem("session_id");
            var main = this;
            var shArchivedBrands = 0;
            if (this.showArchiveBrands) shArchivedBrands = 1;
            brandModule.addBrand(this.selectedCompany.ID, this.newBrandName, shArchivedBrands)
                .then(function (dt) {
                    main.brands = dt['brands'];
                    main.newBrandName = "";
                    // main.companyBrands = main.brands.filter(brand => (brand["COMPANY_ID"] == main.selectedCompany.ID))
                });

        },
        deleteBrand: function (brand) {
            var main = this;
            var shArchivedBrands = 0;
            if (this.showArchiveBrands) shArchivedBrands = 1;
            brandModule.deleteBrand(this.selectedCompany.ID, brand.ID, shArchivedBrands)
                .then(function (dt) {
                    main.brands = dt['brands'];
                    main.companyInfo(main.selectedCompany);
                    // main.companyBrands = main.brands.filter(brand => (brand["COMPANY_ID"] == company.ID))
                });
        },
        //
        //  ------------------------------РАБОТАЕМ С ШАБЛОНОМ!!!
        cutFileName: function (file) {
            var returnFileName = "";
            if (file.length > 20) {
                return file.substr(0, 18) + "...";
            } else {
                return file;
            }
        },
        deleteFile: function (file) {
            var main = this;
            this.yesNoConfirm("Удаление файла", "Удалить файл " + file + "?")
                .then(function (res) {
                    if (res) {
                        templateModule.deleteFile(main.selectedTemplate.ID, file)
                            .then(function (res) {
                                main.templateFiles = res['files'];
                            });
                    } else {
                        console.log("Отмена...");
                    }
                })

        },
        templateInfo: function (template) {
            var main = this;
            main.selectedTemplate = template;
            templateModule.getTemplateCode(main.selectedTemplate.ID)
                .then(function (res) {
                    main.template_code = res;
                    return templateModule.getTemplateFiles(main.selectedTemplate.ID);
                })
                .then(function (res) {
                    console.log(res);
                    main.templateFiles = res['files'];
                    var padding = parseInt($("#templateCodeElement").css("padding-top")) + 1;
                    $("#fileListElement").height(24 * 20 + padding * 2);
                    $('#templateInfoModal').modal('show');
                    //$("#fileListElement").height(height);
                });

        },

        addTemplate: function () {
            var main = this;
            templateModule.addTemplate(this.newTemplateName, this.selectedBrand.ID)
                .then(function(dt){
                    console.log(dt);
                    main.templates = dt['templates'];
                    main.refreshBrandTemplates();
                });
        },
        deleteTemplate: function (template) {
            var main = this;
            main.yesNoConfirm("Удаление шаблона", "Вы уверены, что хотите удалить шаблон? Все файлы и текст шаблона будут удалены.")
                .then(function (res) {
                    if (res) {
                        templateModule.deleteTemplate(template.ID).then(function (dt) {
                            main.templates = dt["templates"];
                            main.refreshBrandTemplates();
                        });
                    }
                });
        },
        upload: function () {
            var main = this;
            //var arr = {1:1,2:2};
            var chain = Promise.resolve();
            var steps = -1;
            var session_id = localStorage.getItem("session_id");
            //console.log(this.files)
            new Promise(function (resolve) {
                for (var x = 0; x < main.updloadingFiles.length; x++) {
                    //var files = main.files;
                    chain = chain.then(function () {
                        return new Promise(function (res) {
                            steps++;
                            var formData = new FormData();
                            formData.append("file", main.updloadingFiles[steps])
                            $.ajax({
                                type: "POST",
                                url: "../../server/upload/" + session_id + "?template_id=" + main.selectedTemplate.ID,
                                //contentType: "text",
                                //dataType: "text",
                                data: formData,
                                processData: false,  // tell jQuery not to process the data
                                contentType: false  // tell jQuery not to set contentType
                            }).done(function () {
                                res("SUCCESS");
                                if (steps == main.updloadingFiles.length - 1) {
                                    resolve("SUCCESS")
                                }
                            }).fail(function (err) {
                                console.error(err);
                                res("ERR");
                            });

                        })

                    });
                }
            }).then(function (res) {
                main.updloadingFiles = [];
                return templateModule.getTemplateFiles(main.selectedTemplate.ID)
            }).then(function (res) {
                main.templateFiles = res['files'];
            })

            ;
        },

        onFileChange: function (e) {
            this.updloadingFiles = e.target.files || e.dataTransfer.files;
            if (!this.updloadingFiles.length)
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


    },
    mounted: function () {
        var main = this;
        var session_id = localStorage.getItem("session_id");
        console.log(session_id);
        var main = this;
        $.ajax({
            type: "GET",
            url: "../../company/" + session_id + "/admin",
            data: []
        }).done(function (dt) {
            console.log(dt);
            main.companies = dt['companies'];
        });

        $.ajax({
            type: "GET",
            url: "../../template/" + session_id + "/admin",
            data: []
        }).done(function (dt) {
            console.log(dt);
            main.templates = dt['templates'];
        });
        var shArchivedBrands = 0;
        if (this.showArchiveBrands) shArchivedBrands = 1;
        brandModule.getListOfBrands("admin", shArchivedBrands)
            .then(function (dt) {
                main.brands = dt['brands'];
            });


    }
})
