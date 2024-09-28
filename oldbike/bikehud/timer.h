#ifndef __shared_utils_h
#define __shared_utils_h

#ifndef _WIN32
#include <sys/time.h>
#endif

//#include <fstream>
#include <iostream>
#include <vector>

using namespace std;


class TimerBase {
public:
    virtual void add(string label, bool do_print=false) = 0;

    void reset() {
        times.clear();
        labels.clear();
    }

    void print() {
        for (size_t i=1; i<times.size(); i++) {
            cout 
                << labels[i] << ": " 
                << (times[i].tv_sec - times[i-1].tv_sec) + (times[i].tv_usec - times[i-1].tv_usec)/1e6  
                << "  ";
        }

        cout << endl;
    }

    string toString() {
        stringstream s;

        for (size_t i=1; i<times.size(); i++) {
            s 
                << labels[i] << ": " 
                << (times[i].tv_sec - times[i-1].tv_sec) + (times[i].tv_usec - times[i-1].tv_usec)/1e6  
                << "  ";
        }

        return s.str();
        //__android_log_print(ANDROID_LOG_INFO, "cvcamera", "%s", s.str().c_str());
    }

    double toDouble(string s) {
        for (size_t i=0; i<labels.size(); i++) {
            if (labels[i] == s) {
                return times[i].tv_sec + times[i].tv_usec/1e6;
            }
        }

        fprintf(stderr, "Label not found: %s\n", s.c_str());
        return -1;
    }

    double diff(string label1, string label2) {
        return toDouble(label2) - toDouble(label1);
    }

protected:
    vector<timeval> times;
    vector<string> labels;
};

#ifdef _WIN32

class Timer : public TimerBase {
public:

    void add(string label, bool do_print=false) {
        labels.push_back(label);

        if (do_print) print();
    }
};

#else

class Timer : public TimerBase {
public:

    void add(string label, bool do_print=false) {
        timeval x;
        gettimeofday(&x, NULL);
        times.push_back(x);
        labels.push_back(label);

        if (do_print) print();
    }

    double get_time() {
        timeval x;
        gettimeofday(&x, NULL);
        return x.tv_sec + x.tv_usec/1e6;
    }
};

#endif // ifdef _win32



#endif // __shared_utils_h
