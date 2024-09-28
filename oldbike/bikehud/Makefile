CFLAGS=
LDFLAGS=
LIBS=

ifeq ($(OS),Windows_NT)
	CC= x86_64-w64-mingw32-g++
#	LDFLAGS+=-static
else
	CC=g++
#	CC=clang++
#	CLANG_CXX_LANGUAGE_STANDARD = gnu++11
#	LDFLAGS+= -stdlib=libc++ 
#	CFLAGS+=-std=c++11 -stdlib=libc++ 

#	CFLAGS+=-m64
#	LDFLAGS+=-m64
endif

LDFLAGS+=-L/usr/X11/lib -L/usr/local/lib -L/opt/local/lib

SUFFIXES += .d

#CFLAGS+=-Wall 

SOURCES =  main.cpp 
#SOURCES += GraphUtils.cpp
#SOURCES += instrument.cpp

CFLAGS+=  -I /usr/X11/include -I/opt/local/include



LIBS += -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_video 
LIBS += -lboost_program_options 
LIBS += -lboost_filesystem -lboost_system 
LIBS += -lsqlite3
LIBS += -lcairo

EXECUTABLE=bikehud
LINK=$(CC)

CFLAGS += -g
#CFLAGS += -O
#CFLAGS += -O2
#CFLAGS += -O3

OBJECTS=$(SOURCES:.cpp=.o)	


#These are the dependency files, which make will clean up after it creates them
DEPFILES=$(SOURCES:.cpp=.d)

all: $(EXECUTABLE)

clean:
	rm -f *.o *.obj *.d $(EXECUTABLE)

-include $(DEPFILES)

$(EXECUTABLE): $(OBJECTS) 
	$(LINK) $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@

$(EXECUTABLE).exe: $(OBJECTS) 
	$(LINK) $(LDFLAGS) $(OBJECTS) $(LIBS)


#This is the rule for creating the dependency files
%.d: %.cpp
	$(CC) $(CFLAGS) -MM -MT '$(patsubst src/%,obj/%,$(patsubst %.cpp,%.o,$<))' $< > $@


# %.d
%.o: %.cpp %.h
	$(CC) $(CFLAGS) -c $< -o $@

%.obj: %.cpp %.h
	$(CC) $(CFLAGS) -c $< -o $@

