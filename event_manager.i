%module event_manager
%{

#include <event_manager.h>

%}

Date dateCreate(int day, int month, int year);
void dateDestroy(Date date);

EventManager createEventManager(Date date);
void destroyEventManager(EventManager em);

EventManagerResult emAddEventByDate(EventManager em, char* event_name, Date date, int event_id);
void emPrintAllEvents(EventManager em, const char* file_name);