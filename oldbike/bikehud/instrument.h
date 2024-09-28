#pragma once

#include "log.h"

#include "opencv/highgui.h"
#include "opencv/cv.h"
#include <cairo/cairo.h>

#include <vector>

#include <boost/lexical_cast.hpp>

using namespace cv;
using namespace std;

#define DEG2RAD(x) (x)/180.0*M_PI

namespace Instrument {

    class Base {
    public:
        Base(Point center, Point dim)
            : _center(center)
            , _dim(dim)
            , _surface(cairo_image_surface_create(CAIRO_FORMAT_ARGB32, _dim.x, _dim.y))
            , _context(cairo_create(_surface))
        {
            debug("Center = %d, %d  Dim = %d, %d\n", _center.x, _center.y, _dim.x, _dim.y);

        }

        virtual void draw(double val, double val2, string unit) = 0;

        virtual void draw_to_file(string filename, double val, double val2, string unit) {
            draw(val, val2, unit);
            cairo_surface_write_to_png(_surface, filename.c_str());
        }

        virtual void draw_to_surface(cairo_t *context, double val, double val2, string unit, double alpha=1) {
            // clear surface
            cairo_set_source_rgba(_context, 0, 0, 0, 0);
            cairo_set_operator(_context, CAIRO_OPERATOR_SOURCE);
            cairo_paint(_context);
            cairo_set_operator(_context, CAIRO_OPERATOR_OVER);
            draw(val, val2, unit);

            double tx = _center.x - _dim.x/2.0;
            double ty = _center.y - _dim.y/2.0;

            cairo_set_source_surface(context, _surface, tx, ty);
            //cairo_rectangle(context, tx, ty, _dim.x, _dim.y);
            //cairo_clip(context);
            cairo_paint_with_alpha(context, alpha);

            /*
            cairo_rectangle(context, tx, ty, _dim.x, _dim.y);
            cairo_set_source_rgba(context, 1.0, 1.0, 0.0, 1);
            cairo_stroke(context);
            */

            /*
            _context = context;
            cairo_push_group(_context);
            cairo_pop_group_to_source(_context);
            cairo_paint_with_alpha(_context, alpha);
            */
        }

    protected:
        Point _center;
        Point _dim;
        cairo_surface_t *_surface;
        cairo_t *_context;
    };

    class PieWedge : public Base {
    public:
        PieWedge(Point center, Point dim, double radius1=0, double radius2=0, double angle1=90+25, double angle2=270)
            : Base(center, dim)
            , _radius1(radius1)
            , _radius2(radius2)
            , _angle1(DEG2RAD(angle1))
            , _angle2(DEG2RAD(angle2))
            , _segments(5)
            , _draw_labels(true)
            , _under_surface(cairo_image_surface_create(CAIRO_FORMAT_ARGB32, _dim.x, _dim.y))
            , _under_context(cairo_create(_under_surface))
            , _over_surface(cairo_image_surface_create(CAIRO_FORMAT_ARGB32, _dim.x, _dim.y))
            , _over_context(cairo_create(_over_surface))
            , _radpat(NULL)
        {
        }

