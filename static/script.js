M.AutoInit()

function internal() {
  $("#external").hide();

  $("#form_type").attr("value", "internal");
}

function external() {
  $("#external").show();

  $("#form_type").attr("value", "external");
}
