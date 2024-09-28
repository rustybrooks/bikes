#!/usr/bin/python

workouts = {
    'E1' : ['Recovery',	'Done in the 1 zone using the small chainring on a flat course. Do these the day after a BT workout. Best if done alone. May also be done on an indoor trainer or rollers, especially if flat courses are not available. Cross training is appropriate for recovery in Preparation, Base 1, and Base 2 periods. An excellent time to do a recovery spin is in the evening on a day when you\'ve done intervals, sprints, a hard group ride, hills or a race. Spinning for 15-30 minutes on rollers or a trainer hastens recovery for most experienced riders. Novices are better taking the time off. These workouts are not scheduled on the Annual Training Plan, but are an integral part of training throughout the season.', ['All']],

    'E2' : ['Aerobic',	'Used for aerobic maintenance and endurance training. Stay primarily in the 1 and 2 zones on a rolling course up to 4% grades. Remain seated on the uphill portions to build greater strength while maintaining a comfortably high cadence. Can be done with a disciplined group or on an indoor trainer by shifting through the gears to simulate rolling hills. Cross training is effective during Preparation and Base 1.', ['All']],
 
    'E3': ['Fixed Gear', 'Set up your bike with a gear that is appropriate for your strength level using a small chainring (39-42) and a large cog (15-19). If you are in your first two years of training, don\'t do this workout. Start by riding flat courses and gradually add rolling hills. Intensity should be mostly in the 2-3 zones. This workout is multi-ability including endurance, strength, and speed - all elements required of Base training.',  ['Base 2', "Base 3"]],
		
    'F1': ['Moderate Hills', 'Select a course that includes several hills of up to 6% gradient that take up to three minutes to ascend. Stay seated on all climbs pedalling from the hips. Cadence at 70 rpm or higher. Stay in the 1-4 zones on this ride.', ['Base 3']],

    'F2': ['Long Hills', 'Ride a course including long gradients of up to 8% that take six or more minutes to climb. Remain mostly seated on the hills and keep your cadence at 60 rpm or higher. Go no higher than 5a zone. Concentrate on bike position and smooth pedalling.', ['Base 3', "Build 1"]],
 
    'F3': ['Steep Hills', 'Ride a course that includes 8% or steeper hills that take less than two minutes to climb. You can do sprints on the same hill with 3-5 minutes of recovery between climbs. Be sure to warm up thoroughly. Intensity may climb to 5b several times with recoveries into the 1 zone. Climb in and out of the saddle. Maintain a cadence of 50-60 rpm. Stop the workout if you cannot maintain at least 50 rpm. Do this workout no more than twice per week. Do not do this workout if you have knee problems.', ['Build 1', "Build 2", "Peak", "Race"]],
		
    'S1': ['Spin-ups', 'On a downhill or on an indoor trainer set to light resistance, for one minute gradually increase cadence to maximum. Maximum is the cadence you can maintain without bouncing. As the cadence increases, allow your lower legs and feet to relax - especially the toes. Hold your maximum for as long as possible. Recover for at least three minutes and repeat several times. These are best done with a handlebar computer that displays cadence. Heart rate and power ratings have no significance for this workout.', [ "Preparation", "Base 1", "Base 2", "Base 3"]],
 
    'S2': ['Isolated Leg', 'With a light resistance on trainer or downhill, do 90% of work with one leg while the other is "along for the ride." Spin with a higher than normal cadence. Change legs when fatigue begins to set in. Can also be done on a trainer with one foot out of the pedal and resting on a stool while the other works. Focus on eliminating "dead" spots at top and bottom of stroke. Heart rate and power ratings have no bearing on this workout.', ['Base 1', "Base 2"]], 

    'S3': ['Cornering' 'On a kerbed street with a clean surface and 90-degree turns, practise cornering techniques: lean both bike and body into turn, lean body while keeping bike upright, and keep body upright while leaning bike. Avoid streets with heavy traffic. Practise several speeds with different angles of approach. Include two or three sprint efforts into the turn. Heart rate and power ratings are not important for this workout.', ['Base 3', 'Build 1', "Build 2"]],
 
    'S4': ['Bumping', 'On a firm, grassy field practise making body contact with a partner while riding slowly. Increase speed as skill improves. Also include touching overlapped wheels.', ['Base 3', "Build 1", "Build 2"]],

    'S5': ['Form Sprints', 'Early in a ride, do 6-10 sprints on a slight downhill or with a tail wind. Each sprint lasts about 15 seconds with a five-minute recovery. These sprints are done for form, so hold back a bit on intensity. Heart rate is not an accurate gauge. Power/RPE should be in the 5b zone. Stand for the first 10 seconds while running smoothly on the pedals building leg speed. Then sit for 5 seconds and maintain a high cadence. Best done alone to avoid "competing."', ['Base 3', "Build 1", "Build 2", "Peak", "Race"]],

    'S6': ['Sprints', 'Within an aerobic ride, include several 10- to 15-second, race-effort sprints. These can be done with another rider or with a group. Designate sprint primes such as signs. Employ all of the techniques of form sprints, only now at a higher intensity. Power/RPE should be 5c zone. Heart rate is not a good indicator. There should be at least five minutes recovery between sprints.', ['Build 1', "Build 2", "Peak", "Race"]],
		
    'M1': ['Tempo', 'On a mostly flat course, or on an indoor trainer, ride continually in the 3 zone without recovery at time-trial cadence. Avoid roads with heavy traffic and stop signs. Stay in an aerodynamic position throughout. Start with 20 to 30 minutes and build to 75 to 90 minutes by adding 10 to 15 minutes each week. This workout may be done two or three times weekly.', [ "Base 2", "Base 3"]]
,
    'M2': ['Cruise Intervals', 'On a relatively flat course, or an indoor trainer, complete three to five work intervals that are six to 12 minutes long. Build to the 4 and 5a zones on each work interval. If training with a heart rate monitor, the work interval starts as soon as you begin pedalling hard - not when you reach the 4 zone. Recover for two or three minutes after each. Recovery should take 2-3 minutes with heart rate dropping into the 2 zone. The first workout should total 0-30 minutes of combined work interval time. Stay relaxed, aerodynamic, and iosely listen to your breathing while pedalling at time-trial cadence.', ['Base 3', "Build 1", "Build 2", "Peak", "Race"]],

    'M3': ['Hill Cruise Intervals', 'Same as M2 cruise intervals, except that you do them on a long 2-4% gradient. These are good if strength is a limiting factor.', ['Build 1', "Build 2", "Peak", "Race"]],

    'M4': ['Motorpaced Cruise Intervals', 'Same as M2 cruise intervals, except that you do this as a motorpaced workout. Whenever doing motorpace use only a motorcycle for pacing. Do not use a car or truck. Not only do they make the workout too fast, they also make it more dangerous. Be sure the driver of the motorcycle has experience with motorpaced workouts and will always be thinking about your safety. Discuss the workout details with the driver before starting.', [ "Build 1", "Build 2", "Peak"]],

    'M5': ['Criss-Cross Threshold', 'On a mostly flat course with little traffic and no traffic lights, ride 20 to 40 minutes in the 4 and 5a zones. Once you have reached the 4 zone, gradually build effort to the top of the 5a zone taking about two minutes to do so. Then begin backing off slightly and slowly drop back to the bottom of the 4 zone taking about two minutes again. Continue this pattern throughout the ride. Cadence will vary. Complete three or four cruise interval workouts before doing this workout.', ['Build 2', 'Peak']],

    'M6': ['Threshold',	'On a mostly flat course with little traffic and no traffic lights, ride 20 to 40 minutes non-stop in the 4 and 5a zones. Stay relaxed, aerodynamic, and closely listen to your breathing throughout. Don\'t attempt a threshold ride until you\'ve completed at least four cruise interval workouts. This workout definitely should be included in your training, preferably on your time-trial bike.', ['Build 2', 'Peak']],

    'M7': ['Motorpaced Threshold', 'Same as M6 threshold, except done as a motorpaced workout.', ['Build 2', 'Peak', 'Race']],
		
    'A1': ['Group Ride', 'Ride how you feel. If tired, sit in or break off and ride by yourself. If fresh, ride hard going into the 5 zones several times.', ['Build 1', 'Build 2', 'Peak', 'Race']],

    'A2': ['SE Intervals', 'After a good warm-up, on a mostly flat course with no stop signs and light traffic, do five work intervals of three-to-six-minutes duration each. Build to the 5b zone on each with a cadence of 90 rpm or higher. If unable to achieve the 5b zone by the end of the third work interval, stop the workout. You aren\'t ready. Recover to the 1 zone for the same time as the preceding work interval.', ['Build 1', 'Build 2', 'Peak', 'Race']],

    'A3': ['Pyramid Intervals', 'The same as SE intervals, except the work intervals are 1-, 2-, 3-, 4-, 4-, 3-, 2-, 1-minutes building to the 5b zone. The recovery after each is equal to the preceding work interval.', ['Build 1', 'Build 2', 'Peak', 'Race']],

    'A4': ['Hill Intervals', 'Following a thorough warm-up, go to a 6-8% hill that takes three to four minutes to go up and do five climbs. Stay seated with cadence at 60 or higher rpm. Build to the 5b zone on each. Recover to the 1 zone by spinning down the hill and at the bottom for a total of three to four minutes depending on how long the climb is.', ['Build 2', 'Peak' ]],

    'A5': ['Lactate Tolerance Reps', 'This is to be done on a flat or slightly uphill course or into the wind. After a long warm-up and several jumps, do four to eight repetitions of 90 seconds to two minutes each. Intensity is 5c zone. Cadence is high. The total of all work intervals must not exceed 12 minutes. Recovery intervals are 2.5 times as long as the preceding work interval. For example, after a two-minute rep, recover for five minutes. Build to this workout conservatively starting with six minutes total and adding no more than two minutes weekly. Do this workout no more than once a week and recover for at least 48 hours after. If you are unable to achieve the 5c zone after three attempts, stop the workout. Do not do this workout if you are in the first two years of training for cycling.', ['Build 2', 'Peak']],

    'A6': ['Hill Reps', 'After a good warm-up, go to a 6-8% hill and do four to eight reps of 90 seconds each. Stay seated for the first 60 seconds as you build to the 5b zone at 60-70 rpm. In the last 30 seconds, shift to a higher gear, stand, and sprint to the top attaining the 5c zone. Recover completely for four minutes after each rep. If you are unable to achieve the 5c zone after three attempts, stop the workout. Do not do this workout if you are in the first two years of training for cycling.', ['Build 2', 'Peak']],
		

    'P1': ['Jumps', 'Warm up well. Then early in a workout, on an indoor trainer or the road, do 15-25 jumps to improve explosive power. Complete three to five sets of five jumps each. Each jump is 10 to 12 revolutions of the cranks (each leg) at high cadence. Recover for one minute between efforts and five minutes between sets. Power/RPE should be zone 5c. Heart rate is not a good indicator of exertion for this workout.', ['Build 1', 'Build 2', 'Peak', 'Race']],

    'P2': ['Hill Sprints', 'Early in the workout, after a good warm-up, go to a hill with a 4-6% gradient. Do six to nine sprints of 20 seconds each. Use a flying start for each sprint taking 10 seconds to build speed on the flat approach while standing. Climb the hill for 10 seconds applying maximal force standing on the pedals with a high cadence. Recover for five minutes after each sprint. Power/RPE should be zone 5c. Heart rate is not a good indicator of exertion for this workout.', ['Build 1', 'Build 2', 'Peak']],

    'P3': ['Crit Sprints', 'Warm up and then go to a course with kerbed corners, clean turns, and little traffic. Do six to nine sprints of 25-35 seconds duration including corners just as in a criterium. Recover to the 1 zone for five minutes after each. Can be done with another rider taking turns leading the sprints.', ['Build 2', 'Peak', 'Race']],

    'T1': ['Aerobic Time Trial', 'This is best on an indoor trainer with a rear-wheel computer pick-up. May also be done on a flat section of road, but weather conditions will have an effect. After a warm-up, ride five miles with heart rate nine to 11 beats below lactate threshold heart rate. Use a standard gear without shifting. Record time. The conditions of this workout must be as similar as possible from one test to the next. This includes the amount of rest since the last BT workout, the length and intensity of the warm-up, the weather if on the road, and the gear used during the test. As aerobic fitness improves, the time should decrease.', ['Base 1', 'Base 2']],

    'T2': ['Time Trial', 'After a 15- to 30-minute warm-up, complete an eight-mile time trial on a flat course. Go four miles out, turn around, and return to the start line. Mark your start and turn for later reference. Look for faster times as your speed- endurance and muscular-endurance improve. In addition to time, record average power/heart rate and peak power/heart rate. Keep the conditions the same from one time trial to the next as in the aerobic time trial. Use any gear and feel free to change gear during the test.', ['Build 1', 'Build 2']],
}