        void init() {
            if (_radpat) cairo_pattern_destroy(_radpat);
            _radpat = cairo_pattern_create_radial(_dim.x/2.0, _dim.y/2.0, _radius1, _dim.x/2.0, _dim.y/2.0, _radius2); 
            cairo_pattern_add_color_stop_rgba(_radpat, 0,  1.0, 0.5, 0.5, 1);
            cairo_pattern_add_color_stop_rgba(_radpat, 1,  0.9, 0.0, 0.0, 1);

            // clear under
            cairo_set_source_rgba(_under_context, 0, 0, 0, 0);
            cairo_set_operator(_under_context, CAIRO_OPERATOR_SOURCE);
            cairo_paint(_under_context);
            cairo_set_operator(_under_context, CAIRO_OPERATOR_OVER);

            // clear over
            cairo_set_source_rgba(_over_context, 0, 0, 0, 0);
            cairo_set_operator(_over_context, CAIRO_OPERATOR_SOURCE);
            cairo_paint(_over_context);
            cairo_set_operator(_over_context, CAIRO_OPERATOR_OVER);

            // under
            if (_angle1 < _angle2) {
                cairo_arc(_under_context, _dim.x/2.0, _dim.y/2.0, _radius1, _angle1, _angle2);
                cairo_arc_negative(_under_context, _dim.x/2.0, _dim.y/2.0, _radius2, _angle2, _angle1);
            } else {
                cairo_arc_negative(_under_context, _dim.x/2.0, _dim.y/2.0, _radius1, _angle1, _angle2);
                cairo_arc(_under_context, _dim.x/2.0, _dim.y/2.0, _radius2, _angle2, _angle1);
            }
            cairo_close_path(_under_context);

            cairo_set_source_rgba(_under_context, 0.0, 0.0, 0.0, 1);
            cairo_fill(_under_context);

            // over
            if (_draw_labels) {
                cairo_select_font_face (_over_context, "sans-serif", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_BOLD);
                cairo_set_font_size(_over_context, 15.0);
                cairo_set_source_rgba(_over_context, .9, .9, .9, 1);
                for (int i=0; i<=_segments; i++) {
                    double ang = _angle1 + i*(_angle2-_angle1)/_segments;
                    double x1 = _dim.x/2.0 + cos(ang)*_radius2*.98;
                    double y1 = _dim.y/2.0 + sin(ang)*_radius2*.98;
                    
                    double x2 = _dim.x/2.0 + cos(ang)*_radius2*.89;
                    double y2 = _dim.y/2.0 + sin(ang)*_radius2*.89;
                    
                    double x3 = _dim.x/2.0 + cos(ang)*_radius2*.80;
                    double y3 = _dim.y/2.0 + sin(ang)*_radius2*.80;
                    
                    cairo_move_to(_over_context, x1, y1);
                    cairo_line_to(_over_context, x2, y2);
                    cairo_stroke(_over_context);
                    
                    //cairo_font_extents_t fe;
                    cairo_text_extents_t te;
                    string label = boost::lexical_cast<string>(int(_minval + i * (_maxval - _minval)/_segments));
                    //char label[] = "100";
                    cairo_text_extents (_over_context, label.c_str(), &te);
                    cairo_line_to(_over_context, x3, y3);
                    cairo_stroke(_over_context);
                    
                   
                    cairo_set_source_rgba(_over_context, .9, .9, .9, 1);
                    cairo_move_to(_over_context, x3 - te.x_bearing - te.width / 2, y3 - te.y_bearing - te.height/2);
                    cairo_show_text(_over_context, label.c_str());
                    
       
                }
            }


        }

        virtual void draw(double val, double val2, string unit) {
            //cairo_new_path(_context);
            cairo_set_source_rgba(_context, 0.0, 0.0, 0.0, 0);

            cairo_set_source_surface(_context, _under_surface, 0, 0);
            cairo_paint(_context);

            // power bar
            double ang = ((val-_minval) / (_maxval - _minval)) * (_angle2 - _angle1) + _angle1;
            if (ang > 2*M_PI) ang = 2*M_PI;
            double rad_diff = _radius2 - _radius1;
            double rad1 = _radius1 + rad_diff*.15;
            double rad2 = _radius1 + rad_diff*.85;
            //debug("min=%f, max=%f, ratio = %f, ang = %f\n", _minval, _maxval, val/(_maxval - _minval), ang);

            if (_angle1 < _angle2) {
                cairo_arc(_context, _dim.x/2.0, _dim.y/2.0, rad1, _angle1, ang);
                cairo_arc_negative(_context, _dim.x/2.0, _dim.y/2.0, rad2, ang, _angle1);
            } else {
                cairo_arc_negative(_context, _dim.x/2.0, _dim.y/2.0, rad1, _angle1, ang);
                cairo_arc(_context, _dim.x/2.0, _dim.y/2.0, rad2, ang, _angle1);
            }
            cairo_close_path(_context);

            cairo_set_source(_context, _radpat);
            cairo_fill(_context);

            cairo_set_source_surface(_context, _over_surface, 0, 0);
            cairo_paint(_context);

        }

