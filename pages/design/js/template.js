/**
 * Created by Golubitskiy_AO on 11.05.2018.
 */

var templateModule ={
    getTemplateFiles: function(template_id){
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "GET",
                url: "../../template/filelist/" + session_id,
                data: {"template_id": template_id}
            }).done(function (dt) {
                resolve(dt);
            });
        })
    },

    getTemplateCode: function (template_id) {
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "GET",
                url: "../../server/templatecode/" + session_id,
                data: {"template_id": template_id}
            }).done(function (dt) {
                resolve(dt);
            });
        })         
    },
    deleteFile: function(template_id, fileName){
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../template/filelist/delete/" + session_id + "?template_id=" + template_id,
                contentType: "application/json",
                data: JSON.stringify({"file_name": fileName})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    addTemplate: function (template_name, brand_id) {
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../template/add/" + session_id + "?brand_id=" + brand_id,
                contentType: "application/json",
                data: JSON.stringify({"template_name": template_name})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    deleteTemplate: function(template_id){
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../template/delete/" + session_id,
                contentType: "application/json",
                data: JSON.stringify({"template_id": template_id})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    saveTemplate: function(template, template_code){
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../template/save/" + session_id,
                contentType: "application/json",
                data: JSON.stringify({
                    "id": template.ID,
                    "name": template.NAME,
                    "project": template.PROJECT,
                    "code": template_code
                })
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    getListOfTemplates: function() {
        let session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "GET",
                url: "../../template/" + session_id + "/user",
                data: []
            }).done(function (dt) {
                resolve(dt)
            });
        });
    },
    preview: function(template_id, data){
        let session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../server/generate/preview/" + template_id +"/" + session_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            }).done(function (dt) {
                resolve(dt);
            });
        });
    }


}
