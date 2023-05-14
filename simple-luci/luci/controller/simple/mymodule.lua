module("luci.controller.simple.mymodule", package.seeall)

function index()
	entry({"simple", "mymodule"}, template("simple/mymodule"), "My Simple Module")
	entry({"simple", "mymodule", "add"}, call("add"))
end

function add()
    local uci = require("luci.model.uci").cursor()
    local value = luci.http.formvalue("myinput")
    uci:set("myapp", "mysection", "myoption", value)
    uci:commit("myapp")
    luci.http.redirect(luci.dispatcher.build_url("simple", "mymodule"))
end
