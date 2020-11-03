M.AutoInit()

function internal() {
  $("#external").hide();

  $("form_type").val("internal");
}

function external() {
  $("#external").show();

  $("form_type").val("external");
}
