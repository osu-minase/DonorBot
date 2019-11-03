import bottle
import json
import config
import discord
import globals
from helpers import coro
class InvalidArgumentsError(Exception):
    pass
class InvalidSecretKeyError(Exception):
    pass
class BotNotInServerError(Exception):
    pass
class NotInServerError(Exception):
    pass
class NoRoleError(Exception):
    pass
@bottle.route('/api/give_donor', method='POST')
def give_donor_post():
    data = {
        'status': 200,
        'message': 'ok'
    }
    try:
        args = ['secret', 'discordid']
        print(type(bottle.request.json))
        for i in args:
            if i not in bottle.request.json:
                raise InvalidArgumentsError()
        if config.secret != bottle.request.json['secret']:
            raise InvalidSecretKeyError()
        discord_server = globals.client.get_guild(config.server)
        if discord_server is None:
            raise BotNotInServerError()
        discord_user = discord_server.get_member(int(bottle.request.json['discordid']))
        if discord_user is None:
            raise NotInServerError()
        donor_role = discord.utils.get(discord_server.roles, id=config.rid)
        if not donor_role:
            raise NoRoleError()
        coro.sync_corotine(discord_user.add_roles(donor_role))
    except InvalidArgumentsError:
        data["status"] = 400
        data["message"] = "Missing/invalid arguments"
    except InvalidSecretKeyError:
        data["status"] = 403
        data["message"] = "Invalid secret key"
    except NotInServerError:
        data["status"] = 404
        data["message"] = "User not in server"
    except BotNotInServerError:
        data["status"] = 403
        data["message"] = "Bot not in server"
    except NoRoleError:
        data["status"] = 500
        data["message"] = "No donators role found in server"
    finally:
        json_data = json.dumps(data)
        yield json_data