annual_hours_lookup = {
    'Yearly':  [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200],

    'Prep':         [3.5, 4.0, 5.0, 6.0, 7.0, 7.5, 8.5, 9.0, 10.0, 11.0, 12.0, 12.5, 13.5, 14.5, 15.0, 16.0, 17.0, 17.5, 18.5, 19.5, 20.0],
    'Base 1-1':     [4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 12.5, 14.0, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5],
    'Base 1-2':     [5.0, 6.0, 7.0, 8.5, 9.5, 10.5, 12.0, 13.0, 14.5, 15.5, 16.5, 18.0, 19.0, 20.0, 21.5, 22.5, 24.0, 25.0, 26.0, 27.5, 28.5],
    'Base 1-3':     [5.5, 6.5, 8.0, 9.5, 10.5, 12.0, 13.5, 14.5, 16.0, 17.5, 18.5, 20.0, 21.5, 22.5, 24.0, 25.5, 26.5, 28.0, 29.5, 30.5, 32.0],
    'Base 1-4':     [3.0, 3.5, 4.0, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.0, 12.0, 12.5, 13.5, 14.0, 14.5, 15.5, 16.0, 17.0],
    'Base 2-1':     [4.0, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 12.5, 12.5, 13.0, 14.5, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0],
    'Base 2-2':     [5.0, 6.5, 7.5, 9.0, 10.0, 11.5, 12.5, 14.0, 15.0, 16.5, 17.5, 19.0, 20.0, 21.5, 22.5, 24.0, 25.0, 26.5, 27.5, 29.0, 30.0],
    'Base 2-3':     [5.5, 7.0, 8.5, 10.0, 11.0, 12.5, 14.0, 15.5, 17.0, 18.0, 19.5, 21.0, 22.5, 24.0, 25.0, 26.5, 28.0, 29.5, 31.0, 32.0, 33.5],
    'Base 2-4':     [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'Base 3-1':     [4.5, 5.5, 7.0, 8.0, 9.0, 10.0, 11.0, 12.5, 13.5, 14.5, 15.5, 17.0, 18.0, 19.0, 20.0, 21.0, 22.5, 23.5, 25.0, 25.5, 27.0],
    'Base 3-2':     [5.0, 6.5, 8.0, 9.5, 10.5, 12.0, 13.5, 14.5, 16.0, 17.0, 18.5, 20.0, 21.5, 23.0, 24.0, 25.0, 26.5, 28.0, 29.5, 30.5, 32.0],
    'Base 3-3':     [6.0, 7.5, 9.0, 10.5, 11.5, 13.0, 15.0, 16.5, 18.0, 19.0, 20.5, 22.0, 23.5, 25.0, 26.5, 28.0, 29.5, 31.0, 32.5, 33.5, 35.0],
    'Base 3-4':     [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'Build 1':      [5.0, 6.5, 8.0, 9.0, 10.0, 11.5, 12.5, 14.0, 15.5, 16.0, 17.5, 19.0, 20.5, 21.5, 22.5, 24.0, 25.0, 26.5, 28.0, 29.0, 30.0],
    'Build 1-Rest': [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'Build 2':      [5.0, 6.0, 7.0, 8.5, 9.5, 10.5, 11.0, 13.0, 14.5, 15.5, 16.5, 18.0, 19.0, 20.5, 21.5, 22.5, 24.0, 25.0, 26.5, 27.0, 28.5],
    'Build 2-Rest': [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'Peak 1':       [4.0, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 13.0, 13.5, 14.5, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.5, 24.0, 25.0],
    'Peak 2':       [3.5, 4.0, 5.0, 6.0, 6.5, 7.5, 8.5, 9.5, 10.0, 11.0, 11.5, 12.5, 13.5, 14.5, 15.0, 16.0, 17.0, 17.5, 18.5, 19.0, 20.0],
    'RaceSat':      [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'RaceSun':      [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'RaceSatSun':   [3.0, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
    'Transition':   [3.1, 3.5, 4.5, 5.0, 5.5, 6.5, 7.0, 8.0, 8.5, 9.0, 10.0, 10.5, 11.5, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5, 16.0, 17.0],
}

weekly_hours_lookup = {
3.0: [1.5, 0.75, 0.75, 0, 0, 0, 0],
3.5: [1.5, 1.0, 1.0, 0, 0, 0, 0],
4.0: [1.5, 1.0, 1.0, 0.5, 0, 0, 0],
4.5: [1.75, 1.0, 1.0, 0.75, 0, 0, 0],
5.0: [2.0, 1.0, 1.0, 1.0, 0, 0, 0],
5.5: [2.0, 1.5, 1.0, 1.0, 0, 0, 0],
6.0: [2.0, 1.0, 1.0, 1.0, 1.0, 0, 0],
6.5: [2.0, 1.5, 1.0, 1.0, 1.0, 0, 0],
7.0: [2, 1.5, 1.5, 1.0, 1.0, 0, 0],
7.5: [2.5, 1.5, 1.5, 1.0, 1.0, 0, 0],
8.0: [2.5, 1.5, 1.5, 1.5, 1.0, 0, 0],
8.5: [3.0, 2.0, 1.5, 1.5, 1.0, 0, 0],
9.0: [3.0, 2.0, 1.5, 1.5, 1.0, 0, 0],
9.5: [3.0, 2.0, 1.5, 1.5, 1.0, 0.5, 0],
10.0: [3, 2, 1.5, 1.5, 1, 1, 0],
10.5: [3.0, 2.0, 2.0, 1.5, 1.0, 1.0, 0],
11.0: [3.0, 2.0, 2.0, 1.5, 1.5, 1.0, 0],
11.5: [3.0, 2.5, 2.0, 1.5, 1.5, 1.0, 0],
12.0: [3.0, 2.5, 2.0, 2.0, 1.5, 1.0, 0],
12.5: [3.5, 2.5, 2.0, 2.0, 1.5, 1.0, 0],
13.0: [3.5, 3.0, 2.0, 2.0, 1.5, 1.0, 0],
13.5: [3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0],
14.0: [4.0, 3.0, 2.5, 2.0, 1.5, 1.0, 0],
14.5: [4.0, 3.0, 2.5, 2.5, 1.5, 1.0, 0],
15.0: [4.0, 3.0, 3.0, 2.5, 1.5, 1.0, 0],
15.5: [4.0, 3.0, 3.0, 2.5, 2.0, 1.0, 0],
16.0: [4.0, 3.5, 3.0, 2.5, 2.0, 1.0, 0],
16.5: [4.0, 3.5, 3.0, 3.0, 2.0, 1.0, 0],
17.0: [4.0, 3.5, 3.0, 3.0, 2.0, 1.5, 0],
17.5: [4.0, 4.0, 3.0, 3.0, 2.0, 1.5, 0],
18.0: [4.0, 4.0, 3.0, 3.0, 2.5, 1.5, 0],
18.5: [4.0, 4.0, 3.0, 3.0, 2.5, 1.5, 0],
19.0: [4.5, 4.5, 3.0, 3.0, 2.5, 1.5, 0],
19.5: [4.5, 4.5, 3.5, 3.0, 2.5, 1.5, 0],
20.0: [4.5, 4.5, 3.5, 3.0, 2.5, 2.0, 0],
20.5: [4.5, 4.5, 3.5, 3.5, 2.5, 2.0, 0],
21.0: [5.0, 4.5, 3.5, 3.5, 2.5, 2.0, 0],
21.5: [5.0, 4.5, 4.0, 3.5, 2.5, 2.0, 0],
22.0: [5.0, 4.5, 4.0, 3.5, 3.0, 2.0, 0],
22.5: [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 0],
23.0: [5.0, 5.0, 4.0, 3.5, 3.0, 2.5, 0],
23.5: [5.5, 5.0, 4.0, 3.5, 3.0, 2.5, 0],
24.0: [5.5, 5.0, 4.5, 3.5, 3.0, 2.5, 0],
24.5: [5.5, 5.0, 4.5, 4.0, 3.0, 2.5, 0],
25.0: [5.5, 5.0, 4.5, 4.0, 3.0, 3.0, 0],
25.5: [5.5, 5.5, 4.5, 4.0, 3.0, 3.0, 0],
26.0: [6.0, 5.5, 4.5, 4.0, 3.0, 3.0, 0],
26.5: [6.0, 5.5, 5.0, 4.0, 3.0, 3.0, 0],
27.0: [6.0, 6.0, 5.0, 4.0, 3.0, 3.0, 0],
27.5: [6.0, 6.0, 5.0, 4.0, 3.5, 3.0, 0],
28.0: [6.0, 6.0, 5.0, 4.0, 3.5, 3.5, 0],
28.5: [6.0, 6.0, 5.0, 4.5, 3.5, 3.5, 0],
29.0: [6.0, 6.0, 5.5, 4.5, 3.5, 3.5, 0],
29.5: [6.0, 6.0, 6.0, 4.5, 3.5, 3.5, 0],
30.0: [6.0, 6.0, 6.0, 4.5, 4.0, 3.5, 0],
30.5: [6.0, 6.0, 6.0, 5.0, 4.0, 3.5, 0],
31.0: [6.0, 6.0, 6.0, 5.0, 4.0, 4.0, 0],
31.5: [6.0, 6.0, 6.0, 5.0, 4.5, 4.0, 0],
32.0: [6.0, 6.0, 6.0, 5.5, 4.5, 4.0, 0],
32.5: [6.0, 6.0, 6.0, 5.5, 4.5, 4.5, 0],
33.0: [6.0, 6.0, 6.0, 5.5, 5.0, 4.5, 0],
33.5: [6.0, 6.0, 6.0, 6.0, 5.0, 4.5, 0],
34.0: [6.0, 6.0, 6.0, 6.0, 5.5, 4.5, 0],
34.5: [6.0, 6.0, 6.0, 6.0, 5.5, 5.0, 0],
35.0: [6.0, 6.0, 6.0, 6.0, 6.0, 5.0, 0],
}

workout_patterns = {
    'Prep': [ ['OFF','E1'], ['E2'], ['S1'], ['E2'], ['OFF','E1'], ['E2'], ['E2'], ],
    'Base 1': [ ['OFF','E1'], ['E2'], ['E2'], ['E2'], ['S1','S2'], ['E2'], ['E2'], ],
    'Base 1-Rest': [ ['OFF','E1','S4'], ['E2'], ['E2'], ['S1','S2','S3','S5'], ['E1'], ['T1'], ['E2'], ],
    'Base 2': [ ['OFF','E1'], ['E3','M1'], ['E2'], ['E2'], ['S1','S2'], ['E2'], ['E2'], ],
    'Base 2-Rest': [ ['OFF','E1','S4'], ['E2'], ['E2'], ['S1','S2','S3','S5'], ['E1'], ['T1'], ['E2'], ],
    'Base 3': [ ['OFF','E1','S4'], ['M1','M2'], ['E2'], ['E3','S1','S3','S5'], ['E2'], ['P1','P2'], ['E2'], ],
    'Base 3-Rest': [ ['OFF','E1','S4'], ['E2'], ['E2'], ['S1','S2','S3','S5'], ['E1'], ['T1'], ['E2'], ],
    'Build 1': [ ['OFF', 'E1', 'S4'], ['M2', 'M3', 'F2', 'F3'], ['E1','E2'], ['P1','S6','A1','A2','A3'], ['S3','S5'], ['CRIT','M4','A1'], ['E1','E2'], ],
    'Build 1-Rest': [ ['OFF','E1','S4'], ['E2'], ['E2'], ['S1','S2','S3','S5'], ['E1'], ['T2'], ['E2'], ],
    'Build 2': [ ['OFF','E1','S4'], ['M2','M3','M4','M5','M6','F3'], ['E1','E2'], ['S6','A1','A2','A3','A4','A5','A6','P1','P2','P3'], ['S3','S5'], ['RR','M7','A1'], ['E1','E2'], ],
    'Build 2-Rest': [ ['OFF','E1','S4'], ['E2'], ['E2'], ['S1','S2','S3','S5'], ['E1'], ['T2'], ['E2'], ],
    'Peak': [ ['OFF','E1'], ['E2'], ['F3','A2','A3','A4','A5','A6','M2','M3','M5','M6','S6','P1','P2','P3'], ['E1','E2'], ['E2','S5'], ['E2'], ['CRIT','M4','M7','A1','A2'], ],
    'RaceSat': [ ['OFF','E1'], ['E2'], ['S6','P1','P3'], ['E1','E2','S5'], ['S6','P1'], ['RACE','M7','A1'], ['E1','E2'], ],
    'RaceSun': [ ['OFF','E1'], ['F3','M2','M3','A2','A3'], ['E1','E2'], ['S6','P1','P3'], ['E1','E2','S5'], ['S6','P1'], ['RACE','M7','A1'], ],
    'RaceSatSun': [ ['OFF','E1'], ['E2'], ['S6','P1','P3'], ['E1','E2','S5'], ['S6','P1'], ['RACE'], ['RACE'], ],
    'Transition': [ ['OFF','E1'], ['E1','S1','S2'], ['E1','S1','S2'], ['E1','S1','S2'], ['E1','S1','S2'], ['E1','S1','S2'], ['E1','S1','S2'], ],

}

def weekly_schedule(period, week, annual_hours):
    dow = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]

    key = "%s-%d" % (period, week)
    hour_list = annual_hours_lookup[key] if key in annual_hours_lookup else annual_hours_lookup[period]

    i = annual_hours_lookup['Yearly'].index(annual_hours)
    weekly_hours = weekly_hours_lookup[hour_list[i]]
    print "Total weekly hours:", weekly_hours
    count = 0

    wh = weekly_hours
    wh[0] = weekly_hours[-1]
    wh[-1] = weekly_hours[0]

    for day, choices in zip(dow, workout_patterns[period]):
	time = wh[count]
        print "%2s %0.1f %s" % (day, time, ' '.join(choices))

	count += 1


    foo = "[table]"
    for day in dow:
        foo += day + "|"
    print foo


    foo = ""
    for c in wh:
        foo += str(c) + "|"
    print foo

    foo = ""
    for c in workout_patterns[period]:
        if "OFF" in c:
            foo += "OFF|"
        else:
            foo += "/".join(c) + "|"
    print foo


weekly_schedule('Build 1', 2, 450)