        void set_range(double minval, double maxval) { 
            fprintf(stderr, "minval set to %f, maxval set to %f\n", minval, maxval);
            _minval = minval;
            _maxval = maxval;
            init();
        }

        void set_draw_labels(bool val) { _draw_labels = val; }

        private:
        double _radius1, _radius2;
        double _angle1, _angle2;
        double _minval, _maxval;
        int _segments; // find a way to automate
        bool _draw_labels;
        cairo_surface_t *_under_surface;
        cairo_t *_under_context;
        cairo_surface_t *_over_surface;
        cairo_t *_over_context;
        cairo_pattern_t *_radpat;
    };

    class LabelWedge : public Base {
    public:
        LabelWedge(Point center, Point dim, double radius1, double radius2, double angle1, double angle2)
            : Base(center, dim)
            , _radius1(radius1)
            , _radius2(radius2)
            , _angle1(DEG2RAD(angle1))
            , _angle2(DEG2RAD(angle2))
        {}

        virtual void draw(double val, double val2, string unit) {
            double fs_small = 14.0;
            double fs_large = 33.0;

            cairo_new_path(_context);
            cairo_arc(_context, _dim.x/2.0, _dim.y/2.0, _radius1, _angle1, _angle2);
            cairo_arc_negative(_context, _dim.x/2.0, _dim.y/2.0, _radius2, _angle2, _angle1);
            cairo_close_path(_context);
            cairo_set_source_rgba(_context, 0.0, 0.0, 0.0, 1);
            cairo_fill(_context);

            cairo_select_font_face (_context, "sans-serif", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_BOLD);
            cairo_set_source_rgba(_context, .9, .9, .9, 1);

            string label = boost::lexical_cast<string>(int(val));
            double ang = _angle1 + (_angle2-_angle1)/2;
            double x = _dim.x/2.0 + cos(ang)*((_radius2-_radius1)/2 + _radius1);
            double y = _dim.y/2.0 + sin(ang)*((_radius2-_radius1)/2 + _radius1);

            cairo_text_extents_t te;
            cairo_text_extents_t te2;
            cairo_set_font_size(_context, fs_large);
            cairo_text_extents (_context, label.c_str(), &te);
            cairo_set_font_size(_context, fs_small);
            cairo_text_extents (_context, unit.c_str(), &te2);

            double box_height = te.height + te2.height;
            double box_width = std::max(te.width, te2.width);

            cairo_move_to(_context, 
                          x - te.x_bearing - te.width/2.0,
                          y - box_height/2.0 + te.height);
            cairo_set_font_size(_context, fs_large);
            cairo_show_text(_context, label.c_str());

            cairo_set_font_size(_context, fs_small);
            cairo_move_to(_context, 
                          x - te2.x_bearing - te2.width/2.0,
                          y - box_height/2.0 + te2.height + te.height);
            cairo_show_text(_context, unit.c_str());
        }

        private:
        double _radius1, _radius2;
        double _angle1, _angle2;
    };

    class LabelCircle : public Base {
    public:
        LabelCircle(Point center, Point dim, double radius)
            : Base(center, dim)
            , _radius(radius)
        {}

