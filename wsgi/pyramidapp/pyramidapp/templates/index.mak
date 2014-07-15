<%inherit file="pyramidapp:templates/layout.mak"/>

<%
from pyramid.security import authenticated_userid 
user_id = authenticated_userid(request)
%>

% if user_id != None:
    Welcome <strong>${user_id}</strong> 
    
    <div id="sse3">
        <div id="sses3">
            <ul>
                <li>
                    <a href="${request.route_url('auth',action='out')}">Sign Out</a>
                </li>
                <li>
                    <a href="${request.route_url('create_event',action='create')}">Create a new Event</a>
                </li>
                <li>
                    <a href="${request.route_url('search',action='create')}">Find an Event</a>
                </li>
                <li>
                    <a href="${request.route_url('sharing',action='create')}">Share your calendar</a>
                </li>
            </ul>
        </div>
    </div>
    
    <div id="eventContent" title="Event Details">
        <div id="eventInfo"></div>
        <div id="eventStart"></div>
        <div id="eventEnd"></div>
        <div id="eventURL"></div>
        <p>
            <strong>
                <a id="eventLink" target="_blank"></a>
            </strong>
        </p>
        <div class="message"></div>
    </div>

    <div id='calendar'></div>

    <script>
        function get_dates(){
            jevents = new Array();

            $.getJSON('/dates', function(data) 
            {
                $.each(data, function (key, data) 
                {
                    var web = data.url;

                    var urlCheck = /(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;

                    if(web){
                        if(urlCheck.test(web) === false) 
                        {
                            web = "http://" + web;
                        }
                    }

                    e = {
                        title:  data.title,
                        description:    data.description,
                        start: new Date(data.start),
                        allDay : data.allDay,
                        end: new Date(data.end),
                        url: web,
                        id : data.id
                    }

                    if(!data.description){
                        e.description = '';
                    }
                    if(!data.end){
                        e.end = new Date(data.end);
                    }
                    if(!data.url){
                        e.url = '';
                    }
                    
                    console.log(e);
                    $('#calendar').fullCalendar('renderEvent', e );
                });
            });
        }

        function load_page(){
            //get_dates();
        }

    $( window ).load(load_page());

    function openModal(id,title, info, start, end, url){
        $("#eventInfo").html("Description:"+info);
        $("#eventStart").html("Start:"+start);
        $("#eventEnd").html("End:"+end);
        $("#eventURL").html("URL:"+url);
        $("#eventContent").dialog({ modal: true, 
            title: 'Event Name:'+title,
            text :'text',
            buttons: {
                Edit: function () {
                    /*
                    $.ajax({
                        type:"POST",
                        url:"/edit",
                        data:{
                            'id':id
                        },
                        success:function(result){
                            $( "#eventContent" ).dialog( "close" );
                        }
                    });
                    */
                    window.location = "/edit_event/"+id;

                },
                Cancel: function () {
                    $( this ).dialog( "close" );
                },
                Remove: function () {
                    $.ajax({
                        type:"POST",
                        url:"/remove",
                        data:{
                            't':title,
                            'd':info,
                            's':start,
                            'e':end,
                            'du':url
                        },
                        success:function(result){
                            $( "#eventContent" ).dialog( "close" );
                            window.location = "/";
                        }
                    });
                }
            },
            close: function (event, ui) {
                $( this ).dialog( "close" );
            }
        });
    }

    $(document).ready(function() {

        $('#calendar').fullCalendar({
                url: '/dates',
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay'
                },
                editable: false,
                events : '/dates',
                eventRender:function(event, element){
                    var url = event.url;
                    element.attr('href', 'javascript:void(0);');
                    element.attr('onclick', 'openModal("'
                    + event.id
                    + '","'
                    + event.title 
                    + '","'
                    + event.description 
                    + '","'
                    + event.start
                    + '","'
                    + event.end
                    + '","' 
                    + url
                    + '");');
                },
                dayClick:function(date, allDay, jsEvent, view)
                {
                    //alert(date);
                },
                eventClick:function(event, jsEvent, view)
                {
                    //alert(event);
                },
                eventMouseout:function(event, jsEvent, view)
                {
                    //alert(event);
                },
                eventMouseover:function(event, jsEvent, view)
                {
                    //alert(event.title);
                }
        });
    });

    </script>
%else:
    <%inherit file="pyramidapp:templates/layout.mak"/>
    <form action="${request.route_url('auth',action='in')}" method="post">
    <label>User</label><input type="text" name="username">
    <label>Password</label><input type="password" name="password">
    <input type="submit" value="Sign in">
    </form>
    <p><a href="${request.route_url('register')}">Register an account</a></p>
%endif