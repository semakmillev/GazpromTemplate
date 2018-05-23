/**
 * Created by Golubitskiy_AO on 11.05.2018.
 */

var brandModule = {

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
    addBrand: function (companyId, brandName, archived) {
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../brand/add/" + session_id + "?company_id=" + companyId+"&archived="+archived,
                contentType: "application/json",
                data: JSON.stringify({"brand_name": brandName})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    saveBrand: function (brandId, brandName, archived){
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../brand/save/" + session_id + "?archived="+archived,
                contentType: "application/json",
                data: JSON.stringify({"brand_id": brandId, "brand_name":brandName})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    deleteBrand: function (companyId, brandId, archived) {
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../brand/delete/" + session_id + "?company_id=" + companyId+"&archived="+archived,
                contentType: "application/json",
                data: JSON.stringify({"brand_id": brandId})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    },
    getListOfBrands: function (role, archived) {
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve) {
            $.ajax({
                type: "GET",
                url: "../../brand/" + session_id + "/" + role + "?archived=" + archived,
                data: []
            }).done(function (dt) {
                console.log(dt);
                resolve(dt);
            });
        });


    },
    getRuleUsers: function(brand_id){
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve) {
            $.ajax({
                type: "GET",
                url: "../../rules/brand/list/" + session_id + "?brand_id=" + brand_id,
                data: []
            }).done(function (dt) {
                console.log(dt);
                resolve(dt);
            });
        });
        
    }
}

