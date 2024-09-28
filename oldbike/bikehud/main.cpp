#include "main.h"
#include "log.h"
#include "GraphUtils.h"
#include "instrument.h"
#include "timer.h"

#include <string>

#include <boost/program_options.hpp>
#include <stdio.h>
#include <sqlite3.h> 

#include <cairo/cairo.h>

#define DOTIME true

using namespace std;
//using namespace cv;

namespace po = boost::program_options;

int data_callback(void *data, int argc, char **argv, char **azColName);

vector<double> timestamp, dist, power, speed, cadence, heart_rate, altitude, latitude, longitude, temp;
double last_timestamp = -1;

double interpolate(vector<double> &data, int index, double seconds) {
    double x;
    if (index > 0) {
        //debug("x = %f, seconds=%f\n", x, seconds);
        x = seconds - index;
        return data[index]*x + data[index-1]*(1-x);
    } else if (index == 0) {
        return data[index];
    } else {
        return 0;
    }
}

void MatToCairo(Mat &MC3,cairo_surface_t *surface) {
    Mat MC4 = Mat(cairo_image_surface_get_height(surface),
                  cairo_image_surface_get_width(surface),
                  CV_8UC4,
                  cairo_image_surface_get_data(surface),
                  cairo_image_surface_get_stride(surface)
                  );

    vector<Mat> Imgs1;
    vector<Mat> Imgs2;
    cv::split(MC4,Imgs1);
    cv::split(MC3,Imgs2);
    for(int i=0;i<3;i++) {
        Imgs1[i]=Imgs2[i];
    }
    Imgs1[3]=255; 
    cv::merge(Imgs1,MC4);
}

void CairoToMat(cairo_surface_t *surface,Mat &MC3) {
    Mat MC4 = Mat(cairo_image_surface_get_height(surface),
                  cairo_image_surface_get_width(surface),
                  CV_8UC4,cairo_image_surface_get_data(surface),
                  cairo_image_surface_get_stride(surface));
    vector<Mat> Imgs1;
    vector<Mat> Imgs2;
    cv::split(MC4,Imgs1);
    cv::split(MC3,Imgs2);
    for(int i=0;i<3;i++) {
        Imgs2[i]=Imgs1[i];
    }

    cv::merge(Imgs2,MC3);

}

template<class T>
T foo_moving_average(T &data, const int window) {
    T out;
    double avg=0;
    int count=0;
    typename T::iterator head = data.begin();;

    for (typename T::iterator it=data.begin(); it!=data.end(); it++) {
        avg += *it;
        if (++count < window) {
            out.push_back(avg/count);
        } else {
            out.push_back(static_cast<double>(avg)/window);
            avg -= *head;
            head++;
        }
    }
    
    return out;
}


