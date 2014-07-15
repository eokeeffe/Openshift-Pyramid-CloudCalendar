<%inherit file="pyramidapp:templates/layout.mak"/>

<form action="${request.route_url('revoke_calendar',action=action)}" method="post">
%if action =='edit':
${form.id()}
%endif

% for error in form.name.errors:
    <div class="error">${ error }</div>
% endfor

<div><label>${form.name.label}</label>${form.name()}</div>

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