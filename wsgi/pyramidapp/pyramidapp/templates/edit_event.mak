<%inherit file="pyramidapp:templates/layout.mak"/>

<script>
  $(function() {
    //$("#${form.start.id}").datepicker({ dateFormat: "dd-mm-yy" });
    //$("#${form.end.id}").datepicker({ dateFormat: "dd-mm-yy" });
    $("#${form.start.id}").datetimepicker({ format:'d-m-Y H:i:s' });
    $("#${form.end.id}").datetimepicker({ format:'d-m-Y H:i:s' });
  });
</script>

<h2>UPDATING EVENT</h2>

<form action="${request.route_url('edit_event',id=id,action=action)}" method="post">
%if action =='edit':
${form.id()}
%endif

% for error in form.title.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.title.label}</label>${form.title()}</div>

% for error in form.description.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.description.label}</label>${form.description()}</div>

% for error in form.start.errors:
<div class="error">${error}</div>
% endfor

<div><label>${form.start.label}</label>${form.start()}</div>

% for error in form.end.errors:
<div class="error">${error}</div>
% endfor

<div><label>${form.end.label}</label>${form.end()}</div>

% for error in form.allDay.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.allDay.label}</label>${form.allDay()}</div>

% for error in form.url.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.url.label}</label>${form.url()}</div>

<div><input type="submit" value="Submit"></div>
</form>
<p><a href="${request.route_url('home')}">Go Back</a></p>

<style type="text/css">
form{
    text-align: right;
}
label{
    min-width: 150px;
    vertical-align: top;
    text-align: right;
    display: inline-block;
}
input[type=text]{
    min-width: 505px;
}
textarea{
    color: #222;
    border: 1px solid #CCC;
    font-family: sans-serif;
    font-size: 12px;
    line-height: 16px;
    min-width: 505px;
    min-height: 100px;
}
.error{
    font-weight: bold;
    color: red;
}
</style>