        virtual void draw(double val, double val2, string unit) {
            double fs_small = 14.0;
            double fs_large = 32.0;

            string label = boost::lexical_cast<string>(int(val));
 
            cairo_new_path(_context);
            cairo_arc(_context, _dim.x/2.0, _dim.y/2.0, _radius, 0, 360);
            cairo_set_source_rgba(_context, 0.0, 0.0, 0.0, 1);
            cairo_fill(_context);

            cairo_select_font_face (_context, "sans-serif", CAIRO_FONT_SLANT_NORMAL, CAIRO_FONT_WEIGHT_BOLD);
            cairo_set_source_rgba(_context, .9, .9, .9, 1);


            cairo_text_extents_t te;
            cairo_text_extents_t te2;
            cairo_set_font_size(_context, fs_large);
            cairo_text_extents (_context, label.c_str(), &te);
            cairo_set_font_size(_context, fs_small);
            cairo_text_extents(_context, unit.c_str(), &te2);

            double box_height = te.height + te2.height;
            double box_width = std::max(te.width, te2.width);

            cairo_move_to(_context, 
                          _dim.x/2.0 - te.x_bearing - te.width/2.0,
                          _dim.y/2.0 - box_height/2.0 + te.height);
            cairo_set_font_size(_context, fs_large);
            cairo_show_text(_context, label.c_str());

            cairo_set_font_size(_context, fs_small);
            cairo_move_to(_context, 
                          _dim.x/2.0 - te2.x_bearing - te2.width/2.0,
                          _dim.y/2.0 - box_height/2.0 + te2.height + te.height);
            cairo_show_text(_context, unit.c_str());
        }

    private:
        double _radius;
    };

    class TextBox : public Base {
    public:
        TextBox(Point center, Point dim)
            : Base(center, dim)
        {}

        virtual void draw(double val, double val2, string unit) {
        }

    };

    class Map : public Base {
    public:
        Map(Point center, Point dim, vector<double> &lats, vector<double> &longs)
            : Base(center, dim)
            , _lats(lats)
            , _longs(longs)
            , lat_min(*std::min_element(lats.begin(), lats.end()))
            , lat_max(*std::max_element(lats.begin(), lats.end()))
            , long_min(*std::min_element(longs.begin(), longs.end()))
            , long_max(*std::max_element(longs.begin(), longs.end()))
            , scaley((lat_max - lat_min)/dim.x)
            , scalex((long_max - long_min)/dim.y)
            , scale(std::max(scalex, scaley)*1)
            , _map_surface(cairo_image_surface_create(CAIRO_FORMAT_ARGB32, _dim.x, _dim.y))
            , _map_context(cairo_create(_map_surface))
        {

            cairo_new_path(_context);

            double fx, fy;
            fx = (_longs[0] - long_min)/scale;
            fy = _dim.y - (_lats[0] - lat_min)/scale  - (1-scaley/scalex)*_dim.y + 2;
            cairo_move_to(_map_context, fx, fy);
            for (int i=1; i<_lats.size(); i++) {
                fx = (_longs[i] - long_min)/scale;
                fy = _dim.y - (_lats[i]-lat_min)/scale  - (1-scaley/scalex)*_dim.y + 2;
                cairo_line_to(_map_context, fx, fy);
            }

            cairo_set_line_width(_map_context, 4);
            cairo_set_source_rgba(_map_context, 0.0, 0.0, 0.0, 1.0);
            cairo_stroke_preserve(_map_context);

            cairo_set_line_width(_map_context, 2.5);
            cairo_set_source_rgba(_map_context, .9, .9, .9, .9);
            cairo_stroke(_map_context);


        }


        virtual void draw(double val, double val2, string unit) {


            double fx, fy;

            cairo_set_source_surface(_context, _map_surface, 0, 0);
            cairo_paint(_context);

            fx = (val - long_min)/scale;
            fy = _dim.y - (val2 - lat_min)/scale  - (1-scaley/scalex)*_dim.y + 2;
            cairo_arc(_context, fx, fy, 7, 0, 360);
            cairo_set_source_rgba(_context, 1.0, 0.0, 0.0, 1);
            cairo_fill(_context);
        }

    private:
        vector<double> _lats, _longs;
        double lat_min, lat_max, long_min, long_max;
        double scalex, scaley, scale;
        cairo_surface_t *_map_surface;
        cairo_t *_map_context;
    };

}
