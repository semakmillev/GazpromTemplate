String.prototype.replaceAll = function (target, replacement) {
    return this.split(target).join(replacement);
};

var app = new Vue({
    el: '#app',
    data: {
        sql: "",
        requestResult: [],
        requestHeader: []
    },
    methods: {
        spin: function(){
            NProgress.start();
        },
        executeScript: function(){
            let main = this;
            let session_id = localStorage.getItem("session_id");
            main.requestResult = [];
            main.requestHeader = [];
            $.ajax({
                type: "POST",
                url: "../../dbbrowser/" + session_id,
                contentType: "application/json",
                data: JSON.stringify({"sql": main.sql})
            }).done(function (dt) {
                if (main.sql.toLowerCase().indexOf("update") > -1 || main.sql.toLowerCase().indexOf("insert") > - 1)
                {
                    alert("Succeed!");
                }else{
                    console.log(dt[0]);
                    main.requestHeader = Object.keys(dt[0]);
                    console.log(main.requestHeader);


                    Object.values(dt[0]);
                    dt.forEach(function(row){
                        main.requestResult.push(main.requestHeader.map(function(v) { return row[v]; }));
                    });
                    //main.requestResult = JSON.parse(dt);
                    console.log(main.requestResult );
                }

            }).fail(function (err) {
                alert(err.responseText);
                // alert(err);
            });
        }

    },
    mounted: function () {

    }
});
