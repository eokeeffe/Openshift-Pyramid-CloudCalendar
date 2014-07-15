import tw2.jqplugins.fullcalendar
from tw2.jqplugins.fullcalendar.widgets import *

class BasicCalendarWidget(FullCalendarWidget):
    '''
    see source code for js functions and `calendar_events`
    '''
    attrs = {'style': 'width: 100%;'}
    def setOptions(self,calendar_events,day_click_js,event_click_js):
        options={'header': 
            {
                'left': 'prev,next today',
                'center': 'title',
                'right': 'month,agendaWeek,agendaDay'
            },
            'events': calendar_events,
            'editable': True,
            'aspectRatio': 1.60,
            'theme': True,
            'dayClick': day_click_js,
            'eventClick': event_click_js,
        }