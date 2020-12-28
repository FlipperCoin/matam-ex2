.PHONY: build test

build: _event_manager.so

test: eventManager.py event_manager.py _event_manager.so
	python3.6 eventManager.py

event_manager.py: event_manager.i
	swig -python event_manager.i

event_manager_wrap.c: event_manager.i
	swig -python event_manager.i

event_manager_wrap.o: event_manager_wrap.c
	gcc -std=c99 -fPIC -c event_manager_wrap.c -o event_manager_wrap.o -I /usr/include/python3.6m -I .

_event_manager.so: event_manager_wrap.o
	ld -shared event_manager.o event_manager_wrap.o date.o priority_queue.o -L/usr/include/python3.6m/ -o _event_manager.so

submission: event_manager.i eventManager.py
	rm -f submission.zip
	zip -j Submission.zip $^