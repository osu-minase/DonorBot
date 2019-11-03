import bottle
import time
import json
import config
import discord
import globals as glob
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
#Ripple code only :3
@bottle.route("/api/v1/clear_donor", method="POST")
def clear_donor_post():
	data = {
		"status": 200,
		"message": "ok"
	}
	try:
		# Get discord expired donors
		expired = glob.db.fetch_all("SELECT discord_roles.discordid, discord_roles.roleid, users.id FROM discord_roles RIGHT JOIN users ON users.id = discord_roles.userid WHERE users.privileges & 4 > 0 AND donor_expire <= %s", [int(time.time())])

		# Do all the work if the query has returned something
		if expired is not None:
			# Get discord server object and make sure it's valid
			discord_server = glob.client.get_server(config.server)
			if discord_server is None:
				raise NotInServerError()

			# Get donators role object
			donor_role = discord.utils.get(discord_server.roles, id=config.rid)

			# Make sure the donorRole is valid
			if donor_role is None:
				coro.sync_coroutine(glob.client.fetch_channel(discord_server.system_channel).send("Error while cleaning expired donors! Looks like the donators role is gone! Nyo-sama where are you? :'("))
				raise NoRoleError()

			# Remove donators and custom roles to expired donors
			for i in expired:
				print("Removing donor for user {}".format(i["id"]))

				# First, remove donor badge
				glob.db.execute("DELETE FROM user_badges WHERE user = %s AND badge = '14' LIMIT 1", [i["id"]])

				# Then, do discord stuff
				# Make sure the discord id is valid
				if i["discordid"] is None or i["discordid"] == 0:
					continue

				# Get the user and make sure he is still inside the server	
				discord_user = discord_server.get_member(str(i["discordid"]))
				if discord_user is None:
					continue

				# Remove donators role
				coro.sync_coroutine(glob.client.remove_roles(discord_user, donor_role))

				# Unlink discord and ripple accounts
				glob.db.execute("DELETE FROM discord_roles WHERE discordid = %s LIMIT 1", [i["discordid"]])

				# Delete profile background
				glob.db.execute("DELETE FROM profile_backgrounds WHERE uid = %s LIMIT 1", [i["id"]])

				# Get the custom role
				custom_role = None
				for j in discord_server.roles:
					if j.id == str(i["roleid"]):
						custom_role = j

				# Make sure the custom role is valid
				if custom_role is None:
					continue

				# Delete custom role from server
				coro.sync_coroutine(glob.client.get_guild(discord_server).fetch_role(custom_role).delete())

		# Remove website and ingame expired donor privilege
		glob.db.execute("UPDATE users SET privileges = privileges & ~4 WHERE privileges & 4 > 0 AND donor_expire <= %s", [int(time.time())])
	except InvalidSecretKeyError:
		data["status"] = 403
		data["message"] = "Bot not in server"
	except NoRoleError:
		data["status"] = 500
		data["message"] = "Donators role not found"
	finally:
		json_data = json.dumps(data)
		yield json_data