int main(int argc, char *argv[]) {

    string output_file;
    string input_file;
    string dbfile;
    string ride_id;
    string vidmode;
    double delay, start_seconds, end_seconds;
    double outfps, infps;
    VideoWriter writer, writer2;
    VideoCapture cap;
    int total_frames;

    // 720p
    //int vid_height = 720;
    //int vid_width = 1280;

    // 1080p
    int vid_height = 1080;
    int vid_width = 1920;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "produce help message")
        ("video-mode,v", po::value<string>(&vidmode)->default_value("DIVX"), "video mode (DIVX, FLV1, I420, etc)")
        ("output-file,o", po::value<string>(&output_file), "Path to output file")        
        ("input-file,i", po::value<string>(&input_file), "Path to input file")        
        ("database,d",    po::value<string>(&dbfile),      "Path to bike database")     
        ("ride-id,r",     po::value<string>(&ride_id),     "Ride id")
        ("fps,f", po::value<double>(&outfps)->default_value(1.0), "Output fps (Frames/s)")
        ("delay", po::value<double>(&delay)->default_value(0), "Data delay in seconds")
        ("start", po::value<double>(&start_seconds)->default_value(0), "Second to start at")
        ("end", po::value<double>(&end_seconds)->default_value(-1), "Second to start at")
        ;

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);    

    sqlite3 *db;
    int rc;
    rc = sqlite3_open(dbfile.c_str(), &db);

    if (rc){
        fprintf(stderr, "Can't open database '%s': %s\n", dbfile.c_str(), sqlite3_errmsg(db));
        exit(0);
    } else {
        fprintf(stderr, "Opened database '%s' successfully\n", dbfile.c_str());
    }

    char *errmsg = 0;

    string sql("select strftime('%s', data_stamp) as data_stamp, distance, speed, position_lat, position_long, temperature, power, heart_rate,cadence,altitude from ride_data where ride_id='" + ride_id + "'");
    int result = sqlite3_exec(db, sql.c_str(), data_callback, NULL, &errmsg);
    if (result != SQLITE_OK) {
        debug("SQL select statement failed: %s -- %x\n", sql.c_str(), result);
        debug("errmsg = %s\n", errmsg);
    }
    sqlite3_close(db);

    debug("Finished loading data: %lu items\n", timestamp.size());


    if (input_file.size()) {
        cap.open(input_file);
        
        if (!cap.isOpened()) {
            fprintf(stderr, "Couldn't open input video file '%s'\n", input_file.c_str());
            exit(1);
        }

        Mat frame;
        cap.read(frame);

        writer.open(output_file,
                    CV_FOURCC(vidmode[0], vidmode[1], vidmode[2], vidmode[3]),
                    //cap.get(CV_CAP_PROP_FOURCC),
                    cap.get(CV_CAP_PROP_FPS),
                    Size(frame.cols, frame.rows));
        infps = cap.get(CV_CAP_PROP_FPS);
        vid_width = frame.cols;
        vid_height = frame.rows;
        total_frames = cap.get(CV_CAP_PROP_FRAME_COUNT);
        debug("FPS = %f, wid=%d, height=%d, frames=%d\n", cap.get(CV_CAP_PROP_FPS), vid_width, vid_height, total_frames);
    } else {
        writer.open(output_file,
                    CV_FOURCC(vidmode[0], vidmode[1], vidmode[2], vidmode[3]),
                    outfps,
                    Size(vid_width, vid_height));

        writer2.open(output_file + ".mask.avi",
                    CV_FOURCC(vidmode[0], vidmode[1], vidmode[2], vidmode[3]),
                    outfps,
                    Size(vid_width, vid_height));
    }

    if (!writer.isOpened()) {
        debug("Could not open the output video %s for write\n", output_file.c_str());
        return -1;
    }


    cairo_surface_t *surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, vid_width, vid_height); 
    cairo_t *context = cairo_create(surface);

    //int W = 400, H = 150;
    /*
    Rect power_region(vid_width-1 - W-20, 10, W+20, H+20);
    Rect cadence_region(vid_width-1 - W-20, 10+10+H, W+20, 10+10+2*H);
    Rect speed_region(20, 10, W+20, H+20);
    Rect hr_region(20, 10 + 10 + H, W+20, 10 + 20 + 2*H);
    */
  
    vector<double> power_avg = foo_moving_average(power, 3);
    //vector<double> speed_avg = foo_moving_average(speed, 5);
    //vector<double> heart_rate_avg = foo_moving_average(heart_rate, 5);
    //vector<double> cadence_avg = foo_moving_average(cadence, 5);


    double power_min = *std::min_element(power_avg.begin(), power_avg.end());
    double power_max = *std::max_element(power_avg.begin(), power_avg.end());
    double speed_min = *std::min_element(speed.begin(), speed.end());
    double speed_max = *std::max_element(speed.begin(), speed.end());
    double hr_min = *std::min_element(heart_rate.begin(), heart_rate.end());
    double hr_max = *std::max_element(heart_rate.begin(), heart_rate.end());
    double cadence_min = *std::min_element(cadence.begin(), cadence.end());
    double cadence_max = *std::max_element(cadence.begin(), cadence.end());

    double lat_min = *std::min_element(latitude.begin(), latitude.end());
    double lat_max = *std::max_element(latitude.begin(), latitude.end());

    debug("power max == %f, size=%lu\n", power_max, power.size());
    debug("latitude max == %f, size=%lu\n", lat_max, power.size());

    //exit(1);



    Point sz(vid_height/3.25, vid_height/3.25);
    Point sz2(vid_height/2.5, vid_height/2.5);
    Point center1 = Point(sz.x/2.0+10, vid_height-sz.x/2.0-10);
    Point center2 = Point(sz.x*1.15, vid_height-sz.x/2.0-10);
    Point center3 = Point(vid_width - sz2.x*.6, sz2.y*.6);

    Instrument::PieWedge pow1(center1, sz, sz.x*.25, sz.x*.5, 90+25, 270-25);
    Instrument::LabelWedge pow2(center1, sz, sz.x*.25, sz.x*.5, 90-26, 90+26);
    Instrument::PieWedge cad1(center1, sz, sz.x*.175, sz.x*.235, 90+0, 90+360.5);
    Instrument::LabelCircle cad2(center1, sz, sz.x*.18);

    //Instrument::PieWedge speed1(center2, sz,  65, 110, 90+25, 270-25);
    Instrument::PieWedge speed1(center2, sz, sz.x*.25, sz.x*.5, 90-25, -90+25);
    Instrument::LabelWedge speed2(center2, sz, sz.x*.25, sz.x*.5, 90-26, 90+26);
    Instrument::PieWedge hr1(center2, sz, sz.x*.175, sz.x*.235, 90+0, 90+360.5);
    Instrument::LabelCircle hr2(center2, sz, sz.x*.18);

    Instrument::Map map(center3, sz2, latitude, longitude);
    //map.init();

    cad1.set_draw_labels(false);
    hr1.set_draw_labels(false);

    pow1.set_range(power_min, int(ceil(power_max/50.0))*50.0);
    cad1.set_range(cadence_min, cadence_max);
    speed1.set_range(speed_min, min(speed_max, 45.0));
    hr1.set_range(std::max(100.0, hr_min), std::min(hr_max, 200.0));
    
    if (input_file.size()) {
        Mat foo;
        debug("Skipping %f seconds (%d frames)\n", start_seconds, int(start_seconds*infps));
        for (int i=0; i<start_seconds*infps; i++) {
            cap.grab();
        }
    }

    //(vid_height, vid_width, CV_8UC3)
    Mat imgtmp;

    if (!input_file.size()) {
        imgtmp = Mat(vid_height, vid_width, CV_8UC3);
    }

    Mat newimg;
    vector<Mat> imgs, imgs2(3);

    //for (size_t index=0; index<timestamp.size(); index++) {
    double seconds = 0;
    int frames=0;
    int index;
    debug("Starting to process\n");
    double alpha = 1;
    Timer t;
    t.add("t1");
    while (true) {
        if (input_file.size()) {
            //debug("Reading frame\n");
            cap.read(imgtmp);
            if (imgtmp.rows == 0 || imgtmp.cols == 0) break;
            seconds = start_seconds + delay + frames/(infps);
            //debug("seconds = %f\n", seconds);
            index = min(int(timestamp.size())-1, int(seconds));
            if (frames % int(infps*10) == 0) {
                t.add("t2");
                debug("Writing data second %d, video second %f (by frame %f) (%s)\n", index, index - delay, frames/(infps), t.toString().c_str());
                t.reset(); t.add("t1");
            }

            //debug("Frame %d, second %f, index %d\n", frames, seconds, index);


            MatToCairo(imgtmp, surface);
            
        } else {
            seconds = frames/outfps;
            index = int(seconds);
            if (index > timestamp.size()-1) break;
            //cairo_set_source_rgba(context, 1, 1, 1, 1);
            cairo_set_source_rgba(context, 0, 0, 0, 0);
            cairo_set_operator(context, CAIRO_OPERATOR_SOURCE);
            cairo_paint(context);
            cairo_set_operator(context, CAIRO_OPERATOR_OVER);
            //imgtmp.setTo(cv::Scalar(255,255,255)); // 
            //MatToCairo(imgtmp, surface);
            if (frames % 20 == 0) 
                debug("Writing frame %d, seconds=%f, index=%d\n", frames, seconds, index);

        }
        if (end_seconds > 0 && frames/outfps > end_seconds) break;


        frames++;
        //debug("%d\n", frames);

        pow2.draw_to_surface(context, index >= 0 ? power_avg[index] : 0, 0.0, "watts", alpha);
        pow1.draw_to_surface(context, interpolate(power_avg, index, seconds), 0.0, "", alpha);

        cad1.draw_to_surface(context, interpolate(cadence, index, seconds), 0.0, "rpm", alpha);
        cad2.draw_to_surface(context, index >= 0 ? cadence[index] : 0, 0.0, "rpm", alpha);


        speed2.draw_to_surface(context, index >= 0 ? speed[index] : 0, 0.0, "mph", alpha);
        speed1.draw_to_surface(context, interpolate(speed, index, seconds), 0.0, "mph", alpha);

        hr1.draw_to_surface(context, interpolate(heart_rate, index, seconds), 0.0, "bpm", alpha);
        hr2.draw_to_surface(context, index >= 0 ? heart_rate[index] : 0, 0.0, "bpm", alpha);

        if (index >= 0) {
            map.draw_to_surface(context, 
                                interpolate(longitude, index, seconds),
                                interpolate(latitude, index, seconds),
                                "", alpha);
        }


        if (writer2.isOpened()) {
        //if (frames <= 1) {
            Mat MC4 = Mat(cairo_image_surface_get_height(surface),
                  cairo_image_surface_get_width(surface),
                  CV_8UC4,cairo_image_surface_get_data(surface),
                  cairo_image_surface_get_stride(surface));
            cv::split(MC4, imgs);

            imgs2[0] = imgs[3];
            imgs2[1] = imgs[3];
            imgs2[2] = imgs[3];
            cv::merge(imgs2, newimg);
            writer2 << newimg;

        	//imwrite(output_file+".png", imgs[3]);
            
            //Mat foo(vid_height, vid_width, CU_8U);
            /*
            Mat black = Mat(vid_height, vid_width, CV_8U);
            black.setTo(0);
            Mat newimg;
            vector<Mat> imgs, imgs2;
            cv::split(MC4, imgs);
            imgs2[0] = black;
            imgs2[1] = black;
            imgs2[2] = black;
            imgs2[3] = imgs[3];
            cv::merge(imgs2,newimg);
            */

        }

        CairoToMat(surface, imgtmp);


        //break;

        writer << imgtmp;

        //imgtmp.release();
    }
        
        
        
    return 0;
}


