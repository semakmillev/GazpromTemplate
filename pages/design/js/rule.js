/**
 * Created by Golubitskiy_AO on 18.05.2018.
 */
var ruleModule = {
    deleteRule: function (rule_id, source, item_id) {
        var session_id = localStorage.getItem("session_id");
        return new Promise(function (resolve, reject) {
            $.ajax({
                type: "POST",
                url: "../../rules/delete/" + source + "/"+ session_id +"?item_id=" + item_id,
                contentType: "application/json",
                data: JSON.stringify({"rule_id": rule_id})
            }).done(function (dt) {
                resolve(dt);
            });
        });
    }
}
