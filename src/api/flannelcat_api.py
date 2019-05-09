from appenlight_client.timing import time_trace
from collections import defaultdict
import datetime
import geojson
import logging
import numpy
import math

from lib.api_framework import api_register, Api, api_bool, api_int, api_list
from lib.client import PUBGClient, Asset
from lib import PLAYERS, client

import playerdb.queries as pq


logger = logging.getLogger(__name__)

COLORS = [
    '#4286f4', '#41f453', '#f44141', '#41f1f4', '#f4b241',
    '#ee41f4', '#3ba087', '#b2b172', '#b27272', '#7772b2',
    '#b27272',
]


@api_register(None, require_login=False)
class PlayerApi(Api):
    @classmethod
    def squad(cls, squad_name=None):
        return pq.squad_members(squad_name=squad_name)

    @classmethod
    def index(cls, player_name=None, player_id=None, pubg_player_id=None):
        p = pq.player_info(player_name=player_name, player_id=player_id, pubg_player_id=pubg_player_id)
        return p

    @classmethod
    def find_player(cls, player_name):
        p = cls.index(player_name=player_name)
        if p:
            return p
        client = PUBGClient()
        return client.find_player(player_name=player_name)

    @classmethod
    def matches(
        cls, player_name=None, player_id=None, pubg_player_id=None, match_id=None, since=None, since_match_id=None,
        page=1, limit=40, sort='-created_at'
    ):
        foo = pq.matches(
            player_name=player_name,
            player_id=player_id,
            pubg_player_id=pubg_player_id,
            match_id=match_id,
            inserted_since=(datetime.datetime.utcnow() - datetime.timedelta(seconds=since)) if since else None,
            since_match_id=since_match_id,
            page=page, limit=limit, sort=sort,
        )
        # logger.warn("%r", foo[0] if foo else None)
        return foo

    @classmethod
    def team_damage(cls, not_damage_type=None, damage_type=None):
        not_damage_type = api_list(not_damage_type)
        damage_type = api_list(damage_type)
        return pq.team_damage(not_damage_type=not_damage_type, damage_type=damage_type)

    @classmethod
    def team_damage_details(cls, attacker=None, victim=None, not_damage_type=None, damage_type=None):
        not_damage_type = api_list(not_damage_type)
        damage_type = api_list(damage_type)
        return pq.team_damage_details(attacker=attacker, victim=victim, not_damage_type=not_damage_type, damage_type=damage_type)


    @classmethod
    def squad_stats(cls, squad_name=None, game_modes=None, seasons=None, sort='player_name'):
        return pq.squad_stats(squad_name=squad_name, game_modes=game_modes, seasons=seasons, sort=sort)


@api_register(None, require_login=False)
class MatchApi(Api):
    @classmethod
    def _map_coords(cls, x, y, scale=1.0):
        return [scale*x, -scale*y]

    @classmethod
    def _map_coords2(cls, x, y, scale=1.0):
        return [-scale*y, scale*x]

    @classmethod
    def game_modes(cls, player_name=None, squad_name=None, seasons=None, start_date=None, end_date=None, sort='game_mode', limit=None):
        return pq.match_game_modes(
            player_name=player_name, squad_name=squad_name, seasons=seasons, start_date=start_date, end_date=end_date,
            sort=sort, limit=limit
        )

    @classmethod
    def seasons(cls):
        return pq.seasons()

    @classmethod
    def stats(cls):
        return pq.match_stats()

    @classmethod
    def match(cls, pubg_match_id=None, match_id=None):
        match = pq.match_info(match_id=match_id, pubg_match_id=pubg_match_id)
        return match

    @classmethod
    def roster(cls, pubg_match_id=None, match_id=None, player_id=None, player_name=None, sort='player_name'):
        logger.warn("roster... %r", pubg_match_id)
        roster = pq.match_rosters(
            pubg_match_id=pubg_match_id, match_id=match_id, player_id=player_id, player_name_team=player_name, sort=sort
        )
        return roster

    @classmethod
    @Api.config(sort_keys=['asset_url'])
    def telemetry(
            cls, pubg_match_id=None, match_id=None, include_types=None, exclude_types=None, player_names=None,
            page=1, limit=1000, sort='asset_url'
    ):
        if isinstance(include_types, str):
            include_types = include_types.split(',')

        if isinstance(exclude_types, str):
            exclude_types = exclude_types.split(',')

        assets = pq.match_assets(pubg_match_id=pubg_match_id, match_id=match_id, sort=sort)
        client = PUBGClient()

        out = []
        rest = limit
        for asset in assets:
            a = Asset(match_id=match_id, data=client.cache_get(asset.asset_url))
            all = a.events(
                include_types=include_types or [],
                exclude_types=exclude_types or [],
                player_names=player_names
            )
            if limit:
                out.extend(all[:rest])
                rest = limit - len(out)
                if rest <= 0:
                    break
            else:
                out.extend(all)

        return out

    @classmethod
    # @time_trace(name='flannelcat_api.massaged_events')
    @Api.config(sort_keys=['asset_url'])
    def massaged_events(
        cls, pubg_match_id=None, match_id=None, include_types=None, exclude_types=None, player_names=None,
        from_sql=False, sort='asset_url', data=None
    ):