int data_callback(void *data, int argc, char **argv, char **azColName) {
    //    debug("%s\n", argv[0]);

    char *strdata = 0;
    char blank[] = "0";
    //debug("--------------------\n");
    for (int i=0; i<argc; i++) {
        if (argv[i] == NULL) 
            strdata = blank;
        else
            strdata = argv[i];

        //debug("label=%s\n", azColName[i]);
        if (strcmp(azColName[i], "data_stamp") == 0)
            timestamp.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "distance") == 0)
            dist.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "speed") == 0)
            speed.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "position_lat") == 0)
            if (argv[i] == NULL) 
                latitude.push_back(latitude.back());
            else
                latitude.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "position_long") == 0)
            if (argv[i] == NULL) 
                longitude.push_back(longitude.back());
            else
                longitude.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "temperature") == 0)
            temp.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "power") == 0) {
            power.push_back(boost::lexical_cast<double>(strdata));
            //debug("Pushing to power: %s -- %f\n", strdata, power.back());
        }
        if (strcmp(azColName[i], "heart_rate") == 0)
            heart_rate.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "cadence") == 0)
            cadence.push_back(boost::lexical_cast<double>(strdata));
        if (strcmp(azColName[i], "altitude") == 0)
            altitude.push_back(boost::lexical_cast<double>(strdata));
    }

    if (last_timestamp > -1) {
        for (double i=last_timestamp+1; i < *timestamp.end(); i++) {
            // debug("timestamp size=%d, pow=%d lat=%d\n", timestamp.size(), power.size(), latitude.size());
            timestamp.push_back(i);
            dist.push_back(dist.back());
            power.push_back(power.back());
            speed.push_back(speed.back());
            cadence.push_back(cadence.back());
            heart_rate.push_back(heart_rate.back());
            altitude.push_back(altitude.back());
            latitude.push_back(latitude.back());
            longitude.push_back(longitude.back());
            temp.push_back(temp.back());
        }
    }

    last_timestamp = *timestamp.end();

     return 0;
}


        /*
        setGraphColor(3);
        //vector this_pow<double> = 
        size_t first = std::max((size_t) 0, index-120);
        size_t last = index;
        drawFloatGraph(vector<double>(&power_avg[first], &power_avg[last]), imgtmp(power_region), power_min, power_max, W, H);
        drawFloatGraph(vector<double>(&speed_avg[first], &speed_avg[last]), imgtmp(speed_region), speed_min, speed_max, W, H);
        drawFloatGraph(vector<double>(&heart_rate[first], &heart_rate[last]), imgtmp(hr_region), hr_min, hr_max, W, H);
        drawFloatGraph(vector<double>(&cadence[first], &cadence[last]), imgtmp(cadence_region), cadence_min, cadence_max, W, H);

        char mystr[100];
        sprintf(mystr, "P: %4.0f  S: %3.0f  HR: %3.0f  C: %3.0f", power[index], speed[index], heart_rate[index], cadence[index]);
        putText(imgtmp, mystr, Point(20, imgtmp.rows-20), FONT_HERSHEY_DUPLEX, .7, Scalar(255, 255, 255), 1.5, 8, false);
        */
