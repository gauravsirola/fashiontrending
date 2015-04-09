from instagram.client import InstagramAPI
from instagram.bind import InstagramAPIError
import sys
import pickle
import time

def get_recent_media(user_id):
	all_media = []
	recent_media = []
	max_id = None
	counter = 0
	while (recent_media is not None):
		try:
			if (max_id is not None):
				recent_media, next_ = api.user_recent_media(user_id=user_id, max_id=max_id)
			else:
				recent_media, next_ = api.user_recent_media(user_id=user_id)
			for media in recent_media:
				all_media.append(media)
			if len(recent_media) > 19:
				max_id = recent_media[-1].id.split('_')[0]
			else:
				print "Found %d" %len(all_media)
				break

		except InstagramAPIError as e:
			print e
			if (e.status_code == 429):
				print "Rate limit reached. Waiting 1min"
				recent_media = []
				time.wait(60)
			elif (e.status_code == 502):
				"Unable to parse response"
				break
			else:
				break
		except:
			"Error getting data for %d" %user_id
			break

	media_counts.append(len(all_media))
	pickle.dump(all_media, save_file)

if __name__ == '__main__':
	media_counts = []
	access_token = sys.argv[1]
	user_ids_file = sys.argv[2]
	output_file = sys.argv[3]
	api = InstagramAPI(access_token=access_token)
	save_file = open(output_file, 'ab')

	#get_recent_media("47791647")

	user_ids = []
	with open(user_ids_file, 'r') as id_file:
		for line in id_file.readlines():
			user_ids.append(line.rstrip('\n'))
			
	# while user_ids[0] != '1535113556':
	# 	user_ids.pop(0)
	# stopped at 10051934
	# media counts [2944, 4328, 279, 1501, 1282, 765, 2445, 886, 1798, 234, 2058, 1168, 64, 2375, 1388, 852, 1142, 1039, 449, 771, 977, 2910, 442, 1228, 591, 4820, 4963, 14073, 4280]
	# [5080, 309, 1, 0, 203, 286, 8701, 234, 3627, 4448, 4230, 2748, 1369]
	# stopped at 13497422
	# sum of 93288
	for user_id in user_ids:
		try:
			print "Crawling %s" %user_id
			get_recent_media(user_id)
			print "Rate limit %s" %api.x_ratelimit_remaining
			print media_counts
		except:
			"Error crawling"
