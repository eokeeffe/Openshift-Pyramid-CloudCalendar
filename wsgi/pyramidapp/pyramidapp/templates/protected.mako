<!DOCTYPE html>
<html>
<head>
    <title>Cloud Calendar</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <meta name="keywords" content="Cloud Calendar" />
    <meta name="description" content="pyramid cloud calendar application" />

    <script src="${request.static_url('pyramidapp:static/lib/jquery.min.js')}"></script>
    <script src="${request.static_url('pyramidapp:static/lib/jquery-ui.custom.min.js')}"></script>
    <script src="${request.static_url('pyramidapp:static/fullcalendar/fullcalendar.min.js')}"></script>

    <link href="${request.static_url('pyramidapp:static/fullcalendar/fullcalendar.css')}" rel='stylesheet' />
    <link href="${request.static_url('pyramidapp:static/fullcalendar/fullcalendar.print.css')}" rel='stylesheet' media='print' />

    <script>
    $(document).ready(function() {
    
        var date = new Date();
        var d = date.getDate();
        var m = date.getMonth();
        var y = date.getFullYear();
        
        $('#calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaWeek,agendaDay'
            },
            editable: true,
            events: [
                {
                    title: 'All Day Event',
                    start: new Date(y, m, 1)
                },
                {
                    title: 'Long Event',
                    start: new Date(y, m, d-5),
                    end: new Date(y, m, d-2)
                },
                {
                    id: 999,
                    title: 'Repeating Event',
                    start: new Date(y, m, d-3, 16, 0),
                    allDay: false
                },
                {
                    id: 999,
                    title: 'Repeating Event',
                    start: new Date(y, m, d+4, 16, 0),
                    allDay: false
                },
                {
                    title: 'Meeting',
                    start: new Date(y, m, d, 10, 30),
                    allDay: false
                },
                {
                    title: 'Lunch',
                    start: new Date(y, m, d, 12, 0),
                    end: new Date(y, m, d, 14, 0),
                    allDay: false
                },
                {
                    title: 'Birthday Party',
                    start: new Date(y, m, d+1, 19, 0),
                    end: new Date(y, m, d+1, 22, 30),
                    allDay: false
                },
                {
                    title: 'Click for Google',
                    start: new Date(y, m, 28),
                    end: new Date(y, m, 29),
                    url: 'http://google.com/'
                }
            ]
        }); 
    });
    </script>

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
    
    <div class="bottom">
    % for m in request.session.pop_flash():
    <p>${m}</p>
    % endfor

    ${next.body()}
    </div>

  <div id="footer">
    <div class="footer">Created By <a href="https://plus.google.com/u/0/+EvanOKeeffe/posts">Evan O'Keeffe</a></div>
  </div>
</body>
</html>