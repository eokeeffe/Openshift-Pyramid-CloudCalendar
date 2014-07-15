<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
  <title>Cloud Calendar</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="Cloud Calendar" />
  <meta name="description" content="pyramid cloud calendar application" />

  <script src="${request.static_url('pyramidapp:static/lib/jquery.min.js')}"></script>
  <script src="${request.static_url('pyramidapp:static/lib/jquery-ui.custom.min.js')}"></script>
  <script src="${request.static_url('pyramidapp:static/fullcalendar/fullcalendar.min.js')}"></script>
  <script src="${request.static_url('pyramidapp:static/menu.js')}"></script>
  <script src="${request.static_url('pyramidapp:static/datetimepicker/jquery.datetimepicker.js')}"></script>

  <link href="${request.static_url('pyramidapp:static/fullcalendar/fullcalendar.css')}" rel='stylesheet' />
  <link href="${request.static_url('pyramidapp:static/fullcalendar/fullcalendar.print.css')}" rel='stylesheet' media='print' />

  <link rel="shortcut icon" href="${request.static_url('pyramidapp:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('pyramidapp:static/pylons.css')}" type="text/css" media="screen" charset="utf-8" />

  <link rel="stylesheet" href="${request.static_url('pyramidapp:static/menu-2.css')}" type="text/css" media="screen" charset="utf-8" />

  <link rel="stylesheet" href="${request.static_url('pyramidapp:static/datetimepicker/jquery.datetimepicker.css')}" type="text/css" media="screen" charset="utf-8" />

  <link rel="stylesheet" href="http://static.pylonsproject.org/fonts/nobile/stylesheet.css" media="screen" />
  <link rel="stylesheet" href="http://static.pylonsproject.org/fonts/neuton/stylesheet.css" media="screen" />

  <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
  <script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>

  <!--[if lte IE 6]>
  <link rel="stylesheet" href="${request.static_url('pyramidapp:static/ie6.css')}" type="text/css" media="screen" charset="utf-8" />
  <![endif]-->

<style>
  body {
    margin-top: 40px;
    text-align: center;
    font-size: 14px;
    font-family: "Lucida Grande",Helvetica,Arial,Verdana,sans-serif;
    }

  #calendar {
    width: 900px;
    margin: 0 auto;
    }
</style>

</head>
<body>
<%
from pyramid.security import authenticated_userid
user_id = authenticated_userid(request)
%>

<div id="wrap">
    % if user_id == None:
      <div id="top">
        <div class="top align-center">
          <div><img src="${request.static_url('pyramidapp:static/pyramid.png')}" width="750" height="169" alt="pyramid"/></div>
        </div>
      </div>
    
    <div id="middle">
      <div class="middle align-center">
        <p class="app-welcome">
          Welcome to <span class="app-name">Cloud Calendar</span>, an application create using<br/>
          the Pyramid web application development framework.
        </p>
      </div>
    </div>
    % endif
    <div id="bottom" style="padding-bottom:50px;">
      <div class="bottom">

        % for m in request.session.pop_flash():
        <p>${m}</p>
        % endfor

        ${next.body()}
      </div>
    </div>
  </div>
  <div id="footer">
    <div class="footer">Created By <a href="https://plus.google.com/u/0/+EvanOKeeffe/posts">Evan O'Keeffe</a></div>
  </div>
</body>
</html>