#        logger.warn("massaged... %r", data)
        if (not pubg_match_id and not match_id and not player_names):
            raise cls.BadRequest("must pass at least pubg_match_id, match_id or player_names")

        from_sql = api_bool(from_sql)

        if isinstance(include_types, str):
            include_types = include_types.split(',')

        if isinstance(exclude_types, str):
            exclude_types = exclude_types.split(',')

        if isinstance(player_names, str):
            player_names = player_names.split(',')

        client = PUBGClient()

        if from_sql:
            a = Asset(pubg_match_id=pubg_match_id, match_id=match_id)
            all = Asset.massaged_events(a, from_sql=from_sql, qmodule=pq, include_types=include_types, exclude_types=exclude_types, player_names=player_names)
        else:
            assets = pq.match_assets(pubg_match_id=pubg_match_id, match_id=match_id, sort=sort)

            all = None
            for asset in assets:
                a = Asset(pubg_match_id=pubg_match_id, match_id=match_id, data=client.cache_get(asset.asset_url))
                all = a.massaged_events(from_sql=from_sql, qmodule=pq, include_types=include_types, exclude_types=exclude_types, player_names=player_names)

        return all

    @classmethod
    def damages(cls, pubg_match_id=None, match_id=None, player_name=None, from_sql=True):
        def _safediv(x, y):
            if y != 0:
                return x/y
            else:
                return 0

        def _consolidate_bluezone(_e):
            # return _e
            newe = []
            blue = None
            groggy = None
            for el in _e:
                if el.type == 'attack' and el.damages and el.damages[0].type == 'Damage_BlueZone':
                    if blue:
                        blue.damages[0].damage += el.damages[0].damage
                    else:
                        blue = el
                elif el.type == 'attack' and el.damages and el.damages[0].type == 'Damage_Groggy':
                    if groggy:
                        groggy.damages[0].damage += el.damages[0].damage
                    else:
                        groggy = el
                else:
                    if blue:
                        newe.append(blue)
                        blue = None
                    if groggy:
                        newe.append(groggy)
                        groggy = None

                    newe.append(el)

            if blue:
                newe.append(blue)
            if groggy:
                newe.append(groggy)

            return newe

        # roster = None
        # if player_name:
        #    roster = flannelcat_api.MatchApi.roster(pubg_match_id=pubg_match_id, player_name=player_name)

        from_sql = api_bool(from_sql)
        player_events = cls.massaged_events(
            pubg_match_id=pubg_match_id, match_id=match_id, player_names=[player_name], from_sql=from_sql,
            include_types=['attack', 'item']
        )

        events = [x for x in player_events[player_name] if x.is_game and x.type == 'attack' or (x.type == 'item' and x.action == 'use')]
        events = _consolidate_bluezone(events)

        client.Event.set_observer(player_name)

        out = []
        for e in events:
            oe = {
                'id': '{}.{}.{}'.format(e.type, e.ts, e.character.player_name),
                'ts': e.ts,
                'type': e.type,
            }
            if e.type == 'attack':
                oe['class'] = 'victim' if e.is_victim((e.damages or [None])[0]) else 'attacker'
                if e.damages:
                    oe['health_string'] = e.health_string(e.damages[0], subject=True)
                    oe['health_string2'] = e.health_string(e.damages[0], subject=False)
                else:
                    oe['health_string'] = e.health_string(None, subject=True)
                    oe['health_string2'] = e.health_string(None, subject=False)

                oe['weapon'] = {
                    'id': pq._clean(e.weapon.id)
                }
                oe['damages'] = [{
                    'kill': x.kill, 'type': pq._clean(x.type), 'reason': x.reason, 'player_name': e.object(x).player_name,
                    'distance': e.distance(x), 'damage': x.damage
                } for x in e.damages]
            elif e.type == 'item' and e.action == 'use':
                oe['class'] = 'use_item'
                oe['item'] = {
                    'id': pq._clean(e.item.id),
                    'category': e.item.category,
                    'subcategory': e.item.sub_category,
                }
            else:
                logger.warn("WTF!")

            out.append(oe)

        return out

    @classmethod
    def telemetry_to_mysql(cls, pubg_match_id=None, match_id=None):
        assets = pq.match_assets(pubg_match_id=pubg_match_id, match_id=match_id)
        client = PUBGClient()

        for asset in assets:
            a = Asset(pubg_match_id=pubg_match_id, match_id=match_id, data=client.cache_get(asset.asset_url))
            a.to_mysql(pq)

    @classmethod
    def map_routes(cls, pubg_match_id=None, match_id=None, players=None, scale=1.0):

        def _map_coords(x, y):
            return [scale*x, -scale*y]

        if isinstance(players, str):
            players = players.split(',')

        include_types = ['position']
        exclude_types = None
        player_names = players

        a = Asset(pubg_match_id=pubg_match_id, match_id=match_id)
        events = Asset.massaged_events(
            a, from_sql=True, qmodule=pq, player_names=player_names,
            include_types=include_types, exclude_types=exclude_types,
        )

        out = []
        for i, p in enumerate(players):
            out.append(geojson.Feature(
                geometry=geojson.LineString([_map_coords(*e.character.location[:2]) for e in events[p] if e.type == 'position']),
                properties={
                    'player_name': p,
                    'index': i,
                    'style': {
                        'color': COLORS[i % len(COLORS)],
                        'weight': 1,
                    },
                }
            ))

        return geojson.FeatureCollection(out)

    @classmethod
    def map_positions(cls, pubg_match_id=None, match_id=None, players=None, scale=1.0):
        if isinstance(players, str):
            players = players.split(',')

        include_types = ['position']
        exclude_types = None
        player_names = players

        a = Asset(pubg_match_id=pubg_match_id, match_id=match_id)
        events = Asset.massaged_events(
            a, from_sql=True, qmodule=pq, player_names=player_names,
            include_types=include_types, exclude_types=exclude_types,
        )

        out = []
        for i, p in enumerate(players):
            out.extend([geojson.Feature(
                geometry=geojson.Point(cls._map_coords(*e.character.location[:2], scale=scale)),
                properties={
                    'ts': e.ts,
                    'index': i,
                    'tag': i,
                }
            ) for e in events[p] if e.type == 'position'])

        return geojson.FeatureCollection(sorted(out, key=lambda x: x.properties['ts']))

    @classmethod
    def map_deaths(cls, pubg_match_id=None, match_id=None, players=None, scale=1.0):
        if isinstance(players, str):
            players = players.split(',')

        players = players or []

        include_types = ['attack', 'periodic', 'position']

        a = Asset(pubg_match_id=pubg_match_id, match_id=match_id)
        events = Asset.massaged_events(
            a, from_sql=True, qmodule=pq, include_types=include_types, by_player=False
        )

        ##################################
        # deaths
        deaths = []
        for e in events:
            if e.type != 'attack':
                continue
            if not e.damages:
                continue

            deaths.extend([geojson.Feature(
                geometry=geojson.Point(cls._map_coords(*d.victim.location[:2], scale=scale)),
                properties={
                    'ts': e.ts,
                    'radius': 10,
                }
            ) for d in e.damages if d.kill])

        ##################################
        # blue circles and warning circles
        blue = []
        warning = []
        warnings = set()
        blues = set()
        for e in [x for x in events if x.type == 'periodic']:
            if e.poison_gas_warning_radius == 0:
                continue

            val = (e.safety_zone_position[0], e.safety_zone_position[1], e.safety_zone_radius)
            if val not in blues:
                blue.append(geojson.Feature(
                    geometry=geojson.Point(cls._map_coords(*e.safety_zone_position, scale=scale)),
                    properties={
                        'ts': e.ts,
                        'radius': e.safety_zone_radius*scale,
                    }
                ))

            val = (e.poison_gas_warning_position[0], e.poison_gas_warning_position[1], e.poison_gas_warning_radius)
            if val not in warnings:
                warnings.add(val)
                warning.append(geojson.Feature(
                    geometry=geojson.Point(cls._map_coords(*e.poison_gas_warning_position, scale=scale)),
                    properties={
                        'ts': e.ts,
                        'radius': e.poison_gas_warning_radius*scale,
                    }
                ))

        ##################################
        # damage dealth
        damages = []
        for e in [x for x in events if x.type == 'attack']:
            for d in e.damages or []:
                if d.victim.player_name not in players and e.character.player_name not in players:
                    continue

                if e.character.location[0] == 0 and e.character.location[1] == 0:
                    continue

                victim = False
                index = -1
                if e.character.player_name in players:
                    index = players.index(e.character.player_name)
                    victim = False
                elif d.victim.player_name in players:
                    index = players.index(d.victim.player_name)
                    victim = True

                damages.append(
                    geojson.Feature(
                        geometry=geojson.GeometryCollection([
                            geojson.Point(cls._map_coords2(*e.character.location[:2], scale=scale)),
                            geojson.Point(cls._map_coords2(*d.victim.location[:2], scale=scale)),
                        ]),
                        properties={
                            'ts': e.ts,
                            'index': index,
                            'victim': victim
                        }
                    )
                )

        ##################################
        # parachute landing locations and plane path
        landings = {}
        lastz = defaultdict(float)
        planex = []
        planey = []
        for e in [x for x in events if x.type == 'position']:
            if e.character.location[2] > 1500:
                planex.append(e.character.location[0])
                planey.append(e.character.location[1])

            if e.character.player_name not in landings:
                diff = lastz[e.character.player_name] - e.character.location[2]
                if e.is_game >= 0.1 and e.character.location[2] < 500 and (diff < 5):
                    index = -1
                    if e.character.player_name in players:
                        index = players.index(e.character.player_name)
                    landings[e.character.player_name] = geojson.Feature(
                        geometry=geojson.Point(cls._map_coords(*e.character.location[:2], scale=scale)),
                        properties={
                            'ts': e.ts,
                            'index': index
                        }
                    )

            lastz[e.character.player_name] = e.character.location[2]

        z = numpy.polyfit(planex, planey, 1)
        p = numpy.poly1d(z)
        xp = numpy.linspace(-8000, 16000, 2)

        lx, ly = xp, p(xp)

        slope = (ly[0]-ly[1], lx[1]-lx[0])
        slopel = math.sqrt(slope[0]*slope[0] + slope[1]*slope[1])
        offset = slope[0]/slopel
        # offset = 1000*(lx[1]-lx[0])/(ly[1]-ly[0])
        # logger.warn("angle = %r, offset = %r - %r", math.degrees(angle), offset, 1000*math.cos(angle))
        # logger.warn("slope = %r, slopel = %r, offset = %r", slope, slopel, offset)
        offset1 = 1000/offset
        offset2 = 2000/offset
        flightpath = [
            geojson.Feature(
                geometry=geojson.LineString([cls._map_coords(x, y, scale=scale) for x, y in zip(lx, ly)]),
                properties={
                    'style': {
                        'weight': 5,
                        'color': 'red',
                        'lineCap': 'square',
                        'dashArray': [25, 25],
                    }
                }
            ),
            geojson.Feature(
                geometry=geojson.Polygon([[cls._map_coords(*p, scale=scale) for p in [
                    (lx[0] - offset1, ly[0]),
                    (lx[0] + offset1, ly[0]),
                    (lx[1] + offset1, ly[1]),
                    (lx[1] - offset1, ly[1]),
                ]]]),
                properties={
                    'style': {
                        'weight': 5,
                        'color': None,
                        'fillColor': 'blue',
                        'fillOpacity': 0.15,
                        'fill': True,
                    }
                }
            ),
            geojson.Feature(
                    geometry=geojson.Polygon([[cls._map_coords(*p, scale=scale) for p in [
                        (lx[0] - offset2, ly[0]),
                        (lx[0] + offset2, ly[0]),
                        (lx[1] + offset2, ly[1]),
                        (lx[1] - offset2, ly[1]),
                    ]]]),
                    properties={
                        'style': {
                            'weight': 5,
                            'color': None,
                            'fillColor': 'red',
                            'fillOpacity': 0.10,
                            'fill': True,
                        }
                    }
            ),
        ]

        return {
            'deaths': geojson.FeatureCollection(deaths),
            'blues': geojson.FeatureCollection(blue),
            'warnings': geojson.FeatureCollection(warning),
            'damages': geojson.FeatureCollection(damages),
            'landings': geojson.FeatureCollection(list(landings.values())),
            'flightpath': geojson.FeatureCollection(flightpath)
        }

    @classmethod
    def map_aggregate_flightpaths(cls, pubg_match_id=None, match_id=None, map_name=None, game_modes=None, scale=1.0):
        def _flightpath(_events):
            coords = [(e.character_location_x, e.character_location_y) for e in _events]
            planex, planey = zip(*coords)
            # logger.warn("%r", coords)
            p = numpy.poly1d(numpy.polyfit(planex, planey, 1))
            xp = numpy.linspace(-8000, 16000, 2)
            lx, ly = xp, p(xp)
            # logger.warn("%r", list(zip(lx, ly)))
            return geojson.Feature(
                geometry=geojson.LineString([cls._map_coords(x, y, scale=scale) for x, y in zip(lx, ly)]),
            )

        where = ["character_location_z > 1500 and winPlace <=2"]
        events = pq.position_events(
            pubg_match_id=pubg_match_id, match_id=match_id,
            extra_where=where, map_name=map_name or 'Desert_Main', game_modes=game_modes.split(',') if game_modes else None, sort='match_id',
        )

        match_id = events[0].match_id
        these_events = []
        paths = []
        for el in events:
            if match_id == el.match_id:
                these_events.append(el)
            else:
                paths.append(_flightpath(these_events))
                match_id = el.match_id
                these_events = [el]

       #  logger.warn("# paths = %r", len(paths))
        paths.append(_flightpath(these_events))

        return geojson.FeatureCollection(paths)

    @classmethod
    def map_aggregate_deaths(cls, map_name=None, game_modes=None, players=None, scale=1.0):
        # logger.warn("players = %r", players)
        if players and isinstance(players, str):
            players = players.split(',')

        players = players or []

        where = ["is_kill"]
        if players:
            sql_players = ','.join(["'{}'".format(x) for x in players])
            where += ["victim_player_id in (select player_id from players where player_name in ({}))".format(sql_players)]

        # logger.warn("players  %r, where = %r", players, where)
        events = pq.attack_event_damages(
            extra_where=where, map_name=map_name or 'Desert_Main',
            game_modes=game_modes.split(',') if game_modes else None, sort='match_id',
        )
        paths = []
        # logger.warn("# deaths = %r", len(events))
        for e in events:
            paths.append(
                geojson.Feature(
                    geometry=geojson.Point(
                        cls._map_coords(e.victim_location_x, e.victim_location_y, scale=scale)
                   )
                )
            )

        return geojson.FeatureCollection(paths)

    @classmethod
    def damage_stats(cls, player=None, game_modes=None, page=1, limit=100, window=10):
        window = api_int(window)
        foo = pq.match_stats_windowed(
            player_name=player,
            game_modes=game_modes.split(',') if game_modes else None,
            page=page, limit=limit, window=window
        )
        # return [(x.created_at, x.kills, x.kills_sum) for x in foo]
        return foo

    @classmethod
    def weapon_hit_stats(self, player_name=None, player_id=None, start_date=None, end_date=None, game_modes=None):
        return pq.weapon_hit_stats(
            player_name=player_name, player_id=player_id,
            start_date=start_date, end_date=end_date, game_modes=game_modes
        )


@api_register(None, require_login=False)
class ESPApi(Api):
    @classmethod
    def index(self, data=None):
        logger.warning("data = %r", data)
        return {}
